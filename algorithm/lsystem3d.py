import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.axiom import Axiom
from utils.rule import Rule
from utils.constants import BASIC_EXAMPLE, TREE_EXAMPLE


class LSystem:
    def __init__(self, axiom: Axiom, rule: Rule) -> None:
        self.axiom = axiom
        self.rule = rule
        self.state = axiom.initial_state
        
    def match_rule(self, rule: Rule, initial_state: str, current_index: int):
        for i in range(0, len(rule.input)):
            if current_index <= len(initial_state) - len(rule.input[i]) and (
                    initial_state[current_index : (current_index + len(rule.input[i]))] == rule.input[i]):
                return i, True
            
        return -1, False

    def iterate(self, iterations: int) -> None:          
        def step(initial_state: str, rule: Rule) -> str:
            new_state = ""

            for i in range(0, len(initial_state)):
                index, if_matched = self.match_rule(rule, initial_state, i)
                if (if_matched):
                    new_state += rule.output[index]
                else:
                    new_state += initial_state[i]

            return new_state

        new_state = self.state

        for i in range(0, iterations):
            new_state = step(new_state, rule)

        self.state = new_state


if __name__ == "__main__":
    axiom, rule = BASIC_EXAMPLE
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=2)
    print(lsystem.state)

    axiom, rule = TREE_EXAMPLE
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=1)
    print(lsystem.state)
