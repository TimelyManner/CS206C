'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import *
import random

from app_queue.snakerun.snakerunframe import *   

class World:
    class Map:  
        SPACE = '0'        
        WALL =  '1' 
        FEED =  '2'
        OBJECT = '3'
                     
        def __init__(self, width, height, size, bg):
            self.width = width
            self.height= height
            self.grain_size = size
            self.tiles = list()
            self.bg = bg            
    
    class Feed:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color
            self.shape_id = None
            self.backup = World.Map.SPACE             
    
    def __init__(self, file=None):
        self.map = World.Map(0, 0, None, None)
        self.loadMap(file)
        self.feed = World.Feed(-100, -100, 'red')
        
    def loadMap(self, file_name):
        self.map.width = 50
        self.map.height = 50
        self.map.grain_size = 15
        self.map.bg = 'green'
        self.map.wall_color = 'brown'        
        self.map.tiles = []
        
    def createFeed(self, display):
        self.feed.color = 'red'        
        self.feed.x = int(random.random()*(self.map.width-1))
        self.feed.y = int(random.random()*(self.map.height-1))                     
        self.feed.shape_id = display.mainCanvas.create_rectangle(self.feed.x*self.map.grain_size, self.feed.y*self.map.grain_size, 
                                            (self.feed.x+1)*self.map.grain_size, (self.feed.y+1)*self.map.grain_size, 
                                            fill=self.feed.color)        
    def removeFeed(self, display, tile = None):
        display.mainCanvas.delete(self.feed.shape_id)
        self.feed = World.Feed(-100, -100, 'red')
    
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
        else:
            return Display.Tile('space', None)