from colorama import Fore, Style
import requests
import urllib3
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, module_name):
    url = f"{target}/{module_name}/Default.aspx"
    response = requests.get(url, verify=False)

    if response.status_code == 200 and response.headers['Content-Type'].startswith('text/html'):
        return True
    
    return False
    