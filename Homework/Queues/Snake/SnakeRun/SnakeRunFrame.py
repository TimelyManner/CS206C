'''
Created on 2017. 2. 12.

@author: jslee
'''

from tkinter import * 
from enum import Enum
from snakerun import snake

class Display(Frame):  
    WIDTH, HEIGHT=50,50   # constants
    GRAIN_SIZE=10            # constants
        
    class State(Enum):
        INIT=0
        PLAYING=1
        STOPPED=2
        GAMEOVER=3
                      
    def __init__(self, master=None):
        root = Tk()
        root.resizable(0,0)   
        Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()    
        self.curstate=Display.State.INIT
                 
    def Play(self):
        if self.curstate != Display.State.PLAYING:
            self.toPlay()
    
    def toPlay(self):
        self.curstate=Display.State.PLAYING
        self.playButton.config(state=DISABLED) 
        self.stopButton.config(state=NORMAL)
        self.showText('Playing...')
        self.draw()          
    
    def stop(self):
        if self.curstate == Display.State.PLAYING:
            self.toStop()

    def toStop(self):
        self.curstate=Display.State.STOPPED
        self.playButton.config(state=NORMAL)
        self.playButton.config(text='Play')
        self.stopButton.config(state=DISABLED)
        self.showText('Stopped...')

    def toGaveOver(self):
        self.curstate=Display.State.GAMEOVER
        self.playButton.config(state=NORMAL)
        self.playButton.config(text='Play')
        self.stopButton.config(state=DISABLED)
        self.showText('Game over...') 
            
    def quit(self):
        print('Good bye~')
        quit()
        
    def createWidgets(self):
        self.headLabel = Label(self)
        self.mainCanvas = Canvas(self, bg='blue',
            width=(Display.WIDTH*Display.GRAIN_SIZE), 
            height=(Display.HEIGHT*Display.GRAIN_SIZE))            
        self.logo = PhotoImage(file='kaist_logo.gif')
        self.logoLabel = Label(self, image=self.logo)  
        self.playButton = Button(self, text='Play',
            command=self.Play)            
        self.stopButton = Button(self, text='Stop',
            command=self.stop, state=DISABLED)            
        self.quitButton = Button(self, text='Quit',
            command=self.quit)            
        self.scrollbar=Scrollbar(self)
        self.text = Text(self, yscrollcommand=self.scrollbar.set, width=20,
                         bg='green', fg='white')
        self.scrollbar.config(command=self.text.yview)
        
        self.headLabel.grid(row=0, column=0, rowspan=1, columnspan=23, sticky=N+W+S+E)
        self.mainCanvas.grid(row=1, column=0, rowspan=20, columnspan=20, sticky=N+W+S+E)
        self.logoLabel.grid(row=1, column=20, columnspan=1, rowspan=3, sticky=N+W+S+E)         
        self.playButton.grid(row=1, column=21, columnspan=3, sticky=N+W+S+E)      
        self.stopButton.grid(row=2, column=21, columnspan=3,sticky=N+W+S+E)    
        self.quitButton.grid(row=3, column=21, columnspan=3,sticky=N+W+S+E)
        self.text.grid(row=4, column=20, rowspan=23, columnspan=3, sticky=N+W+S+E)
        self.scrollbar.grid(row=4, column=24, rowspan=23, columnspan=1, sticky=N+W+S+E)
        
        self.rect_list = list()
        self.rect_pos = list()
        self.rect_id = self.mainCanvas.create_rectangle(0, 0, Display.GRAIN_SIZE, Display.GRAIN_SIZE, fill='yellow')
        
        class Pos:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        self.rect_list.append(self.rect_id)   
        self.rect_pos.append( Pos(0,0) )      

        self.showText('Ready...')
        
    def showText(self, text_new):
        self.text.insert(END, text_new)
        
    def draw(self):
        self.mainCanvas.move(self.rect_list[0], Display.GRAIN_SIZE, 0)           