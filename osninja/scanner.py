import json
import osninja.mem
import osninja.checks.AppDefinition
import osninja.checks.ReferencesHealth
import osninja.checks.LanguageResources
import osninja.checks.DefaultEntry
import osninja.generate_module_stuff
import osninja.knownModule
import osninja.checks.ModuleServices

from colorama import Fore, Style


def process_modules(modules):
    if osninja.mem.config['perms']:
        return osninja.generate_module_stuff.generate_module_stuff(modules)
    return modules

def module_references_scan(url, root_module_name, module_name, results):
    if module_name in results['module_references'] and len(results['module_references'][module_name]) > 0:
        return 
    
    if osninja.knownModule.is_internal_module(module_name):
        return

    print(f"\r\033[K[*] Scanning {module_name}", end="")
    try:
        referenced_modules = osninja.checks.ReferencesHealth.run(url, root_module_name, module_name)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error while scanning {module_name}: {e}{Style.RESET_ALL}\n")

    results['module_references'][module_name] = referenced_modules or []
    
    for referenced_module_name in referenced_modules:
        module_references_scan(url, root_module_name, referenced_module_name, results)
        module_references_scan(url, referenced_module_name, referenced_module_name, results)

def scan(url):
    results = {
        "module_references": {},
        "appdefinitions": {},
        "language_resources": {},
        "default_entries": [],
        "moduleservices": {}
    }
    
    print(f"{Fore.GREEN}[*] Starting Module References scan {url}{Style.RESET_ALL}")
    for root_module in process_modules(osninja.mem.config['known']):
        module_references_scan(url, root_module, root_module, results)
    print(f"\n{Fore.GREEN}[*] Found {len(results["module_references"])} modules in total{Style.RESET_ALL}")

    print(f"{Fore.GREEN}[*] Starting AppDefinition scan {url}{Style.RESET_ALL}")
    for module_name in results["module_references"]:
        print(f"\r\033[K[*] Scanning {module_name}", end="")
        try:
            appdefinition = osninja.checks.AppDefinition.run(url, module_name)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error while scanning {module_name}: {e}{Style.RESET_ALL}\n")

        if appdefinition:
            results["appdefinitions"][module_name] = appdefinition 
    print(f"\n{Fore.GREEN}[*] Found {len(results['appdefinitions'])} AppDefinitions in total{Style.RESET_ALL}")

    print(f"{Fore.GREEN}[*] Starting LanguageResources scan {url}{Style.RESET_ALL}")

    for module_name in results["module_references"]:
        print(f"\r\033[K[*] Scanning {module_name}", end="")
        try:
            language_resources = osninja.checks.LanguageResources.run(url, module_name)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error while scanning {module_name}: {e}{Style.RESET_ALL}\n")

        if language_resources:
            results["language_resources"][module_name] = language_resources

    print(f"\n{Fore.GREEN}[*] Found {len(results['language_resources'])} LanguageResources in total{Style.RESET_ALL}")

    print(f"{Fore.GREEN}[*] Starting DefaultEntry scan {url}{Style.RESET_ALL}")
    for module_name in results["module_references"]:
        print(f"\r\033[K[*] Scanning {module_name}", end="")
        try:
            default_entry = osninja.checks.DefaultEntry.run(url, module_name)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error while scanning {module_name}: {e}{Style.RESET_ALL}\n")

        if default_entry:
            results["default_entries"].append(module_name)

    print(f"\n{Fore.GREEN}[*] Found {len(results['default_entries'])} DefaultEntries in total{Style.RESET_ALL}")

    print(f"{Fore.GREEN}[*] Starting ModuleServices scan {url}{Style.RESET_ALL}")
    for module_name in results["module_references"]:
        print(f"\r\033[K[*] Scanning {module_name}", end="")
        try:
            module_services = osninja.checks.ModuleServices.run(url, module_name)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error while scanning {module_name}: {e}{Style.RESET_ALL}\n")

        if module_services:
            results["moduleservices"][module_name] = module_services
    
    return results
