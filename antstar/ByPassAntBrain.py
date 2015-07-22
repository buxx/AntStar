from antstar.AntBrain import AntBrain
from antstar.exceptions import Blocked, AlreadyWalkedAround
from antstar.geometry import direction_modifiers


class ByPassAntBrain(AntBrain):

    def __init__(self, host, home_vector):
        super().__init__(host, home_vector)
        self._memory_since_blocked = []
        self._clean_memory = False
        self._by_passing = False
        self._distance_when_blocked = None

    def get_memory_since_blocked(self):
        return self._memory_since_blocked

    def get_last_memory_since_blocked(self):
        return self._memory_since_blocked[-2]

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

    def erase(self):
        super().erase()
        self._set_memory_since_blocked([])
        self._set_by_passing(False)
        self._set_distance_when_blocked(None)

    def _has_moved(self, direction):
        vector = direction_modifiers[direction]
        self.update_home_vector_with_vector(vector)

        if self.is_by_passing():
            self._add_memory_since_blocked(self._host.get_position())
            if self._get_distance_from_end() < self._get_distance_when_blocked():
                self._set_by_passing(False)
                if self._clean_memory:
                    self._set_memory_since_blocked([])
        else:
            if not self._clean_memory:
                self._add_memory_since_blocked(self._host.get_position())

    def advance(self):
        if not self.is_by_passing():
            try:
                direction = self._get_advance_direction()
            except Blocked:
                self._set_by_passing(True)
                self._set_distance_when_blocked(self._get_distance_from_end())
                return self.advance()
        else:
            try:
                direction = self._get_by_pass_advance_direction()
            except AlreadyWalkedAround:
                self._set_memory_since_blocked([])
                return self.advance()

        self._host.move_to(direction)
        self._has_moved(direction)

    def _get_advance_direction(self):
        direction_of_home = self._get_direction_of_home()

        if self._feeler.direction_is_free(direction_of_home):
            return direction_of_home

        raise Blocked()

    def _get_by_pass_advance_direction(self):
        raise NotImplementedError()
