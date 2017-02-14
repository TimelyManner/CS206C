'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import *
from collections import deque
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
        self.tail_queue = deque([])
    
    def _right(self, grain_size):
        self.head.x += 1
        
    def _left(self, grain_size):
        self.head.x -= 1

    def _up(self, grain_size):
        self.head.y -= 1
        
    def _down(self, grain_size):
        self.head.y += 1
        
    def soundPositive(self):
        winsound.Beep(2500, 100)
        
    def soundNegative(self):
        winsound.Beep(1000, 200)
        
    def moveAndShow(self, display, tile=None):
        switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
        func = switcher.get(self.head.dir, lambda: 'nothing')
        func(display.map_grain_size)   
        
        x1,x2=self.head.x*display.map_grain_size, (self.head.x+1)*display.map_grain_size
        y1,y2=self.head.y*display.map_grain_size, (self.head.y+1)*display.map_grain_size
        new_head_shape_id = display.mainCanvas.create_rectangle(x1, y1, x2, y2, fill=self.head.color)             
        
        if self.tail_queue.__len__() > 0:
            tail_shape_id = self.tail_queue.popleft()            
            display.mainCanvas.delete(tail_shape_id)
            
        self.tail_queue.append(new_head_shape_id)
        
        if tile != None and tile.type == 'feed':
            display.mainCanvas.delete(tile.shape_id) 
        
class MySnake(Snake):
    def __init__(self, x, y, color, dir):
        Snake.__init__(self, x, y, color, dir)
        
    def moveAndShow(self, display, tile=None):
        switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
        func = switcher.get(self.head.dir, lambda: 'nothing')
        func(display.map_grain_size)   
        
        x1,x2=self.head.x*display.map_grain_size, (self.head.x+1)*display.map_grain_size
        y1,y2=self.head.y*display.map_grain_size, (self.head.y+1)*display.map_grain_size
        
        if self.tail_queue.__len__() > 1:   # if any tail exists
            for i in range(self.tail_queue.__len__()-1, 0, -1):                        
                pre_color = fill=display.mainCanvas.itemcget( self.tail_queue[i-1], 'fill')
                display.mainCanvas.itemconfig(self.tail_queue[i],
                                              fill=pre_color) 
        if tile != None: 
            if tile.type == 'space':
                new_head_shape_id = display.mainCanvas.create_rectangle(x1, y1, x2, y2, fill=self.head.color)             
                if self.tail_queue.__len__() > 0:
                    tail_shape_id = self.tail_queue.popleft()            
                    display.mainCanvas.delete(tail_shape_id)
            elif tile.type == 'feed':
                tail_shape_id = self.tail_queue[0]
                tile_color = display.mainCanvas.itemcget(tile.shape_id, 'fill')
                display.mainCanvas.itemconfig(tail_shape_id, fill=tile_color)
                self.head.shape_id = tile.shape_id
                display.mainCanvas.itemconfig(self.head.shape_id, fill=self.head.color)
                new_head_shape_id = self.head.shape_id  
                                  
            self.tail_queue.append(new_head_shape_id)
            return True                                  