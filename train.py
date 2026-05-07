import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from stable_baselines3 import PPO
from rl_env import GBFVSEnv
from module.callback import RewardLoggerCallback
import argparse
from pathlib import Path
from stable_baselines3.common.callbacks import CheckpointCallback, CallbackList

parser = argparse.ArgumentParser()
parser.add_argument('--resume', action='store_true', help='Resume training from saved model')
args = parser.parse_args()

env = GBFVSEnv()
callback = RewardLoggerCallback()

base_dir = Path(__file__).parent
checkpoint_path = base_dir / 'model' / 'Gymnasium' / 'checkpoints'

checkpoint_callback = CheckpointCallback(
    save_freq=512,
    save_path=str(checkpoint_path),
    name_prefix='ppo_gbfvs',
    save_replay_buffer=False,
)

if args.resume:
    checkpoint_dir = base_dir / 'model' / 'Gymnasium' / 'checkpoints'
    checkpoints = sorted(
        checkpoint_dir.glob('ppo_gbfvs_*_steps.zip'),
        key=lambda x: int(x.stem.split('_')[2])
    )
    latest_checkpoint = checkpoints[-1]
    latest_steps = int(latest_checkpoint.stem.split('_')[2])
    print(f"Loading checkpoint: {latest_checkpoint} ({latest_steps} steps)")
    model = PPO.load(latest_checkpoint, env=env, device='cpu')

else:
    model = PPO(
        'MlpPolicy',
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=512,
        batch_size=128,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.15,
        ent_coef=0.02,
        vf_coef=0.5,
        max_grad_norm=0.5,
        device='cpu'
    )
    print("Starting new training...")

model.learn(
    total_timesteps=10000,
    callback=CallbackList([callback, checkpoint_callback]),
    reset_num_timesteps=False
)
model_path = (
    base_dir / 'model' / 'Gymnasium' /
    f'ppo_gbfvs_{model.num_timesteps}_steps'
)
model.save(model_path)
env.close()