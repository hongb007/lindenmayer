class Rule:
    def __init__(
        self,
        input_rules: list[list[str | float]]
    ) -> None:
        self.list = self.process_rules(input_rules=input_rules)
        
    def process_rules(self, input_rules: list[list[str | float]]):
        processed_rules = []
        
        for i in range(len(input_rules)):
            processed_rules.append({
                "symbol": input_rules[i][0],
                "new_symbol": input_rules[i][1],
                "chance": input_rules[i][2],
            })
            
        return processed_rules
            