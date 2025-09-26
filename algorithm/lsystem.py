import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.axiom import Axiom
from utils.rule import Rule
from utils.constants import BASIC_EXAMPLE, TREE_EXAMPLE

np.random.seed(0)


class LSystem:
    def __init__(self, axiom: Axiom, rule: Rule) -> None:
        self.axiom = axiom
        self.rule = rule
        self.state = axiom.initial_state

    def match_rule(self, rule: Rule, initial_state: str, current_index: int):
        valid_outputs = []
        chance_limit = np.random.uniform(0, 1)
        added_prob = 0

        for i in range(0, len(rule.list)):
            if current_index <= len(initial_state) - len(rule.list[i]["symbol"]) and (
                initial_state[
                    current_index : (current_index + len(rule.list[i]["symbol"]))
                ]
                == rule.list[i]["symbol"]
            ):
                valid_outputs.append(rule.list[i])

        valid_outputs_sorted = sorted(
            valid_outputs, key=lambda chance: chance["chance"]
        )

        for i in range(0, len(valid_outputs_sorted)):
            # Get the numeric chance value first
            current_chance = valid_outputs_sorted[i]["chance"]

            # Only process if the chance is not zero
            if current_chance != 0:
                added_prob += current_chance
                if chance_limit <= added_prob:
                    return len(valid_outputs_sorted[i]["symbol"]), valid_outputs_sorted[i]["new_symbol"]

        return 1, initial_state[current_index]

    def iterate(self, iterations: int) -> None:
        def step(input_state: str, rule: Rule) -> str:
            new_state = ""
            i = 0
            
            while i < len(input_state):
                old_symbol_length, new_symbol = self.match_rule(rule, input_state, i)
                new_state += new_symbol
                i += old_symbol_length

            return new_state

        new_state = self.state

        for i in range(0, iterations):
            new_state = step(new_state, self.rule)

        self.state = new_state


if __name__ == "__main__":
    name, axiom, rule = BASIC_EXAMPLE
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=2)
    print(lsystem.state)

    name, axiom, rule = TREE_EXAMPLE
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=1)
    print(lsystem.state)
