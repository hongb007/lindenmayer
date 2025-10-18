#!/usr/bin/env python3
"""
L-System Tree Visualizer from JSON Files

This script loads pre-generated tree data from JSON files and creates 3D visualizations
using a plotting style consistent with the LSystemTree class.
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def visualize_tree_from_json(
    json_file_path, title=None, branch_colors=None, figsize=(12, 9), elev=25, azim=-60
):
    """
    Creates a 3D visualization from JSON data using diameter for line thickness.
    """
    # 1. Load data
    tree_data = load_tree_data(json_file_path)
    name = tree_data["name"]

    # 2. Setup Plot and Default Colors
    if branch_colors is None:
        branch_colors = {
            "F": "saddlebrown",
            "S": "darkgreen",
            "L": "green",
            "C": "limegreen",
            "A": "orange",
            "default": "gray",
        }

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    # 3. Consolidate all branches from single or batched data
    all_branches = []
    
    if "batches" in tree_data:
        print(f"Visualizing '{name}' with {len(tree_data['batches'])} batches...")
        for batch in tree_data["batches"]:
            # Ensure the diameter key exists for each batch
            if "diameter" not in batch:
                raise KeyError(
                    f"Required field 'diameter' missing from a batch in {json_file_path}"
                )
            # Combine all branch attributes into one list
            batch_branches = list(
                zip(batch["start"], batch["end"], batch["btype"], batch["diameter"])
            )
            all_branches.extend(batch_branches)
    else:  # Fallback for old, non-batched format
        print(f"Visualizing single tree '{name}'...")
        if "diameter" not in tree_data:
            raise KeyError(f"Required field 'diameter' missing from {json_file_path}")
        all_branches = list(
            zip(
                tree_data["start"],
                tree_data["end"],
                tree_data["btype"],
                tree_data["diameter"],
            )
        )
        
    all_diameters = np.array([branch[3] for branch in all_branches])
    min_diam = np.min(all_diameters)
    max_diam = np.max(all_diameters)

    MIN_LINEWIDTH = 1.0
    MAX_LINEWIDTH = 15.0

    # 4. Plotting logic from your class method
    all_points = [np.array([0.0, 0.0, 0.0])]
    print(f"Total branches to render: {len(all_branches)}")
    for start, end, btype, diameter in all_branches:
        start, end = np.array(start), np.array(end)
        
        # linewidth = diameter
        
        # Avoid division by zero if all diameters are the same
        if (max_diam - min_diam) > 0:
            norm_diam = (diameter - min_diam) / (max_diam - min_diam)
            linewidth = MIN_LINEWIDTH + norm_diam * (MAX_LINEWIDTH - MIN_LINEWIDTH)
        else:
            linewidth = MIN_LINEWIDTH # Assign a default if all are same size
        
        ax.plot(
            *zip(start, end),
            color=branch_colors.get(btype, branch_colors["default"]),
            linewidth=linewidth,
        )
        all_points.extend([start, end])

    # 5. Set plot limits to create a cubic bounding box
    # if len(all_points) > 1:
    #     pts = np.array(all_points)
    #     max_range = (pts.max(axis=0) - pts.min(axis=0)).max() / 2.0
    #     mid = (pts.max(axis=0) + pts.min(axis=0)) / 2.0
    #     if max_range == 0:
    #         max_range = 1.0  # Add a buffer for single-point trees
    #     ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    #     ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    #     ax.set_zlim(mid[2] - max_range, mid[2] + max_range)

    # 6. Finalize and show the plot
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title if title else f"3D L-System Tree: {name}")
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    # This function now handles showing the plot itself
    plt.show()


def load_tree_data(json_file_path):
    """Loads and validates tree data from a JSON file, supporting both single and batched formats."""
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    with open(json_file_path, "r") as f:
        data = json.load(f)

    # All formats must have a 'name'
    if "name" not in data:
        raise KeyError("Required field 'name' missing from JSON file")

    # If 'batches' key exists, it's the new format. This is a sufficient check.
    if "batches" in data:
        return data

    # Otherwise, assume it's the old format and validate its required fields.
    else:
        for field in ["start", "end", "btype"]:
            if field not in data:
                raise KeyError(f"Required field '{field}' missing from JSON file")
        if not (len(data["start"]) == len(data["end"]) == len(data["btype"])):
            raise ValueError("Inconsistent data lengths in JSON file.")
        return data


def list_available_trees(trees_dir="results/trees"):
    """Lists available tree JSON files in a directory."""
    if not os.path.isdir(trees_dir):
        print(f"Warning: Trees directory not found at '{trees_dir}'")
        return []
    json_files = sorted([f for f in os.listdir(trees_dir) if f.endswith(".json")])
    return [os.path.join(trees_dir, f) for f in json_files]


def run_visualization_cli(trees_dir="results/trees"):
    """Runs the command-line interface for visualizing trees."""
    print("\nL-System Tree Visualizer")
    print("========================")

    available_trees = list_available_trees(trees_dir)
    if not available_trees:
        print("No tree files found to visualize. Please generate trees first.")
        return

    print("Available trees:")
    for i, path in enumerate(available_trees, 1):
        print(f"  {i}. {os.path.basename(path)}")

    try:
        choice = (
            input(f"\nSelect a tree to visualize (1-{len(available_trees)}) or 'all': ")
            .strip()
            .lower()
        )
        if choice == "all":
            for tree_file in available_trees:
                visualize_tree_from_json(tree_file)
        else:
            tree_index = int(choice) - 1
            if 0 <= tree_index < len(available_trees):
                visualize_tree_from_json(available_trees[tree_index])
            else:
                print("Invalid selection.")
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number or 'all'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    # For the worlds currently
    run_visualization_cli(trees_dir="results/trees/worlds")
