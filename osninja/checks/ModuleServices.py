from colorama import Fore, Style
import requests
import urllib3
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, module_name):

    results = {}

    moduleinfo = run_moduleinfo(target, module_name)

    if 'manifest' in moduleinfo:
        results['urls'] = list(moduleinfo['manifest']['urlMappings'])
        results['assets'] = list(moduleinfo['manifest']['urlVersions'])

    pwa_manifest  = run_pwa_manifest(target, module_name)

    if pwa_manifest != {}:
        results['name'] = pwa_manifest['name']
        results['short_name'] = pwa_manifest['short_name']
        results['description'] = pwa_manifest['description']

    return results

def run_moduleinfo(target, module_name):
    url = f"{target}/{module_name}/moduleservices/moduleinfo"
    response = requests.get(url, verify=False)
    moduleinfo = {}

    if response.status_code == 200 and response.headers['Content-Type'].startswith('application/json'):
        moduleinfo = response.json()
    
    return moduleinfo

def run_pwa_manifest(target, module_name):
    url = f"{target}/{module_name}/moduleservices/pwa/manifest"
    response = requests.get(url, verify=False)

    pwa_manifest = {}

    if response.status_code == 200 and response.headers['Content-Type'].startswith('application/json'):
        pwa_manifest = response.json()

    return pwa_manifest
