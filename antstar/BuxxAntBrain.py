from antstar.AntBrain import AntBrain
from antstar.exceptions import Blocked, AlreadyWalkedAround
from antstar.geometry import direction_modifiers, get_position_with_direction_decal, slightly, \
    get_nearest_direction


class BuxxAntBrain(AntBrain):

    def __init__(self, host, home_vector):
        super().__init__(host, home_vector)
        self._memory_since_blocked = []
        self._by_passing = False
        self._distance_when_blocked = None
        self._last_direction_tested = None
        self._directions_tested = []

    def get_memory_since_blocked(self):
        return self._memory_since_blocked

    def _set_memory_since_blocked(self, memory_since_blocked):
        self._memory_since_blocked = memory_since_blocked

    def _add_memory_since_blocked(self, position):
        memory_since_blocked = self.get_memory_since_blocked()
        memory_since_blocked.append(position)
        self._set_memory_since_blocked(memory_since_blocked)

    def is_by_passing(self):
        return self._by_passing

    def _set_by_passing(self, by_passing):
        self._by_passing = by_passing

    def _get_distance_when_blocked(self):
        return self._distance_when_blocked

    def _set_distance_when_blocked(self, distance):
        self._distance_when_blocked = distance

    def has_moved(self):
        if self.is_by_passing():
            self._add_memory_since_blocked(self._host.get_position())
            if self._get_distance_from_end() < self._get_distance_when_blocked():
                self._set_by_passing(False)
                self._set_memory_since_blocked([])

    def advance(self):
        if not self.is_by_passing():
            try:
                direction = self._get_advance_direction()
            except Blocked:
                self._set_by_passing(True)
                self._set_distance_when_blocked(self._get_distance_from_end())
                self._add_memory_since_blocked(self._host.get_position())
                return self.advance()
        else:
            try:
                direction = self._get_by_pass_advance_direction()
            except AlreadyWalkedAround:
                self._set_memory_since_blocked([])
                return self.advance()

        self._host.move_to(direction)

    def _get_advance_direction(self):
        direction_of_home = self._get_direction_of_home()

        if self._feeler.direction_is_free(direction_of_home):
            return direction_of_home

        raise Blocked()

    def _get_by_pass_advance_direction(self):
        """
        TODO: Very complex here !
        :return:
        """
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
