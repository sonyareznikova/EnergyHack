from flask import Flask, render_template, jsonify
from running_support import *
from dms import *

app = Flask(__name__)

# initialise DMS
current_dms = init_dms()


@app.route('/')
def start():
    return render_template('dashboard.html', number_of_houses = len(current_dms.village.houses), number_of_flats = 999, number_of_sockets = 5)

@app.route('/data')
def data():
    # power history list
    current_overall_power = current_dms.get_power_history()
    # get max_power
    max_power = [current_dms.max_power] * 27
    devices_stats = current_dms.get_device_stats()
    return jsonify({'results': current_overall_power, 'max_power': max_power, 'inter': devices_stats['interruptible devices'], 'therm': devices_stats['thermal devices'], 'shift': devices_stats["shiftable devices"], 'nonswitch':devices_stats["non-switchable devices"]})