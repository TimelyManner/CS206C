'''
Created on 2017. 2. 17.

@author: jslee
'''
from app_queue.snakerun.snakerunframe import *
from app_queue.snakerun.world import *
from posix import getcwd
from builtins import type

class MyWorld(World):
    class Tile():
        def __init__(self, x, y, type, shape_id):
            self.x = x
            self.y = y
            self.type = type
            self.shape_id = shape_id
    
    def __init__(self, file):
        World.__init__(self, file)
        
    def putTileToMap(self, x, y, type, shape_id = None):
        self.map.tiles[(x,y)].type = type
        self.map.tiles[(x,y)].shape_id = shape_id
        
    def getTileFromMap(self, x, y, option):
        if option == 'type':
            return self.map.tiles[(x,y)].type
        elif option == 'shape_id':
            return self.map.tiles[(x,y)].shape_id        
        
    def createFeed(self, display):
        while self.map.cnt_feed > 0:
            self.feed.color = random.choice(['red', 'blue', 'black', 'yellow'])
            feed_ok = False        
            while feed_ok == False:
                self.feed.x = int(random.random()*(self.map.width-1))
                self.feed.y = int(random.random()*(self.map.height-1))
                if self.getTileFromMap(self.feed.x, self.feed.y, 'type') == World.Map.SPACE:
                    feed_ok = True   
                         
            self.feed.shape_id = display.mainCanvas.create_rectangle(self.feed.x*self.map.grain_size, self.feed.y*self.map.grain_size, 
                                                (self.feed.x+1)*self.map.grain_size, (self.feed.y+1)*self.map.grain_size, 
                                                fill=self.feed.color)
            self.putTileToMap(self.feed.x, self.feed.y, World.Map.FEED, self.feed.shape_id)
            self.map.cnt_feed = self.map.cnt_feed - 1

    def removeFeed(self, display, tile):
        display.mainCanvas.delete(tile.shape_id)
        self.putTileToMap(tile.x, tile.y, World.Map.SPACE, tile.shape_id)
        self.map.cnt_feed = self.map.cnt_feed + 1
        
    def loadMap(self, file_name):
        file_object = open(file_name, 'r')
 
        t_map = file_object.read()
        i_map = list(t_map.split())
        self.map.width = int(i_map[0])
        self.map.height = int(i_map[1])
        self.map.grain_size = int(i_map[2])
        self.map.bg = i_map[3]
        self.map.wall_color = i_map[4]        
        self.map.cnt_feed = int(i_map[5])
        self.sleep_time = int(i_map[6])
        column_len = len(i_map[7])
        l_map = i_map[7:len(i_map)]
        self.map.tiles = dict()
        row = 0   
        switch_code = {'0':World.Map.SPACE, '1': World.Map.WALL, 
                       '2':World.Map.FEED, '3':World.Map.OBJECT}
        for l in l_map:
            l_map = list(l)
            col = 0
            for r in l_map:
                self.map.tiles[(col,row)] = MyWorld.Tile(col, row, switch_code.get(r,-1),None)
                col = col + 1
            row = row + 1 
        file_object.close()
        row_len = row
        if self.map.width != column_len or self.map.height != row_len: 
            print('Map errors: width {} or height {} is wrong!'.format(column_len, row_len))
        else:
            print('Map is correct!')
            
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
        
        if x < 0 or y < 0 or x >= self.map.width or y >= self.map.height:
            return Display.Tile('out', None)        
        elif self.getTileFromMap(x, y, 'type') == World.Map.WALL:
            return Display.Tile('wall', None, x, y)  
        elif self.getTileFromMap(x, y, 'type') == World.Map.FEED:
            return Display.Tile('feed', self.getTileFromMap(x, y, 'shape_id'), x, y)
        elif self.getTileFromMap(x, y, 'type') == World.Map.OBJECT:
            return Display.Tile('tail', None, x, y)
        else:
            return Display.Tile('space', None, x, y)  