'''
Test driver for license conflict script
Feb 27, 2024, MK




'''

import argparse
import logging
import sys

from license_conflict_report import generate_license_conflict_report

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("blackduck").setLevel(logging.DEBUG)

def parse_command_args():

    parser = argparse.ArgumentParser("test_license_conflicts.py")
    parser.add_argument("-u", "--base-url",     required=True, help="Hub server URL e.g. https://your.blackduck.url")
    parser.add_argument("-t", "--token-file",   required=True, help="File containing access token")
    parser.add_argument("-nv", "--no-verify",   action='store_false', help="Disable TLS certificate verification")
    mux = parser.add_mutually_exclusive_group()
    mux.add_argument("-pn", "--project-name", required=False, help="Project Name")
    parser.add_argument("-pv", "--project-version-name", required=False, help="Project Version Name")
    mux.add_argument("-sbom", required=False, help="SBOM File to process")
    parser.add_argument("-ld", "--license-data", required=False, default='license_data.json', help="Local license data storage")
    parser.add_argument("-o", "--output-file", required=False, default=None, help="CSV file name for output")
    return parser.parse_args()


def main():
    args = parse_command_args()
    
    if args.sbom:
        logging.info(f"Processing SBOM file {args.sbom}")
        report = generate_license_conflict_report(sbom=args.sbom, 
                                                  license_data_file=args.license_data,
                                                  csv_report_file=args.output_file)
        
    if args.project_name and args.project_version_name:
        logging.info(f"Processing Project {args.project_name} Version {args.project_version_name}")
        with open(args.token_file, 'r') as tf:
            token = tf.readline().strip()
        generate_license_conflict_report(base_url=args.base_url, 
                                                  token=token, 
                                                  no_verify=args.no_verify, 
                                                  project_name=args.project_name, 
                                                  project_version_name=args.project_version_name,
                                                  license_data_file=args.license_data,
                                                  csv_report_file=args.output_file)
        # Note that if csv_output file is not specified, it will be generated automatically as
        # ProjectName_Version_YYYY-MM-DD_HHMMSS.csv


    
if __name__ == "__main__":
    sys.exit(main())


