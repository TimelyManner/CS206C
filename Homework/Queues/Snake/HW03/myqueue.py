'''
Created on 2017. 2. 17.

@author: jslee
'''

from collections import deque

class MyQueue(deque):
# class MyQueue(list):
    def __init__(self):        
        deque.__init__(self)        
#         list.__init__(self)

#     def append(self, o):
#         pass
#      
#     def popleft(self):
#         pass

#     def is_empty(self):
#         pass
#     
#     def is_full(self):
#         pass
#     
#     def len(self):     
    