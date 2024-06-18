class RuleStatus:
    def __init__(self, rule_id: str, rule_state: bool, observation_desc: str):
        self.rule_state = rule_state
        self.rule_id = rule_id
        self.observation_desc = observation_desc
