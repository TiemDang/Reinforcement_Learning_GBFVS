class Reward:
    def __init__(self, round_bonus=1.0, set_bonus=3.0):
        self.round_bonus = round_bonus
        self.set_bonus = set_bonus

    def step_reward(self, prev_my_hp, curr_my_hp, prev_opp_hp, curr_opp_hp, miss_penalty):
        return float((prev_opp_hp - curr_opp_hp) - (prev_my_hp - curr_my_hp) + miss_penalty)

    def round_end_reward(self, winner):
        return self.round_bonus if winner == 'p1' else -self.round_bonus

    def set_end_reward(self, winner):
        return self.set_bonus if winner == 'p1' else -self.set_bonus