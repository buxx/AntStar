from antstar.geometry import get_degree_from_north, get_direction_for_degrees


class AntBrain:

    def __init__(self, host, start_position, end_position):
        self._host = host
        self._home_vector = (-(start_position[0] - end_position[0]), -(start_position[1] - end_position[1]))
        self._end_position = end_position
        self._memory_since_blocked = []
        self._by_passing = False
        self._distance_when_blocked = None
        self._feeler = self._host.get_feeler()

    def get_memory_since_blocked(self):
        return self._memory_since_blocked

    def has_moved(self):
        raise NotImplementedError()

    def advance(self):
        raise NotImplementedError()

    def _get_distance_from_end(self):
        return abs((self._home_vector[0] + self._home_vector[1]) / 2)

    def _get_direction_of_home(self):
        current_position = self._host.get_position()
        return get_direction_for_degrees(get_degree_from_north(current_position, self._end_position))

    def update_home_vector(self, vector):
        self._home_vector = (self._home_vector[0] - vector[0], self._home_vector[1] - vector[1])

    def _get_home_position(self):
        current_position = self._host.get_position()
        return current_position[0] + self._home_vector[0], current_position[1] + self._home_vector[1]
