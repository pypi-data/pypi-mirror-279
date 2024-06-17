'''
Created on February 12, 2024
@author: kumykov

Copyright (C) 2024 Synopsys, Inc.
http://www.synopsys.com/

This software implements Protex license conflict model as an 
external add-on to Black Duck.
Calculations are based on Protex license representation.

'''

import sys
import argparse
import io
import json
import logging
import time

from zipfile import ZipFile

from blackduck import Client
from pprint import pprint

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("blackduck").setLevel(logging.DEBUG)

# Defining some globals
PERMITTED = 'PERMITTED'
FORBIDDEN = 'FORBIDDEN'
REQUIRED = 'REQUIRED'



# skipTermsForForbiddenVsRequired = ['Hold Liable', 'Sub-License']
# skipTermsForForbiddenVsPermitted = ['Hold Liable', 'Sub-License']
skipTermsForForbiddenVsRequired = []
skipTermsForForbiddenVsPermitted = []

skipForbiddenVsPermittedCheck = False  # this check has limited value, and creates lots of noise

# Terms for Software Programmer Category
termsCategoryProgrammer = ['Include Copyright', 'Include License', 'Include Notice', 'State Changes']

# Terms for Software Release Category
termsCategoryRelease = ['Disclose Source', 'Distribute', 'Distribute Original']

# Terms for Legal Category
termsCategoryLegal = ['Anti DRM Provision',  'Compensate Damages', 'Hold Liable', 'License Back', 'Modify', 'Reverse Engineer', \
       'Patent Retaliation', 'Place Additional Restrictions', 'Place Warranty', 'Sub-License', 'Use Patent Claims', 'Right to Copy']

# Terms for Business Category
termsCategoryBusiness = ['Fees', 'Use Trademarks']

class LicenseData():
    def __init__(self, filename = 'License_data.json'):
        self.filename = filename
        self.data = None
        self.forbidden = []
        self.permitted = []
        self.required = []
        self.load_data()

    def load_data(self):
        with open(self.filename,'r') as f:
            self.data = json.load(f)
        logging.debug(f"Loaded {len(self.data)} Licenses from {self.filename}")
        for l in self.data:
            ref_id = l.get('spdxId', None)
            if not ref_id:
                ref_id = f"LicenseRef-{l['_meta']['href'].split('/')[5]}"
            for t in l['licenseTerms']:
                if t['responsibility'] == FORBIDDEN:
                    self.forbidden.append({ref_id:t['name']})
                elif t['responsibility'] == PERMITTED:
                    self.permitted.append({ref_id:t['name']})
                elif t['responsibility'] == REQUIRED:
                    self.required.append({ref_id:t['name']})
                else:
                    logging.error(f"Unknown responsibility {t['responsibility']}")

    def get_license(self, ref_id):
        if ref_id.startswith('LicenseRef'):
            uuid = ref_id[11:]
            matches = [l for l in self.data if l['_meta']['href'].endswith(uuid)]    
        else:
            matches = [l for l in self.data if l.get('spdxId', None) == ref_id]
        return None if len(matches) == 0 else matches[0]
    
    def intersect_values(self, list1, list2):
        return [value for value in list1 if value in list2]

    # produces a list of conflicted terms for a pair of licenses
    # in format [ID1, ID2, [Term1, Term2 ...]] 
    def get_license_conflict(self, a, b):
        conflicts = []
        license1 = self.get_license(a)
        license2 = self.get_license(b)
        license1_forbidden_terms = {t[a] for t in self.forbidden if a in t}
        license1_permitted_terms = {t[a] for t in self.permitted if a in t}
        license1_required_terms = {t[a] for t in self.required if a in t}
        license2_forbidden_terms = {t[b] for t in self.forbidden if b in t}
        license2_permitted_terms = {t[b] for t in self.permitted if b in t}
        license2_required_terms = {t[b] for t in self.required if b in t}

        conflicts = []    
        # Processing Forbidden vs. Permitted terms    
        conflicts.extend(self.intersect_values(license1_forbidden_terms, license2_permitted_terms))
        conflicts.extend(self.intersect_values(license2_forbidden_terms, license1_permitted_terms))
        # Processing Forbidden vs. Required terms 
        conflicts.extend(self.intersect_values(license2_forbidden_terms, license1_required_terms))
        conflicts.extend(self.intersect_values(license2_required_terms, license1_forbidden_terms))
        # Remove skipped terms
        for term in skipTermsForForbiddenVsRequired:
            if term in conflicts:
                conflicts.remove(term)
        if len(conflicts):
            return [a, b, conflicts]
        else:
            return None
    
    # Produces a list of license pair and associated conflicting terms 
    # as returned by @get_license_conflict method
    def get_license_conflicts_list(self, unique_license_list):
        import itertools
        conflict_list = []
        for a, b in itertools.combinations(unique_license_list, 2):
            cc = self.get_license_conflict(a, b)
            if cc and (not (cc in conflict_list or [cc[1], cc[0], cc[2]] in conflict_list)):
                conflict_list.append(cc)
        return conflict_list

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

def find_project_by_name(bd, project_name):
    params = {
        'q': [f"name:{project_name}"]
    }
    projects = [p for p in bd.get_resource('projects', params=params) if p['name'] == project_name]
    assert len(projects) == 1, f"Project {project_name} not found."
    return projects[0]

def find_project_version_by_name(bd, project, version_name):
    params = {
        'q': [f"versionName:{version_name}"]
    }
    versions = [v for v in bd.get_resource('versions', project, params=params) if v['versionName'] == version_name]
    assert len(versions) == 1, f"Project version {version_name} for project {project['name']} not found"
    return versions[0]

def create_sbom_report(bd, version, type, include_subprojects):
    post_data = {
            'reportFormat': "JSON",
            'sbomType': type,
            'includeSubprojects': include_subprojects	
    }
    sbom_reports_url = version['_meta']['href'] + "/sbom-reports"

    bd.session.headers["Content-Type"] = "application/vnd.blackducksoftware.report-4+json"
    r = bd.session.post(sbom_reports_url, json=post_data)
    if (r.status_code == 403):
        logging.debug("Authorization Error - Please ensure the token you are using has write permissions!")
    r.raise_for_status()
    location = r.headers.get('Location')
    assert location, "Hmm, this does not make sense. If we successfully created a report then there needs to be a location where we can get it from"
    return location

def download_report(bd, location, retries):
    report_id = location.split("/")[-1]
    if retries:
        logging.debug(f"Retrieving generated report from {location}")
        response = bd.session.get(location)
        report_status = response.json().get('status', 'Not Ready')
        if response.status_code == 200 and report_status == 'COMPLETED':
            response = bd.session.get(location + "/download.zip", headers={'Content-Type': 'application/zip', 'Accept':'application/zip'})
            if response.status_code == 200:
                return response.content
            else:
                logging.error("Ruh-roh, not sure what happened here")
                return None
        else:
            logging.debug(f"Report status request {response.status_code} {report_status} ,waiting {retries} seconds then retrying...")
            time.sleep(60)
            retries -= 1
            return download_report(bd, location, retries)
    else:
        logging.debug(f"Failed to retrieve report {report_id} after multiple retries")
        return None

def un_group_licenses(license_list):
    singular = [l for l in license_list if not l.startswith("(")]
    groups = [l for l in license_list if l.startswith("(")]
    import re
    for group in groups:
        l = re.split("\(|\)|AND|OR| ", group)
        singular += list(filter(len,l))
    return singular

def get_component_conflicts(ref_id1, ref_id2, sbom_data, license_conflict_list):
    id1_licenses = un_group_licenses([package['licenseConcluded'] for package in sbom_data['packages'] if package['SPDXID'] == ref_id1])
    id2_licenses = un_group_licenses([package['licenseConcluded'] for package in sbom_data['packages'] if package['SPDXID'] == ref_id2])
    result = []
    for l1 in id1_licenses:
        for l2 in id2_licenses:
            if l1 != l2:
                l = [con for con in license_conflict_list if l1 in con and l2 in con]
                result.extend(l)
    if len(result):
        return result
    else:
        return None
    
def get_component_name_version(ref_id, sbom_data):
    c = [p for p in sbom_data['packages'] if p['SPDXID'] == ref_id]
    return (c[0]['name'], c[0]['versionInfo'])

def has_license(ref_id, license_ref, sbom_data):
    components = [c for c in sbom_data['packages'] if c['SPDXID'] == ref_id]
    return [license_ref in components[0]['licenseConcluded']]

def write_csv_report(conflict_report_data, sbom_data, license_data: LicenseData, output_file='output.csv'):
    result = []
    import csv
    with open(output_file,"w") as csvfile:
        fieldnames = ['Category','ComponentName','ComponentLicense','ConflictingComponentName'
                      ,'ConflictingComponentLicense','ConflictingLicenseTerm'
                      ,'TermValue','ConflictingTermValue','TermDescription','ConflictingTermDescription']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for item in conflict_report_data:
            component_name = get_component_name_version(item[0], sbom_data)
            conflicting_component_name = get_component_name_version(item[1], sbom_data)
            for c in item[2]:
                if has_license (item[0], c[0], sbom_data)[0]:
                    license_ref = c[0]
                    conflicting_license_ref = c[1]
                else:
                    license_ref = c[1]
                    conflicting_license_ref = c[0]
                license = license_data.get_license(license_ref)
                license_terms = license['licenseTerms']
                conflicting_license = license_data.get_license(conflicting_license_ref)
                conflicting_license_terms = conflicting_license['licenseTerms']
                license_name = license['name']
                conflicting_license_name = conflicting_license['name']
                for term in c[2]:
                    if term in termsCategoryBusiness:
                        category = 'BUSINESS'
                    elif term in termsCategoryLegal:
                        category = 'LEGAL'
                    elif term in termsCategoryProgrammer:
                        category = 'SOFTWARE PROGRAMMER'
                    elif term in termsCategoryRelease:
                        category = 'SOFTWARE RELEASE'
                    else:
                        category = 'OTHER'
                    term_values = [(lt['responsibility'], lt['description']) for lt in license_terms if term == lt['name']][0]
                    conflicting_term_values = [(lt['responsibility'], lt['description']) for lt in conflicting_license_terms if term == lt['name']][0]
                    result = f"{category},{component_name},{license_name},{conflicting_component_name},{conflicting_license_name},{term}"
                    result += f",{term_values[0]},{conflicting_term_values[0]},{term_values[1]},{conflicting_term_values[1]}"
                    row = dict()
                    row['Category'] = category
                    row['ComponentName'] = component_name[0] + " " + component_name[1]
                    row['ComponentLicense'] = license_name
                    row['ConflictingComponentName'] = conflicting_component_name[0] + " " + conflicting_component_name[1]
                    row['ConflictingComponentLicense'] = conflicting_license_name
                    row['ConflictingLicenseTerm'] = term
                    row['TermValue'] = term_values[0]
                    row['ConflictingTermValue'] = conflicting_term_values[0]
                    row['TermDescription'] = term_values[1]
                    row['ConflictingTermDescription'] = conflicting_term_values[1]
                    writer.writerow(row)



def generate_license_conflict_report(**kwargs):
    sbom = kwargs.get('sbom', None)
    base_url = kwargs.get('base_url', None)
    token = kwargs.get('token', None)
    no_verify = kwargs.get('no_verify', None)
    project_name = kwargs.get('project_name', None)
    project_version_name = kwargs.get('project_version_name', None)
    license_data_file = kwargs.get('license_data', 'license_data.json')
    csv_report_file = kwargs.get('csv_report_file', None)
    if sbom:
        logging.debug(f"Loading SBOM file {sbom}")
        sbom_data = load_sbom_report(sbom)
    else:
        bd = Client(base_url=base_url, token=token, verify=no_verify, timeout=60.0, retries=4)
        sbom_data = produce_online_sbom_report(bd, project_name, project_version_name)
    # Get toplevel reference id
    document_spdx_id = sbom_data['SPDXID']
    document_describes = [rel['relatedSpdxElement'] for rel in sbom_data['relationships'] if rel['spdxElementId'] == document_spdx_id and rel['relationshipType'] == 'DESCRIBES']
    if not document_describes:
        doc_name = sbom_data['name']
        packages = sbom_data['packages']
        document_describes = [p['SPDXID'] for p in packages if doc_name == f"{p['name']}-{p['versionInfo']}"] 
    project_spdx_id = document_describes[0]
    # Rebuild component tree, so relationship path could be retrieved.
    component_tree = get_component_tree(project_spdx_id, sbom_data['relationships'])
    # Get full component list
    component_list = [c['SPDXID'] for c in sbom_data['packages']]
    # Generate list of unique licenses present in the project
    license_list = [c['licenseConcluded'] for c in sbom_data['packages']]
    unique_license_list = un_group_licenses(list(set(license_list)))
    # Load License Data
    license_data = LicenseData(license_data_file)
    # Get conflicts between unique licenses
    license_conflict_list = license_data.get_license_conflicts_list(unique_license_list)
    # Report conflicting components
    total_comparisons = 0
    total_conflicts = 0
    logging.info(f"Processing list of {len(component_list)} components")
    import itertools
    conflict_report_data = []
    for ref_id1, ref_id2 in itertools.combinations(component_list,2):
        if evaluate_rel_paths(ref_id1, ref_id2, component_tree):
            conflicts = get_component_conflicts(ref_id1, ref_id2, sbom_data, license_conflict_list)
            if conflicts:
                total_conflicts += 1
                conflict_report_data.append([ref_id1, ref_id2, conflicts])
            total_comparisons += 1
    logging.info(f"Processed {total_comparisons} component pairs, {total_conflicts} conflicts detected")
    if not csv_report_file:
        project_name_version = get_component_name_version(project_spdx_id, sbom_data)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        csv_report_file = f"{project_name_version[0]}_{project_name_version[1]}_{timestamp}.csv".replace(" ","_")
    logging.info(f"Writing report into {csv_report_file}")
    write_csv_report(conflict_report_data, sbom_data, license_data, csv_report_file)

def get_component_tree(spdx_id, relationships):
    children = {rel['relatedSpdxElement']:{'rel': rel['relationshipType'], 'children': {}} for rel in relationships if rel['spdxElementId'] == spdx_id and not rel_in_use(rel['relationshipType'])}
    children.update({rel['spdxElementId']:{'rel': rel['relationshipType'], 'children': {}} for rel in relationships if rel['relatedSpdxElement'] == spdx_id and rel_in_use(rel['relationshipType'])})
    if len(children) == 0:
        return None
    for child in children.keys():
        c = get_component_tree(child, relationships)
        if c:
            children[child]['children'] = c
    return children

def get_component_relationship_path(spdx_id, component_tree):
    path = []
    if spdx_id in component_tree.keys():
        path.append(component_tree[spdx_id]['rel'])
        return path
    else:
        for id in component_tree.keys():
            subtree = component_tree[id]['children']
            if subtree:
                path.append(component_tree[id]['rel'])
                subpath = get_component_relationship_path(spdx_id, subtree) 
                if subpath:
                    path.extend(subpath)
                    return path
                else:
                    path.pop()
            else:
                continue
        return None

# Evaluate relationship paths and and return false if relationship that 
# contains OTHER od DEV_TOOL_OF
def evaluate_rel_paths(ref_id1, ref_id2, component_tree):
    rel_path1 = get_component_relationship_path(ref_id1, component_tree)
    rel_path2 = get_component_relationship_path(ref_id2, component_tree)
    if rel_path1 == None and rel_path2 == None:
        reduced = []
    elif rel_path1 == None:
        reduced = rel_path2
    elif rel_path2 == None:
        reduced = rel_path1
    else:
        while len(rel_path1) > 0 and len(rel_path2) > 0:
            if rel_path1[0] == rel_path2[0]:
                rel_path1.pop(0)
                rel_path2.pop(0)
            else:
                break
        reduced = rel_path1 + rel_path2
    excluding_rel = ['OTHER', 'DEV_TOOL_OF']
    intersect = [x for x in reduced if x in excluding_rel]
    if len(intersect) > 0:
        return False
    else:
        return True
        
def rel_in_use (relationship):
    return relationship in ['DESCRIBED_BY',
                        'CONTAINED_BY',
                        'DEPENDS_ON',
                        'DEPENDENCY_OF',
                        'DEPENDENCY_MANIFEST_OF',
                        'BUILD_DEPENDENCY_OF',
                        'DEV_DEPENDENCY_OF',
                        'OPTIONAL_DEPENDENCY_OF',
                        'PROVIDED_DEPENDENCY_OF',
                        'TEST_DEPENDENCY_OF',
                        'RUNTIME_DEPENDENCY_OF',
                        'EXAMPLE_OF',
                        'GENERATED_FROM',
                        'ANCESTOR_OF',
                        'DESCENDANT_OF',
                        'VARIANT_OF',
                        'DATA_FILE_OF',
                        'TEST_CASE_OF',
                        'BUILD_TOOL_OF',
                        'DEV_TOOL_OF',
                        'TEST_OF',
                        'TEST_TOOL_OF',
                        'DOCUMENTATION_OF',
                        'OPTIONAL_COMPONENT_OF',
                        'METAFILE_OF',
                        'PACKAGE_OF',
                        'PREREQUISITE_FOR',
                        'REQUIREMENT_DESCRIPTION_FOR',
                        'SPECIFICATION_FOR']


def load_sbom_report(sbom):
    with open(sbom, 'r') as f:
        sbom_data = json.load(f)
    return sbom_data

def produce_online_sbom_report(bd, project_name, project_version_name):
    project = find_project_by_name(bd, project_name)
    logging.debug(f"Project {project['name']} located")
    version = find_project_version_by_name(bd, project, project_version_name)
    logging.debug(f"Version {version['versionName']} located")
    location = create_sbom_report(bd, version, 'SPDX_23', True)
    logging.debug(f"Created SBOM report of type SPDX_23 for project {project_name}, version {project_version_name} at location {location}")
    sbom_data_zip = download_report(bd, location, 60)
    logging.debug(f"Deleting report from Black Duck {bd.session.delete(location)}")
    zip=ZipFile(io.BytesIO(sbom_data_zip), "r")
    sbom_data = {name: zip.read(name) for name in zip.namelist()}
    filename = [i for i in sbom_data.keys() if i.endswith(".json")][0]
    return json.loads(sbom_data[filename])
    
def parse_command_args():

    parser = argparse.ArgumentParser("license_conflicts")
    parser.add_argument("-u", "--base-url",     required=False, help="Hub server URL e.g. https://your.blackduck.url")
    parser.add_argument("-t", "--token-file",   required=False, help="File containing access token")
    parser.add_argument("-nv", "--no-verify",   action='store_false', help="Disable TLS certificate verification")
    mux = parser.add_mutually_exclusive_group()
    mux.add_argument("-ldd", "--license-data-download", action='store_true', help="Download license data into a file specified with -ld/--license-data parameter")
    mux.add_argument("-pn", "--project-name", required=False, help="Project Name")
    parser.add_argument("-pv", "--project-version-name", required=False, help="Project Version Name")
    mux.add_argument("-sbom", required=False, help="SBOM File to process")
    parser.add_argument("-ld", "--license-data", required=False, default='license_data.json', help="Local license data storage")
    parser.add_argument("-o", "--output-file", required=False, default=None, help="CSV file name for license conflict report output")
    return parser.parse_args()

def main():
    args = parse_command_args()

    if args.sbom:
        logging.info(f"Processing SBOM file {args.sbom}")
        report = generate_license_conflict_report(sbom=args.sbom, 
                                                  license_data_file=args.license_data,
                                                  csv_report_file=args.output_file)
        return
        
    with open(args.token_file, 'r') as tf:
        token = tf.readline().strip()

    if args.project_name and args.project_version_name:
        logging.info(f"Processing Project {args.project_name} Version {args.project_version_name}")
        generate_license_conflict_report(base_url=args.base_url, 
                                                  token=token, 
                                                  no_verify=args.no_verify, 
                                                  project_name=args.project_name, 
                                                  project_version_name=args.project_version_name,
                                                  license_data_file=args.license_data,
                                                  csv_report_file=args.output_file)
        # Note that if csv_output file is not specified, it will be generated automatically as
        # ProjectName_Version_YYYY-MM-DD_HHMMSS.csv
        return
    
    if args.license_data_download:
        logging.info(f"Downloading license data from {args.base_url} into {args.output_file}")
        download_license_data(base_url=args.base_url, token=token, no_verify=args.no_verify, output_file = args.license_data)
        logging.info(f"Done.")
        return

if __name__ == "__main__":
    sys.exit(main())