from drawille import Canvas, getTerminalSize, line
import json
import requests


class MapCanvas(object):
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

    def line(self, lat1, lon1, lat2, lon2):
        x1 = self.get_x(lon1)
        x2 = self.get_x(lon2)
        y1 = self.get_y(lat1)
        y2 = self.get_y(lat2)
        for x,y in line(x1, y1, x2, y2):
            self.canvas.set(x,y)

def main():
    world_map = MapCanvas()
    
    with open('world.json') as f:
        world = json.load(f)
    for shape in world['shapes']:
        for index, point in list(enumerate(shape)):
            lat1 = float(point['lat'])
            lon1 = float(point['lon'])
            lat2 = float(shape[index - 1]['lat'])
            lon2 = float(shape[index - 1]['lon'])
            world_map.plot(lat1, lon1)
            world_map.line(lat1, lon1, lat2, lon2)
    print(world_map.canvas.frame())

if __name__ == "__main__":
    main()

