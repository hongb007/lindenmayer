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
        
    def remove_symbol(self, symbol: str):
        self.state = self.state.replace(symbol, '')
                
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

        # If no rules matched at all, the character is unchanged.
        if not valid_outputs:
            return 1, initial_state[current_index]

        # First, find the length of the longest symbol among all matches.
        longest_symbol_len = len(max(valid_outputs, key=lambda r: len(r["symbol"]))["symbol"])

        # Then, filter the list to only include rules for that longest symbol.
        prioritized_rules = [
            r for r in valid_outputs if len(r["symbol"]) == longest_symbol_len
        ]
        
        chance_limit = np.random.uniform(0, 1)
        added_prob = 0

        for i in range(0, len(prioritized_rules)):
            current_chance = prioritized_rules[i]["chance"]
            if current_chance != 0:
                added_prob += current_chance
                if chance_limit <= added_prob:
                    return len(prioritized_rules[i]["symbol"]), prioritized_rules[i]["new_symbol"]

        # If no probabilistic rule was chosen, return the original (longest) matched symbol.
        return longest_symbol_len, initial_state[current_index : current_index + longest_symbol_len]

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
