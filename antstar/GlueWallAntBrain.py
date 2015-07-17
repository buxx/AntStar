from antstar.ByPassAntBrain import ByPassAntBrain
from antstar.exceptions import Blocked
from antstar.geometry import get_position_with_direction_decal as decal, get_direction_between_near_points, \
    around_positions_of


class GlueWallAntBrain(ByPassAntBrain):

    def __init__(self, host, home_vector):
        super().__init__(host, home_vector)
        self._current_wall_square_position = None
        self._around_host_positions = []
        self._is_re_walking = False

    def _get_current_wall_position(self):
        return self._current_wall_square_position

    def _set_current_wall_square(self, position_of_square):
        self._current_wall_square_position = position_of_square

    def _set_by_passing(self, by_passing):
        """

        When we leave the wall, we must empty the _current_wall_square

        :param by_passing:
        :return:
        """
        super()._set_by_passing(by_passing)
        if not by_passing:
            self._set_current_wall_square(None)

    def _update_host_around_positions(self):
        self._around_host_positions = around_positions_of(self._host.get_position())

    def _position_is_around_host(self, position):
        return position in self._around_host_positions

    def is_re_walking(self):
        return self._is_re_walking

    def _set_is_re_walking(self, is_re_walking):
        self._is_re_walking = is_re_walking

    def _get_advance_direction(self):
        """

        :return: int direction
        """
        try:
            return super()._get_advance_direction()
        except Blocked:
            self._trig_blocked()
            raise

    def _trig_blocked(self):
        """

        Update attributes to start a by pass

        :return:
        """
        home_direction = self._get_direction_of_home()
        current_position = self._host.get_position()
        wall_position = decal(home_direction, current_position)
        self._set_current_wall_square(wall_position)

    def _get_by_pass_advance_direction(self):
        """

        Return a direction for bypass mode

        :return: int direction
        """
        self._update_host_around_positions()

        try:
            # Thirst we try to follow the current wall
            return self._get_direction_for_walls([self._get_current_wall_position()])
        except Blocked:
            next_walls_positions = self._get_next_visible_walls_positions()
            try:
                # If we can't follow current wall, follow next walls
                return self._get_direction_for_walls(next_walls_positions, can_re_walk=True)
            except Blocked:
                # Absolutely blocked, start a new walk
                self._set_memory_since_blocked([])
                return self._get_by_pass_advance_direction()

    def _get_direction_for_walls(self, walls_positions, can_re_walk=False, re_walk=False):
        """

        Return possibles directions for parameter walls

        :param walls_positions: positions of looked walls
        :param can_re_walk: if no road found, allow retry with re walk
        :param re_walk: allow walk on already walked positions
        :return: direction
        """
        for next_wall_position in walls_positions:
            to_wall_directions = self._get_to_wall_directions(next_wall_position, can_re_walk=re_walk)
            if to_wall_directions:
                self._set_current_wall_square(next_wall_position)
                self._set_is_re_walking(re_walk)
                return to_wall_directions[0]

        if can_re_walk:
            return self._get_direction_for_walls(walls_positions, re_walk=True)

        raise Blocked()

    def _get_next_visible_walls_positions(self):
        """

        Return positions of ant visible walls

        :return: list: list of positions
        """
        walls_to_look_around = [self._get_current_wall_position()]
        for wall_to_look_around in walls_to_look_around:
            around_wall_positions = around_positions_of(wall_to_look_around)
            around_wall_walls = [pos for pos in around_wall_positions
                                 if self._position_is_around_host(pos)
                                 and not self._feeler.position_is_free(pos)
                                 and pos not in walls_to_look_around
                                 and pos != self._get_current_wall_position()]
            walls_to_look_around.extend(around_wall_walls)

        return walls_to_look_around

    def _get_to_wall_directions(self, wall_position, can_re_walk=False):
        """

        Return possible directions for given wall

        :param wall_position: position of looked wall
        :param can_re_walk: allow directions on already walked position
        :return: list of directions
        """
        host_position = self._host.get_position()
        around_this_wall_positions = around_positions_of(wall_position)

        visible_around_this_wall_positions = []
        for position in around_this_wall_positions:
            if self._position_is_around_host(position) and self._feeler.position_is_free(position):
                visible_around_this_wall_positions.append(position)

        if not can_re_walk:
            return [get_direction_between_near_points(host_position, pos)
                    for pos in visible_around_this_wall_positions
                    if pos not in self.get_memory_since_blocked()]
        elif self.is_re_walking():
            visible_around_this_wall_positions = [pos for pos in visible_around_this_wall_positions
                                                  if not pos == self.get_last_memory_since_blocked()]

        return [get_direction_between_near_points(host_position, pos)
                for pos in visible_around_this_wall_positions]
