'''
Created on 2017. 2. 12.

@author: jslee
'''
class Snake:
    class Dir:
        RIGHT=0
        DOWN=1
        LEFT=2
        UP=3
        
    class Node:
        def __init__(self, x, y, width, height, color):            
            self.x=x
            self.y=y
            self.width = width
            self.height = height
            self.color = color
            
    class Head(Node):
        def __init__(self, x, y, width, height, color, dir, speed):
            Snake.Node.__init__(self, x, y, width, height, color)
            self.dir = dir
            self.speed = speed
        
    def __init__(self, x=0, y=0, width=10, height=10, color='yellow', dir=Dir.RIGHT, speed=0.01):
        self.head = self.Head( x, y, width, height, color, dir, speed)
        
#a = Snake()

        
                
     
        