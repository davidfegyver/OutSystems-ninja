from colorama import Fore, Style
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, root_module_name, module_name):
    url = f"{target}/{root_module_name}/scripts/{module_name}.languageResources.js"
    response = requests.get(url, verify=False)

    languageResources = {}

    if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('application/javascript'):
        matches = re.findall(r'this\.setMessage\("([^"]+)",\s*"([^"]+)"\)', response.text)

        languageResources = {key: value for key, value in matches}

    else:
        print(f"{Fore.YELLOW}[!] languageResources for {root_module_name}/{module_name} not found{Style.RESET_ALL}")
    
    return languageResources
