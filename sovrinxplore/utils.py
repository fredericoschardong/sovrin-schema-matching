import json
import rocksdb


def load_schemas(ledger: str, silent: bool) -> list:
    db = rocksdb.DB('sovrinxplore/ledgers/%s' % ledger, 
                    rocksdb.Options(create_if_missing=False,
                                    keep_log_file_num=1,
                                    stats_dump_period_sec=0))
    total_schemas = int.from_bytes(db.get(b'total_schemas'), byteorder='big')
    
    if not silent:
        print("Total schemas: %d" % total_schemas)
    
    return [json.loads(db.get(b'schema_%d' % i).decode('ascii')) for i in range(1, total_schemas)]

def normalize_schemas(schemas: list) -> list:
    return [' '.join(schema) for schema in schemas]
