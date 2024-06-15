import argparse
import pathlib
from tdta.purl_publish import publish_to_purl
from tdta.tdt_export import export_cas_data
from tdta.anndata_export import export_anndata


def main():
    parser = argparse.ArgumentParser(prog="tdta", description='TDT actions cli interface.')
    subparsers = parser.add_subparsers(help='Available TDT actions', dest='action')

    create_purl_operation_parser(subparsers)
    create_save_operation_parser(subparsers)
    create_anndata_operation_parser(subparsers)

    args = parser.parse_args()

    if args.action == "purl-publish":
        publish_to_purl(str(args.input), str(args.taxonomy), str(args.user))
    elif args.action == "export":
        cache_folder_path = None
        if "cache" in args and args.cache:
            cache_folder_path = args.cache
        export_cas_data(args.database, args.output, cache_folder_path)
    elif args.action == "anndata":
        cache_folder_path = None
        if "cache" in args and args.cache:
            cache_folder_path = args.cache
        export_anndata(args.database, args.json, args.output, cache_folder_path)


def create_purl_operation_parser(subparsers):
    parser_purl = subparsers.add_parser("purl-publish",
                                        description="The PURL publication parser",
                                        help="Published the given taxonomy to the PURL system.")
    parser_purl.add_argument('-i', '--input', action='store', type=pathlib.Path, required=True)
    parser_purl.add_argument('-t', '--taxonomy', required=True)
    parser_purl.add_argument('-u', '--user', required=True)


def create_save_operation_parser(subparsers):
    parser_export = subparsers.add_parser("export", add_help=False,
                                          description="The data exporter parser",
                                          help="Gather data from TDT tables and saves CAS data to the output location.")
    parser_export.add_argument('-db', '--database', action='store', type=pathlib.Path, required=True,
                               help="Database file path.")
    parser_export.add_argument('-o', '--output', action='store', type=pathlib.Path, required=True,
                               help="Output file path.")
    parser_export.add_argument('-c', '--cache', action='store', type=pathlib.Path,
                               help="Dataset cache folder path.")


def create_anndata_operation_parser(subparsers):
    parser_anndata = subparsers.add_parser("anndata", add_help=False,
                                          description="The AnnData exporter parser",
                                          help="Gather data from TDT tables and saves AnnData to the output location.")
    parser_anndata.add_argument('-db', '--database', action='store', type=pathlib.Path, required=True,
                               help="Database file path.")
    parser_anndata.add_argument('-j', '--json', action='store', type=pathlib.Path, required=True,
                                help="Json output file path.")
    parser_anndata.add_argument('-o', '--output', action='store', type=pathlib.Path, required=True,
                               help="Anndata output folder path.")
    parser_anndata.add_argument('-c', '--cache', action='store', type=pathlib.Path,
                               help="Dataset cache folder path.")


if __name__ == "__main__":
    main()
