import json
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from algorithm.lsystem import LSystem
from algorithm.lsystem_tree import LSystemTree
from utils.constants import ZONO_TREE

np.random.seed(0)

num_worlds = 100
plant = ZONO_TREE

for i in range(0,num_worlds):
    name, axiom, rule = plant
    lsystem = LSystem(axiom=axiom, rule=rule)
    
    batches = False

    if plant == ZONO_TREE:
        iterations = 7
        remove_a_string = True
        branch_length = 0.2
        angle = 22.5
        initial_diameter = 0.10 
        diameter_scale = 0.9 
        num_batches = 1

    lsystem.iterate(iterations=iterations)
    if remove_a_string:
        lsystem.remove_symbol("A")

    string = lsystem.state

    # print(f"Processing L-System String: {string}\n")

    lsystem_tree = LSystemTree(
        string,
        branch_length=0.2,
        angle_deg=angle,
        initial_diameter=initial_diameter,
        diameter_scale=diameter_scale,
    )

    # Get the list of branches
    all_trees = lsystem_tree.generate_batch_trees(num_batches=1)

    all_batches_data = []
    all_branch_length_data = []

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
        all_branch_length_data.append(len(tree_branches))

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
        "branch_lengths": all_branch_length_data,
        "matched_rules_num": lsystem.get_rule_statistics(),
        "batches": all_batches_data,
    }
    os.makedirs(os.path.join(os.getcwd(), "results", "trees", "worlds"), exist_ok=True)

    with open(f"results/trees/worlds/lsystem_{i}_{name}.json", "w") as f:
        json.dump(stats, f, indent=2)
        
    print(f"Saved to: results/trees/worlds/lsystem_{i}_{name}.json")
