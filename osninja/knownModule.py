import os 

with open(os.path.join(os.path.dirname(__file__), "wordlists/known.txt"), "r") as f:
    internals = [line.strip() for line in f.read().split("\n") if line.strip()]

def is_internal_module(module_name):
    return module_name in internals