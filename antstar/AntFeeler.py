from antstar.geometry import get_position_with_direction_decal


class AntFeeler:

    def __init__(self, host, grid):
        self._host = host
        self._grid = grid

    def direction_is_free(self, direction):
        position = self._host.get_position()
        will_position = get_position_with_direction_decal(direction, position)
        return self._grid.is_free(will_position)
