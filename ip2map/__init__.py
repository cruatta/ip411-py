from drawille import Canvas, getTerminalSize
import json
import requests

from pprint import pprint

class MapCanvas():
    def __init__(self):
        self.canvas = Canvas()
        w, h = getTerminalSize()

        self.canvas_width = w * 2 - 1
        self.canvas_height = h * 4 - 5

    def get_x(self, longitude): 
        adjusted_lon = longitude + 180 

        if adjusted_lon == 0: 
            return 0
        elif adjusted_lon > 360:
            return self.canvas_width
        else:
            return adjusted_lon * self.canvas_width / 360

    def get_y(self, latitude):
        adjusted_lat = latitude + 90
        # print(adjusted_lat)

        if adjusted_lat == 0:
            return self.canvas_height
        elif adjusted_lat > 180: 
            return 0
        else:  
            return self.canvas_height - adjusted_lat * self.canvas_height / 180

    def plot(self, latitude, longitude, char=None):
        x = self.get_x(longitude)
        y = self.get_y(latitude)

        if char is None:
            self.canvas.set(x, y)
        else:
            self.canvas.set_text(x, y, char)

# Be lazy
def main():
    map = MapCanvas()
    map.canvas.set_text(map.canvas_width, map.canvas_height, 'x')
    
    with open('world.json') as f:
        world = json.load(f)
    for shape in world['shapes']:
        for point in shape:
            lat = float(point['lat'])
            lon = float(point['lon'])
            map.plot(lat, lon)
    print(map.canvas.frame())

if __name__ == "__main__":
    main()

