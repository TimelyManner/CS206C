'''
Created on 2017. 2. 17.

@author: jslee
'''

from collections import deque

class MyQueue(deque):
    '''
    classdocs
    '''

    def __init__(self):
        deque.__init__(self)
        '''
        Constructor
        '''
#     def append(self, param):
#         pass
#     
#     def popleft(self):
#         pass