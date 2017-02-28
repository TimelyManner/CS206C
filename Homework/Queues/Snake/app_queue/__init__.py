'''
Created on 2017. 2. 17.

@author: jslee
'''
import os, sys
from sys import platform as _platform 
    
s_dir = os.path.dirname(os.path.abspath(__file__) )
if s_dir not in sys.path:
    sys.path.append(s_dir)

s_dir = s_dir + '\..'
if s_dir not in sys.path:
    sys.path.append(s_dir)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   
os.chdir(ROOT_DIR)
print(ROOT_DIR)

print('The reference program is running under \'{}\' platform, with arguments {}'.format(_platform, sys.argv[1:]) )

