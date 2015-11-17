from drawille import Canvas, getTerminalSize, line
import json
import requests
import sys
import re

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
    if len(sys.argv) < 2:
        r = requests.get('http://ipinfo.io/json')
    else:
        r = requests.get('http://ipinfo.io/{0}/json'.format(sys.argv[1]))

    if not r.ok:
        exit(1)

    response = json.loads(r.text)
    loc = re.match("(.*),(.*)", response['loc'])
    ip_lat = float(loc.group(1))
    ip_lon = float(loc.group(2))
    city = response['city']
    region = response['region']
    country = response['country']
    org = response['org']

    world_map = MapCanvas()
    
    with open('world.json') as f:
        world = json.load(f)
    for shape in world['shapes']:
        for index, point in list(enumerate(shape)):
            lat_a = float(point['lat'])
            lon_a = float(point['lon'])
            lat_b = float(shape[index - 1]['lat'])
            lon_b = float(shape[index - 1]['lon'])
            world_map.plot(lat_a, lon_a)
            world_map.line(lat_a, lon_a, lat_b, lon_b)
    world_map.plot(ip_lat, ip_lon, 'X')
    world_map.canvas.set_text(0, world_map.canvas_height-8, 'Latitude/Longitude: {0},{1}'.format(ip_lat, ip_lon))
    world_map.canvas.set_text(0, world_map.canvas_height-4, '{0}'.format(org))
    world_map.canvas.set_text(0, world_map.canvas_height, '{0}, {1}, {2}'.format(city, region, country))
    print(world_map.canvas.frame())

if __name__ == "__main__":
    main()

