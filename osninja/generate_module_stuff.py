import os 
import re

def generate_module_stuff(module_names):
    results = set()
    results.update(module_names)

    with open(os.path.join(os.path.dirname(__file__), "wordlists/endings.txt"), "r") as f:
        endings = [re.split(r" +", line)[0] for line in f.read().split("\n") if line.strip()]


    for module_name in module_names:
        results.add(module_name.split("_")[0])

    
    for module_name in module_names:
        for ending in endings:
            results.add(f"{module_name}{ending}")
            results.add(f"{module_name.split("_")[0]}{ending}")
            
    return list(results)
