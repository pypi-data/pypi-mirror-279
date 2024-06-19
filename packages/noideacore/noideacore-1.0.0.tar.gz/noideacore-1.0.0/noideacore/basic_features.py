import os
from pathlib import Path
import webbrowser

def get_current_directory():
    return Path.cwd()

def get_current_file_name():
    return os.path.basename(__file__)

def path_join(path1, path2):
    return os.path.join(path1, path2)

def open_browser_with_url(url:str):
    webbrowser.open(url)

def if_directory_not_exists(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def string_in_list(string:str):
    List = string.split(', ')
    List[0] = List[0][List[0].find('[')+1:]
    List[-1] = List[-1][:List[-1].find(']')]
    return List