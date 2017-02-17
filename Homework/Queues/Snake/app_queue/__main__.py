'''
Created on 2017. 2. 17.

@author: jslee
'''
import os, sys 
    
if __name__ == '__main__':
    s_dir = os.path.dirname(os.path.abspath(__file__))  + '/..'
    sys.path.append(s_dir)
    print(sys.path)
    import app_queue