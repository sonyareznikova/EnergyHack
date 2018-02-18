from dms import DMS


def get_all_sockets(dms:DMS):
    result = []

    for house in dms.village.houses:
        for flat in house.flats:
            result.append(flat.sockets)
    return result


def create_n_thermal_devices(n, base_title, power, dms):
    pass

def create_n_non_switchable_devices(n, base_title, power, dms):
    pass

def create_n_interruptable_devices(n, base_title, power, dms):
    pass

def create_n_shiftable_devices(n, base_title, power, dms):
    pass