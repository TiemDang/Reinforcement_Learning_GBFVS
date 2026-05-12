import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from stable_baselines3 import PPO
from rl_env import GBFVSEnv
from pathlib import Path

base_dir = Path(__file__).parent
#model_path = base_dir / 'model' / 'Gymnasium' / 'ppo_gbfvs_best'
model_path = base_dir / 'model' / 'Gymnasium' / 'checkpoints' / 'ppo_gbfvs_15872_steps'

env = GBFVSEnv()
model = PPO.load(model_path, env=env, device='cpu')

obs, _ = env.reset()
total_reward = 0

while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward
    if terminated:
        print(f"Episode reward: {total_reward:.3f}")
        total_reward = 0
        obs, _ = env.reset()

env.close()

