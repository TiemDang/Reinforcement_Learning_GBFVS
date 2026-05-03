import json
import matplotlib.pyplot as plt

with open('/home/venus/venus/rl_gbfvs/visualize/rewards.json') as f:
    data = json.load(f)

episodes = [d['episode'] for d in data]
rewards = [d['reward'] for d in data]

plt.plot(episodes, rewards)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Reward per Episode')
plt.savefig('reward_plot.png')
plt.show()