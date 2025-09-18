from utils.axiom import Axiom
from utils.rule import Rule

BASIC_EXAMPLE = [Axiom("FR"), Rule([["F", "FRF"]])]
TREE_EXAMPLE = [Axiom("X"), Rule([["X", "F-[[X]+X]+F[+FX]-X"], 
                                  ["F", "FF"]])]