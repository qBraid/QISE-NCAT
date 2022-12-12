"""
The colors module is a simple module written to help
students understand how python modules work. It contains
the following:

colors: a list of standard colors
get_random_color: a function to select a random color from
    the list of standard colors
ColorScheme: a class that for holding functionality related to color schemes


This particular part of the module is called the doc string.
"""


import random


colors = ['red','orange','yellow','green','blue', 'violet', 'black', 'grey','white']

def get_random_color():
    
    """Return a random color from the list of standard colors."""
    
    return random.choice(colors)


class ColorScheme:
    
    """ColorScheme: class for functionality related to color schemes
    
    
    Args:
        name: name of color scheme
        color_list: list of colors in the scheme
    
    Attrs:
        name: name of color scheme
        _colors: list of colors
        
    Methods:
        colors: return the list of colors in the scheme
        add_color: add color to color scheme
        remove_color: remove color from color scheme
        get_random_color: get random color from color scheme"""
    
    def __init__(self, name, color_list):
        
        self.name = name
        self._colors = color_list
        
    def colors(self):
        return self._colors
    
    def add_color(self, new_color):
        self._colors.append(new_color)
        
    def remove_color(self, color_to_remove):
        if color_to_remove not in self._colors:
            print('Color not in color list.')
        else:
            self._colors.remove(color_to_remove)
        
    def get_random_color(self):
        return random.choice(self._colors)
    
    def _private_method_(self):
        pass
    
    def _private_method2_(self):
        pass