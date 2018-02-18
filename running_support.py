from dms import DMS


def get_all_sockets(dms:DMS):
    result = []

    for house in dms.village.houses:
        for flat in house.flats:
            result.append(flat.sockets)
    return result
