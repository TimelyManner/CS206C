'''
Created on 2017. 2. 17.

@author: jslee
'''
from sys import platform as _platform
import random
from app_queue.snakerun.world import *
from app_queue.snakerun.snake import *
from app_queue.snakerun.snakerunframe import *

from app_queue.mysnakerun.world import *
from app_queue.mysnakerun.snake import *

def goToProjectRootDirectory():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   
    os.chdir(ROOT_DIR)

print('The reference program is running under \'{}\' platform'.format(_platform) )
goToProjectRootDirectory()
random.seed()
rand_dir = int(random.random()*3)
switch_code = {0:'right', 1:'up', 2:'left', 3:'right'}

'''
You can change the following codes for the homework
'''
playground = MyWorld('map2.txt')
mysnake = MySnake(int(playground.map.width/2), int(playground.map.height/2), 
                  'white', switch_code.get(rand_dir))
app = Display(playground, mysnake)
app.master.title('Snake Run with your queues')
app.mainloop()

