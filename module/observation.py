import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
from ultralytics import YOLO


class Observation :
    def __init__(self, img, yolo_model, skill_threshold=100):
        self.img = img
        self.yolo_model = yolo_model
        self.skill_threshold = skill_threshold
        

    def read_hp(self, region_hp):
        img_hp_crop = self.img.crop(region_hp)
        img_arr = np.array(img_hp_crop)

        # Mask for hp color
        mask_green = (
            (img_arr[:, :, 0] > 170) & (img_arr[:, :, 0] < 202) &
            (img_arr[:, :, 1] > 225) & (img_arr[:, :, 1] < 240) &
            (img_arr[:, :, 2] > 158) & (img_arr[:, :, 2] < 195)
        )

        mask_cyan = (
            (img_arr[:, :, 0] > 172) & (img_arr[:, :, 0] < 185) &
            (img_arr[:, :, 1] > 224) & (img_arr[:, :, 1] < 232) &
            (img_arr[:, :, 2] > 238) & (img_arr[:, :, 2] < 248)
        )

        green_cols = np.any(mask_green, axis=0)
        cyan_cols = np.any(mask_cyan, axis=0)

        # Calc hp left
        hp_percent_green = np.sum(green_cols) / img_arr.shape[1]
        hp_percent_cyan = np.sum(cyan_cols) / img_arr.shape[1]
        
        return max(hp_percent_green, hp_percent_cyan)
            

    def read_bp(self, region_bp):
        img_bp_crop = self.img.crop(region_bp)
        img_arr = np.array(img_bp_crop)
        width = img_arr.shape[1]
        bp_count = 0

        for i in range(3):
            start = (width) // 3 * i
            end = (width // 3) * (i + 1)
            section = img_arr[:, start:end, :]
            mask_bp = (
                (section[:, :, 0] < 100) &
                (section[:, :, 1] > 200) &
                (section[:, :, 2] > 200)
            )
            if np.any(mask_bp):
                bp_count += 1

        return bp_count
    

    def read_gauge(self, region_gauge):
        img_gauge_crop = self.img.crop(region_gauge)

        # Convert before OCR
        gauge = img_gauge_crop.convert('L')
        gauge = ImageEnhance.Contrast(gauge).enhance(2.0)

        img_arr = np.array(gauge)
        img_arr = (img_arr > 128).astype(np.uint8) * 255
        gauge = Image.fromarray(img_arr)

        # Read gauge value > convert to float
        gauge_percent = pytesseract.image_to_string(gauge, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
        try :
            gauge_percent = float(gauge_percent)
        except ValueError:
            gauge_percent = 0.0
        
        return gauge_percent
    

    def enemy_state(self) :
        img = self.img.convert('RGB')
        img_arr = np.array(img)

        results = self.yolo_model(img_arr, imgsz=1280, conf=0.5, verbose=False)[0]
        boxes = results.boxes.xyxy.cpu().numpy()
        classes = results.boxes.cls.cpu().numpy()

        if len(boxes) < 2:
            return None, 0, 0
        
        centers = [((x1 + x2) / 2, (y1 + y2) / 2) for x1, y1, x2, y2 in boxes[:2]]
        distance = np.sqrt((centers[1][0] - centers[0][0])**2 + (centers[1][1] - centers[0][1])**2)

        # Check if enemy is block or not
        high_block = int(2 in classes)
        low_block = int(3 in classes)
        return distance, high_block, low_block
    

    def check_skill_cooldown(self, region_skill):
        img_skill_crop = self.img.crop(region_skill)
        img_skill_crop = img_skill_crop.convert('L')
        
        img_arr = np.array(img_skill_crop)
        top_half = img_arr[:img_arr.shape[0]//2, :]
        brightness = top_half.mean()
        return brightness > self.skill_threshold
    

    def update(self, img):
        self.img = img.convert('RGB')