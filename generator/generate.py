from sys import stderr, path
path.append('.')
import time
import numpy as np
import pandas as pd
import requests as req
import xmltodict
from pprint import pprint
from google.protobuf.json_format import MessageToDict
from math import radians, pi
from numpy.random import beta, randint, uniform
import pygeotile.tile

import generator.proto.vector_tile_pb2

REQ_CODES = req.status_codes._codes
API_KEY_PATH = "generator/.tomtomkey"
API_KEY = open(API_KEY_PATH).read().strip()
API_ROOT = "api.tomtom.com"

DECAY_PERIOD = 15*1_000 # seconds
DECAY_PERIOD /= 5
DECAY_LIMIT = 0.25

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
        print(f"GET {url_safe}", file=stderr)
    if not res:
        code = str(res.status_code)
        if code in REQ_CODES:
            code += f" ({REQ_CODES[code][0]})"
        print(f"ERR {code} -- {url_safe}", file=stderr)
        return None
    return res


COLS = []
def init_state():
    lat, lon = 52.52343, 13.41144 # berlin
    X = pd.read_csv('res/berlin-parking.csv', index_col=0)
    N = len(X)
    #X["lat"] = 0.3 * (beta(3, 3, size=N) - 0.5) + lat
    #X["lon"] = 0.6 * (beta(3, 3, size=N) - 0.5) + lon
    X["decay"] = beta(3, 2, size=N)
    X.loc[X.decay < DECAY_LIMIT, 'decay'] = 0
    X["parked"] = X.decay >= DECAY_LIMIT
    X["last_seen"] = time.time()
    X["time_parked"] = 0
    # cheats
    global COLS
    COLS = ['parked', 'decay', 'last_seen', 'time_parked']
    COLS = [X.columns.get_loc(c) for c in COLS if c in X]
    return X


def next_state(X):
    # advance decay of parked cars to t
    parked = X.parked == True
    t = time.time() - X.loc[parked, 'time_parked']
    X.loc[parked, 'decay'] = np.e**(-t/DECAY_PERIOD)
    # mark timed out slots as free
    timeout = X.decay < DECAY_LIMIT
    X.loc[timeout, ['decay', 'parked', 'time_parked']] = 0
    X.loc[timeout, 'parked'] = False
    # park random cars
    R = X[X.parked == False].sample(frac=0.05) # amount of cars
    chances = uniform(0, 1, len(R))
    R = R[chances <= 0.3] # probability of parking
    X = did_park(X, R.index)
    return X


def did_park(X, indices):
    t = time.time()
    X.iloc[indices, COLS] = (True, 1, t, t)
    return X


if __name__ == "__main__":
    S = init_state()
    S.to_csv('res/parking.csv')

