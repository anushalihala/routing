import geopy.distance

def get_distance(pos1, pos2):
    return geopy.distance.distance(pos1, pos2).m