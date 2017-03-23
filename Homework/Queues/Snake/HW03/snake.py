'''
Created on 2017. 2. 12.

@author: jslee
'''
import os, sys, random
from tkinter import *
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    pass
    # linux
elif _platform == "darwin":
    pass
    # MAC OS X
elif _platform == "win32":
    # Windows
    import winsound

class Snake:
    class Head:     # To define the head of the snake    
        def __init__(self, x, y, color, dir):
            self.x=x
            self.y=y
            self.color = color             
            self.dir = dir
        
    def __init__(self, x=0, y=0, color='yellow'):
        random.seed()   # To get the random function prepared with the seed of current time
        rand_dir = int(random.random()*3)   # To get a randomized number between 0 and 3
        switch_code = {0:'right', 1:'up', 2:'left', 3:'right'}  # To return a direction string according to the random number
        
        self._head = self.Head( x, y, color, switch_code.get(rand_dir, 'right'))        
        self._new_head_shape_id = None
    
    def get_head_info(self):
        return (self._head.x, self._head.y, self._head.dir)
    
    def _right(self, grain_size):
        self._head.x += 1
        
    def _left(self, grain_size):
        self._head.x -= 1

    def _up(self, grain_size):
        self._head.y -= 1
        
    def _down(self, grain_size):
        self._head.y += 1
        
    def make_sound(self, case):
        if case == 'positive':
            if _platform == 'win32':
                winsound.Beep(2500, 100)
            else:
                sys.stdout.write('\a')
                sys.stdout.flush()
        elif case == 'negative':
            if _platform == 'win32':
                winsound.Beep(1000, 200)
            else:
                sys.stdout.write('\a')
                sys.stdout.flush()
        
    def make_move(self, display, tile=None):    # To handle a move of the snake in given display canvas 
        switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
        func = switcher.get(self._head.dir, lambda: 'nothing')
        func(display.map_grain_size)   
        
        x1,x2=self._head.x*display.map_grain_size, (self._head.x+1)*display.map_grain_size
        y1,y2=self._head.y*display.map_grain_size, (self._head.y+1)*display.map_grain_size 

        if self._new_head_shape_id != None:       
            display.main_canvas.delete( self._new_head_shape_id)    # To delete the previous head in given display canvas         
        self._new_head_shape_id = display.main_canvas.create_rectangle(
            x1, y1, x2, y2, fill=self._head.color)                  # To create the new head at the next location in given display canvas                                           