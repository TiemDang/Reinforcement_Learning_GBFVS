import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from stable_baselines3 import PPO
from rl_env import GBFVSEnv
from module.callback import RewardLoggerCallback
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--resume', action='store_true', help='Resume training from saved model')
args = parser.parse_args()

env = GBFVSEnv()
callback = RewardLoggerCallback()

base_dir = Path(__file__).parent
model_path = base_dir / 'model' / 'Gymnasium' / 'ppo_gbfvs'

if args.resume:
    model = PPO.load(model_path, env=env)
    print("Resuming training from saved model...")
else:
    model = PPO(
        'MlpPolicy',
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=128,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.15,
        ent_coef=0.02,
        vf_coef=0.5,
        max_grad_norm=0.5,
        device='cuda'
    )
    print("Starting new training...")

model.learn(total_timesteps=150_000, callback=callback)
model.save(model_path)
env.close()