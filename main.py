import datetime

from timeit import default_timer as timer

from argparse import ArgumentParser

from texttable import Texttable

from sovrinxplore.strats import Spacy

LEDGERS = ['live', 'sandbox', 'builder']

parser = ArgumentParser()
parser.add_argument('--ledger', choices=LEDGERS, default='live')
parser.add_argument('--hits', type=int, default=5, help='Use 0 to return all schemas and ignore the query.')
parser.add_argument('--table-width', type=int, default=80)
parser.add_argument('--print-time-only', default=False, action='store_true')
parser.add_argument('--print-seq-only', default=False, action='store_true')
parser.add_argument('--min-score', type=float, default=0.0)
args = parser.parse_args()

strat = Spacy(args.ledger)
strat.train(args.print_time_only or args.print_seq_only)

start_time = timer()

try:
    query = input().rstrip()

    while query != "":
        results = strat.predict(query, args.hits, args.min_score, args.print_seq_only)

        if args.print_seq_only:
            print(results)
        else:
            rows = [results[0]._fields]

            for row in results:
                rows.append(row)

            table = Texttable(args.table_width)
            table.add_rows(rows)
            
            if not args.print_time_only:
                print(table.draw())
            
        query = input().rstrip()

except EOFError as error:
    pass
    
time_delta = timer() - start_time

if args.print_seq_only:
    exit()

if args.print_time_only:
    print(time_delta)
else:
    print("Enlapsed time to schema match:", datetime.timedelta(seconds=time_delta))
