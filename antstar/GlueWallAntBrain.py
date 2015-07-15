from antstar.ByPassAntBrain import ByPassAntBrain
from antstar.exceptions import Blocked, AlreadyWalkedAround
from antstar.geometry import get_position_with_direction_decal as decal, directions, get_direction_between_near_points, \
    around_positions_of


class GlueWallAntBrain(ByPassAntBrain):
    """
    Aller sur une case vide que si:
      * cette case est adjascente a la case de mur en cours
      ou
      * cette case est adjascente a la case d'un mur adjascente au mur en cours
    Interdire cette case vide si;
      * On est déjà aller dessus et qu'il y a une autre case adjascente (crit. au dessus)

      TODO: Pas maximums!
      TODO: generateurs
    """

    def __init__(self, host, home_vector):
        super().__init__(host, home_vector)
        self._current_wall_square_position = None
        self._around_host_positions = []

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

    def _get_advance_direction(self):
        try:
            return super()._get_advance_direction()
        except Blocked:
            home_direction = self._get_direction_of_home()
            current_position = self._host.get_position()
            wall_position = decal(home_direction, current_position)
            self._set_current_wall_square(wall_position)
            raise

    def _get_by_pass_advance_direction(self):
        self._update_host_around_positions()
        next_walls_positions = self._get_next_visible_walls_positions()
        # Priorité au mur en cours
        next_walls_positions.insert(0, self._get_current_wall_position())

        for next_wall_position in next_walls_positions:
            to_wall_directions = self._get_to_wall_directions(next_wall_position)
            if to_wall_directions:
                self._set_current_wall_square(next_wall_position)
                return to_wall_directions[0]

        for next_wall_position in next_walls_positions:
            to_wall_directions = self._get_to_wall_directions(next_wall_position, can_re_walk=True)
            if to_wall_directions:
                self._set_current_wall_square(next_wall_position)
                return to_wall_directions[0]

        raise AlreadyWalkedAround()

    def _get_next_visible_walls_positions(self):
        walls_to_look_around = [self._get_current_wall_position()]
        for wall_to_look_around in walls_to_look_around:
            around_wall_positions = around_positions_of(wall_to_look_around)
            around_wall_walls = [pos for pos in around_wall_positions
                                 if self._position_is_around_host(pos)
                                 and not self._feeler.position_is_free(pos)
                                 and pos not in walls_to_look_around]
            walls_to_look_around.extend(around_wall_walls)

        return walls_to_look_around

    def _get_to_wall_directions(self, wall_position, can_re_walk=False):
        # directions: ou on n'a pas marché (sauf si), adjsascente au mur en cours
        # TODO: Cache de position around ? etc ? generateurs!
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

        return [get_direction_between_near_points(host_position, pos)
                for pos in visible_around_this_wall_positions]

    # def _get_by_pass_advance_direction(self):
    #     near_wall_directions = self._get_near_wall_directions()
    #
    #     if not near_wall_directions:
    #         raise AlreadyWalkedAround()
    #
    #     if len(near_wall_directions) == 1:
    #         return near_wall_directions[0]
    #
    #     for near_wall_direction in near_wall_directions:
    #         if near_wall_direction not in self.get_memory_since_blocked():
    #             return near_wall_direction
    #
    #     raise AlreadyWalkedAround()
    #
    #     # Dans ces directions, prendre que si [que 1 et deja marché] ou pas marché
    #
    # def _get_near_wall_directions(self):
    #     """
    #     :return: List of directions who are near the current wall or near a next wall
    #     """
    #     return [direction for direction in directions if self._direction_is_free_and_glue_wall(direction)]
    #
    # def _direction_is_free_and_glue_wall(self, direction):
    #     if not self._feeler.direction_is_free(direction):
    #         return False
    #
    #     current_position = self._host.get_position()
    #     will_position = decal(direction, current_position)
    #
    #     if self._position_is_near_current_wall(will_position):
    #         return True
    #
    #     if self._position_is_near_next_wall(will_position):
    #         return True
    #
    #     return False
    #
    # def _position_is_near_current_wall(self, position):
    #     current_wall_position = self._get_current_wall_position()
    #     around_wall_positions = [decal(direction, current_wall_position) for direction in directions]
    #     return position in around_wall_positions
    #
    # def _position_is_near_next_wall(self, position):
    #     next_walls_positions = self._get_next_walls_position()
    #
    #
    #
    #     next_walls_around_positions = []
    #     # TODO: [] double ?
    #     for next_wall_position in next_walls_positions:
    #         for next_wall_around_position in [decal(direction, next_wall_position) for direction in directions]:
    #             next_walls_around_positions.append(next_wall_around_position)
    #
    #     return position in next_walls_around_positions
    #
    # def _get_next_walls_position(self):
    #     """
    #
    #     Return only visible wall !
    #
    #     :return:
    #     """
    #     current_wall_position = self._get_current_wall_position()
    #     current_ant_position = self._host.get_position()
    #     around_ant_positions = [decal(direction, current_ant_position) for direction in directions]
    #     around_current_wall_positions = [decal(direction, current_wall_position) for direction in directions]
    #     around_current_wall_positions_near_ant = list(filter(lambda pos: pos in around_ant_positions, around_current_wall_positions))
    #     next_walls_positions = list(filter(lambda pos: not self._feeler.direction_is_free(get_direction_between_near_points(current_ant_position, pos)), around_current_wall_positions_near_ant))
    #     return next_walls_positions
    #
    #
    #     possibles_movements = {}
    #
    #     for next_wall_position in next_walls_positions:
    #         around_next_wall_positions = [decal(direction, current_ant_position) for direction in directions]
    #         for next_wall_around_position in around_next_wall_positions:
    #             if next_wall_around_position in around_current_wall_positions:
    #                 if next_wall_around_position not in possibles_movements:
    #                     possibles_movements[next_wall_position] = []
    #                 possibles_movements[next_wall_position].append(next_wall_around_position)
    #
    #     return possibles_movements