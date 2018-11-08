from ggame import App, Color, LineStyle, Sprite, RectangleAsset, CircleAsset, EllipseAsset, PolygonAsset, ImageAsset, Frame
from math import floor
import random
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
clear = Color(0xffffff, 0.0)
thinline = LineStyle(2, black)
thickline = LineStyle(5, black)
grid=RectangleAsset(30,30,thinline,white)
quadrant=RectangleAsset(450,450,thickline,clear) 
for w in range(0,30):
    for h in range(0,30):
        Sprite(grid, (30*w,30*h))
for w in range(0,2):
    for h in range(0,2):
        Sprite(quadrant, (450*w,450*h))
class Point(Sprite):
    def __init__(self, position, color, equation, depVar):
        super().__init__()
class Line(Sprite):
    def __init__(self):
        super().__init__()
class Graph(App):
    def __init__(self):
        super().__init__()
myapp = Graph()
myapp.run()
