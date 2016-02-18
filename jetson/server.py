import sys
import time
import base64
import logging

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

from gevent import monkey, Greenlet


import config
from modules.driver_vision import DriverVision
from modules.targeting import Targeting
from modules.network_tables import NetworkTables
from modules import cv2_polyfill

monkey.patch_all()
cv2_polyfill.polyfill()

app = Flask(__name__)
socketio = SocketIO(app)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)
logging.getLogger('nt').addHandler(stream_handler)

jetson_targeting = Targeting()
jetson_driver_vision = DriverVision(targeting=jetson_targeting)

jetson_network_tables = NetworkTables()
jetson_network_tables.set_socketio(socketio)
jetson_network_tables.set_choosers([
    config.NT_AUTONOMOUS_COMMAND_SELECTOR,
    config.NT_DRIVER_DIRECTION_SELECTOR
])


# --
# DRIVER-STATION-FACING ROUTES
# --


@app.route('/')
def home():
    """Request the main dashboard screen for driver station"""
    return render_template('index.html',
                           width=config.DRIVER_CAMERA_WIDTH,
                           height=config.DRIVER_CAMERA_HEIGHT
                           )


@socketio.on('request_network_tables')
def request_network_tables():
    """Request a full update of the network tables"""
    data = jetson_network_tables.get_all_values()
    emit('network_tables_update', data)


@socketio.on('edit_network_tables')
def edit_network_tables(data):
    """Edits network tables value based on websocket request"""
    jetson_network_tables.put_value(data['key'], data['value'], data['type'])


# @socketio.on('connect')
# def on_connect():
#     print 'connect'
#     jetson_network_tables.put_value('dashboard_connected', True)


# @socketio.on('disconnect')
# def on_disconnect():
#     print 'disconnect'
#     jetson_network_tables.put_value('dashboard_connected', False)

# --
# CONTINUALLY-RUNNING FUNCTIONS
# --


def request_targeting():
    match = jetson_targeting.find_target()
    if match:
        jetson_network_tables.put_value('target_found', True, 'boolean')
        jetson_network_tables.put_value('target_details', match, 'object')
    else:
        jetson_network_tables.put_value('target_found', False, 'boolean')

    continually_request_targeting()


def continually_request_targeting():
    if jetson_network_tables.get_value('targeting_enabled') or \
        jetson_network_tables.get_value(config.NT_DRIVER_DIRECTION_SELECTOR +
                                        '/selected') == 'shooting':
        # print 'Targeting enabled, running'
        g = Greenlet(request_targeting)
        g.start_later(config.TARGETING_INTERVAL)
    else:
        # print 'Targeting not enabled, rechecking'
        g = Greenlet(continually_request_targeting)
        g.start_later(config.TARGETING_RETRY_INTERVAL)


def request_driver_vision():
    selected_camera = jetson_network_tables.get_value(
        config.NT_DRIVER_DIRECTION_SELECTOR + '/selected')

    # print selected_camera
    jpeg = jetson_driver_vision.get_current_frame(camera=selected_camera,
                                                  make_jpeg=True)
    socketio.emit('driver_vision', {
        'raw': 'data:image/jpeg;base64,' + base64.b64encode(jpeg),
        'timestamp': time.time()
    })

    continually_request_driver_vision()


def continually_request_driver_vision():
    if True or jetson_network_tables.get_value('dashboard_connected'):
        # print 'Driver vision enabled, running'
        g = Greenlet(request_driver_vision)
        g.start_later(config.DRIVER_STREAM_INTERVAL)
    else:
        # print 'Driver vision not enabled, rechecking'
        g = Greenlet(continually_request_driver_vision)
        g.start_later(config.DRIVER_STREAM_RETRY_INTERVAL)


if __name__ == '__main__':
    continually_request_targeting()
    continually_request_driver_vision()

    # Allow custom port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = config.PORT

    socketio.run(app, host=config.HOST, port=port)
