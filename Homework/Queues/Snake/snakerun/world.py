'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import *
import random
from snakerunframe import *

class World:
    class Map:  
        SPACE = '0'        
        WALL = '1'              
        def __init__(self, width, height, size, bg):
            self.width = width
            self.height= height
            self.grain_size = size
            self.tiles = None
            self.bg = bg            
    
    class Feed:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color
            self.shape_id = None             
    
    def __init__(self, file):
        self.map = World.Map(0, 0, None, None)
        self.loadMap(file)
        '''      
        self.grain_size = 15
        self.width = 50
        self.height = 50
       
        self.bg = 'green' 
        ''' 
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
        elif x < 0 or y < 0 or x >= self.map.width or y >= self.map.height:
            return Display.Tile('wall', None)        
        else:
            return Display.Tile('space', None)
        
class MyWorld(World):
    def __init__(self, file):
        World.__init__(self, file)
        
    def createFeed(self, display):
        self.feed.color = random.choice(['red', 'blue', 'black', 'yellow'])
        
        feed_ok = False        
        while feed_ok == False:
            self.feed.x = int(random.random()*(self.map.width-1))
            self.feed.y = int(random.random()*(self.map.height-1))
            if self.map.tiles[self.feed.y][self.feed.x] == World.Map.SPACE:
                feed_ok = True   
                     
        self.feed.shape_id = display.mainCanvas.create_rectangle(self.feed.x*self.map.grain_size, self.feed.y*self.map.grain_size, 
                                            (self.feed.x+1)*self.map.grain_size, (self.feed.y+1)*self.map.grain_size, 
                                            fill=self.feed.color)
        
    def loadMap(self, file_name):
        file_object = open(file_name, 'r')
        t_map = file_object.read()
        i_map = list(t_map.split())
        self.map.width = int(i_map[0])
        self.map.height = int(i_map[1])
        self.map.grain_size = int(i_map[2])
        self.map.bg = i_map[3]
        self.map.wall_color = i_map[4]        
        column_len = len(i_map[5])
        l_map = i_map[5:len(i_map)]
        self.map.tiles = list()
        row_len = 0   
        for l in l_map:
            row_len = row_len + 1
            self.map.tiles.append(l)
        file_object.close()
        if self.map.width != column_len or self.map.height != row_len: 
            print('Map errors: width {} or height {} is wrong!'.format(column_len, row_len))
            
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
        
        if self.map.tiles[y][x] == World.Map.WALL:
            return Display.Tile('wall', None)  
        elif x == self.feed.x and y == self.feed.y:
            return Display.Tile('feed', self.feed.shape_id)
        else:
            return Display.Tile('space', None)  