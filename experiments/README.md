# Manually selected results

The manually selected results for the queries described in our paper are here listed, along with the synonyms found on the ledger (schema transactions) and their respective IDs (seqNo).

## first name
| Synonym      | Exact Field  | seqNo |
|:-------------|:-------------|:----:|
first name  | `first_name`, `First name`, `First name`, `DEMO-First Name`, `First name`, `first_name`, `DEMO-First Name`, `firstname`, `DEMO-First Name`, `firstName`, `C19EOLegalFirstName`, `First Name`, `firstName`, `firstName`, `userFirstName`, `firstName`, `First name`, `first_name`, `first_name`, `first_name`, `first_name`, `First Name`, `farmer_first_name`, `farmer_first_name`, `farmer_first_name`, `firstName`, `farmer_first_name`, `farmer_first_name`, `farmer_first_name`, `First Name`, `First Name`, `First Name`, `First Name`, `First Name`, `Buyer First Name`, `First Name` | 14632, 31583, 31622, 33629, 35079, 43843, 47768, 54022, 54331, 54389, 54402, 54517, 54538, 54542, 54556, 54572, 54605, 54761, 54773, 54788, 54802, 55727, 56307, 56308, 56309, 56389, 57498, 58175, 58693, 59004, 59551, 59552, 59553, 59555, 59556, 59557
name | `DEMO-Name`, `name`, `name`, `name`, `DEMO-Name`, `name`, `name`, `name`, `name`, `name`, `name`, `name`, `name`, `name` | 47766, 54002, 54003, 54170, 54171, 54439, 54782, 54796, 56136, 56365, 57614, 57630, 58041, 58042
given name  | `Given Name`, `givenNames`, `Given Name`, `Given Name`, `Given Name`, `Given Names`| 54679, 58011, 58608, 58699, 59232, 59554
patient first name   | `Patient First Name`, `Patient First Name`, `Patient First Name`, `Patient First Name`, `Patient First Name` | 57735, 57765, 57873, 57900, 58081
member name  | `Member Name`, `Member Name` | 15227, 15463
full name | `Full Name`, `Full Name` | 54564, 54602
inspector name | `inspector_name` | 58160
student name | `DEMO-Student Name` | 33627

## company job
| Synonym      | Exact Field  | seqNo |
|:-------------|:-------------|:----:|
organization |`organization`, `organization`, `organization`, `organization`, `organization_name`, `organization_name`, | 54782, 54796, 57614, 57630, 58692, 59050
company | `company_name`, `companyGroup`, `company`, `Company`, `Company`, `company`, `Company` | 54439, 54533, 54556, 54602, 55727, 56389, 59004
employer | `employer`, `Employer`, `Employer`|54019, 59552, 59553
department |`department`, `department`, `department`| 54020, 54876, 55429
role | `role`, `role`| 56138, 56181
contract |`Contract Signed Date` | 59556
payment | `payment_indicator`| 54767


All schemas with `employee`, `income`, `job`, `position`, `work` were added by other synonyms. 

## address 
| Synonym      | Exact Field  | seqNo |
|:-------------|:-------------|:----:|
country |`country`, `country`, `country`, `country`, `DEMO-Country of Residence`,`country`, `country`, `country`, `country`, `country`,`country_of_origin`,`issuingCountry`, `personIdentifierCountry`, `otherDocCountry`, `Country Code`| 99, 188, 1050, 12027, 33629, 41055, 50799, 54000, 54001, 54004, 56308, 58011, 58039, 59554
address | `address`, `address`, `address`, `address`, `address`,`address`, `address`, `supplier_address`, `address`, `Street Address` | 14635, 43843, 54393, 56310, 57498, 58043, 58044, 58462, 58693, 59556
State |`state`, `institution_state`, `institution_state`, `state`|54767, 54792, 54806, 56516
Street |`DEMO-Street Name`, `street`|47768, 54023
Zip |`DEMO-Zip`|54331
city |`city`|54170


All schemas with `postal code`, `province`,`municipality` were added by other synonyms. 

# Gather Results

Do not run the following commands, unless you have manually updated the list above with the new schemas.

## All schemas

We need to store all schemas to calculate statistics.

```
echo "-" | docker run -i sovrin-schema-matching:cli --hits 0 --print-seq-only | jq -c '. | sort' > analysis/raw_results/all_schemas.json
```

## This work

```
echo "first name" | docker run -i sovrin-schema-matching:cli --hits 200 --min-score 0.6 --print-seq-only | jq -c '. | sort' > analysis/raw_results/spacy_first_name.json
echo "company job" | docker run -i sovrin-schema-matching:cli --hits 200 --min-score 0.6 --print-seq-only | jq -c '. | sort' > analysis/raw_results/spacy_company_job.json
echo "address" | docker run -i sovrin-schema-matching:cli --hits 200 --min-score 0.6 --print-seq-only | jq -c '. | sort' > analysis/raw_results/spacy_address.json
```


## vonx.io

```
curl 'https://sovrin-mainnet-browser.vonx.io/ledger/domain?page=1&page_size=200&query=first%20name&type=101' | jq -c '[.results[] | .txnMetadata.seqNo] | sort' > analysis/raw_results/vonx_first_name.json
curl 'https://sovrin-mainnet-browser.vonx.io/ledger/domain?page=1&page_size=200&query=company%20job&type=101' | jq -c '[.results[] | .txnMetadata.seqNo] | sort' > analysis/raw_results/vonx_company_job.json
curl 'https://sovrin-mainnet-browser.vonx.io/ledger/domain?page=1&page_size=200&query=address&type=101' | jq -c '[.results[] | .txnMetadata.seqNo] | sort' > analysis/raw_results/vonx_address.json
```

## indyscan.io

```
curl 'https://indyscan.io/api/networks/SOVRIN_MAINNET/ledgers/domain/txs?filterTxNames=%5B%22SCHEMA%22%5D&format=expansion&search=first%20name&size=500&skip=0&sortFromRecent=false' | jq -c '[.[] | .imeta.seqNo] | sort' > analysis/raw_results/indyscan_first_name.json
curl 'https://indyscan.io/api/networks/SOVRIN_MAINNET/ledgers/domain/txs?filterTxNames=%5B%22SCHEMA%22%5D&format=expansion&search=company%20job&size=500&skip=0&sortFromRecent=false' | jq -c '[.[] | .imeta.seqNo] | sort' > analysis/raw_results/indyscan_company_job.json
curl 'https://indyscan.io/api/networks/SOVRIN_MAINNET/ledgers/domain/txs?filterTxNames=%5B%22SCHEMA%22%5D&format=expansion&search=address&size=500&skip=0&sortFromRecent=false' | jq -c '[.[] | .imeta.seqNo] | sort' > analysis/raw_results/indyscan_address.json
```

# Run analysis

```
$ docker build -t sovrin-schema-matching:cli .
$ docker run -it --entrypoint "/usr/local/bin/python" sovrin-schema-matching:cli /app/analysis
Query address
Results for spacy
              precision    recall  f1-score   support

       False       0.81      0.87      0.84       116
        True       0.35      0.25      0.29        32

    accuracy                           0.74       148
   macro avg       0.58      0.56      0.56       148
weighted avg       0.71      0.74      0.72       148


Results for indyscan
              precision    recall  f1-score   support

       False       0.84      0.96      0.90       116
        True       0.69      0.34      0.46        32

    accuracy                           0.82       148
   macro avg       0.76      0.65      0.68       148
weighted avg       0.81      0.82      0.80       148


Results for vonx
              precision    recall  f1-score   support

       False       0.89      0.96      0.92       116
        True       0.78      0.56      0.65        32

    accuracy                           0.87       148
   macro avg       0.84      0.76      0.79       148
weighted avg       0.87      0.87      0.86       148


Query first_name
Results for spacy
              precision    recall  f1-score   support

       False       0.77      0.93      0.84        81
        True       0.88      0.67      0.76        67

    accuracy                           0.81       148
   macro avg       0.83      0.80      0.80       148
weighted avg       0.82      0.81      0.81       148


Results for indyscan
              precision    recall  f1-score   support

       False       0.64      1.00      0.78        81
        True       1.00      0.31      0.48        67

    accuracy                           0.69       148
   macro avg       0.82      0.66      0.63       148
weighted avg       0.80      0.69      0.64       148


Results for vonx
              precision    recall  f1-score   support

       False       0.70      1.00      0.83        81
        True       1.00      0.49      0.66        67

    accuracy                           0.77       148
   macro avg       0.85      0.75      0.74       148
weighted avg       0.84      0.77      0.75       148


Query company_job
Results for spacy
              precision    recall  f1-score   support

       False       0.90      0.99      0.94       125
        True       0.90      0.39      0.55        23

    accuracy                           0.90       148
   macro avg       0.90      0.69      0.74       148
weighted avg       0.90      0.90      0.88       148


Results for indyscan
              precision    recall  f1-score   support

       False       0.84      1.00      0.92       125
        True       0.00      0.00      0.00        23

    accuracy                           0.84       148
   macro avg       0.42      0.50      0.46       148
weighted avg       0.71      0.84      0.77       148


Results for vonx
              precision    recall  f1-score   support

       False       0.84      1.00      0.92       125
        True       0.00      0.00      0.00        23

    accuracy                           0.84       148
   macro avg       0.42      0.50      0.46       148
weighted avg       0.71      0.84      0.77       148
```

# Scalability

See [the README.md on the scalability folder](https://github.com/fredericoschardong/sovrin-schema-matching/tree/main/experiments/scalability) for more details.
