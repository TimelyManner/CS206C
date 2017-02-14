'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import *
import random
from snakerunframe import *

class World:
    class Feed:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color
            self.shape_id = None             
    
    def __init__(self, file):
        self.map= self.loadMap(file)        
        self.grain_size = 15
        self.width = 50
        self.height = 50
        self.bg = 'green'
        self.feed = World.Feed(-100, -100, 'red')
        
    def loadMap(self, file_name):
        print('loaed a map from \'{}\''.format(file_name))
        
    def createFeed(self, display):
        self.feed.color = 'red'        
        self.feed.x = int(random.random()*(self.width-1))
        self.feed.y = int(random.random()*(self.height-1))                     
        self.feed.shape_id = display.mainCanvas.create_rectangle(self.feed.x*self.grain_size, self.feed.y*self.grain_size, 
                                            (self.feed.x+1)*self.grain_size, (self.feed.y+1)*self.grain_size, 
                                            fill=self.feed.color)        
    def removeFeed(self, display):
        display.mainCanvas.delete(self.feed.shape_id)
        self.feed = None
    
    def getForwardTile(self, snake):
        if snake.head.dir == 'right':
            x = snake.head.x + 1
            y = snake.head.y
        elif snake.head.dir == 'left':
            x = snake.head.x - 1
            y = snake.head.y
        elif snake.head.dir == 'up':
            x = snake.head.x
            y = snake.head.y - 1
        else:
            x = snake.head.x
            y = snake.head.y + 1
        
        if x == self.feed.x and y == self.feed.y:
            return Display.Tile('feed', self.feed.shape_id)
        elif x < 0 or y < 0 or x >= self.width or y >= self.height:
            return Display.Tile('wall', None)        
        else:
            return Display.Tile('space', None)
        
class MyWorld(World):
    def __init__(self, file):
        World.__init__(self, file)
        
    def createFeed(self, display):
        self.feed.color = random.choice(['red', 'blue', 'black', 'yellow'])        
        self.feed.x = int(random.random()*(self.width-1))
        self.feed.y = int(random.random()*(self.height-1))   
                     
        self.feed.shape_id = display.mainCanvas.create_rectangle(self.feed.x*self.grain_size, self.feed.y*self.grain_size, 
                                            (self.feed.x+1)*self.grain_size, (self.feed.y+1)*self.grain_size, 
                                            fill=self.feed.color)    
        