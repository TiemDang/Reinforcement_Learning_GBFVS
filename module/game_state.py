import cv2
import numpy as np
import mss
from PIL import Image
import time

class GameState:
    def __init__(self, conf_threshold=0.7):
        self.conf_threshold = conf_threshold

        self.template_engage = cv2.imread('/home/venus/venus/rl_gbfvs/template/engage_template.png')
        self.template_engage = cv2.cvtColor(self.template_engage, cv2.COLOR_BGRA2BGR)

        self.region_engage = (206, 295, 2393, 1223)

        self.sct = mss.mss()

    def _get_screenshot(self):
        raw = self.sct.grab(self.sct.monitors[1])
        return Image.frombytes('RGB', raw.size, raw.rgb)

    def update(self, img):
        self.pil_img = img
        self.screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def _match(self, screen_crop, template):
        result = cv2.matchTemplate(screen_crop, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val if max_val >= self.conf_threshold else None
    
    def get_region(self, region):
        x1, y1, x2, y2 = region
        return self.screen[y1:y2, x1:x2]

    def check_engage(self):
        crop_engage = self.get_region(self.region_engage)
        return self._match(crop_engage, self.template_engage)
    
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
    
    def check_attack_hit(self, opp_hp_before, opp_hp_after):
        return (opp_hp_before - opp_hp_after) > 0
    
    def _wait_for_engage(self):
        while True:
            img = self._get_screenshot()
            self.update(img)
            if self.check_engage():
                print("Engage detected. Battle start in 1 !")
                time.sleep(0.7) # delay before can control character
                break
            time.sleep(10/60) # 10 frame check for engage sign
    
    def check_round_end(self, my_hp, opp_hp):
        if my_hp <= 0.01:
            return 'p2'
        if opp_hp <= 0.01:
            return 'p1'
        return None
    
    def close(self):
        self.sct.close()

