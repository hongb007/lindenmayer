#!/usr/bin/env python3
"""
Example usage of the zonotope class
"""
import torch
import matplotlib.pyplot as plt
import numpy as np
from zonopy.contset.zonotope.zono import zonotope

def main():
    print("=== Zonotope Class Usage Examples ===\n")
    
    # Set device and dtype
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    dtype = torch.float32
    print(f"Using device: {device}")
    
    # ===== 1. Creating Zonotopes =====
    print("1. Creating Zonotopes")
    print("-" * 30)
    
    # Method 1: From center and generators
    center = torch.tensor([1.0, 2.0], dtype=dtype, device=device)
    generators = torch.tensor([[0.5, 0.0], [0.0, 0.3], [0.2, 0.1]], dtype=dtype, device=device)
    Z = torch.vstack([center, generators])  # Shape: [4, 2] = [center + 3 generators, 2D]
    
    # Get center find vectors for cylinder base
    a = torch.tensor(start-end)
    a_hat = a / torch.linalg.norm(a)
    center = a
    if (a[0] == 0 and a[1] == 0):
        u = torch.cross(a, torch.tensor([1,0,0]))
    else:
        u = torch.cross(a, torch.tensor([0,0,1]))
    
    u_hat = u / torch.linalg.norm(u)
    
    v = torch.cross(a_hat, u_hat)
    v_hat = v / torch.linalg.norm(v)
    
    # Get generators for cylinder
    Z = center
    radius = 5
    m = 10
    for i in range(0, m):
        generator = radius * (torch.cos(2*np.pi/m) * u_hat + torch.cos(2*np.pi/m)*v_hat)
        Z = torch.vstack([Z, generator])
    
    
    zono1 = zonotope(Z, dtype=dtype, device=device)