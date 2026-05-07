import json
from stable_baselines3.common.callbacks import BaseCallback

class RewardLoggerCallback(BaseCallback):
    def __init__(self):
        super().__init__()

        self.best_reward = float('-inf')
        self.current_reward = 0

        self.file_path = '/home/venus/venus/rl_gbfvs/visualize/rewards.json'

        try:
            with open(self.file_path, 'r') as f:
                self.episode_rewards = json.load(f)

            self.episode_count = len(self.episode_rewards)

            if self.episode_rewards:
                self.best_reward = max(
                    ep['reward'] for ep in self.episode_rewards
                )

            print(f"Loaded {self.episode_count} episodes from rewards.json")
            print(f"Best reward: {self.best_reward:.3f}")

        except FileNotFoundError:
            self.episode_rewards = []
            self.episode_count = 0

    def _on_step(self):
        self.current_reward += self.locals['rewards'][0]

        if self.locals['dones'][0]:

            reward = float(self.current_reward)

            self.episode_count += 1

            self.episode_rewards.append({
                'episode': self.episode_count,
                'reward': reward
            })

            if reward > self.best_reward:
                self.best_reward = reward

                self.model.save(
                    '/home/venus/venus/rl_gbfvs/model/Gymnasium/ppo_gbfvs_best'
                )

                print(f"New best model | Reward: {reward:.3f}")

            self.current_reward = 0

            with open(self.file_path, 'w') as f:
                json.dump(
                    self.episode_rewards,
                    f,
                    indent=4
                )

        return True