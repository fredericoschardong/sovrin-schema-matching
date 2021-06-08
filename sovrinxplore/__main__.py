from sovrinxplore import spacy


if __name__ == '__main__':
    from sovrinxplore import cli

    args = cli.parser.parse_args()

    spacy.apply(args.ledger, args.query)

