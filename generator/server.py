#!/usr/bin/env python3

import os, sys, time, threading, traceback
from sys import stderr, argv
from pprint import pprint
sys.path.append('.')

from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS

from generator.generate import init_state, next_state

app = Flask(__name__)
CORS(app)

UPDATE_RATE = 2 # Hz

sem = threading.Lock()
sem.acquire()
state = init_state()
sem.release()

def log(*args):
    print(file=stderr, *args)

def update_state(elapsed):
    global state
    sem.acquire()
    state = next_state(state)
    sem.release()

def add_observation(lat, lon, parked1):
    sem.acquire(timeout=1)
    slot = (state.lat == lat) & (state.lon == lon)
    if not any(slot):
        log('ERR invalid lat and lon')
        sem.release()
        return
    i = state[slot][0].index
    T = time.time()
    parked0 = state.loc[i, 'parked']
    state.loc[i, 'last_seen'] = T
    state.loc[i, 'parked'] = parked1
    state.loc[i, 'decay'] = 1 if parked else 0
    if parked0 == False and parked1 == True:
        state.loc[i, 'time_parked'] = T
    sem.release()

def timer():
    threading.Timer(UPDATE_RATE, timer).start()
    update_state(UPDATE_RATE)

@app.route('/map', methods=['GET'])
def map():
    return jsonify(state.to_dict(orient='list'))

@app.route('/geo', methods=['GET'])
def geo():
    data = state.to_dict(orient='list')
    data['coords'] = list(zip(state.lat, state.lon))
    data.pop('lat')
    data.pop('lon')
    return jsonify(data)

@app.route('/observe', methods=['POST'])
def update():
    if any(key not in request.args for key in ['lat', 'lon', 'parked']):
        return make_response('bad parameters', 400)
    lat, lon = float(request.args['lat']), float(request.args['lon'])
    parked = bool(int(request.args['parked']))
    add_observation(lat, lon, parked)
    return make_response('ok', 200)

@app.errorhandler(400)
def bad_request(error):
    return make_response('bad request', 400)

@app.errorhandler(404)
def bad_request(error):
    return make_response('not found', 404)

if __name__ == '__main__':
    program = argv[0]
    if len(argv) < 3:
        log(f'usage: {argv[0]} 0.0.0.0 6060')
        exit(1)

    _, host, port = argv
    timer()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host=host, port=int(port), threaded=True)

