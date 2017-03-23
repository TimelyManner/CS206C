'''
Created on 2017. 2. 12.

@author: jslee
'''
import random
from tkinter import *

class World:
    class Map:
        def __init__(self, file):     # To create a default-set map
            if file == None:
                self.width = 50
                self.height = 50
                self.grain_size = 15
                self.bg = 'green'
                self.wall_color = 'brown'
                self.tiles = []
                self.sleep_time = 200   # To set periodic time in millisecond for the tick-based refresh of window display
            else:
                self.load_map(file)
                
        def load_map(self, file):   # To handle to load a map information from given file, but left empty for some future extension
            pass                  
            
    class Cell:         # To define types of cells with unique integers in the world  
        OUT     = -1    # For out of screen
        SPACE   = 0     # For empty cells        
        WALL    = 1     # For wall cells
        FEED    = 2     # For feed cells
        OBJECT  = 3     # For moving object cells
                     
        def __init__(self, width, height, size, fill):  # To initialize the basic attributes of the cell
            self.width = width      
            self.height= height
            self.grain_size = size                      # To set the size of the cell  
            self.fill = fill                            # To set the basic color for filling the cell            
    
    class Feed:                                         # To define the type of feed used in the world 
        def __init__(self, x=-1000, y=-1000, color='red', shape_id = None):
            self.x = x
            self.y = y
            self.color = color
            self.shape_id = shape_id                        # To maintain shape id for the feed as Tkinter's canvas item 
    
    def __init__(self, file=None):                                 # To initialize the basic attributes of the world
        self.map = World.Map(file)
        self.score = 0                  
        
    def create_feed(self, display):                     # To create a feed in given display with default color, random position and shape id as a canvas item
        self.feed = World.Feed(int(random.random()*(self.map.width-1)), int(random.random()*(self.map.height-1))) 
        self.feed.shape_id = display.main_canvas.create_rectangle(self.feed.x*self.map.grain_size, self.feed.y*self.map.grain_size, 
                                            (self.feed.x+1)*self.map.grain_size, (self.feed.y+1)*self.map.grain_size, 
                                            fill=self.feed.color)
                
    def remove_feed(self, display, tile = None):         # To remove the default feed
        if self.feed:
            self.score += 1
            display.show_text('Score:{}'.format(self.score))
            display.main_canvas.delete(self.feed.shape_id)
            del self.feed
            
    def get_tile_ahead(self, snake):                    # To get a tile info right ahead of given snake in its moving direction
        sx, sy, sdir = snake.get_head_info()
        
        if sdir == 'right':
            x = sx + 1
            y = sy
        elif sdir == 'left':
            x = sx - 1
            y = sy
        elif sdir == 'up':
            x = sx
            y = sy - 1
        else:
            x = sx
            y = sy + 1
        
        if x == self.feed.x and y == self.feed.y:
            return (World.Cell.FEED, self.feed.shape_id, x, y)
        else:
            return (World.Cell.SPACE, self.feed.shape_id, x, y)