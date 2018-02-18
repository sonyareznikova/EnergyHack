from dms import DMS
from entities import *
from devices import *


def get_all_sockets(dms:DMS):
    result = []

    for house in dms.village.houses:
        for flat in house.flats:
            result.extend(flat.sockets)
    return result


def create_n_thermal_devices(n, base_title, power, sockets):
    added_devices = 0
    id = 1000
    for socket in sockets:
        if socket.device:
            continue
        device = ThermalDevice("{}_{}".format(base_title, id), power)
        id += 1
        socket.attach_device(device)
        socket.start_by_user()
        added_devices += 1
        if added_devices >= n:
            break
    print("Added {} thermal devices".format(added_devices))


def create_n_non_switchable_devices(n, base_title, power, sockets):
    added_devices = 0
    id = 100
    for socket in sockets:
        if socket.device:
            continue
        device = NonSwitchableDevice("{}_{}".format(base_title, id), power, -1)
        id += 1
        socket.attach_device(device)
        socket.start_by_user()
        added_devices += 1
        if added_devices >= n:
            break
    print("Added {} non switchable devices".format(added_devices))


def create_n_interruptable_devices(n, base_title, power, sockets):
    added_devices = 0
    id = 500
    for socket in sockets:
        if socket.device:
            continue
        device = InterruptibleDevice("{}_{}".format(base_title, id), power)
        id += 1
        socket.attach_device(device)
        socket.start_by_user()
        added_devices += 1
        if added_devices >= n:
            break
    print("Added {} non interruptible devices".format(added_devices))


def create_n_shiftable_devices(n, base_title, power, sockets):
    added_devices = 0
    id = 5000
    for socket in sockets:
        if socket.device:
            continue
        device = ShiftableDevice("{}_{}".format(base_title, id), power, 20)
        id += 1
        socket.attach_device(device)
        socket.start_by_user()
        added_devices += 1
        if added_devices >= n:
            break
    print("Added {} non shiftable devices".format(added_devices))

def create_n_random_devices(n, base_title, power, sockets):
    added_devices = 0
    id = 5000
    for socket in sockets:
        if socket.device:
            continue
        device = NonSwitchableDevice("{}_{}".format(base_title, id), power, 10)
        id += 1
        socket.attach_device(device)
        socket.start_by_user()
        added_devices += 1
        if added_devices >= n:
            break
    print("Added {} non shiftable devices".format(added_devices))

def init_dms():
    dms = DMS(200)
    village = Village(dms)
    dms.village = village
    dms.start()
    sockets = get_all_sockets(dms)

    create_n_thermal_devices(24, "AC", 2, sockets)
    create_n_interruptable_devices(24, "Boiler", 2, sockets)
    create_n_non_switchable_devices(100, "Lamp", 0.5, sockets)
    create_n_shiftable_devices(10, "Washing machine", 2, sockets)

    return dms


