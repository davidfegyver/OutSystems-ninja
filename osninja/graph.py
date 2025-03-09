import json
import networkx as nx
import matplotlib.pyplot as plt
import osninja.knownModule

def write_graph(data, filename):
    module_references_list = data["module_references"]

    G = nx.DiGraph()

    for module_name, module_references in module_references_list.items():
        for referenced_module in module_references:
            if not osninja.knownModule.is_internal_module(referenced_module):
                G.add_edge(module_name, referenced_module)

        node_colors = []

        for node in G.nodes():
            if node not in module_references_list:
                node_colors.append("blue")
            elif node in data['appdefinitions'] or node in data['moduleservices'] or node in data['language_resources']:
                node_colors.append("green")
            elif node in data['default_entries']:
                node_colors.append("red")
            else:
                node_colors.append("blue")

    node_sizes = [G.degree(n) * 100 for n in G.nodes()]

    plt.figure(figsize=(30,30))
    #pos = nx.spring_layout(G)
    pos = nx.circular_layout(G)
    nx.draw(G, pos, 
            node_color=node_colors,
            node_size=node_sizes,
            with_labels=True, 
            font_size=8,
            alpha=0.5,
            width=1,
            edge_color="gray",
            font_color="black",
            font_weight="bold")
    plt.title("Module Dependency Graph")
    plt.savefig(filename, dpi=300)