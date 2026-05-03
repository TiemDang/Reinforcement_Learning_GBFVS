import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract


class GameState:
    def __init__(self, conf_threshold=0.3):
        self.conf_threshold = conf_threshold

        self.template_engage = cv2.imread('/home/venus/venus/rl_gbfvs/template/engage_2_template.png')
        self.template_engage = cv2.cvtColor(self.template_engage, cv2.COLOR_BGRA2BGR)

        self.template_p1_win_set   = cv2.imread('/home/venus/venus/rl_gbfvs/template/p1_wm_template.png')
        self.template_p1_win_set = cv2.cvtColor(self.template_p1_win_set, cv2.COLOR_BGRA2BGR)
        
        self.template_p2_win_set   = cv2.imread('/home/venus/venus/rl_gbfvs/template/p2_wm_template.png')
        self.template_p2_win_set = cv2.cvtColor(self.template_p2_win_set, cv2.COLOR_BGRA2BGR)

        self.p1_crop_loc = (93, 617, 438, 703)
        self.p2_crop_loc = (2118, 621, 2440, 699)

    def update(self, img):
        self.pil_img = img
        self.screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def _match(self, template):
        result = cv2.matchTemplate(self.screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val if max_val >= self.conf_threshold else None

    def detect_engage(self):
        return self._match(self.template_engage)
    
    def round_winner(self, img_crop):
        img_convert = img_crop.convert('L')
        img_convert = ImageEnhance.Contrast(img_convert).enhance(2.0)

        arr = np.array(img_convert)
        arr = (arr > 128).astype(np.uint8) * 255

        img_convert = Image.fromarray(arr)

        player = pytesseract.image_to_string(
            img_convert,
            config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )

        player = ''.join(ch for ch in player if ch.isalnum())
        return player
    
    def detect_round_end(self):
        # Crop 
        img_p1 = self.pil_img.crop((self.p1_crop_loc))
        img_p2 = self.pil_img.crop((self.p2_crop_loc))

        # OCR
        p1 = self.round_winner(img_p1)
        p2 = self.round_winner(img_p2)
        if p1=="PLAYER1":
            return 'p1'
        
        if p2=="PLAYER2":
            return 'p2'

        return None

    def detect_set_end(self):
        p1 = self._match(self.template_p1_win_set)
        p2 = self._match(self.template_p2_win_set)
        if p1 and p2:
            return 'p1' if p1 > p2 else 'p2'
        if p1:
            return 'p1'
        if p2:
            return 'p2'
        return None
