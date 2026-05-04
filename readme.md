
# **Reinforcement Learning GBFVS Bot**



## **1. Overview**
This project presents an AI agent trained using reinforcement learning to play Granblue Fantasy Versus: Rising (GBFVS). The agent learns to control the character Galleon in order to defeat opponents.  
GBFVS is a 2D fighting game. Additional details about the gameplay can be found on YouTube or Steam page.

## **2. Agent-Environment Loop**
- At each timestep, the agent captures the current game screen and applies OCR and image processing techniques to extract relevant features as observations.
- Based on these observations, the agent selects an action for a character it control according to its policy.
- The environment then transitions to a new state, and a reward is computed.  
- This loop continues until the episode terminates.

## **3. RL interaction components**
### **3.1 Environment**
The game screen during a match in Granblue Fantasy Versus: Rising.
### **3.2 Observation (17 features)**
OCR and computer vision are used to extract relevant information directly from captured game screens, forming an observation vector. Raw images are not used as direct input to the agent.

- **HP** : pixel color masking on fixed screen regions
- **Gauge** : value extraction on fixed screen regions
- **BP (Bravery Points)** : count cyan pixels across 3 diamond regions
- **Skill cooldown** : brightness thresholding on skill icon top half  
- **Character distance** : YOLO-based detection with Euclidean distance between character centers  
- **Opponent block state** : YOLO-based detection with class labels (normal / high block / low block)

Observation vector Details :

| Index | Feature | Description | Range |
|---|---|---|---|
| 0 | my_hp | Character HP | 0~1 |
| 1 | opp_hp | Opponent HP | 0~1 |
| 2 | my_gauge | Character gauge (required to use certain skills) | 0~1 |
| 3 | opp_gauge | Opponent Gauge | 0~1 |
| 4 | my_bp | Character BP (each player has 3 BP; 1 BP is consumed to perform a special attack) | 0~1 |
| 5 | opp_bp | Opponent BP | 0~1 |
| 6 | distance | Character distance | 0~1 |
| 7~10 | my_skill_1~4 | Whether each skill is on cooldown | 0 or 1 |
| 11~14 | opp_skill_1~4 | Whether each opponent skill is on cooldown | 0 or 1 |
| 15 | high_block | Whether the opponent is using a high block | 0 or 1 |
| 16 | low_block | Whether the opponent is using a low block | 0 or 1 |
### **3.3 Actions**
A discrete action space of 50 actions, including normal attacks, special attacks, movement, and defensive options.
### **3.4 Ternimation condition**
The episode terminates when a match is completed. A match consists of up to 3 rounds; the first player to win 2 rounds wins the match.
### **3.5 Rewards & Penalty**
| Event                                       | Reward      |
|---------------------------------------------|-------------|
| Dealing damage                              | + hp_change |
| Receiving damage                              | - hp_change |
| Winning a round                                   | +1          |
| Losing a round                                  | -1          |
| Winning a match                                   | +3          |
| Losing a match                                  | -3          |
| Using a skill without meeting requirements | -0.05       |

The purpose of the reward is to encourage the agent to win matches while taking as few hits as possible.  


## **4. Project Structure**
```
Reinforcement_Learning_GBFVS/
├── module/
│   ├── actions.py       # Action space (50 actions)
│   ├── observation.py   # Game state reading (HP, gauge, BP, skills, distance...)
│   ├── game_state.py    # Detect round begin and round end.
│   ├── reward.py        # Reward function
│   └── callback.py      # Training logger
├── model/
│   └── YOLO/best.pt     # YOLO model for character detection
├── templates/           # Template images for engage detection
├── visualize/           # Saving the reward for each episode for visualization
├── requirements.txt  
├── rl_env.py            # Gymnasium environment
└── train.py             # Training script

```
## **5. Requirements**
- OS: Linux
- Python 3.10 or higher
- CUDA-compatible GPU
- Game: Granblue Fantasy Versus: Rising (Steam) & DLC Character Galleon
## **6. Usage**
### **6.1 Clone The Repo**
```
git clone https://github.com/TiemDang/Reinforcement_Learning_GBFVS.git
cd Reinforcement_Learning_GBFVS
```
### **6.2 Install Requirements**
Running these command to install the required packages.
```
pip install -r requirements.txt
sudo apt install tesseract-ocr xdotool
```
### **6.3 Training**  

- Run the following commands:
```
python train.py  # Train a new model
python train.py --resume  # Resume training from a saved model
```
- Launch the game and navigate to Versus mode. Select Galleon (Player 1) and Narmaya (Player 2), choose the Celestial View stage, and wait for the match to begin. The agent controls Player 1, while Player 2 is controlled by the AI of the game.
## **7. Results**
### **7.1 Visualize Rewards**
### **7.2 Video**