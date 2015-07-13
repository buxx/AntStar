from antstar.AntBrain import AntBrain
from antstar.ByPassAntBrain import ByPassAntBrain
from antstar.exceptions import Blocked, AlreadyWalkedAround
from antstar.geometry import get_position_with_direction_decal, slightly, get_nearest_direction, directions


class DirectionByPassAntBrain(ByPassAntBrain):

    MODE_A = 'a'
    MODE_B = 'b'

    def __init__(self, host, home_vector):
        super().__init__(host, home_vector)
        self._last_direction_tested = None
        self._directions_tested = []
        self._mode = self.MODE_A

    def _get_by_pass_advance_direction(self):
        self._last_direction_tested = self._get_direction_of_home()
        self._directions_tested = []

        while True:
            try_direction = self._get_new_by_pass_try_direction()

            if self._by_pass_direction_is_possible(try_direction):
                return try_direction

            self._directions_tested.append(try_direction)
            if len(self._directions_tested) > 7:
                raise AlreadyWalkedAround()

            self._last_direction_tested = try_direction

    def _get_new_by_pass_try_direction(self):
        if self._mode == self.MODE_B:

            available_directions = [direct for direct in directions if direct not in self._directions_tested]
            return get_nearest_direction(self._get_home_position(),
                                         self._host.get_position(),
                                         available_directions)

        if self._last_direction_tested in self._directions_tested:

            slightly_available = slightly[self._last_direction_tested]
            return [direct for direct in slightly_available if direct not in self._directions_tested][0]
        else:
            return get_nearest_direction(self._get_home_position(),
                                         self._host.get_position(),
                                         slightly[self._last_direction_tested])

    def _by_pass_direction_is_possible(self, direction):
        if direction not in self._directions_tested:
                try_position = get_position_with_direction_decal(direction, self._host.get_position())
                if try_position not in self.get_memory_since_blocked() and self._feeler.direction_is_free(direction):
                    return True
        return False
