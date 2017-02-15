'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import *
from collections import deque
import winsound
from snakerun.world import *

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
    
    class Tail:
        def __init__(self, shape_id, x, y):
            self.shape_id = shape_id
            self.x = x
            self.y = y
    
    def __init__(self, x, y, color, dir):
        Snake.__init__(self, x, y, color, dir)
        
    def moveAndShow(self, display, tile=None):
        if tile != None:
            pre_head_x = self.head.x
            pre_head_y = self.head.y
            
            switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
            func = switcher.get(self.head.dir, lambda: 'nothing')
            func(display.map_grain_size)   
            
            x1,x2=self.head.x*display.map_grain_size, (self.head.x+1)*display.map_grain_size
            y1,y2=self.head.y*display.map_grain_size, (self.head.y+1)*display.map_grain_size
            
            if self.tail_queue.__len__() >= 2:   # if any tail exists without the head
                for i in range(len(self.tail_queue)-1, 0, -1):                        
                    pre_color = fill=display.mainCanvas.itemcget( self.tail_queue[i-1].shape_id, 'fill')
                    display.mainCanvas.itemconfig(self.tail_queue[i].shape_id,
                                                  fill=pre_color)
            
            new_head_shape_id = display.mainCanvas.create_rectangle(x1, y1, x2, y2, fill=self.head.color)   
             
            if tile.type == 'space':                          
                if len(self.tail_queue) >= 1:
                    tail = self.tail_queue.popleft()            
                    display.mainCanvas.delete(tail.shape_id)
                if len(self.tail_queue) >= 1:                                        
                    display.world.putThingToMap(tail.x, tail.y, World.Map.SPACE)                    

            elif tile.type == 'feed':                
                tail = self.tail_queue[0]
                tile_color = display.mainCanvas.itemcget(tile.shape_id, 'fill')
                display.mainCanvas.itemconfig(tail.shape_id, fill=tile_color)
                         
            self.tail_queue.append(MySnake.Tail(new_head_shape_id,self. head.x, self.head.y))
            if len(self.tail_queue) >= 2:                
                display.world.putThingToMap(pre_head_x, pre_head_y, World.Map.OBJECT)
            return True                                  