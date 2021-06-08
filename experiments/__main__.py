from sklearn.metrics import classification_report
import json

if __name__ == '__main__':
    try:
        with open(f"analysis/raw_results/all_schemas.json") as f:
            all_txn = json.load(f)
    except FileNotFoundError:
        exit("missing analysis/raw_results/all_schemas.json")

    for query in ["address", "first_name", "company_job"]:
        print("Query", query)

        try:
            with open(f"analysis/raw_results/manual_{query}.json") as f:
                manual = json.load(f)
        except FileNotFoundError:
            exit(f"missing analysis/raw_results/manual_{query}.json is missing")

        y_true = []

        for txn in all_txn:
            y_true.append(txn in manual)

        for method in ["spacy", "indyscan", "vonx"]:
            try:
                with open(f"analysis/raw_results/{method}_{query}.json") as f:
                    method_results = json.load(f)
            except FileNotFoundError:
                exit(f"missing analysis/raw_results/{method}_{query}.json")

            y_pred = []

            for txn in all_txn:
                y_pred.append(txn in method_results)

            print("Results for", method)
            print(classification_report(y_true, y_pred, zero_division=0))
            print()

