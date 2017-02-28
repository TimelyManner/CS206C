'''
Created on 2017. 2. 28.

@author: Lee
'''
import os, sys
    
s_dir = os.path.dirname(os.path.abspath(__file__))
if s_dir not in sys.path:
    sys.path.append(s_dir)