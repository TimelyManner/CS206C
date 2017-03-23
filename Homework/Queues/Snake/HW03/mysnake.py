'''
Created on 2017. 2. 17.

@author: jslee
'''
from myqueue import *
from world import *
from snake import *

class MySnake(Snake):
    class Tail:
        def __init__(self, shape_id, x, y):
            self.shape_id = shape_id
            self.x = x
            self.y = y
    
    def __init__(self, x, y, color):
        Snake.__init__(self, x, y, color)
        self.tail_queue = MyQueue()        
        
    def make_move(self, display, tile=None):
        '''
        7. To refine the corresponding base method
        display: main window (app_queue.snakerunframe.Display)
        tile: tile info to get next (app_queue.snakerunframe.Display.Tile)
        '''
        if tile != None:
            pre_head_x = self._head.x
            pre_head_y = self._head.y
            
            switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
            func = switcher.get(self._head.dir, lambda: 'nothing')
            func(display.map_grain_size)   
            
            x1,x2=self._head.x*display.map_grain_size, (self._head.x+1)*display.map_grain_size
            y1,y2=self._head.y*display.map_grain_size, (self._head.y+1)*display.map_grain_size
            
            if len(self.tail_queue) >= 2:   # if any tail exists
                for i in range(len(self.tail_queue)-1, 0, -1):                        
                    pre_color = fill=display.main_canvas.itemcget( self.tail_queue[i-1].shape_id, 'fill')
                    display.main_canvas.itemconfig(self.tail_queue[i].shape_id,
                                                  fill=pre_color)
            new_head_shape_id = display.main_canvas.create_rectangle(x1, y1, x2, y2, fill=self._head.color)   
             
            if tile.type == World.Cell.SPACE:                          
                if len(self.tail_queue) >= 1:
                    tail = self.tail_queue.popleft()            
                    display.main_canvas.delete(tail.shape_id)                                                        
                    display.world.put_tile(tail.x, tail.y, World.Cell.SPACE)
            elif tile.type == World.Cell.FEED:                
                tail = self.tail_queue[0]
                tile_color = display.main_canvas.itemcget(tile.shape_id, 'fill')
                display.main_canvas.itemconfig(tail.shape_id, fill=tile_color)
                         
            self.tail_queue.append(MySnake.Tail(new_head_shape_id,self._head.x, self._head.y))
            
            if len(self.tail_queue) >= 2:                
                display.world.put_tile(pre_head_x, pre_head_y, World.Cell.OBJECT)
            return True    