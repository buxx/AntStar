from antstar.geometry import get_position_with_direction_decal, distance_from_points


class AntFeeler:

    def __init__(self, host, grid, feel_distance=1):
        self._host = host
        self._grid = grid
        self._feel_distance = feel_distance

    def direction_is_free(self, direction):
        position = self._host.get_position()
        will_position = get_position_with_direction_decal(direction, position)
        return self._grid.is_free(will_position)

    def position_is_free(self, position):
        if distance_from_points(position, self._host.get_position()) > self._feel_distance:
            raise Exception("Can't feel so far")
        return self._grid.is_free(position)
