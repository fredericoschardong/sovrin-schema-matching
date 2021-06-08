<a href="https://github.com/fredericoschardong/sovrin-schema-matching/actions?query=workflow%3Abuild"><img alt="Actions Status" src="https://github.com/fredericoschardong/sovrin-schema-matching/workflows/build/badge.svg"></a><a href="https://github.com/fredericoschardong/sovrin-schema-matching/actions?query=workflow%3Apooling"><img alt="Actions Status" src="https://github.com/fredericoschardong/sovrin-schema-matching/workflows/pooling/badge.svg"></a>

# Matching Metadata on Blockchain for Self-Sovereign Identity

Schema matching on the Sovrin network using natural language processing.

## Downloading the latest schemas from the ledger

Build the docker image for the pooling service:

```
$ docker build -t sovrin-schema-matching:pooling-service sovrinxplore/ledgers/
```

To run it you have to share the `sovrinxplore/ledgers` folder, which is where the RocksDB with the schemas resides:

```
$ docker run --mount type=bind,source="$(pwd)/sovrinxplore/ledgers",target=/app/ledgers sovrin-schema-matching:pooling-service
```

Furthermore, to sync the `sandbox` or `builder` ledgers, just add the ledger name at the end of the command line:

```
$ docker run --mount type=bind,source="$(pwd)/sovrinxplore/ledgers",target=/app/ledgers -it sovrin-schema-matching:pooling-service sandbox
$ docker run --mount type=bind,source="$(pwd)/sovrinxplore/ledgers",target=/app/ledgers -it sovrin-schema-matching:pooling-service builder
```

You can add those calls to a time-based job scheduler (`cron`) to always have the latest transactions, i.e. to effectively have a pooling service.

## Schema matching

First you have to build the docker image for the schema matching CLI:

```
$ docker build -t sovrin-schema-matching:cli .
```

Whatever is provided on the `stdio` is queried. Also, the `sovrinxplore/ledgers` folder needs to be shared to get the latest schemas (or you can rebuild the docker image on your cron job):

```
$ echo "first name" | docker run --mount type=bind,source="$(pwd)/sovrinxplore/ledgers",target=/app/sovrinxplore/ledgers -i sovrin-schema-matching:cli
Total schemas: 149
+-------+-------+--------------------------------------------------------------+
| score | seqNo |                            values                            |
+=======+=======+==============================================================+
| 0.897 | 54605 | ['Time', 'First name', 'Date', 'Email', 'Webinar name',      |
|       |       | 'Last name', 'URL']                                          |
+-------+-------+--------------------------------------------------------------+
| 0.880 | 54517 | ['Account ID', 'Last Name', 'Email', 'First Name']           |
+-------+-------+--------------------------------------------------------------+
| 0.832 | 59004 | ['Company', 'Issue Date', 'Event Name', 'Attendee Type',     |
|       |       | 'Event Date', 'Last Name', 'Email', 'First Name', 'Event     |
|       |       | Identifier']                                                 |
+-------+-------+--------------------------------------------------------------+
| 0.831 | 59553 | ['Role', 'Employer', 'System Access', 'First Name',          |
|       |       | 'Location', 'Last Name']                                     |
+-------+-------+--------------------------------------------------------------+
| 0.824 | 55727 | ['QiqoURL', 'Company', 'Event Name', 'Purchase Date',        |
|       |       | 'Amount Paid', 'Event Date', 'Ticket Type', 'Email', 'First  |
|       |       | Name', 'Last Name']                                          |
+-------+-------+--------------------------------------------------------------+

Enlapsed time to schema match: 0:00:00.123772
```

## Results

See [the README.md on the experiments folder](https://github.com/fredericoschardong/sovrin-schema-matching/tree/main/experiments) for more details.
