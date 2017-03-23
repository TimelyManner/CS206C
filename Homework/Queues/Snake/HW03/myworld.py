'''
Created on 2017. 2. 17.

@author: jslee
'''
from builtins import type
from world import *
from snakerunframe import *

class MyWorld(World):
        
    class MyMap(World.Map):
        def __init__(self, file):
            World.Map.__init__(self, file)
            
        def load_map(self, file_name):            
            '''
            1. To refine the corresponding base method here
            file_name: file_name (string)
            return: success or fail (bool)
            '''            
            file_object = open(file_name, 'r')     
            t_map = file_object.read()
            i_map = list(t_map.split())
            self.width = int(i_map[0])
            self.height = int(i_map[1])
            self.grain_size = int(i_map[2])
            self.bg = i_map[3]
            self.wall_color = i_map[4]        
            self.cnt_feed = int(i_map[5])
            self.sleep_time = int(i_map[6])
            column_len = len(i_map[7])
            l_map = i_map[7:len(i_map)]
            self.tiles = dict()
            row = 0   
            switch_code = {'0':World.Cell.SPACE, '1': World.Cell.WALL, 
                           '2':World.Cell.FEED, '3':World.Cell.OBJECT}
            for l in l_map:
                l_map = list(l)
                col = 0
                for r in l_map:
                    self.tiles[(col,row)] = Display.Tile(switch_code.get(r,-1), None, col, row, )
                    col = col + 1
                row = row + 1 
            file_object.close()
            row_len = row
            if self.width != column_len or self.height != row_len: 
                print('Map errors: width {} or height {} is wrong!'.format(column_len, row_len))
                return False
            else:
                print('Map is correct!') 
                return True           
    
    def __init__(self, file):        
        self.map = MyWorld.MyMap(file)
        self.feed = MyWorld.Feed()
        
    def put_tile(self, x, y, type, shape_id = None):
        '''
        2. To write a code to put a tile with type and canvas item at given position 
        x: column (int)
        y: row (int)
        type: cell type (app_queue.snakerun.word.World.Cell)
        shape_id: rectangle id created in the canvas
        '''
        self.map.tiles[(x,y)].type = type
        self.map.tiles[(x,y)].shape_id = shape_id
        
    def get_tile(self, x, y, option):   
        '''
        3. To write a code to get a tile at given position 
        x: column (int)
        y: row (int)
        optin: attribute name of the tile (str)
        return: the value of corresponding attribute
        '''
        if option == 'type':
            return self.map.tiles[(x,y)].type
        elif option == 'shape_id':
            return self.map.tiles[(x,y)].shape_id        
        
    def create_feed(self, display): 
        '''
        4. To refine the corresponding base method
        display: main window (app_queue.snakerunframe.Display)
        '''
        while self.map.cnt_feed > 0:
            self.feed.color = random.choice(['red', 'blue', 'black', 'yellow'])
            feed_ok = False        
            while feed_ok == False:
                self.feed.x = int(random.random()*(self.map.width-1))
                self.feed.y = int(random.random()*(self.map.height-1))
                if self.get_tile(self.feed.x, self.feed.y, 'type') == World.Cell.SPACE:
                    feed_ok = True   
                         
            self.feed.shape_id = display.main_canvas.create_rectangle(self.feed.x*self.map.grain_size, self.feed.y*self.map.grain_size, 
                                                (self.feed.x+1)*self.map.grain_size, (self.feed.y+1)*self.map.grain_size, 
                                                fill=self.feed.color)
            self.put_tile(self.feed.x, self.feed.y, World.Cell.FEED, self.feed.shape_id)
            self.map.cnt_feed -= 1

    def remove_feed(self, display, tile=None):
        '''
        5. To refine the corresponding base method 
        display: main window (app_queue.snakerunframe.Display)
        tile: tile object to remove (app_queue.snakerunframe.Display.Tile)
        '''
        display.main_canvas.delete(tile.shape_id)
        self.put_tile(tile.x, tile.y, World.Cell.SPACE)
        self.map.cnt_feed += 1
            
    def get_tile_ahead(self, snake):
        '''
        6. To refine the corresponding base method
        snake: snake (MySnake)
        return: tile object to remove (app_queue.snakerunframe.Display.Tile)  
        '''
        if snake._head.dir == 'right':
            x = snake._head.x + 1
            y = snake._head.y
        elif snake._head.dir == 'left':
            x = snake._head.x - 1
            y = snake._head.y
        elif snake._head.dir == 'up':
            x = snake._head.x
            y = snake._head.y - 1
        else:
            x = snake._head.x
            y = snake._head.y + 1
        
        if x < 0 or y < 0 or x >= self.map.width or y >= self.map.height:
            return (World.Cell.OUT, None, x, y)        
        elif self.get_tile(x, y, 'type') == World.Cell.FEED:
            return (World.Cell.FEED, self.get_tile(x, y, 'shape_id'), x, y)
        else:
            return (self.get_tile(x, y, 'type'), None, x, y)
 