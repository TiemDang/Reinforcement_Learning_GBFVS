import time
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mss
from PIL import Image
import datetime
from ultralytics import YOLO

from module import GalleonActions, Observation, GameState, Reward

REGIONS = {
    'my_hp':       (275, 104, 1148, 115),
    'opp_hp':      (1412, 104, 2285, 115),
    'my_gauge':    (671, 132, 780, 185),
    'opp_gauge':   (1785, 132, 1880, 185),
    'my_bp':       (980, 35, 1130, 85),
    'opp_bp':      (1430, 35, 1580, 85),
    'my_skill_1':  (295, 138, 380, 220),
    'my_skill_2':  (385, 138, 465, 220),
    'my_skill_3':  (470, 138, 547, 220),
    'my_skill_4':  (555, 138, 636, 220),
    'opp_skill_1': (2180, 138, 2265, 220),
    'opp_skill_2': (2095, 138, 2175, 220),
    'opp_skill_3': (2010, 138, 2090, 220),
    'opp_skill_4': (1924, 138, 2005, 220),
}

class GBFVSEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.actions = GalleonActions()
        self.action_space = spaces.Discrete(len(self.actions.ACTION_MAP))
        self.action_duration = self.actions.ACTION_DURATION
        self.observation_space = spaces.Box(
            low=0.0, high=1.0,
            shape=(17,),
            dtype=np.float32
        )

        self.sct = mss.mss()
        self.game_state = GameState(conf_threshold=0.7)
        self.reward_fn = Reward()

        self.yolo_model = YOLO('/home/venus/venus/rl_gbfvs/model/YOLO/best.pt')
        self.yolo_model.to('cuda')

        self.prev_my_hp = 1.0
        self.prev_opp_hp = 1.0

        self.episode_count = 0

        self.p1_round_wins = 0
        self.p2_round_wins = 0

    def _get_screenshot(self):
        raw = self.sct.grab(self.sct.monitors[1])
        return Image.frombytes('RGB', raw.size, raw.rgb)

    def _get_obs(self, obs):
        distance, high_block, low_block = obs.enemy_state()
        if distance is None:
            distance = 0.0

        return np.array([
            obs.read_hp(REGIONS['my_hp']),
            obs.read_hp(REGIONS['opp_hp']),
            obs.read_gauge(REGIONS['my_gauge']) / 100,
            obs.read_gauge(REGIONS['opp_gauge']) / 100,
            obs.read_bp(REGIONS['my_bp']) / 3,
            obs.read_bp(REGIONS['opp_bp']) / 3,
            distance / 2560,
            float(obs.check_skill_cooldown(REGIONS['my_skill_1'])),
            float(obs.check_skill_cooldown(REGIONS['my_skill_2'])),
            float(obs.check_skill_cooldown(REGIONS['my_skill_3'])),
            float(obs.check_skill_cooldown(REGIONS['my_skill_4'])),
            float(obs.check_skill_cooldown(REGIONS['opp_skill_1'])),
            float(obs.check_skill_cooldown(REGIONS['opp_skill_2'])),
            float(obs.check_skill_cooldown(REGIONS['opp_skill_3'])),
            float(obs.check_skill_cooldown(REGIONS['opp_skill_4'])),
            float(high_block),
            float(low_block),
        ], dtype=np.float32)
    

    def _wait_for_engage(self):
        while True:
            img = self._get_screenshot()
            self.game_state.update(img)
            if self.game_state.detect_engage():
                print("Engage detected. Battle start in 1 !")
                time.sleep(0.7) # delay before can control character
                break
            time.sleep(10/60) # 10 frame check for engage sign

    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._wait_for_engage()

        img = self._get_screenshot()
        obs = Observation(img, self.yolo_model)
        obs_vec = self._get_obs(obs)

        self.prev_my_hp = obs_vec[0]
        self.prev_opp_hp = obs_vec[1]
        self.prev_obs_vec = obs_vec
        self.p1_round_wins = 0
        self.p1_round_wins = 0

        return obs_vec, {}
    

    def wait_action(self, duration):
        interval = 30/60  #  1/2 second
        elapsed = 0
        while elapsed < duration:
            time.sleep(interval)
            elapsed += interval
            img = self._get_screenshot()
            obs = Observation(img, self.yolo_model)
            obs_vec = self._get_obs(obs)
            round_winner = self.game_state.detect_round_end(obs_vec[0], obs_vec[1])


            if round_winner:
                return 'round', round_winner
            
        return None, None
    

    def check_action_valid(self, action, prev_obs_vec):
        my_hp = prev_obs_vec[0]
        my_gauge = prev_obs_vec[2]
        my_bp = prev_obs_vec[4]

        ultimate_skills = [27, 28, 29, 30, 31]
        universal_actions = [32, 33]
        skybound_art = [34, 35]
        super_skybound_art = [36]

        if action in ultimate_skills and my_gauge < 0.5:
            return False
        if action in universal_actions and my_bp < 1/3:
            return False
        if action in skybound_art and my_gauge < 1 :
            return False
        if action in super_skybound_art and ( my_gauge < 1 or my_hp > 0.3 ) :
            return False
        
        return True

    def step(self, action):
        if not self.check_action_valid(action, self.prev_obs_vec):
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Invallid Action: {self.actions.ACTION_MAP[action].__name__} | Reward: -0.05")
            return self.prev_obs_vec, -0.05, False, False, {}
        

        #self.actions._reset_keys()
        self.actions.ACTION_MAP[action]()
        event_type, winner = self.wait_action(self.action_duration[action])

        img = self._get_screenshot()
        obs = Observation(img, self.yolo_model)
        self.game_state.update(img)
        obs_vec = self._get_obs(obs)

        curr_my_hp = obs_vec[0]
        curr_opp_hp = obs_vec[1]

        reward = self.reward_fn.step_reward(
            self.prev_my_hp, curr_my_hp,
            self.prev_opp_hp, curr_opp_hp
        )
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
                f"my_hp: {curr_my_hp:.3f} | opp_hp: {curr_opp_hp:.3f} | "
                f"Action: {self.actions.ACTION_MAP[action].__name__} | Reward: {reward:.3f}")

        terminated = False

        if event_type == 'round':
            round_winner = winner
        else :
            round_winner = self.game_state.detect_round_end(curr_my_hp, curr_opp_hp)

        if round_winner :
            if round_winner == 'p1':
                self.p1_round_wins += 1
            else:
                self.p2_round_wins += 1
            
            reward += self.reward_fn.round_end_reward(round_winner)
            reward = float(reward)

            if self.p1_round_wins == 2:
                self.episode_count += 1
                self.p1_round_wins = 0
                self.p2_round_wins = 0
                reward += float(self.reward_fn.set_end_reward('p1'))
                print(f"Episode {self.episode_count} completed | p1 win | Reward: {reward:.3f}\n{'_'*20}")
                terminated = True
                self.actions.rematch()

            elif self.p2_round_wins == 2 :
                self.episode_count += 1
                self.p1_round_wins = 0
                self.p2_round_wins = 0
                reward += float(self.reward_fn.set_end_reward('p2'))
                print(f"Episode {self.episode_count} completed | p2 win | Reward: {reward:.3f}\n{'_'*20}")
                terminated = True
                self.actions.rematch()

            else :
                print(f"Round end | {round_winner} win | Reward: {reward:.3f}")
                self._wait_for_engage()
                img = self._get_screenshot()
                obs_new = Observation(img, self.yolo_model)
                obs_vec = self._get_obs(obs_new)
                self.prev_my_hp = obs_vec[0]
                self.prev_opp_hp = obs_vec[1]
                self.prev_obs_vec = obs_vec
                return obs_vec, reward, terminated, False, {}



        self.prev_my_hp = curr_my_hp
        self.prev_opp_hp = curr_opp_hp
        self.prev_obs_vec = obs_vec
        return obs_vec, reward, terminated, False, {}

    def close(self):
        self.sct.close()