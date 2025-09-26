#!/usr/bin/env python3
"""
L-System Tree Visualizer from JSON Files

This script loads pre-generated tree data from JSON files and creates 3D visualizations.
The JSON files should contain branch data with start points, end points, and branch types.
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def load_tree_data(json_file_path):
    """
    Load tree data from a JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file containing tree data
        
    Returns:
        dict: Tree data with 'name', 'start', 'end', and 'btype' fields
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        KeyError: If required fields are missing from the JSON
    """
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Validate required fields
    required_fields = ['name', 'start', 'end', 'btype']
    for field in required_fields:
        if field not in data:
            raise KeyError(f"Required field '{field}' missing from JSON file")
    
    return data

def visualize_tree_from_json(json_file_path, title=None, show_nodes=True, 
                           branch_colors=None, node_size=50, line_width=2, 
                           figsize=(12, 9), elev=25, azim=-60, save_path=None):
    """
    Create a 3D visualization of a tree from JSON data.
    
    Args:
        json_file_path (str): Path to the JSON file
        title (str): Title for the plot (defaults to tree name from JSON)
        show_nodes (bool): Whether to show nodes as points
        branch_colors (dict): Dictionary mapping branch types to colors
        node_size (int): Size of the node markers
        line_width (int): Width of the branch lines
        figsize (tuple): Figure size (width, height)
        elev (int): Elevation angle for 3D view
        azim (int): Azimuth angle for 3D view
        save_path (str): Optional path to save the visualization
        
    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Load tree data
    tree_data = load_tree_data(json_file_path)
    
    # Extract data
    name = tree_data['name']
    start_points = np.array(tree_data['start'])
    end_points = np.array(tree_data['end'])
    branch_types = tree_data['btype']
    
    # Validate data consistency
    num_branches = len(start_points)
    if len(end_points) != num_branches or len(branch_types) != num_branches:
        raise ValueError(f"Inconsistent data lengths: start={len(start_points)}, "
                        f"end={len(end_points)}, types={len(branch_types)}")
    
    print(f"Visualizing tree '{name}' with {num_branches} branches")
    
    # Default colors for different branch types
    if branch_colors is None:
        branch_colors = {
            'F': 'saddlebrown',    # Main trunk/branches
            'S': 'chocolate',      # Secondary branches  
            'L': 'forestgreen',    # Leaves
            'A': 'orange',         # Additional elements
            'B': 'sienna',         # Branch segments
            'K': 'darkgreen',      # Small twigs
            'T': 'brown',          # Trunk
            'root': 'black'        # Root (fallback)
        }
    
    # Create the 3D plot
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    # Track all points for setting axis limits
    all_points = np.vstack([start_points, end_points])
    
    # Group branches by type for efficient plotting
    branch_type_groups = {}
    for i, branch_type in enumerate(branch_types):
        if branch_type not in branch_type_groups:
            branch_type_groups[branch_type] = []
        branch_type_groups[branch_type].append(i)
    
    # Plot branches grouped by type
    for branch_type, indices in branch_type_groups.items():
        color = branch_colors.get(branch_type, 'gray')
        
        # Plot all branches of this type
        for i in indices:
            start = start_points[i]
            end = end_points[i]
            
            # Draw the branch
            ax.plot([start[0], end[0]], 
                   [start[1], end[1]], 
                   [start[2], end[2]], 
                   color=color, linewidth=line_width, alpha=0.8)
    
    # Draw nodes if requested
    if show_nodes:
        unique_types = set(branch_types)
        for branch_type in unique_types:
            color = branch_colors.get(branch_type, 'red')
            type_indices = [i for i, bt in enumerate(branch_types) if bt == branch_type]
            
            # Plot start and end points for this type
            type_starts = start_points[type_indices]
            type_ends = end_points[type_indices]
            
            ax.scatter(type_starts[:, 0], type_starts[:, 1], type_starts[:, 2], 
                      c=color, s=node_size, alpha=0.6)
            ax.scatter(type_ends[:, 0], type_ends[:, 1], type_ends[:, 2], 
                      c=color, s=node_size, alpha=0.6)
    
    # Set equal aspect ratio and nice limits
    if len(all_points) > 0:
        # Calculate bounds with some padding
        x_min, x_max = all_points[:, 0].min(), all_points[:, 0].max()
        y_min, y_max = all_points[:, 1].min(), all_points[:, 1].max()
        z_min, z_max = all_points[:, 2].min(), all_points[:, 2].max()
        
        # Add padding (10% of range)
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1
        z_range = z_max - z_min if z_max != z_min else 1
        
        padding = 0.1
        ax.set_xlim(x_min - padding * x_range, x_max + padding * x_range)
        ax.set_ylim(y_min - padding * y_range, y_max + padding * y_range)
        ax.set_zlim(z_min - padding * z_range, z_max + padding * z_range)
        
        # Set equal aspect ratio for better tree visualization
        max_range = max(x_range, y_range, z_range)
        if max_range > 0:
            ax.set_box_aspect([x_range/max_range, y_range/max_range, z_range/max_range])
    
    # Labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    if title is None:
        title = f"3D L-System Tree: {name}"
    ax.set_title(title)
    
    # Set view angle
    ax.view_init(elev=elev, azim=azim)
    
    # Create legend for branch types
    unique_types = set(branch_types)
    if unique_types:
        legend_elements = []
        for branch_type in sorted(unique_types):
            color = branch_colors.get(branch_type, 'gray')
            legend_elements.append(Line2D([0], [0], color=color, 
                                        linewidth=line_width, label=f"Type '{branch_type}'"))
        
        if legend_elements:
            ax.legend(handles=legend_elements, loc='upper right')
    
    # Print statistics
    print("Tree Statistics:")
    print(f"  Total branches: {num_branches}")
    print(f"  Branch types: {sorted(unique_types)}")
    print("  Spatial extent:")
    print(f"    X: {x_min:.2f} to {x_max:.2f} (range: {x_range:.2f})")
    print(f"    Y: {y_min:.2f} to {y_max:.2f} (range: {y_range:.2f})")
    print(f"    Z: {z_min:.2f} to {z_max:.2f} (range: {z_range:.2f})")
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {save_path}")
    
    return fig, ax

def list_available_trees(trees_dir="results/trees"):
    """
    List all available tree JSON files.
    
    Args:
        trees_dir (str): Directory containing tree JSON files
        
    Returns:
        list: List of available JSON file paths
    """
    if not os.path.exists(trees_dir):
        print(f"Trees directory not found: {trees_dir}")
        return []
    
    json_files = [f for f in os.listdir(trees_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"No JSON files found in {trees_dir}")
        return []
    
    print(f"Available tree files in {trees_dir}:")
    for i, filename in enumerate(json_files, 1):
        print(f"  {i}. {filename}")
    
    return [os.path.join(trees_dir, f) for f in json_files]

def visualize_multiple_trees(trees_dir="results/trees", save_images=False):
    """
    Visualize all trees in the specified directory.
    
    Args:
        trees_dir (str): Directory containing tree JSON files
        save_images (bool): Whether to save visualization images
    """
    tree_files = list_available_trees(trees_dir)
    
    if not tree_files:
        return
    
    for tree_file in tree_files:
        try:
            print(f"\n{'='*50}")
            print(f"Visualizing: {os.path.basename(tree_file)}")
            print(f"{'='*50}")
            
            save_path = None
            if save_images:
                base_name = os.path.splitext(os.path.basename(tree_file))[0]
                save_path = f"{base_name}_visualization.png"
            
            fig, ax = visualize_tree_from_json(
                tree_file,
                show_nodes=True,
                node_size=30,
                line_width=2,
                elev=30,      # Good angle for trees
                azim=-45,     # Nice rotation
                save_path=save_path
            )
            
            plt.show()
            
        except Exception as e:
            print(f"Error visualizing {tree_file}: {e}")
            continue

# Main execution
if __name__ == "__main__":
    # You can customize this section to visualize specific trees
    
    # Option 1: Visualize a specific tree
    # Uncomment and modify the path as needed
    # tree_file = "results/trees/lsystem_oak_tree.json"
    # fig, ax = visualize_tree_from_json(tree_file)
    # plt.show()
    
    # Option 2: Visualize all available trees
    print("L-System Tree Visualizer")
    print("========================")
    
    # List available trees
    available_trees = list_available_trees()
    
    if available_trees:
        print("\nSelect visualization mode:")
        print("1. Visualize all trees")
        print("2. Visualize a specific tree")
        print("3. Quick demo with oak tree")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                visualize_multiple_trees(save_images=False)
            elif choice == "2":
                print("\nAvailable trees:")
                for i, tree_file in enumerate(available_trees, 1):
                    tree_name = os.path.basename(tree_file)
                    print(f"  {i}. {tree_name}")
                
                tree_choice = input(f"\nSelect tree (1-{len(available_trees)}): ").strip()
                try:
                    tree_index = int(tree_choice) - 1
                    if 0 <= tree_index < len(available_trees):
                        selected_tree = available_trees[tree_index]
                        print(f"\nVisualizing: {os.path.basename(selected_tree)}")
                        fig, ax = visualize_tree_from_json(selected_tree)
                        plt.show()
                    else:
                        print("Invalid selection!")
                except ValueError:
                    print("Invalid input! Please enter a number.")
            elif choice == "3":
                # Quick demo with oak tree if available
                oak_file = None
                for tree_file in available_trees:
                    if "oak" in tree_file.lower():
                        oak_file = tree_file
                        break
                
                if oak_file:
                    print(f"\nQuick demo with: {os.path.basename(oak_file)}")
                    fig, ax = visualize_tree_from_json(
                        oak_file,
                        title="Demo: Oak Tree from JSON",
                        elev=25,
                        azim=-60
                    )
                    plt.show()
                else:
                    print("Oak tree file not found. Using first available tree.")
                    if available_trees:
                        fig, ax = visualize_tree_from_json(available_trees[0])
                        plt.show()
            else:
                print("Invalid choice!")
                
        except KeyboardInterrupt:
            print("\nVisualization cancelled.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No tree files found to visualize!")