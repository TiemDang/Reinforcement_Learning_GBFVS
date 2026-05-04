import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract


class GameState:
    def __init__(self, conf_threshold=0.7):
        self.conf_threshold = conf_threshold

        self.template_engage = cv2.imread('/home/venus/venus/rl_gbfvs/template/engage_template.png')
        self.template_engage = cv2.cvtColor(self.template_engage, cv2.COLOR_BGRA2BGR)

        self.region_engage = (206, 295, 2393, 1223)

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

    def detect_engage(self):
        crop_engage = self.get_region(self.region_engage)
        return self._match(crop_engage, self.template_engage)
    
    def detect_round_end(self, my_hp, opp_hp):
        if my_hp <= 0.01:
            return 'p2'
        if opp_hp <= 0.01:
            return 'p1'
        return None

