from colorama import Fore, Style
import requests
import urllib3
import json
import re
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, data):
    results = {}

    for module_name in data['moduleservices']:
        print(f"{Fore.GREEN}[*] Starting Screen Services scan {module_name}{Style.RESET_ALL}")
     
        results[module_name] = {}
        module_paths = data['moduleservices'][module_name]['assets']

        module_js_paths = filter_js(module_paths)
        for js_path in module_js_paths:
            js_url = f"{target}{js_path}"
            js_name = js_path.split("/")[-1]
            
            if js_name in results[module_name]:
                continue

            results[module_name][js_name] = {}
            try:
                response = requests.get(js_url, verify=False)
                if response.status_code == 200 and response.headers['Content-Type'].startswith('application/javascript'):
                    if "callServerAction" in response.text:
                        callServerActions = extract_callServerActions(response.text)
                        results[module_name][js_name]['callServerActions'] = callServerActions
                
                if results[module_name][js_name]:
                    inputs = extract_inputs(response.text)
                    results[module_name][js_name]['inputs'] = inputs

            except Exception as e:
                print(f"\n{Fore.RED}[!] Error while scanning {js_path}: {e}{Style.RESET_ALL}\n")

        results[module_name] = {key: value for key, value in results[module_name].items() if value}
    return results


def filter_js(paths):
    js_paths = [path for path in paths if path.endswith(".js")]
    wanted = ['mvc', 'controller']
    
    return [path for path in js_paths if any(w in path for w in wanted)]

def extract_callServerActions(js):
    pattern = re.compile(r'callServerAction\("[^"]+",\s*"([^"]+)"')
    matches = pattern.finditer(js)
    matches = [{"start":match.start(), "endpoint": match.group(1)} for match in matches]
    return matches

def extract_inputs(js):
    pattern = re.compile(r'(\w+):\s+OS\.DataConversion\.ServerDataConverter\.to\(\w+, OS\.DataTypes\.DataTypes\.(\w+)\)')
    matches = pattern.finditer(js)
    matches = [{"start":match.start(), 'variable':{
        "name": match.group(1),
        "type": match.group(2)
    }} for match in matches]
    return matches




def openapi_generator(target, results):
    openapi_spec = {
    "openapi": "3.0.0",
    "servers": [
        {
            "url": target
        }
    ],
    "info": {
        "title": "OutSystems ScreenServices API for " + target,
        "version": "1.0.0",
        "description": "Auto-generated OpenAPI specification with OSninja"
    },
    "paths": {
    },
    "components": {
        "securitySchemes": {
            "CSRFtoken": {
                "type": "apiKey",
                "in": "header",
                "name": "X-Csrftoken",
            }
        }
    },
    "security": [
        {
            "CSRFtoken": []
        }
    ]

    #  header : X-Csrftoken: T6C+9iB49TLra4jEsMeSckDMNhQ=
    }
    for module_name in results:
        for js_name in results[module_name]:
            last_start = 0
            for action in results[module_name][js_name]['callServerActions']:
                endpoint = action['endpoint']
                full_api_path = f"/{module_name}/{endpoint}"
                viewName = ".".join(js_name.split(".")[1:3])

                apiVersion = "GzexgMqKYFKDrTYvpVFbKA"

                if full_api_path  in openapi_spec['paths']:
                    continue

                openapi_spec['paths'][full_api_path] = {}

                current_start = action['start']
                inputs = results[module_name][js_name]['inputs']
                inputParameters = {}
                for input_ in inputs:
                    if input_['start'] > last_start and input_['start'] < current_start:
                        inputParameters[input_['variable']['name']] = {

                                "type": OSType2openapi(input_['variable']['type'])
                            
                        }

                        last_start = input_['start']

            
                openapi_spec['paths'][full_api_path]['post'] = {
                    "summary": f"Call {endpoint} from {module_name}",
                    "description": f"Call {endpoint} from {module_name}",
                    "operationId": f"{module_name}_{endpoint}",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "versionInfo": {
                                            "type": "object",
                                            "properties": {
                                                "moduleVersion": {
                                                    "type": "string",
                                                    "example": "-"
                                                    
                                                },
                                                "apiVersion": {
                                                    "type": "string",
                                                    "example": apiVersion
                                                }
                                            }
                                        },
                                        "viewName": {
                                            "type": "string",
                                            "example": viewName
                                        },
                                        "inputParameters": {
                                            "type": "object",
                                            "properties": inputParameters
                                                
                                            
                                        },
                                        "clientVariables": {
                                            "type": "object"
                                        }

                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }


                    
                
                last_start = current_start


    return openapi_spec

def OSType2openapi(OSType): 
    if OSType == "Text":
        return "string"
    elif OSType == "Integer":
        return "integer"
    elif OSType == "Record":
        return "object"
    elif OSType == "RecordList":
        return "object"
    elif OSType == "DateTime":
        return "string"
    elif OSType == "Boolean":
        return "boolean"
    else:
        return "string"

