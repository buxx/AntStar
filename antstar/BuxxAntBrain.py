from antstar.AntBrain import AntBrain
from antstar.exceptions import Blocked, AlreadyWalkedAround
from antstar.geometry import direction_modifiers, get_position_with_direction_decal, slightly, \
    get_nearest_direction


class BuxxAntBrain(AntBrain):

    def __init__(self, host, start_position, end_position):
        super().__init__(host, start_position, end_position)
        self._memory_since_blocked = []
        self._by_passing = False
        self._distance_when_blocked = None
        self._last_direction_tested = None
        self._directions_tested = []

    def get_memory_since_blocked(self):
        return self._memory_since_blocked

    def has_moved(self):
        if self._by_passing:
            self._memory_since_blocked.append(self._host.get_position())
            if self._get_distance_from_end() < self._distance_when_blocked:
                self._by_passing = False
                self._memory_since_blocked = []

    def advance(self):
        if not self._by_passing:
            try:
                advance_vector = self._get_advance_vector()
            except Blocked:
                self._by_passing = True
                self._distance_when_blocked = self._get_distance_from_end()
                self._memory_since_blocked.append(self._host.get_position())
                return self.advance()
        else:
            try:
                advance_vector = self._get_by_pass_advance_vector()
            except AlreadyWalkedAround:
                self._memory_since_blocked = []
                return self.advance()

        self._host.move_to(advance_vector)

    def _get_advance_vector(self):
        direction_of_home = self._get_direction_of_home()

        if self._feeler.direction_is_free(direction_of_home):
            return direction_modifiers[direction_of_home]

        raise Blocked()

    def _get_by_pass_advance_vector(self):
        """
        TODO: Very complex here !
        :return:
        """
        self._last_direction_tested = self._get_direction_of_home()
        self._directions_tested = []

        while True:
            try_direction = self._get_new_by_pass_try_direction()

            if self._by_pass_direction_is_possible(try_direction):
                return direction_modifiers[try_direction]

            self._directions_tested.append(try_direction)
            if len(self._directions_tested) > 7:
                raise AlreadyWalkedAround()

            self._last_direction_tested = try_direction

    def _get_new_by_pass_try_direction(self):
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
                if try_position not in self._memory_since_blocked and self._feeler.direction_is_free(direction):
                    return True
        return False