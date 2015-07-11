from antstar.AntBrain import AntBrain
from antstar.exceptions import Blocked, AlreadyWalkedAround
from antstar.geometry import direction_modifiers, get_position_with_direction_decal, slightly, \
    get_nearest_direction
import random

class BuxxAntBrain(AntBrain):

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
        direction_of_home = self._get_direction_of_home()
        home_position = self._get_home_position()
        current_position = self._host.get_position()
        direction_walkable = False
        directions_tested = []
        last_direction_tested = direction_of_home
        while not direction_walkable:
            if last_direction_tested in directions_tested:
                slightly_available = slightly[last_direction_tested]
                try_direction = [dir for dir in slightly_available if dir not in directions_tested][0]
            else:
                try_direction = get_nearest_direction(home_position, current_position, slightly[last_direction_tested])
            if try_direction not in directions_tested:
                try_position = get_position_with_direction_decal(try_direction, current_position)
                if try_position not in self._memory_since_blocked and self._feeler.direction_is_free(try_direction):
                    return direction_modifiers[try_direction]
                directions_tested.append(try_direction)

            if len(directions_tested) > 7:
                raise AlreadyWalkedAround()

            last_direction_tested = try_direction
