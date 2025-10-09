import json
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from algorithm.lsystem import LSystem
from algorithm.lsystem_tree import LSystemTree
from utils.constants import BUSH_3D, SETH_TREE, ZONO_TREE

plant_list = [ZONO_TREE]

for plant in plant_list:
    name, axiom, rule = plant
    lsystem = LSystem(axiom=axiom, rule=rule)
    
    batches = True

    # Use n=7 iterations for bush as specified in the figure
    # iterations = 7 if name == "bush_3d" else 5
    if plant_list == [ZONO_TREE]:
        iterations = 7
        remove_a_string = True
        branch_length = 0.2
        angle = 22.5
        initial_diameter = 0.10 # 1.25
        diameter_scale = 0.85 # 0.85
        num_batches = 2
    else:
        iterations = 5
        remove_a_string = False
        branch_length = 0.2
        angle = 22.5
        initial_diameter = 10.0
        diameter_scale = 0.85
        num_batches = 1

    lsystem.iterate(iterations=iterations)
    if remove_a_string:
        lsystem.remove_symbol("A")

    string = lsystem.state

    print(f"Processing L-System String: {string}\n")

    # angle = 22.5 if name == "bush_3d" else 40
    # if name == "seth_tree":
    #     angle = 26
    lsystem_tree = LSystemTree(
        string,
        branch_length=0.2,
        angle_deg=angle,
        initial_diameter=initial_diameter,
        diameter_scale=diameter_scale,
    )

    # Print the hierarchical structure of the tree
    # print("--- Tree Structure ---")
    # lsystem_tree.show()

    # Get the list of branches
    if batches:
        all_trees = lsystem_tree.generate_batch_trees(num_batches=num_batches)
        name = name + "_batches"
    else:
        all_trees = lsystem_tree.generate_batch_trees(num_batches=num_batches)

    all_batches_data = []

    print("\n--- Branch List ---")
    print("Format: (start_point, end_point, branch_type, diameter)")

    # Handle batched trees (list of branch lists)
    for tree_idx, tree_branches in enumerate(all_trees):
        print(f"Tree {tree_idx + 1}: {len(tree_branches)} branches")
        
        # Create lists for the current batch
        b_start, b_end, b_type, b_diameter = [], [], [], []

        for start, end, btype, diameter in tree_branches:
            b_start.append(start.tolist())
            b_end.append(end.tolist())
            b_type.append(btype)
            b_diameter.append(diameter)
        
        # Append the dictionary for the current batch
        all_batches_data.append({
            "start": b_start,
            "end": b_end,
            "btype": b_type,
            "diameter": b_diameter,
        })

    # The final dictionary now contains a list of batches
    stats = {
        "name": name,
        "iterations": iterations,
        "remove_a_string": remove_a_string,
        "branch_length": branch_length,
        "angle": angle,
        "initial_diameter": initial_diameter,
        "diameter_scale": diameter_scale,
        "num_batches": num_batches,
        "batches": all_batches_data,
    }
    os.makedirs(os.path.join(os.getcwd(), "results", "trees"), exist_ok=True)

    with open(f"results/trees/lsystem_{name}.json", "w") as f:
        json.dump(stats, f, indent=2)
        
    print(f"Saved to: results/trees/lsystem_{name}.json")
