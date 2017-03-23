'''
Created on 2017. 2. 17.

@author: jslee
'''
from snake import *
from world import *
from snakerunframe import *
from myworld import *
from mysnake import *
import tools

tools.init_env()
id = 'base version'
playground = None
mysnake = None

if len(sys.argv) < 2:  # When being run with no additional argument
    playground = World()    # To create a default world for a snake
    mysnake = Snake(int(playground.map.width/2), 
                    int(playground.map.height/2), 'white')   # To create a snake with initial position, color   
else:       
    id = sys.argv[1]
    playground = MyWorld('map2.txt')    # To create a world from map file named "map2.txt"
    mysnake = MySnake(int(playground.map.width/2), 
                      int(playground.map.height/2), 'white')

if playground == None or mysnake == None:
    print('Error: run after implementing your snake!')
else:
    app = Display(playground, mysnake)      # To create a window frame with given world and snake 
    app.master.title('Snake Run with queues: ' + id)    # To set the window title with given 1st argument
    app.mainloop()