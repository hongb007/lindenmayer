from utils.axiom import Axiom
from utils.rule import Rule

BASIC_EXAMPLE = [Axiom("FR"), Rule([["F", "FRF", 1.0], ["F", "FFFR", 0.0]])]
TREE_EXAMPLE = [
    Axiom("X"),
    Rule(
        [
            ["X", "F-[[X]+X]+F[+FX]-X", 0.5],
            ["X", "F-[[X]+X]+F[+FX]-X", 0.5],
            ["F", "FF", 1.0],
        ]
    ),
]
