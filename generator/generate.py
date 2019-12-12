import numpy as np
import pandas as pd
import requests as req
import xmltodict
from pprint import pprint
from sys import stderr
from google.protobuf.json_format import MessageToDict
from math import radians, pi
import pygeotile.tile

import generator.proto.vector_tile_pb2

req_codes = req.status_codes._codes


API_KEY = open("generator/.tomtomkey").read().strip()
API_ROOT = "api.tomtom.com"


def latlon2tile(lat, lon, zoom):
    x, y = pygeotile.tile.Tile.for_latitude_longitude(lat, lon, zoom).google
    return int(x), int(y)


def coord2tile(coord, zoom):
    return latlon2tile(coord["lat"], coord["lon"], zoom)


def xml(response):
    return xmltodict.parse(response.text)


def json(response):
    return response.json()


def pbf(Message, response):
    msg = Message()
    msg.ParseFromString(response.content)
    return msg
    # return MessageToDict(msg)


def tomtom_url(path, args):
    url = f"https://{API_ROOT}/{path}"
    arg_str = "&".join([f"{k}={v}" for k, v in args.items()])
    if arg_str:
        url += "?" + arg_str
    return url


def tomtom(path, debug=True, **args):
    args_ = args.copy()
    args_["key"] = API_KEY
    url = tomtom_url(path, args_)
    res = req.get(url)
    url_safe = tomtom_url(path, args)
    if debug:
        print(f"GET {url}", file=stderr)
    if not res:
        code = str(res.status_code)
        if code in req_codes:
            code += f" ({req_codes[code][0]})"
        print(f"ERR {code} -- {url_safe}", file=stderr)
        return None
    return res


def init_state(count=100):
    lat, lon = 52.52343, 13.41144
    X = pd.DataFrame()
    X["lat"] = 0.1 * (np.random.beta(2, 2, size=count) - 0.5) + lat
    X["lon"] = 0.1 * (np.random.beta(2, 2, size=count) - 0.5) + lon
    X["state"] = np.random.randint(2, size=count)
    return X


def next_state(X):
    return X


if __name__ == "__main__":
    # xml(tomtom('search/2/search/berline.xml'))
    # xml(tomtom('parkingprobabilities/v1/nl/amsterdam/probabilities'))
    # xml(tomtom('parkingprobabilities/v1'))
    # xml(tomtom('search/2/additionalData.json', geometries=<geometryIds>[&geometriesZoom=<zoomLevel>]
    # pprint(json(tomtom('search/2/geocode/berlin.xml', countrySet='DE', limit='1')))
    # berlin = json(tomtom('search/2/search/berlin.json', limit=1, countrySet='DE'))
    # pprint(berlin)

    # zoom = 7
    # coord = berlin['results'][0]['position']
    # x, y = coord2tile(coord, zoom)
    # print(coord, x, y)
    # map = tomtom(f'map/1/tile/basic/main/{zoom}/{x}/{y}.pbf')
    # pprint(dir(val))
    # pprint(pbf(proto.vector_tile_pb2.Tile, map))
    # print(init_state())
    print(init_state())
