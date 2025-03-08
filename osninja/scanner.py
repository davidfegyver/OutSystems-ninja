import json
import osninja.mem
import osninja.checks.AppDefinition
import osninja.checks.ReferencesHealth
import osninja.checks.LanguageResources
import osninja.generate_module_stuff

def process_modules(modules):
    if osninja.mem.config['perms']:
        return osninja.generate_module_stuff.generate_module_stuff(modules)
    return modules
    

def scan_module(url, root_module_name, module_name, results):
    if f"{root_module_name}/{module_name}" in results['scanned_modules']:
        return 
    
    results['scanned_modules'].add(f"{root_module_name}/{module_name}")
    
    results['modules'][root_module_name][module_name] = {}

    appdefinition = {}
    languageResources = {}
    referenced_modules = []
    
    print(f"[*] Running referencesHealth check for {root_module_name}/{module_name}")

    try:
        referenced_modules = osninja.checks.ReferencesHealth.run(url, root_module_name, module_name)
    except Exception as e:
        print(f"[*] Error running referencesHealth check for {root_module_name}/{module_name}: {e}")

    results['modules'][root_module_name][module_name]['referenced_modules'] = referenced_modules
    
    if len(referenced_modules) == 0:
        print(f"[*] No referenced modules found for {root_module_name}/{module_name}")
        results['modules'][root_module_name].pop(module_name)
        return

    if root_module_name == module_name:
        print(f"[*] Running appDefinition check for {root_module_name}/{module_name}")
        try:
            appdefinition = osninja.checks.AppDefinition.run(url, root_module_name, root_module_name)
        except Exception as e:
            print(f"[*] Error running appDefinition check for {root_module_name}/{module_name}: {e}")
            appdefinition = {}
        results['modules'][root_module_name][module_name]['appDefinition'] = appdefinition
        
    print(f"[*] Running languageResources check for {root_module_name}/{module_name}")
    try:
        languageResources = osninja.checks.LanguageResources.run(url, root_module_name, module_name)
    except Exception as e:
        print(f"[+] Error running languageResources check for {root_module_name}/{module_name}: {e}")

    results['modules'][root_module_name][module_name]['languageResources'] = languageResources
    
    for ref_module in process_modules(referenced_modules):
        scan_module(url, root_module_name, ref_module, results)

    if appdefinition == {} and languageResources == {} and referenced_modules == []:
        print(f"[*] No appDefinition, languageResources or referenced_modules found for {root_module_name}/{module_name}")

def scan(url):
    results = {
        "modules": {},
        "scanned_modules": set()
    }
    

    for root_module in process_modules(osninja.mem.config['known']):
        results['modules'][root_module] = {}
        scan_module(url, root_module,root_module, results)


    for root_module in results['scanned_modules'].copy():
        root_module = root_module.split('/')[1]
        if root_module not in results['modules']: 
            results['modules'][root_module] = {}
        scan_module(url, root_module, root_module, results)
    
    for root_module in results['modules'].copy():
        if results['modules'][root_module] == {}:
            results['modules'].pop(root_module)
    
    return results
