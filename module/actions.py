import pyautogui
import subprocess
import time


class GalleonActions:
    def __init__(self):
        result = subprocess.run(
            ['xdotool', 'search', '--name', 'Granblue Fantasy Versus: Rising'],
            capture_output=True, text=True
        )
        ids = result.stdout.strip().split('\n')
        self.window_id = ids[-1]
        self.ACTION_MAP = [
            self.normal_attack_z,
            self.chain_attack_z,
            self.low_attack_z,
            self.low_attack_z_2hit,
            self.normal_attack_x,
            self.chain_normal_attack_x,
            self.low_attack_x,
            self.normal_attack_c,
            self.chain_normal_attack_c,
            self.low_attack_c,
            self.will_of_the_earth_light,
            self.will_of_the_earth_med,
            self.will_of_the_earth_heavy,
            self.bedrock_blast,
            self.bedrock_blast_z,
            self.bedrock_blast_x,
            self.bedrock_blast_c,
            self.primordial_grasp,
            self.primordial_grasp_enhanced,
            self.muddy_embrace,
            self.muddy_embrace_enhanced,
            self.meteorite,
            self.meteorite_enhanced,
            self.meteorite_hold,
            self.meteorite_hold_enhanced,
            self.seism,
            self.seism_charge,
            self.will_of_the_earth_gauge,
            self.bedrock_blast_gauge,
            self.primordial_grasp_gauge,
            self.muddy_embrace_gauge,
            self.meteorite_gauge,
            self.raging_strike,
            self.raging_strike_chain,
            self.terrestrial_pulse_t,
            self.terrestrial_pulse_p,
            self.swat,
            self.walk_forward,
            self.walk_backward,
            self.dash_forward,
            self.dash_backward,
            self.run_forward,
            self.high_block,
            self.low_block,
            self.throw,
            self.throw_backward,
            self.dodge,
            self.jump_forward,
            self.jump_backward,
        ]


        self.ACTION_DURATION = [
            0.44, # normal_attack_z
            1.37, # chain_attack_z
            0.87, # low_attack_z
            1.07, # low_attack_z_2hit
            0.6, # normal_attack_x
            1.4, # chain_normal_attack_x
            0.87, # low_attack_x
            0.8, # normal_attack_c
            1.54, # chain_normal_attack_c
            1.2, # low_attack_c
            0.74, # will_of_the_earth_light
            1.04, # will_of_the_earth_med
            0.97, # will_of_the_earth_heavy
            0.7, # bedrock_blast
            0.7, # bedrock_blast_z
            1.1, # bedrock_blast_x
            1.4, # bedrock_blast_c
            2.7, # primordial_grasp
            2.74, # primordial_grasp_enhanced
            3.2, # muddy_embrace
            3.67, # muddy_embrace_enhanced error !
            0.47, # meteorite
            0.5, # meteorite_enhanced
            0.77, # meteorite_hold
            0.8, # meteorite_hold_enhanced
            1.0, # seism
            1.3, # seism_charge
            1.24, # will_of_the_earth_gauge
            3.6, # bedrock_blast_gauge
            2.77, # primordial_grasp_gauge
            3.9, # muddy_embrace_gauge
            1.1, # meteorite_gauge
            1.5, # raging_strike
            2.34, # raging_strike_chain
            7.74, # terrestrial_pulse_t
            3.7, # terrestrial_pulse_p
            10.87, # swat
            0.3, # walk_forward
            0.3, # walk_backward
            0.64, # dash_forward
            0.67, # dash_backward
            0.5, # run_forward
            1.0, # high_block
            1.0, # low_block
            1.8, # throw
            1.9, # throw_backward
            1.37, # dodge
            1.17, # jump_forward
            1.07 # jump_backward
        ]
    
    def _reset_keys(self):
        for key in ['Right', 'Left', 'Up', 'Down', 's']:
            pyautogui.keyUp(key)
            subprocess.run(['xdotool', 'keyup', '--window', self.window_id, key])
    

    def normal_attack_z(self):
        #self._reset_keys()
        pyautogui.keyDown('z')
        pyautogui.keyUp('z')


    def chain_attack_z(self):
        #self._reset_keys()
        command = ['z', 'z', 'z', 'z']
        for key in command:
            pyautogui.keyDown(key)
            pyautogui.keyUp(key)


    def low_attack_z(self):
        #self._reset_keys()
        pyautogui.keyDown('Down')
        pyautogui.keyDown('z')
        time.sleep(0.3)
        pyautogui.keyUp('Down')
        pyautogui.keyUp('z')


    def low_attack_z_2hit(self):
        #self._reset_keys()
        pyautogui.keyDown('Down')
        for i in range(2):
            pyautogui.keyDown('z')
            pyautogui.keyUp('z')
        time.sleep(0.3)
        pyautogui.keyUp('Down')


    def normal_attack_x(self):
        #self._reset_keys()
        pyautogui.keyDown('x')
        pyautogui.keyUp('x')
    

    def chain_normal_attack_x(self): 
        #self._reset_keys()
        command = ['x', 'x', 'x', 'x']
        for key in command:
            pyautogui.keyDown(key)
            pyautogui.keyUp(key)


    def low_attack_x(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'x'])
        time.sleep(0.3)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'x'])



    def normal_attack_c(self):
        #self._reset_keys()
        pyautogui.keyDown('c')
        pyautogui.keyUp('c')
    
    
    def chain_normal_attack_c(self): 
        #self._reset_keys()
        command = ['c', 'c', 'c', 'c']
        for key in command:
            pyautogui.keyDown(key)
            pyautogui.keyUp(key)


    def low_attack_c(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'c'])
        time.sleep(0.3)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'c'])
    
    
    def will_of_the_earth_light(self): # Will of the Earth (light version)
        #self._reset_keys()
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
    
    
    def will_of_the_earth_med(self): # Will of the Earth (medium version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'a', 'x'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'a', 'x'])
        

    def will_of_the_earth_heavy(self): # Will of the Earth (heavy version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'a', 'c'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'a', 'c'])


    def bedrock_blast(self): # Bedrock Blast (basic version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right', 'a'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right', 'a'])


    def bedrock_blast_z(self): # Bedrock Blast (z version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right', 'a', 'z'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right', 'a', 'z'])


    def bedrock_blast_x(self): # Bedrock Blast (x version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right', 'a', 'x'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right', 'a', 'x'])


    def bedrock_blast_c(self): # Bedrock Blast (c version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right', 'a', 'c'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right', 'a', 'c'])


    def primordial_grasp(self): # Primordial Grasp
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Left', 'a'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Left', 'a'])


    def primordial_grasp_enhanced(self): # Primordial Grasp (enhanced version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Left', 'a', 'c'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Left', 'a', 'c'])


    def muddy_embrace(self): # Muddy Embrace
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Up'])
        time.sleep(0.03)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Up'])
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'a'])
        time.sleep(0.1)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'a'])

    
    def muddy_embrace_enhanced(self): # Muddy Embrace (enhanced version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Up'])
        time.sleep(0.03)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Up'])
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'c', 'a'])
        time.sleep(0.1)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'c', 'a'])

    
    def meteorite(self): # raise 1 level of meteorite
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'a'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'a'])


    def meteorite_enhanced(self): # raise 2 levels of meteorite
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'a', 'c'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'a', 'c'])


    def meteorite_hold(self): # meteorite hold (raise 2 lv for basic version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'a'])
        time.sleep(0.3)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'a'])


    def meteorite_hold_enhanced(self): # meteorite hold (raise 3 lv for enhanced version)
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'a', 'c'])
        time.sleep(0.3)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'a', 'c'])


    def seism(self):
        #self._reset_keys()
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')

    
    def seism_charge(self):
        #self._reset_keys()
        pyautogui.keyDown('v')
        time.sleep(0.3)
        pyautogui.keyUp('v')


    # Skill use gauge (50% sba gauge)
    def will_of_the_earth_gauge(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'a', 'v'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'a', 'v'])


    def bedrock_blast_gauge(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right', 'a', 'v'])
        time.sleep(0.2)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right', 'a', 'v'])


    def primordial_grasp_gauge(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Left', 'v', 'a'])
        time.sleep(0.2)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Left', 'v', 'a'])


    def muddy_embrace_gauge(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Up'])
        time.sleep(0.1)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Up'])
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'a', 'v'])
        time.sleep(0.05)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'a', 'v'])


    def meteorite_gauge(self): # raise 1 level of meteorite
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Down', 'a', 'v'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Down', 'a', 'v'])


    def raging_strike(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'x', 'c'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'x', 'c'])

    
    def raging_strike_chain(self):
        #self._reset_keys()
        for i in range(2):
            self.raging_strike()
            time.sleep(0.2)


    def terrestrial_pulse_t(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'f', 'a'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'f', 'a'])


    def terrestrial_pulse_p(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Left', 'f', 'a'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Left', 'f', 'a'])


    def swat(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'f', 'a', 'v'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'f', 'a', 'v'])


    # Simple action (walk, dash, run, block, throw, dodge)
    # walk
    def walk_forward(self):
        #self._reset_keys()
        pyautogui.keyDown('Right')
        time.sleep(0.3)
        pyautogui.keyUp('Right')


    
    def walk_backward(self):
        #self._reset_keys()
        pyautogui.keyDown('Left')
        time.sleep(0.3)
        pyautogui.keyUp('Left')


    # dash
    def dash_forward(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 's', 'Right'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 's', 'Right'])


    def dash_backward(self):
        #self._reset_keys()
        for i in range(2):
            subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Left'])
            subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Left'])


    # Run
    def run_forward(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right'])
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right'])
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right'])
        time.sleep(0.5)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right'])



    # Block
    def high_block(self):
        #self._reset_keys()
        pyautogui.keyDown('s')
        time.sleep(1.0)
        pyautogui.keyUp('s')



    def low_block(self):
        #self._reset_keys()
        pyautogui.keyDown('s')
        pyautogui.keyDown('Down')
        time.sleep(1.0)
        pyautogui.keyUp('s')
        pyautogui.keyUp('Down')


    # Throw
    def throw(self):
        #self._reset_keys()
        pyautogui.keyDown('f')
        time.sleep(0.3)
        pyautogui.keyUp('f')


    def throw_backward(self):
        #self._reset_keys()
        pyautogui.keyDown('Left')
        pyautogui.keyDown('f')
        time.sleep(0.3)
        pyautogui.keyUp('Left')
        pyautogui.keyUp('f')


    # Dodge
    def dodge(self):
        #self._reset_keys()
        pyautogui.keyDown('s')
        pyautogui.keyDown('Left')
        time.sleep(0.3)
        pyautogui.keyUp('s')
        pyautogui.keyUp('Left')


    # Jump
    def jump_forward(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Right', 'Up'])
        time.sleep(0.3)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Right', 'Up'])


    def jump_backward(self):
        #self._reset_keys()
        subprocess.run(['xdotool', 'keydown', '--window', self.window_id, 'Left', 'Up'])
        time.sleep(0.3)
        subprocess.run(['xdotool', 'keyup', '--window', self.window_id, 'Left', 'Up'])


    # Rematch when set end. 1 set = 3 game, win 2/3 = win 1 set
    def rematch(self): # Enter 2 time for rematch
        time.sleep(25)
        for i in range(2):
            pyautogui.keyDown('enter') # Display menu
            time.sleep(0.3)
            pyautogui.keyUp('enter')
            time.sleep(3)



# def main():
#     galleon = GalleonActions()
#     time.sleep(3)  # Wait for 3 seconds before executing the action
#     actions = [ galleon.low_block]

#     for action in actions:
#         action()
#         time.sleep(3)

# if __name__ == "__main__":
#     main()