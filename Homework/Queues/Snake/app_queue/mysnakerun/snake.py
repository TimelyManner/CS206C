'''
Created on 2017. 2. 17.

@author: jslee
'''
from app_queue.snakerun.snake import *
from app_queue.snakerun.world import *
from app_queue.mysnakerun.queue import *

class MySnake(Snake):
    class Tail:
        def __init__(self, shape_id, x, y):
            self.shape_id = shape_id
            self.x = x
            self.y = y
    
    def __init__(self, x, y, color, dir):
        Snake.__init__(self, x, y, color, dir)
        self.tail_queue = MyQueue()
        
    def moveAndShow(self, display, tile=None):
        '''
        display: main window (app_queue.snakerunframe.Display)
        tile: tile info to get next (app_queue.snakerunframe.Display.Tile)
        '''
        if tile != None:
            pre_head_x = self.head.x
            pre_head_y = self.head.y
            
            switcher = {'right':self._right, 'left':self._left, 'up':self._up, 'down':self._down}
            func = switcher.get(self.head.dir, lambda: 'nothing')
            func(display.map_grain_size)   
            
            x1,x2=self.head.x*display.map_grain_size, (self.head.x+1)*display.map_grain_size
            y1,y2=self.head.y*display.map_grain_size, (self.head.y+1)*display.map_grain_size
            
            if len(self.tail_queue) >= 2:   # if any tail exists without the head
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
                    display.world.putTileToMap(tail.x, tail.y, World.Cell.SPACE)                    

            elif tile.type == 'feed':                
                tail = self.tail_queue[0]
                tile_color = display.mainCanvas.itemcget(tile.shape_id, 'fill')
                display.mainCanvas.itemconfig(tail.shape_id, fill=tile_color)
                         
            self.tail_queue.append(MySnake.Tail(new_head_shape_id,self. head.x, self.head.y))
            if len(self.tail_queue) >= 2:                
                display.world.putTileToMap(pre_head_x, pre_head_y, World.Cell.OBJECT)
            return True    