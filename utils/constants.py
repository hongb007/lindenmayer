from utils.axiom import Axiom
from utils.rule import Rule

"""
L-SYSTEM SYMBOL DEFINITIONS

Variables:
    A: Apex/bud, a point where new growth can occur.
    F: Forward, drawing a branch segment.
    S: A longer branch segment.
    L: A leaf structure.
    f: Forward, but without drawing. Used for positioning.

Constants (delta = __ degrees):
    [: Push the current state (position, orientation) onto the stack.
    ]: Pop the state from the stack.
    +: Turn Left (Yaw). By an angle delta.
    -: Turn Right (Yaw). By angle delta.
    &: Pitch Down. By angle delta.
    ^: Pitch Up. By angle delta.
    \\: Roll Left. By angle delta.
    /: Roll Right. By angle delta.
    |: Turn around (180 degree rotation).
"""

BASIC_EXAMPLE = [
    "Basic Example",
    Axiom("FR"),
    Rule([["F", "FRF", 1.0], ["F", "FFFR", 0.0]]),
]

TREE_EXAMPLE = [
    "Tree Example",
    Axiom("X"),
    Rule(
        [
            ["X", "F-[[X]+X]+F[+FX]-X", 0.5],
            ["X", "F-[[X]+X]+F[+FX]-X", 0.5],
            ["F", "FF", 1.0],
        ]
    ),
]

# DECIDUOUS_TREE = [
#     "deciduous_tree",
#     Axiom("T"),  # Start with trunk
#     Rule(
#         [
#             # Trunk grows and creates main branches
#             ["T", "F[+&B][-&B][/&B][\\&B]T", 0.6],  # 60% continue trunk with 4 branches
#             ["T", "F[+&B][-&B]T", 0.3],  # 30% continue with 2 branches
#             ["T", "FL", 0.1],  # 10% trunk terminates with leaf
#             # Branch growth - more likely to terminate with leaves
#             ["B", "F[+B][-B]", 0.4],  # 40% fork into two branches
#             ["B", "FF[+L][-L]", 0.3],  # 30% grow and add side leaves
#             ["B", "FL", 0.3],  # 30% terminate with leaf
#             # Segment rules
#             ["F", "FS", 0.7],  # 70% grow longer
#             ["F", "F", 0.3],  # 30% stay same length
#             ["S", "S", 1.0],  # Segments are stable
#             # Leaf structure - creates a cluster
#             ["L", "[&L1][^L1][+L1][-L1]", 1.0],
#             ["L1", "[{+f-f+f-f}]", 1.0],  # Individual leaf shape
#         ]
#     ),
# ]

# NATURAL_DECIDUOUS = [
#     "natural_deciduous",
#     Axiom("T"),
#     Rule(
#         [
#             # Trunk grows with more staggered and asymmetric branches
#             [
#                 "T",
#                 "F[+++&B]F[---/&B]T",
#                 0.3,
#             ],  # 30% trunk grows with two staggered, slightly rolled branches
#             [
#                 "T",
#                 "F[+++&B]F[\\&B]F[---&B]T",
#                 0.25,
#             ],  # 25% trunk grows with three staggered branches
#             [
#                 "T",
#                 "F[+/&B]F[-\\&B]F[//&B]F[\\&B]T",
#                 0.3,
#             ],  # 30% four-way spreading with rolls
#             ["T", "F[+++++&B]F[-----&B]T", 0.1],  # 10% very wide spreading
#             ["T", "FFL", 0.05],  # 5% trunk terminates early
#             # Branches have more varied growth, including a slight downward pull (gravity)
#             ["B", "F[+++K]F[--&K]", 0.3],  # 30% fork asymmetrically into smaller twigs
#             [
#                 "B",
#                 "FF[---&K][^K]",
#                 0.25,
#             ],  # 25% grow longer, one branch droops, one reaches up
#             ["B", "F[/K]F[\\K]F[+K]F[-K]", 0.3],  # 30% four-way spreading twigs
#             ["B", "F[+++++K]F[-----K]", 0.1],  # 10% very wide branches
#             ["B", "FL", 0.05],  # 5% terminate with a leaf
#             # Twigs for finer detail with full 3D spread
#             ["K", "F[++L][--L]", 0.4],
#             ["K", "F[/L][\\L]", 0.3],  # Roll-based spreading
#             ["K", "FL", 0.3],
#             # Segments grow longer to create thicker looking branches
#             ["F", "FS", 0.7],
#             ["F", "F", 0.3],
#             ["S", "S", 1.0],
#             # Irregular leaf cluster
#             ["L", "[&L1][^+L1][-L1]", 1.0],
#             ["L1", "[{+f-f+f-f}]", 1.0],
#         ]
#     ),
# ]

# Example from Lindenmayer paper
BUSH_3D = [
    "bush_3d",
    Axiom("A"),  # ω : A
    Rule(
        [
            # p₁: A → [&FL!A]/////'[&FL!A]////////'[&FL!A]
            # This creates three main branches with different roll orientations
            ["A", "[&FL!A]/////'[&FL!A]////////'[&FL!A]", 1.0],
            
            # p₂: F → S/////F  
            # Forward segments become longer segments with roll
            ["F", "S/////F", 1.0],
            
            # p₃: S → FL
            # Longer segments become forward + leaf
            ["S", "FL", 1.0],
            
            # p₄: L → [''^∧∧{-f+f+f-|-f+f+f}]
            # Leaves create detailed polygonal structures
            ["L", "[''^∧∧{-C+C+C-|-C+C+C}]", 1.0],
        ]
    ),
]

REALISTIC_TREE = [
    "realistic_tree", 
    Axiom("T"),  # Start with trunk like ZONO_TREE
    Rule(
        [
            # Initial trunk rule - creates visible trunk before branching
            ["T", "IIIIIIIA", 1.0],  # Draw trunk then start main growth
            
            # Main branching - optimized for 15k at 6 iterations  
            ["A", "F[^FL!A][&FL!A][+FL!A][-FL!A]", 0.9],  # 4-way branching, increased to 90%
            ["A", "FL", 0.1],  # 10% early termination
            
            # Trunk/branch segments - final tuning for 15k target
            ["F", "FS[&L][+L]", 0.4],  # 40% extend with two side leaves (increased)
            ["F", "FS[&L]", 0.3],      # 30% extend with one side leaf  
            ["F", "FS", 0.2],          # 20% just extend
            ["F", "F", 0.1],           # 10% stay short
            
            # Longer segments - increased detail for 15k target
            ["S", "FC", 0.75],      # 75% become regular segment + leaf detail (increased) 
            ["S", "F", 0.25],       # 25% just become regular segment (decreased)
            
            # Leaf clusters - realistic leaf shape from BUSH_3D
            ["L", "[''^∧∧{-C+C+C-|-C+C+C}]", 1.0],  # Detailed zigzag leaf pattern
            
            # Leaf detail segments
            ["C", "C", 1.0],  # Leaf details are stable
        ]
    ),
]

ZONO_TREE = [
    "zono_tree",
    Axiom("T"),  # ω : A
    Rule(
        [
            # Initial trunk rule - creates visible trunk before branching
            ["T", "III!IIII!IIII!IIII!!!A", 1.0],  # Draw trunk then start main growth
            
            # p₁: A → [&FL!A]/////'[&FL!A]////////'[&FL!A]
            # This creates three main branches with different roll orientations
            ["A", "[FL!A][&FL!A]/////'[&&FL!A]////////'[&FL!A]", 0.6],
            ["A", "/////'[&&&FL!A]/////'[&FL!A]////////'[&&FL!A]////////'[&&FL!A]", 0.15],
            ["A", "'[&&&FL!A]", 0.25],
            
            # p₂: F → S/////F  
            # Forward segments become longer segments with roll
            ["F", "S/////F", 0.7],
            ["F", "S", 0.3],

            
            # p₃: S → FL
            # Longer segments become forward + leaf
            ["S", "!FL", 0.7],
            ["S", "L", 0.3],
            
            # p₄: L → [''^∧∧{-f+f+f-|-f+f+f}]
            # Leaves create detailed polygonal structures
            # ["L", "[!!''^∧∧{-C+C+C-|-C+C+C}]", 1.0],
        ]
    ),
]

# angle is 18
PLANT_SYSTEM = [
    "plant_system",
    Axiom("A"),  # ω: plant (using A for plant/apex)
    Rule(
        [
            # p₁: plant → internode + [ plant + flower ] - - // [ - - leaf ] internode [ + + leaf ] - [ plant flower ] + + plant flower
            # Mapping: plant→A, internode→F, flower→W, leaf→L
            ["A", "F+[A+W]--//[--L]F[++L]-[AW]++AW", 1.0],
            
            # p₂: internode → F seg [// & & leaf ] [// ^ ^ leaf ] F seg
            # Mapping: internode→F, seg→S, leaf→L
            ["F", "FS[//&&L][//^^L]FS", 1.0],
            
            # p₃: seg → seg F seg
            # Mapping: seg→S
            ["S", "SFS", 1.0],
            
            # p₄: leaf → [ { +f-f+ | +f-f-f } ]
            # Using your leaf pattern for consistency
            ["L", "['^∧∧{-C+C+C-|-C+C+C}]", 1.0],
            
            # p₅: flower → [ & & & wedge ] /// wedge /// wedge /// wedge
            # Mapping: flower→W, wedge→V
            ["W", "[&&&V]///V///V///V", 1.0],
            
            # p₆: pedicel → FF (not used in main rules but included)
            # This would be for P→FF if we had pedicel symbol
            
            # p₇: wedge → [^ ^ F ] [ { & & & & -f+f | -f+f } ]
            # Mapping: wedge→V, using your leaf pattern for the geometric part
            ["V", "[^^F][&&&&{-C+C|-C+C}]", 1.0],
            
            # Make C stable for leaf details
            ["C", "C", 1.0],
        ]
    ),
]

SETH_TREE = [
    "seth_tree",
    Axiom("F"),  # Start with a forward segment
    Rule(
        [
            # Original: F → FFv[!vF^F^F]([!(F)F)F]^[!^FvFvF])[!)F(F(F]
            # Converted: v→&, (→\, )→/
            ["F", "FF&[!&F^F^F]\\[!\\F/F/F]^[!^F&F&F]/[!/F\\F\\F]", 1.0],
            
            # Simplification rule: FF → F
            ["FF", "F", 1.0],
        ]
    ),
]
