from stable_baselines3.common.callbacks import BaseCallback
import json

class RewardLoggerCallback(BaseCallback):
    def __init__(self):
        super().__init__()
        self.episode_rewards = []
        self.current_reward = 0
        self.episode_count = 0

    def _on_step(self):
        self.current_reward += self.locals['rewards'][0]
        if self.locals['dones'][0]:
            self.episode_count += 1
            self.episode_rewards.append({
                'episode': self.episode_count,
                'reward': self.current_reward
            })
            self.current_reward = 0
            with open('/home/venus/venus/rl_gbfvs/visualize/rewards.json', 'w') as f:
                json.dump(self.episode_rewards, f)
        return True