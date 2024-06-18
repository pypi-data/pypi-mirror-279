from .. import basic_features
from . import html
import os

class graph():

    def __init__(self, labels:list, data:dict, name:str = 'myChart', type ='line'):
        basic_features.if_directory_not_exists('html')
        self.labels = labels
        self.data = data
        self.name = name
        self.type = type

    def basic_view(self, width_height = (100, 100), title ='Chart.js Line Chart'):
        script1, html_script, script2 = html.charts.full_build(self.labels, self.data, self.name, width_height, title, self.type)
        basic_html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title>{script1}</head><body>{html_script}{script2}</body></html>'''
        path = basic_features.get_current_directory()
        path = os.path.join(path, 'html', 'view.html')
        with open(path, 'w') as file:
            file.write(basic_html)
        basic_features.open_browser_with_url(path)
