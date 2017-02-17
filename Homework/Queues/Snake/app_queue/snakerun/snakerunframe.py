'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import * 
from enum import *
from sys import platform as _platform

from app_queue.snakerun.world import *
   
class Display(Frame): 
    if _platform == 'win32':
        KEY_LEFT=37
        KEY_RIGHT=39
        KEY_SPACE=32
    elif _platform == 'darwin':
        KEY_LEFT=8124162
        KEY_RIGHT=8189699
        KEY_SPACE=3211296
    else:
        pass     
     
    class State(Enum):
        INIT=0
        PLAYING=1
        STOPPED=2
        GAMEOVER=3
        
    class Tile:
        def __init__(self, type, shape_id=None, x=-1, y=-1):
            self.type = type
            self.shape_id = shape_id
            self.x = x
            self.y = y
                      
    def __init__(self, world=None, snake=None, sleep_time=1000):

        if world != None and snake != None:
            self.snake = snake
            self.world = world
            self.map_grain_size = world.map.grain_size
            self.map_width = world.map.width
            self.map_height = world.map.height
            self.map_bg = world.map.bg
            self.sleep_time = sleep_time
            
            root = Tk()
            root.resizable(0,0)   
            Frame.__init__(self, root)   
            self.config(bg='black')    
            self.grid()                   
            self.createWidgets()    
            self.curstate=Display.State.INIT
            self.world.createFeed(self)
            self.snake.moveAndShow(self, Display.Tile('space'))            
            self.job_id = None
            row_cnt = 0
            for row in world.map.tiles:
                for i in range(0, len(row)):
                    if row[i] == world.Map.WALL:
                        self.mainCanvas.create_rectangle(i*world.map.grain_size,
                                                         row_cnt*world.map.grain_size, 
                                                         (i+1)*world.map.grain_size, 
                                                         (row_cnt+1)*world.map.grain_size, fill = world.map.wall_color)
                row_cnt = row_cnt +1
                               
                
            self.focus_set()
            self.key_processing = False
            
        else:
            quit()                
                 
    def play(self):
        if self.curstate != Display.State.PLAYING:
            self.toPlay()
    
    def toPlay(self):
        self.curstate=Display.State.PLAYING
        self.playButton.config(state=DISABLED) 
        self.stopButton.config(state=NORMAL)
        self.tick()
    
    def stop(self):
        if self.curstate != Display.State.STOPPED:
            self.toStop()

    def toStop(self):
        self.after_cancel(self.job_id)        
        
        self.curstate=Display.State.STOPPED
        self.playButton.config(state=NORMAL)
        self.playButton.config(text='Play')
        self.stopButton.config(state=DISABLED)

    def toGaveOver(self):
        self.curstate=Display.State.GAMEOVER
        self.playButton.config(state=NORMAL)
        self.playButton.config(text='Play')
        self.stopButton.config(state=DISABLED)
        self.showText('Game over...') 
            
    def quit(self):
        self.showText('Good bye~')
        quit()
        
    def createWidgets(self):
        self.mainCanvas = Canvas(self, bg=self.map_bg,
            width=(self.map_width*self.map_grain_size), 
            height=(self.map_height*self.map_grain_size))           
        self.logo = PhotoImage(file='kaist_logo.gif')
        self.logoLabel = Label(self, image=self.logo)  
        self.playButton = Button(self, text='Play',
            command=self.play)            
        self.stopButton = Button(self, text='Stop',
            command=self.stop, state=DISABLED)            
        self.quitButton = Button(self, text='Quit',
            command=self.quit)            
        self.scrollbar=Scrollbar(self)
        self.text = Text(self, yscrollcommand=self.scrollbar.set, width=20,
                         bg='green', fg='white')
        self.scrollbar.config(command=self.text.yview)
        
        self.mainCanvas.grid(row=0, column=0, rowspan=20, columnspan=20, sticky=N+W+S+E)
        self.logoLabel.grid(row=0, column=20, columnspan=1, sticky=N+W+S+E)         
        self.playButton.grid(row=1, column=20, columnspan=1, sticky=N+W+S+E)      
        self.stopButton.grid(row=2, column=20, columnspan=1, sticky=N+W+S+E)    
        self.quitButton.grid(row=3, column=20, columnspan=1, sticky=N+W+S+E)

        self.bind('<Key>', self.key)             
        self.bind('<Button-1>', self.callback)
        
    def showText(self, text_new):
        print(text_new)
        
    def callback(self, event):
        self.focus_set()
        
    def toggle(self):
        switch_code = {Display.State.PLAYING:self.stop, Display.State.STOPPED:self.play}
        func = switch_code.get(self.curstate, None)
        if func != None:
            func()                
    
    def key(self, event):  
        if self.key_processing == True: return
        if event.keycode == self.KEY_SPACE:
            self.toggle()
            return                                
        elif event.keycode == self.KEY_LEFT:
            switchcode = {'up':'left', 'left':'down', 'down':'right', 'right':'up'}
        elif event.keycode == self.KEY_RIGHT:
            switchcode = {'up':'right', 'left':'up', 'down':'left', 'right':'down'}
        else: 
            return
        self.key_processing = True
        
        self.snake.head.dir = switchcode.get(self.snake.head.dir)
        self.play()
        
    def tick(self):
        if self.curstate == Display.State.PLAYING:   
            self.refresh()
            if self.job_id != None: self.after_cancel(self.job_id) 
            self.job_id = self.after(self.sleep_time, self.tick)
        else:
            if self.job_id != None: self.after_cancel(self.job_id) 
        
    def crashed(self, msg):
        self.snake.soundNegative()        
        self.showText(msg)
        self.stop()
            
    def refresh(self):
        tile = self.world.getForwardTile(self.snake)        
        if tile.type == 'wall' or tile.type == 'tail' or tile.type == 'out':
            self.crashed('Oops! you met [{}]'.format(tile.type))
        elif tile.type == 'feed':
            self.snake.soundPositive()
            self.snake.moveAndShow(self, tile)
            self.world.removeFeed(self, tile)
            self.world.createFeed(self)           
        elif tile.type == 'space':
            self.snake.moveAndShow(self, tile)
        
        self.key_processing = False