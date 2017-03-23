'''
Created on 2017. 3. 23.

@author: Lee
'''
import os, sys
from sys import platform as _platform 
   
def init_env():  
    s_dir = os.path.dirname(os.path.abspath(__file__) )
    if s_dir not in sys.path:
        sys.path.append(s_dir)  # To add the current directory to PYTHONPATH
     
    s_dir = s_dir + '\..'
    if s_dir not in sys.path:
        sys.path.append(s_dir)  # To add the project-root directory to PYTHONPATH
     
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   
    os.chdir(ROOT_DIR)          # To change current directory to the root of "app_queue" package, 
                                # so that it is allowed to open file resources (icon, map, etc.) with relative paths
    
    print('The reference program is running under \'{}\' platform, with arguments {}'.format(_platform, sys.argv[1:]) )