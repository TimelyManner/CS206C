'''
Created on 2017. 2. 12.

@author: jslee
'''

from snakerun.snakerunframe import *
from snake import *
from world import *
import random
from sys import platform as _platform

print('your program is running under {} platform'.format(_platform) )

random.seed()
rand_dir = int(random.random()*3)
switch_code = {0:'right', 1:'up', 2:'left', 3:'right'}

playground = MyWorld('map2.txt')
mysnake = MySnake(int(playground.map.width/2), int(playground.map.height/2), 
                  'white', switch_code.get(rand_dir))

app = Display(playground, mysnake, 200)
app.master.title('Snake Run with your queues')
app.mainloop()