import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.axiom import Axiom
from utils.rule import Rule
from utils.constants import BASIC_EXAMPLE, TREE_EXAMPLE

class LSystem:
    def __init__(self, axiom: Axiom, rule: Rule) -> None:
        self.axiom = axiom
        self.rule = rule
        self.state = axiom.initial_state
        self.matched_rules = {} # Dictionary to help keep track of rule matches
        for r in rule.list:
            rule_key = f"{r['symbol']} -> {r['new_symbol']}"
            self.matched_rules[rule_key] = 0
        
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
                    rule_key = f"{prioritized_rules[i]['symbol']} -> {prioritized_rules[i]['new_symbol']}"
                    self.matched_rules[rule_key] += 1
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
        
    def get_rule_statistics(self) -> list[str | int]:
        # print("\nRule application statistics:")
        # print("---------------------------")
        
        list = []
        
        for rule_str, count in self.matched_rules.items():
            list.append([f"{rule_str}", count])
            
        return list
        
        # print("---------------------------")

    def estimate_branch_groups(self, string=None):
        """
        Estimate branch groups using a simple bracket count.
        
        Returns number of estimated groups
        """
        if string is None:
            string = self.state
            
        rotation_chars = set(["+", "-", "&", "^", "/", "\\", "|"])
        
        i = 0
        count = 0
        
        while i < len(string) - 1:
            if(string[i] == "[" and string[i+1] in rotation_chars):
                count += 1
            i += 1
        
        bracket_count = string.count("[")
        
        
        # Estimate groups as: 
        # 1 (initial trunk) + number of branch points
        estimated_groups = bracket_count + 1
        
        return count


if __name__ == "__main__":
    np.random.seed(0)
    
    name, axiom, rule = BASIC_EXAMPLE
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=2)
    print(lsystem.state)

    name, axiom, rule = TREE_EXAMPLE
    lsystem = LSystem(axiom=axiom, rule=rule)
    lsystem.iterate(iterations=1)
    print(lsystem.state)
