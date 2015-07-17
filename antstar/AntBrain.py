import math

from antstar.geometry import get_degree_from_north, get_direction_for_degrees


class AntBrain:

    def __init__(self, host, home_vector):
        self._host = host
        self._home_vector = home_vector
        current_position = self._host.get_position()
        self._end_position = current_position[0] + home_vector[0], current_position[1] + home_vector[1]
        self._feeler = self._host.get_feeler()

    def _get_home_vector(self):
        return self._home_vector

    def _set_home_vector(self, home_vector):
        self._home_vector = home_vector

    def _get_end_position(self):
        return self._end_position

    def has_moved(self):
        raise NotImplementedError()

    def advance(self):
        raise NotImplementedError()

    def _get_distance_from_end(self):
        home_vector = self._get_home_vector()
        return math.hypot(home_vector[0], home_vector[1])

    def _get_direction_of_home(self):
        current_position = self._host.get_position()
        end_position = self._get_end_position()
        return get_direction_for_degrees(get_degree_from_north(current_position, end_position))

    def update_home_vector_with_vector(self, vector):
        self._set_home_vector((self._home_vector[0] - vector[0], self._home_vector[1] - vector[1]))

    def _get_home_position(self):
        current_position = self._host.get_position()
        home_vector = self._get_home_vector()
        return current_position[0] + home_vector[0], current_position[1] + home_vector[1]
