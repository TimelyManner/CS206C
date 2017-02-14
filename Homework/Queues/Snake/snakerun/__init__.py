'''
Created on 2017. 2. 12.

@author: jslee
'''

from snakerun.snakerunframe import *
from snakerun.snake import *
from snakerun.world import *
import random

random.seed()
rand_dir = int(random.random()*3)
switch_code = {0:'right', 1:'up', 2:'left', 3:'right'}

playground = MyWorld('map1.txt') 
mysnake = MySnake(int(playground.width/2), int(playground.height/2), 'white', switch_code.get(rand_dir))

app = Display(playground, mysnake, 200)
app.master.title('Snake Run with your queues')
app.mainloop()