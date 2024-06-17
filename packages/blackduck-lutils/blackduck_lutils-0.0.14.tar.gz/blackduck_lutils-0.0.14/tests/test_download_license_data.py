'''
Test driver for license conflict script
Feb 27, 2024, MK




'''

import argparse
import json
import logging
import sys

from blackduck import Client
from pprint import pprint

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("blackduck").setLevel(logging.DEBUG)

def download_license_data(**kwargs):
    base_url = kwargs.get('base_url', None)
    token = kwargs.get('token', None)
    no_verify = kwargs.get('no_verify', None)
    output_file = kwargs.get('output_file', None)
    bd = Client(base_url=base_url, token=token, verify=no_verify, timeout=60.0, retries=4)
    licenses = bd.get_items("/api/licenses")
    data = []
    for license in licenses:
        license_terms = [l for l in bd.get_resource('license-terms', license)]
        license['licenseTerms'] = license_terms
        data.append(license)
    with open(output_file,'w') as f:
        json.dump(data,f)
    logging.info(f"{len(data)} Licenses retrieved")

def parse_command_args():

    parser = argparse.ArgumentParser("test_download_license_data.py")
    parser.add_argument("-u", "--base-url",     required=True, help="Hub server URL e.g. https://your.blackduck.url")
    parser.add_argument("-t", "--token-file",   required=True, help="File containing access token")
    parser.add_argument("-nv", "--no-verify",   action='store_false', help="Disable TLS certificate verification")
    parser.add_argument("-pn", "--project-name", required=False, help="Project Name")
    parser.add_argument("-pv", "--project-version-name", required=False, help="Project Version Name")
    parser.add_argument("-o", "--output-file", required=False, default='license_data.json', help="Local Storage file for license information")
    return parser.parse_args()

def main():
    args = parse_command_args()
    
    with open(args.token_file, 'r') as tf:
        token = tf.readline().strip()
    logging.info(f"Downloading license data from {args.base_url} into {args.output_file}")
    report = download_license_data(base_url=args.base_url, token=token, no_verify=args.no_verify, output_file = args.output_file)
    logging.info(f"Done.")
    
if __name__ == "__main__":
    sys.exit(main())


