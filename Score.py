from pico2d import *
import numpy as np

import game_framework



class game_Score:
    def __init__(self):
        self.total_Score = 0
        self.font = load_font('font\\godoMaum.ttf', 50)
        self.timer = 0

    def draw(self):
        self.font.draw(810, 200, 'score : %3d' % self.total_Score, (0, 0, 0))

    def update(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.5:
            self.total_Score += 1
            self.timer = 0
        pass



