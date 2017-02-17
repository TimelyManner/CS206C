'''
Created on 2017. 2. 17.

@author: jslee
'''
from app_queue.snakerun.snakerunframe import *
from app_queue.snakerun.world import *
from posix import getcwd

class MyWorld(World):
    def __init__(self, file):
        World.__init__(self, file)
        
    def putThingToMap(self, x, y, obj):
       self.map.tiles[y][x] = obj
        
    def getThingFromMap(self, x, y):
        return self.map.tiles[y][x]          
        
    def createFeed(self, display):
        self.feed.color = random.choice(['red', 'blue', 'black', 'yellow'])
        
        feed_ok = False        
        while feed_ok == False:
            self.feed.x = int(random.random()*(self.map.width-1))
            self.feed.y = int(random.random()*(self.map.height-1))
            if self.getThingFromMap(self.feed.x, self.feed.y) == str(World.Map.SPACE):
                feed_ok = True   
                     
        self.feed.shape_id = display.mainCanvas.create_rectangle(self.feed.x*self.map.grain_size, self.feed.y*self.map.grain_size, 
                                            (self.feed.x+1)*self.map.grain_size, (self.feed.y+1)*self.map.grain_size, 
                                            fill=self.feed.color)
        self.putThingToMap(self.feed.x, self.feed.y, World.Map.FEED)

    def removeFeed(self, display, tile):
        display.mainCanvas.delete(tile.shape_id)
        self.putThingToMap(tile.x, tile.y, World.Map.SPACE)
        
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
            self.map.tiles.append(list(l))
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
        
        if x < 0 or y < 0 or x >= self.map.width or y >= self.map.height:
            return Display.Tile('out', None)        
        elif self.getThingFromMap(x, y) == World.Map.WALL:
            return Display.Tile('wall', None, x, y)  
        elif self.getThingFromMap(x, y) == World.Map.FEED:
            return Display.Tile('feed', self.feed.shape_id, x, y)
        elif self.getThingFromMap(x, y) == World.Map.OBJECT:
            return Display.Tile('tail', None, x, y)
        else:
            return Display.Tile('space', None, x, y)  