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

DECIDUOUS_TREE = [
    "deciduous_tree",
    Axiom("T"),  # Start with trunk
    Rule(
        [
            # Trunk grows and creates main branches
            ["T", "F[+&B][-&B][/&B][\\&B]T", 0.6],  # 60% continue trunk with 4 branches
            ["T", "F[+&B][-&B]T", 0.3],  # 30% continue with 2 branches
            ["T", "FL", 0.1],  # 10% trunk terminates with leaf
            # Branch growth - more likely to terminate with leaves
            ["B", "F[+B][-B]", 0.4],  # 40% fork into two branches
            ["B", "FF[+L][-L]", 0.3],  # 30% grow and add side leaves
            ["B", "FL", 0.3],  # 30% terminate with leaf
            # Segment rules
            ["F", "FS", 0.7],  # 70% grow longer
            ["F", "F", 0.3],  # 30% stay same length
            ["S", "S", 1.0],  # Segments are stable
            # Leaf structure - creates a cluster
            ["L", "[&L1][^L1][+L1][-L1]", 1.0],
            ["L1", "[{+f-f+f-f}]", 1.0],  # Individual leaf shape
        ]
    ),
]

NATURAL_DECIDUOUS = [
    "natural_deciduous",
    Axiom("T"),
    Rule(
        [
            # Trunk grows with more staggered and asymmetric branches
            [
                "T",
                "F[+++&B]F[---/&B]T",
                0.3,
            ],  # 30% trunk grows with two staggered, slightly rolled branches
            [
                "T",
                "F[+++&B]F[\\&B]F[---&B]T",
                0.25,
            ],  # 25% trunk grows with three staggered branches
            [
                "T",
                "F[+/&B]F[-\\&B]F[//&B]F[\\&B]T",
                0.3,
            ],  # 30% four-way spreading with rolls
            ["T", "F[+++++&B]F[-----&B]T", 0.1],  # 10% very wide spreading
            ["T", "FFL", 0.05],  # 5% trunk terminates early
            # Branches have more varied growth, including a slight downward pull (gravity)
            ["B", "F[+++K]F[--&K]", 0.3],  # 30% fork asymmetrically into smaller twigs
            [
                "B",
                "FF[---&K][^K]",
                0.25,
            ],  # 25% grow longer, one branch droops, one reaches up
            ["B", "F[/K]F[\\K]F[+K]F[-K]", 0.3],  # 30% four-way spreading twigs
            ["B", "F[+++++K]F[-----K]", 0.1],  # 10% very wide branches
            ["B", "FL", 0.05],  # 5% terminate with a leaf
            # Twigs for finer detail with full 3D spread
            ["K", "F[++L][--L]", 0.4],
            ["K", "F[/L][\\L]", 0.3],  # Roll-based spreading
            ["K", "FL", 0.3],
            # Segments grow longer to create thicker looking branches
            ["F", "FS", 0.7],
            ["F", "F", 0.3],
            ["S", "S", 1.0],
            # Irregular leaf cluster
            ["L", "[&L1][^+L1][-L1]", 1.0],
            ["L1", "[{+f-f+f-f}]", 1.0],
        ]
    ),
]

BETTER_3D_TREE = [
    "better_3d_tree",
    Axiom("T"),
    Rule(
        [
            # Trunk with full 360° branching
            ["T", "F[+^B]F[-&B]F[/^B]F[\\&B]T", 0.4],  # 4-way symmetric branching
            ["T", "F[++^B]F[--&B]F[//^B]F[\\\\&B]T", 0.3],  # Wider 4-way branching
            ["T", "F[+++&B]F[---^B]T", 0.2],  # Simple wide branching
            ["T", "FL", 0.1],
            # Branches spread in all directions
            ["B", "F[+K]F[-K]F[/K]F[\\K]", 0.4],  # 4-way spreading
            ["B", "F[++K]F[--K]", 0.3],  # Wide spreading
            ["B", "F[&K]F[^K]", 0.2],  # Up/down variation
            ["B", "FL", 0.1],
            # Fine branches
            ["K", "F[+L]F[-L]", 0.6],
            ["K", "F[/L]F[\\L]", 0.3],  # Roll-based leaves
            ["K", "FL", 0.1],
            # Growth
            ["F", "FS", 0.7],
            ["F", "F", 0.3],
            # ["S", "S", 1.0],
            # Leaves
            ["L", "[&L1][^L1][+L1][-L1]", 1.0],
            ["L1", "[{f}]", 1.0],
        ]
    ),
]
