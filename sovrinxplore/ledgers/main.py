# @author: Ryan West (ryan.west@sovrin.org) at https://github.com/sovrin-foundation/steward-tools/blob/master/local_ledger/local_ledger.py
# Changes made by Frederico Schardong (frede.sch@gmail.com)

import asyncio
import json
import rocksdb
import os
import sys

from indy import ledger, pool

class TxnDoesNotExistException(Exception):
    pass


class InvalidLedgerResponseException(Exception):
    pass


# TODO: add option to download specific set of txns instead of all
class LocalLedger():
    '''
    Uses a rocksdb key-value db to download and store an indy network ledger
    Automatically downloads all transactions as they are added on the net
    Allows for simple transaction reading by sequence number

    NOTE: Currently this uses an indy GET_TXN request for every txn on ledger.
    This is slow and extremely chatty, and should eventually be replaced with
    a batch message request or catchup solutions; however, these options still
    need to be implemented in indy-sdk.
    '''

    def __init__(self, databaseDir, poolname, did):
        '''Setup for inital use'''
        self.poolname = poolname
        self.did = did
        if not os.path.isdir(databaseDir):
            print('Local ledger database not found; creating a new one')
        # _db should not be modified directly, as len(_db) may no longer
        # be accurate
        self._db = rocksdb.DB(
            databaseDir, rocksdb.Options(create_if_missing=True,keep_log_file_num=1,stats_dump_period_sec=0))
        self.pool_handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self._db

    async def connect(self):
        '''Connects to the pool specified in the constructor, using given wallet and did'''

        await pool.set_protocol_version(2)

        try:
            await pool.create_pool_ledger_config(self.poolname, json.dumps({"genesis_txn": f'/app/ledgers/pool_transactions_%s_genesis' % NETWORK}))
        except:
            await pool.delete_pool_ledger_config(self.poolname)
            await pool.create_pool_ledger_config(self.poolname, json.dumps({"genesis_txn": f'/app/ledgers/pool_transactions_%s_genesis' % NETWORK}))

        self.pool_handle = await pool.open_pool_ledger(self.poolname, None)

    async def disconnect(self):
        '''Closes indy wallet and pool connections'''

        await pool.close_pool_ledger(self.pool_handle)

    async def downloadTxn(self, pool_handle, submitter_did, which_ledger,
                          seq_no):
        '''Attempts to download the transaction with given sequence number'''

        # build get_txn request
        getTxnJson = await ledger.build_get_txn_request(submitter_did,
                                                        which_ledger, seq_no)
        # get response from ledger
        response = await ledger.submit_request(pool_handle, getTxnJson)
        # serialize json into object
        try:
            responseJson = json.loads(response)['result']
        except KeyError as e:
            print('result attribute not found in response. Response:')
            print(response)
            raise e

        # if we're at the last txn on the ledger, stop trying to download more
        if responseJson['data'] is None:
            raise TxnDoesNotExistException()

        try:
            key = responseJson['seqNo']
            value = responseJson['data']
        except Exception:
            print('\nError in response message:')
            print('\n', json.dumps(json.loads(response), indent=4))
            raise InvalidLedgerResponseException()
            
        if value["txn"]["type"] == "101":
            self._db.put(self._intToBytes(key), json.dumps(value).encode())

    async def update(self, limit=None):
        ''' Downloads new transactions to sync local db with the remote.
            limit: highest txn sequence number to get before stopping'''

        if limit is not None and limit < 1:
            raise Exception('Limit must be at least 1')

        # gets the last sequence number stored locally and updates from there
        curTxn = self.getTxnCount() + 1
        if curTxn is None:
            curTxn = 1

        printedDownload = False
        while limit is None or limit >= curTxn:
            try:
                await self.downloadTxn(self.pool_handle, self.did,
                                       'DOMAIN', curTxn)
            # if there is no txn, we've reached the most recent one so break
            except TxnDoesNotExistException:
                break

            if not printedDownload:
                printedDownload = True
            print('.', end='', flush=True)
            self.updateTxnCount(curTxn)
            # Keep track of the most recent transaction sequence number
            curTxn += 1

        if limit is None:
            print('Local ledger is up to date.')
        else:
            print('Local ledger has reached limit of', str(limit), 'txns.')

    async def update_concurrent(self, threads = 8):
        ''' @author: Frederico Schardong (frede.sch@gmail.com) '''

        # gets the last sequence number stored locally and updates from there
        curTxn = self.getTxnCount() + 1

        if curTxn is None:
            curTxn = 1

        print('Last transaction sequence number:', str(curTxn - 1))

        while True:
            calls = []

            for i in range(threads):
                calls.append(self.downloadTxn(self.pool_handle, self.did, 'DOMAIN', curTxn + i))
            try:
                await asyncio.gather(*calls)

            except TxnDoesNotExistException:
                break

            print('.', end='', flush=True)

            self.updateTxnCount(curTxn + threads)

            # Keep track of the most recent transaction sequence number
            curTxn += threads

        # get the last txn one by one to ensure we have them all
        await self.update()

        schema_count = int.from_bytes(self._db.get(b'total_schemas'), byteorder='big') if self._db.get(b'total_schemas') else 1

        for i in range(1, self.getTxnCount() + 1):
            if self._db.get(self._intToBytes(i)):
                schema = json.loads(self._db.get(self._intToBytes(i)).decode('ascii'))
                schema = {'key': schema['txnMetadata']['seqNo'],
                          'value': schema['txn']['data']['data']['attr_names']}
                
                self._db.put(b'schema_%d' % schema_count, json.dumps(schema).encode())
            
                #self._db.put(b'schema_%d' % schema_count, self._db.get(self._intToBytes(i)))
                self._db.delete(self._intToBytes(i))
                schema_count += 1

        self._db.put(b'total_schemas', int.to_bytes(schema_count, 10, byteorder='big'))
        
    def _intToBytes(self, x):
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    def updateTxnCount(self, count):
        '''Updates the transaction count (stored as a key-value pair in db)'''

        self._db.put(b'lastTxnDownloaded', int.to_bytes(
            count, 10, byteorder='big'))

    def getTxnCount(self):
        '''Gets the number of transactions'''

        try:
            return int.from_bytes(self._db.get(b'lastTxnDownloaded'),
                                  byteorder='big')
        except Exception:
            return 0

async def main():
    global NETWORK

    if len(sys.argv) != 2:
        NETWORK = 'live'
    else:
        if sys.argv[1] == 'live' or sys.argv[1] == 'sandbox' or sys.argv[1] == 'builder':
            NETWORK = sys.argv[1]
        else:
            exit("Only options are live, sandbox or builder")
            
    print("Syncing %s" % NETWORK)

    ll = LocalLedger("/app/ledgers/%s" % NETWORK, "sovrin", "W5CH4SUhAVFhyfzEQwRHVd")

    # establishes a connection with the pool object
    await ll.connect()

    # updates the pool till the most recent txn is reached (may take awhile)
    await ll.update_concurrent(100)

    await ll.disconnect()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
