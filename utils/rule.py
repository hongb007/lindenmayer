class Rule:
    def __init__(
        self,
        rules: list[list[str]]
    ) -> None:
        self.input, self.output = self.process_rules(rules=rules)
        
    def process_rules(self, rules: list[list[str]]):
        input = []
        output = []
        
        for i in range(len(rules)):
            input.append(rules[i][0])
            output.append(rules[i][1])
            
        return input, output
            