import os 
import re

def generate_module_stuff(module_names):
    results = set()
    results.update(module_names)

    with open(os.path.join(os.path.dirname(__file__), "wordlists/modules.txt"), "r") as f:
        endings = [re.split(r" +", line)[0] for line in f.read().split("\n") if line.strip()]

    for module_name in module_names:
        results.update(module_name.split("_"))

    for module_name in module_names:
        for ending in endings:
            if not module_name.endswith(ending):
                results.add(f"{module_name}{ending}")

    return results