'''
Created on 2017. 2. 17.

@author: jslee
'''

import random, sys

random.seed()
rand_dir = int(random.random()*3)
switch_code = {0:'right', 1:'up', 2:'left', 3:'right'}

'''
You can change the following codes for the homework
'''

if sys.argv[0] != '__main__':   # When run by shell prompt
    import __init__

id = 'base version'
if len(sys.argv) <= 1:  # When run with no additional arguments
    from snakerun.snake import *
    from snakerun.snakerunframe import *
     
    playground = World('map2.txt')
    mysnake = Snake(int(playground.map.width/2), int(playground.map.height/2), 
                      'white', switch_code.get(rand_dir))
else:
    from mysnakerun.world import *
    from mysnakerun.snake import *
    
    id = sys.argv[1]
    playground = MyWorld('map2.txt')
    mysnake = MySnake(int(playground.map.width/2), int(playground.map.height/2), 
                      'white', switch_code.get(rand_dir))

app = Display(playground, mysnake)
app.master.title('Snake Run with queues: ' + id)
app.mainloop()
