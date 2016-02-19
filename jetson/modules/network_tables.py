from functools import partial

from networktables import NetworkTable
from networktables.util import ChooserControl

import config


class NetworkTablesConnectionListener(object):

    def __init__(self, cb):
        self.callback = cb

    def connected(self, table):
        self.callback(True, table)

    def disconnected(self, table):
        self.callback(False, table)


class NetworkTables(object):

    TYPES = {
        'str': 'string',
        'int': 'number',
        'float': 'number',
        'bool': 'boolean'
    }

    def __init__(self):
        self.socketio = None
        self.value_cache = {
            'connected_to_robot': False,
            'targeting_enabled': False
        }

        NetworkTable.setIPAddress(config.ROBOT_IP_ADDRESS)
        NetworkTable.setClientMode()
        NetworkTable.initialize()

        self.sd = NetworkTable.getTable('SmartDashboard')
        self.sd.addTableListener(self.on_value_changed, immediateNotify=True)

        self.c_listener = NetworkTablesConnectionListener(
            self.on_connection_changed)
        self.sd.addConnectionListener(self.c_listener, True)

    def set_choosers(self, choosers):
        for c in choosers:
            ChooserControl(
                c,
                on_choices=partial(self.on_chooser_choices, c),
                on_selected=partial(self.on_chooser_selected, c)
            )

    def make_formatted_type(self, t, default='string'):
        return self.TYPES.get(str(t), default).capitalize()

    def on_chooser_choices(self, key, choices):
        # print 'choices', key, choices
        self.on_value_changed(self.sd, '/'.join([key, 'options']), choices)

    def on_chooser_selected(self, key, selected):
        # print 'selected', key, selected
        self.on_value_changed(self.sd, '/'.join([key, 'selected']), selected)

    def on_value_changed(self, table, key, value, is_new=False):
        # print 'value changed!!!', table, key, value
        self.emit({
            key: value
        })

    def on_connection_changed(self, is_connected, table):
        # print 'connection changed', is_connected, table
        self.emit({
            'connected_to_robot': is_connected
        })
        # if is_connected:
        #     self.sd.removeTableListener(self.on_value_changed)
        #     self.sd.removeTableListener(self.on_subtable_value_changed)
        #     self.sd.addTableListener(self.on_value_changed)
        #     self.sd.addSubTableListener(self.on_subtable_value_changed)

        # for key in table.entryStore.keys():
        #     self.on_value_changed(table, key, table.getValue(key), True)

    def put_value(self, key, value, valueType='object'):
        formattedType = self.make_formatted_type(type(value), valueType)
        # print formattedType
        # print key, value, formattedType
        if formattedType.lower() != 'object':
            getattr(self.sd, 'put' + formattedType)(key, value)
            return

        # For objects, serialize into "--" objects
        for subkey, subvalue in value.iteritems():
            getattr(self.sd, 'put' + self.make_formatted_type(
                type(subvalue)))(key + '--' + subkey, subvalue)

    def get_value(self, key):
        return self.sd.getValue(key, defaultValue=self.value_cache.get(key,
                                                                       None))

    def get_all_values(self):
        return self.value_cache

    def set_socketio(self, socketio):
        self.socketio = socketio

    def emit(self, data):
        # print 'emit', data
        self.value_cache.update(data)
        if self.socketio:
            self.socketio.emit('network_tables_update', data)
