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
    
    def __right(self, grain_size):
        self.head.x += 1
        
    def __left(self, grain_size):
        self.head.x -= 1

    def __up(self, grain_size):
        self.head.y -= 1
        
    def __down(self, grain_size):
        self.head.y += 1
        
    def soundPositive(self):
        winsound.Beep(2500, 100)
        
    def soundNegative(self):
        winsound.Beep(1000, 200)
        
    def moveandshow(self, display, feed=None):
        switcher = {'right':self.__right, 'left':self.__left, 'up':self.__up, 'down':self.__down}
        func = switcher.get(self.head.dir, lambda: 'nothing')
        func(display.map_grain_size)   
        
        x1,x2=self.head.x*display.map_grain_size, (self.head.x+1)*display.map_grain_size
        y1,y2=self.head.y*display.map_grain_size, (self.head.y+1)*display.map_grain_size
        
        if self.tail_queue.__len__() > 1:   # if any tail exists
            for i in range(self.tail_queue.__len__()-1, 0, -1):                        
                pre_color = fill=display.mainCanvas.itemcget( self.tail_queue[i-1], 'fill')
                display.mainCanvas.itemconfig(self.tail_queue[i],
                                              fill=pre_color) 
        if feed == None:
            new_head_shape_id = display.mainCanvas.create_rectangle(x1, y1, x2, y2, fill=self.head.color)             
            if self.tail_queue.__len__() > 0:
                tail_shape_id = self.tail_queue.popleft()            
                display.mainCanvas.delete(tail_shape_id)
        else:
            self.soundPositive()
            tail_shape_id = self.tail_queue[0]
            display.mainCanvas.itemconfig(tail_shape_id, fill=feed.color)
            self.head.shape_id = feed.shape_id
            display.mainCanvas.itemconfig(self.head.shape_id, fill=self.head.color)
            new_head_shape_id = self.head.shape_id                        
                    
        self.tail_queue.append(new_head_shape_id)
                                              