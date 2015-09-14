from antstar.ByPassAntBrain import ByPassAntBrain
from antstar.exceptions import Blocked
from antstar.geometry import get_position_with_direction_decal as decal, around_positions_of, \
    get_direction_between_near_points, direct_around_positions_of


class StickWallAntBrain(ByPassAntBrain):

    def __init__(self, host, home_vector):
        super().__init__(host, home_vector)
        self._current_wall_position = None
        self._previous_wall_position = None
        self._current_wall_changed = False
        self._memory_length = 3

    def _get_advance_direction(self):
        try:
            return super()._get_advance_direction()
        except Blocked:
            self._trig_blocked()
            raise

    def _trig_blocked(self):
        home_direction = self._get_direction_of_home()
        current_position = self._host.get_position()
        wall_position = decal(home_direction, current_position)
        self._set_current_wall_position(wall_position)

    def erase(self):
        super().erase()
        self._set_current_wall_square(None)
        self._set_is_re_walking(False)

    def _get_by_pass_advance_direction(self):
        self._update_host_around_positions()
        self._current_wall_changed = False
        self._advance_current_wall()

        try:
            return self._get_direction_for_current_wall()
        except Blocked:
            self._set_previous_wall_position(None)
            return self._get_direction_for_current_wall()

    def _advance_current_wall(self):
        """
        Avancer de mur en mur collant au mur en cours (la règle étant que ce ne doit pas être un mur déjà visité)
        Regle 2: Avance que de mur en mur en angle droit. Pas de diagonales.
        """
        while True:
            try:
                self._advance_current_wall_iteration()
                self._current_wall_changed = True
            except StopIteration:
                return

    def _advance_current_wall_iteration(self):
        direct_around_positions = direct_around_positions_of(self._get_current_wall_position())
        direct_around_wall_positions = [pos for pos in direct_around_positions
                                        if self._position_is_around_host(pos)  # Must be visible by ant
                                        and not self._feeler.position_is_free(pos)]  # And not penetrable

        for new_wall_position in direct_around_wall_positions:
            if new_wall_position != self._get_previous_wall_position():
                self._advance_wall_on(new_wall_position)
                return

        raise StopIteration()

    def _advance_wall_on(self, position):
        self._set_previous_wall_position(self._current_wall_position)
        self._set_current_wall_position(position)

    def _has_moved(self, direction):
        super()._has_moved(direction)
        if not self._current_wall_changed:
            self._set_previous_wall_position(None)

    def _get_direction_for_current_wall(self):
        around_wall_positions = around_positions_of(self._get_current_wall_position())
        # Keep positions in host visible field
        visible_around_wall_positions = self._reduce_positions_by_host_visibility(around_wall_positions)
        ordered_visible_around_wall_positions = self._order_positions_by_not_walked(visible_around_wall_positions)
        return next(self._change_positions_to_directions(ordered_visible_around_wall_positions))

    def _get_current_wall_position(self):
        return self._current_wall_position

    def _set_current_wall_position(self, position):
        self._current_wall_position = position

    def _get_previous_wall_position(self):
        return self._previous_wall_position

    def _set_previous_wall_position(self, position):
        self._previous_wall_position = position

    def _reduce_positions_by_host_visibility(self, positions):
        return (pos for pos in positions
                if self._position_is_around_host(pos)
                and self._feeler.position_is_free(pos))

    def _change_positions_to_directions(self, positions):
        host_position = self._host.get_position()
        return (get_direction_between_near_points(host_position, pos)
                for pos in positions)

    def _get_next_visible_walls_positions(self, from_position):
        """

        Return positions of ant visible walls

        :return: list: list of positions
        """
        walls_to_look_around = [from_position]
        for wall_to_look_around in walls_to_look_around:
            around_wall_positions = around_positions_of(wall_to_look_around)
            around_wall_walls = (pos for pos in around_wall_positions
                                 if self._position_is_around_host(pos)
                                 and not self._feeler.position_is_free(pos)
                                 and pos not in walls_to_look_around
                                 and pos != self._get_current_wall_position())
            walls_to_look_around.extend(around_wall_walls)

        return walls_to_look_around

    def _position_is_around_host(self, position):
        return position in self._around_host_positions

    def _order_positions_by_not_walked(self, positions):
        return sorted(positions,
                      key=lambda pos: pos not in self.get_memory_since_blocked(),
                      reverse=True)
