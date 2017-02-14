'''
Created on 2017. 2. 12.

@author: jslee
'''
class World:
    class Tile:
        SPACE=0
        FEED=1
        WALL=2            
    
    def __init__(self, file):
        self.map= self.loadMap('map1.txt')
        
    def loadMap(self, file_name):
        pass
      