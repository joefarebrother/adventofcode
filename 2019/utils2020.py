#https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
#pylint: disable(import-error)
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from utils import * 