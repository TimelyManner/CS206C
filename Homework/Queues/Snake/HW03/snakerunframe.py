'''
Created on 2017. 2. 12.

@author: jslee
'''
from tkinter import * 
from enum import *
from sys import platform as _platform

class Display(Frame): 
    
    if _platform == 'win32':        # For setting different key codes for operation systems
        KEY_LEFT=37
        KEY_RIGHT=39
        KEY_SPACE=32
    elif _platform == 'darwin':
        KEY_LEFT=8124162
        KEY_RIGHT=8189699
        KEY_SPACE=3211296
    else:
        pass     
     
    class State(Enum):  # To define all states that the Tkinter's frame is supposed to reach
        INIT=0
        PLAYING=1
        STOPPED=2
        GAMEOVER=3
        
    class Tile: # To define a graphical tile used in Tkinter's canvas
        def __init__(self, type, shape_id=None, x=-1, y=-1):
            self.type = type
            self.shape_id = shape_id
            self.x = x
            self.y = y
                      
    def __init__(self, world=None, snake=None):
        if world != None and snake != None:
            self.__task = []
            self.__task.append(self._refresh)
            self.snake = snake
            self.world = world
            self.map_grain_size = world.map.grain_size
            self.map_width = world.map.width
            self.map_height = world.map.height
            self.map_bg = world.map.bg
            self.__sleep_time = world.map.sleep_time
            
            root = Tk()
            root.resizable(0,0)             # To prevent the whole window size from being changed   
            Frame.__init__(self, root)   
            self.config(bg='black')    
            self.grid()                   
            self._create_widgets()    
            self._to_init()
            
            self.world.create_feed(self)            
            self.snake.make_move(self, Display.Tile(world.Cell.SPACE))         
            self.__job_id = None

            for d in world.map.tiles:
                if world.map.tiles[d].type == world.Cell.WALL:
                    x = world.map.tiles[d].x
                    y = world.map.tiles[d].y
                    world.map.tiles[d].shape_id = self.main_canvas.create_rectangle(x*world.map.grain_size,
                                                     y*world.map.grain_size, 
                                                     (x+1)*world.map.grain_size, 
                                                     (y+1)*world.map.grain_size, fill = world.map.wall_color)
                    
            self.focus_set()
            self.__key_processing = False
            
        else:
            _quit()                
    
    def _play(self):    
        if self.__cur_state != Display.State.PLAYING:
            self._to_play()
    
    def _stop(self):    
        if self.__cur_state != Display.State.STOPPED:
            self._to_stop()
    
    def _to_init(self): # To set the frame state to "INIT"
        self.__cur_state=Display.State.INIT
    
    def _to_play(self): # To set the frame state to "PLAY"
        self.__cur_state=Display.State.PLAYING
        self.__play_button.config(state=DISABLED) 
        self.__stop_button.config(state=NORMAL)
        self._tick()

    def _to_stop(self): # To set the frame state to "STOPPED"
        self.after_cancel(self.__job_id)        
        
        self.__cur_state=Display.State.STOPPED
        self.__play_button.config(state=NORMAL)
        self.__play_button.config(text='Play')
        self.__stop_button.config(state=DISABLED)

    def _to_game_over(self):    # To set the frame state to "GAMEOVER"
        self.__cur_state=Display.State.GAMEOVER
        self.__play_button.config(state=NORMAL)
        self.__play_button.config(text='Play')
        self.__stop_button.config(state=DISABLED)
        self.show_text('Game over...') 
            
    def _quit(self):
        self.show_text('Good bye~')
        _quit()
        
    def _create_widgets(self):  # To create all necessary widgets on the frame window
        self.main_canvas = Canvas(self, bg=self.map_bg,
            width=(self.map_width*self.map_grain_size), 
            height=(self.map_height*self.map_grain_size))           
        self.__logo = PhotoImage(file='kaist_logo.gif')
        self.__logo_label = Label(self, image=self.__logo)  
        self.__play_button = Button(self, text='Play',
            command=self._play)            
        self.__stop_button = Button(self, text='Stop',
            command=self._stop, state=DISABLED)            
        self.__quit_button = Button(self, text='Quit',
            command=self.quit)            
        self.__scrollbar=Scrollbar(self)
        self.__text = Text(self, yscrollcommand=self.__scrollbar.set, width=20,
                         bg='green', fg='white')
        self.__scrollbar.config(command=self.__text.yview)
        
        self.main_canvas.grid(row=0, column=0, rowspan=20, columnspan=20, sticky=N+W+S+E)
        self.__logo_label.grid(row=0, column=20, columnspan=1, sticky=N+W+S+E)         
        self.__play_button.grid(row=1, column=20, columnspan=1, sticky=N+W+S+E)      
        self.__stop_button.grid(row=2, column=20, columnspan=1, sticky=N+W+S+E)    
        self.__quit_button.grid(row=3, column=20, columnspan=1, sticky=N+W+S+E)

        self.bind('<Key>', self._key)   # To find key events with the function _key             
        
    def show_text(self, text_new):
        print(text_new)
        
    def _toggle(self):  # To make the frame state toggled between PLAY and STOPPED
        switch_code = {Display.State.PLAYING:self.stop, Display.State.STOPPED:self.play}
        func = switch_code.get(self.curstate, None)
        if func != None:
            func()                
    
    def _key(self, event):  # To handle key events  
        if self.__key_processing == True: return
        if event.keycode == self.KEY_SPACE:
            self._toggle()
            return                                
        elif event.keycode == self.KEY_LEFT:
            switchcode = {'up':'left', 'left':'down', 'down':'right', 'right':'up'}
        elif event.keycode == self.KEY_RIGHT:
            switchcode = {'up':'right', 'left':'up', 'down':'left', 'right':'down'}
        else: 
            return
        self.__key_processing = True
        
        self.snake._head.dir = switchcode.get(self.snake._head.dir)
        self._play()
        
    def _tick(self):    # To handle time-periodic task
        if self.__cur_state == Display.State.PLAYING:
            if self.__job_id != None: self.after_cancel(self.__job_id)
               
            for task in self.__task:    # execute each function registered as a task
                task()

            self.__key_processing = False                     # To make key processing synchronized at any time             
            self.__job_id = self.after(self.__sleep_time, self._tick)
        else:
            if self.__job_id != None: self.after_cancel(self.__job_id) 
        
    def _crashed(self, msg):    # To handle crashed cases of the snake
        self.snake.make_sound('negative')        
        self.show_text(msg)
        self._stop()
            
    def _refresh(self):         # To properly handle in search of what exists right ahead of the snake 
        type,shape_id,x,y = self.world.get_tile_ahead(self.snake)    # To get a tile object right ahead of the snake
        tile = Display.Tile(type, shape_id, x, y)        
        if tile.type == self.world.Cell.FEED:
            self.snake.make_sound('positive')
            self.snake.make_move(self, tile)
            self.world.remove_feed(self, tile)
            self.world.create_feed(self)           
        elif tile.type == self.world.Cell.SPACE:
            self.snake.make_move(self, tile)
        elif tile.type in { self.world.Cell.OUT, self.world.Cell.WALL, self.world.Cell.OBJECT }:
            msg = {self.world.Cell.OUT:'out', self.world.Cell.WALL:'wall',  self.world.Cell.OBJECT:'object'}
            self._crashed('Your snake has crashed into: ' + str(msg[tile.type]))