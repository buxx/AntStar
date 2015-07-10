from math import degrees, acos, sqrt

NORTH = 11
NORTH_EST = 12
EST = 15
SOUTH_EST = 18
SOUTH = 17
SOUTH_WEST = 16
WEST = 13
NORTH_WEST = 10

directions = (
    10, 11, 12,
    13,     15,
    16, 17, 18
)

direction_modifiers = {
    10: (-1, -1),
    11: (0, -1),
    12: (1, -1),
    13: (-1, 0),
    15: (1, 0),
    16: (-1, 1),
    17: (0, 1),
    18: (1, 1),
}

directions_degrees = {
    (0, 22.5): 11,
    (22.5, 67): 12,
    (67, 112.5): 15,
    (112.5, 157.5): 18,
    (157.5, 202.5): 17,
    (202.5, 247.5): 16,
    (247.5, 292.5): 13,
    (292.5, 337.5): 10,
    (337.5, 360): 11,
    (337.5, 0): 11
}

slightly = {
    10: (13, 11),
    11: (10, 12),
    12: (11, 15),
    13: (10, 16),
    15: (12, 18),
    16: (13, 17),
    17: (16, 18),
    18: (15, 17),
}


def get_direction_for_degrees(degrees):
    if degrees < 0:
        degrees = 360 - abs(degrees)
    for plage in directions_degrees:
        if plage[0] <= degrees <= plage[1]:
            return directions_degrees[plage]
    raise Exception("Unknow plage for degree \"" + str(degrees) + '"')


def get_position_with_direction_decal(direction, point):
    x, y = point
    directions_modifier = direction_modifiers[direction]
    return x + directions_modifier[0], y + directions_modifier[1]


def get_degree_from_north(a, b):
    if a == b:
        return 0

    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    Dx, Dy = ax, ay-1
    ab = sqrt((bx-ax)**2 + (by-ay)**2)
    aD = sqrt((Dx-ax)**2 + (Dy-ay)**2)
    Db = sqrt((bx-Dx)**2 + (by-Dy)**2)

    degs = degrees(acos( ( ab**2 + aD**2 - Db**2 ) / ( 2 * ab * aD ) ))
    if bx < ax:
        return 360 - degs
    return degs
