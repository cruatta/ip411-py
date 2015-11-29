import json
import re
import sys
import os

import requests
from drawille import Canvas, getTerminalSize, line

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

class WorldMap(MapCanvas):
    def __init__(self):
        super(WorldMap, self).__init__()

        with open(os.path.join(sys.prefix, 'lib', 'ip411', 'world.json'), ) as f:
            world = json.load(f)
        for shape in world['shapes']:
            for index, point in list(enumerate(shape)):
                lat_a = float(point['lat'])
                lon_a = float(point['lon'])
                lat_b = float(shape[index - 1]['lat'])
                lon_b = float(shape[index - 1]['lon'])
                self.plot(lat_a, lon_a)
                self.line(lat_a, lon_a, lat_b, lon_b)

def ip_info(ip=None):

    if ip is None:
        r = requests.get('http://ipinfo.io/json')
    else:
        r = requests.get('http://ipinfo.io/{0}/json'.format(sys.argv[1]))

    if not r.ok:
        raise Exception('Invalid Response from ipinfo.io')

    response = json.loads(r.text)

    try:
        assert 'loc' in response
    except AssertionError as e:
        raise Exception('Response from ipinfo.io contains no loc')

    loc = re.match("(.*),(.*)", response['loc'])
    lat = float(loc.group(1))
    lon = float(loc.group(2))
    response['lat'] = lat
    response['lon'] = lon

    return response
