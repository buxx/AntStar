from antstar.exceptions import Blocked
from antstar.geometry import get_degree_from_north, get_direction_for_degrees, direction_modifiers, \
    get_position_with_direction_decal


class AntBrain:

    def __init__(self, host, start_position, end_position):
        self._host = host
        self._home_vector = (-(start_position[0] - end_position[0]), -(start_position[1] - end_position[1]))
        self._end_position = end_position
        self._memory_since_blocked = []
        self._by_passing = False
        self._distance_when_blocked = None
        self._feeler = self._host.get_feeler()

    def has_moved(self):
        if self._by_passing:
            self._memory_since_blocked.append(self._host.get_position())

    def advance(self):
        if not self._by_passing:
            try:
                advance_vector = self._get_advance_vector()
            except Blocked as exc:
                self._by_passing = True
                self._distance_when_blocked = self._distance_from_end()
                return self.advance()
        else:
            advance_vector = self._get_by_pass_advance_vector()
        self._host.move_to(advance_vector)

    def _distance_from_end(self):
        return (self._home_vector[0] + self._home_vector[1]) / 2

    def update_home_vector(self, vector):
        self._home_vector = (self._home_vector[0] - vector[0], self._home_vector[1] - vector[1])

    def _get_advance_vector(self):
        current_position = self._host.get_position()
        direction_of_home = get_direction_for_degrees(get_degree_from_north(current_position, self._end_position))

        if self._feeler.direction_is_free(direction_of_home):
            return direction_modifiers[direction_of_home]

        raise Blocked()

    def _get_by_pass_advance_vector(self):
        raise NotImplementedError()