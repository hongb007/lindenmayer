import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from algorithm.lsystem import LSystem
from algorithm.lsystem_tree import LSystemTree
from utils.constants import BETTER_3D_TREE, DECIDUOUS_TREE

plant_list = [DECIDUOUS_TREE]

for plant in plant_list:
    name, axiom, rule = plant
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=4)

    string = lsystem.state

    print(f"Processing L-System String: {string}\n")

    # Create the tree object
    lsystem_tree = LSystemTree(string, branch_length=3, angle_deg=40)

    # Print the hierarchical structure of the tree
    # print("--- Tree Structure ---")
    # lsystem_tree.show()

    # Get the list of branches
    branch_list = lsystem_tree.get_branches()

    b_start = []
    b_end = []
    b_type = []

    print("\n--- Branch List ---")
    print("Format: (start_point, end_point, branch_type)")
    for i, (start, end, btype) in enumerate(branch_list):
        # Convert NumPy arrays to Python lists for JSON serialization
        b_start.append(start.tolist())
        b_end.append(end.tolist())
        b_type.append(btype)
        # Format numpy arrays for cleaner printing
        # start_str = np.array2string(start, precision=2, separator=', ')
        # end_str = np.array2string(end, precision=2, separator=', ')
        # print(f"Branch {i+1}: ({start_str}, {end_str}, '{btype}')")

    stats = {
            'name': name,
            'start': b_start,
            'end': b_end,
            'btype': b_type
        }

    os.makedirs(os.path.join(os.getcwd(), "results", "trees"), exist_ok=True)

    with open(f"results/trees/lsystem_{name}.json", 'w') as f:
        json.dump(stats, f, indent=2)

