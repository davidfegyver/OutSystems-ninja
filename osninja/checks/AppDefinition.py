from colorama import Fore, Style
import requests
import urllib3
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, root_module_name, module_name):
    url = f"{target}/{root_module_name}/scripts/{module_name}.appDefinition.js"
    response = requests.get(url, verify=False)

    appdefinition = {}

    if response.status_code == 200 and response.headers['Content-Type'] == 'application/javascript':
        match = re.search(r'return (\{.*\});', response.text, re.DOTALL)
        if match:
            appdefinition = json.loads(re.sub(r'(\w+):', r'"\1":', match.group(1)))

    else:
        print(f"{Fore.YELLOW}[!] appDefinition for {root_module_name}/{module_name} not found{Style.RESET_ALL}")
    
    return appdefinition