from colorama import Fore, Style
import requests
import urllib3
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, root_module_name, module_name):
    url = f"{target}/{root_module_name}/scripts/{module_name}.referencesHealth.js"
    response = requests.get(url, verify=False)

    referencedModules = []

    if response.status_code == 200 and response.headers['Content-Type'] == 'application/javascript':
        referencedModules = re.findall(r"Reference to producer '([^']+)'" , response.text, re.DOTALL)

    else:
        print(f"{Fore.YELLOW}[!] referencesHealth for {root_module_name}/{module_name} not found{Style.RESET_ALL}")
    
    return referencedModules