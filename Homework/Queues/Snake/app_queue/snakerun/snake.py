'''
Created on 2017. 2. 12.

@author: jslee
'''

import os, sys
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
    class Head:    
        def __init__(self, x, y, color, dir):
            self.x=x
            self.y=y
            self.color = color             
            self.dir = dir    
        
    def __init__(self, x=0, y=0, color='yellow', dir='right'):
        self.head = self.Head( x, y, color, dir)        
        self.new_head_shape_id = None
    
    def _right(self, grain_size):
        self.head.x += 1
        
    def _left(self, grain_size):
        self.head.x -= 1

    def _up(self, grain_size):
        self.head.y -= 1
        
    def _down(self, grain_size):
        self.head.y += 1
        
    def soundPositive(self):
        if _platform == 'win32':
            winsound.Beep(2500, 100)
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()
        
    def soundNegative(self):
        if _platform == 'win32':
            winsound.Beep(1000, 200)
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()
        
    def moveAndShow(self, display, tile=None):
        switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
        func = switcher.get(self.head.dir, lambda: 'nothing')
        func(display.map_grain_size)   
        
        x1,x2=self.head.x*display.map_grain_size, (self.head.x+1)*display.map_grain_size
        y1,y2=self.head.y*display.map_grain_size, (self.head.y+1)*display.map_grain_size 
        if self.new_head_shape_id != None:       
            display.mainCanvas.delete( self.new_head_shape_id)         
        self.new_head_shape_id = display.mainCanvas.create_rectangle(x1, y1, x2, y2, fill=self.head.color)                                           