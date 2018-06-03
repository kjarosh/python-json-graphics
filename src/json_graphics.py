'''
@author: Kamil Jarosz
'''

from PIL import Image, ImageDraw
import json
import re


class InvalidFormatError(Exception):
    pass


class Drawable:

    def draw(self, draw):
        raise NotImplementedError()


class Point(Drawable):

    def __init__(self, color, x, y):
        self._color = color
        self._xy = [(x, y)]
    
    def draw(self, draw):
        draw.point(self._xy, self._color)
    
    @staticmethod
    def parse(color, data):
        return Point(color, data['x'], data['y'])


class Rectangle(Drawable):

    def __init__(self, color, x, y, width, height):
        self._color = color
        self._xy = [x, y, x + width, y + height]
    
    def draw(self, draw):
        draw.rectangle(self._xy, self._color)

    @staticmethod
    def parse(color, data):
        return Rectangle(color, data['x'], data['y'], data['width'], data['height'])


class Square:

    @staticmethod
    def parse(color, data):
        return Rectangle(color, data['x'], data['y'], data['size'], data['size'])


class Polygon(Drawable):
    
    def __init__(self, color, points):
        self._color = color
        self._xy = points
    
    def draw(self, draw):
        draw.polygon(self._xy, self._color)
    
    @staticmethod
    def parse(color, data):
        return Polygon(color, [(x, y) for [x, y] in data['points']])


class Ellipse(Drawable):
    
    def __init__(self, color, x, y, ra, rb):
        self._color = color
        self._xy = [(x - ra, y - rb), (x + ra, y + rb)]
    
    def draw(self, draw):
        draw.ellipse(self._xy, self._color)
    
    @staticmethod
    def parse(color, data):
        return Ellipse(color, data['x'], data['y'], data['radiusx'], data['radiusy'])


class Circle:
    
    @staticmethod
    def parse(color, data):
        return Ellipse(color, data['x'], data['y'], data['radius'], data['radius'])


class GraphicsFile(Drawable):
    figures = {
        'point': Point,
        'rectangle': Rectangle,
        'square': Square,
        'polygon': Polygon,
        'circle': Circle,
        'ellipse': Ellipse
    }
    
    re_color_html = re.compile('^#[0-9A-Za-z]{6}$')
    _rgb_val = '(\\d{1,2}|2[0-4][0-9]|25[0-5])'
    re_color_rgb = re.compile('^\\(' + _rgb_val + ',' + _rgb_val + ',' + _rgb_val + '\\)$')
    
    def __init__(self, data):
        self._palette = data['palette']
        self._screen = data['screen']
        self._figures = [self.__parsefig(fig) for fig in data['figures']]
    
    def __parsefig(self, data):
        figtype = data['type']
        
        if not figtype in self.figures:
            raise InvalidFormatError('Unsupported figure type: ' + figtype)
        
        if 'color' in data:
            color = data['color']
        else:
            if not 'default_color' in self._screen:
                raise InvalidFormatError(
                    'Figure with no color specified; no default color found')
            
            color = self._screen['default_color']
        color = self.__parsecolor(color)
        
        return self.figures[figtype].parse(color, data)
    
    def __parsecolor(self, color):
        if self.re_color_html.match(color):
            return color
        
        if self.re_color_rgb.match(color):
            return 'rgb' + color
        
        if not color in self._palette:
            raise InvalidFormatError('Unsupported color format: ' + color)
        
        return self._palette[color]
    
    def to_image(self):
        screen_size = (self._screen['width'], self._screen['height'])
        
        img = Image.new('RGB', screen_size, self._screen['background'])
        draw = ImageDraw.Draw(img)
        
        for f in self._figures:
            f.draw(draw)
        
        del draw
        
        return img
    
    @staticmethod
    def from_file(filename):
        with open(filename) as opened:
            data = json.load(opened)
        
        return GraphicsFile(data)
    
    @staticmethod
    def from_str(string):
        data = json.loads(string)
        return GraphicsFile(data)

