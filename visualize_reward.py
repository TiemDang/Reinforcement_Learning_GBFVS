import json
import matplotlib.pyplot as plt

with open('/home/venus/venus/rl_gbfvs/visualize/rewards.json') as f:
    data = json.load(f)

episodes = [d['episode'] for d in data]
rewards = [d['reward'] for d in data]
colors = ['green' if r > 0 else 'red' for r in rewards]

plt.figure(figsize=(12, 6))
plt.plot(episodes, rewards, color='gray', linewidth=0.8, alpha=0.5)  
plt.scatter(episodes, rewards, c=colors, s=30, zorder=5)              
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Reward per Episode')
plt.savefig('reward_plot.png')
plt.show()