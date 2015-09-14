class Grid:

    FREE = 0
    WALL = '#'

    @classmethod
    def from_string(cls, string):
        map_text_rows = [text_row.replace(' ', '') for text_row in filter(None, string.split("\n"))]
        start = next(cls.find_position_in_text('S', map_text_rows))
        end = next(cls.find_position_in_text('X', map_text_rows))
        wall_positions = cls.find_position_in_text(cls.WALL, map_text_rows)

        grid = cls(
            width=len(map_text_rows[0]),
            height=len(map_text_rows),
            start=start,
            end=end
        )

        grid.add_wall(wall_positions)
        return grid

    @classmethod
    def find_position_in_text(cls, to_find, list_to_search_in):
        for y, row in enumerate(list_to_search_in):
            if to_find in row:
                for x in [i for i, item in enumerate(row) if item == to_find]:
                    yield x, y

    def __init__(self, width, height, start, end):
        self._grid = []
        for x in range(height):
            self._grid.append([self.FREE] * width)
        self._start = start
        self._end = end

    def add_wall(self, positions):
        for position in positions:
            x = position[0]
            y = position[1]
            self._grid[y][x] = self.WALL

    def print(self, ant):
        ant_x, ant_y = ant.get_position()
        bypass_memory = ant.get_bypass_memory()
        for y, row in enumerate(self._grid):
            display_row = list(row)
            if y == self._start[1]:
                display_row[self._start[0]] = 'S'
            if y == self._end[1]:
                display_row[self._end[0]] = 'X'
            for bypass_memory_position in bypass_memory:
                if bypass_memory_position[1] == y:
                    display_row[bypass_memory_position[0]] = ','
            if y == ant_y:
                display_row[ant_x] = 'A'

            # DEV: Protected usage for debug (and StickWallAntBrain depend)
            if ant._brain._current_wall_position and y == ant._brain._current_wall_position[1]:
                display_row[ant._brain._current_wall_position[0]] = 'O'
            if ant._brain._previous_wall_position and y == ant._brain._previous_wall_position[1]:
                display_row[ant._brain._previous_wall_position[0]] = 'o'

            display_row = [i if i is not 0 else ' ' for i in display_row]
            print(*display_row)

    def get_start_position(self):
        return self._start

    def get_end_position(self):
        return self._end

    def is_free(self, position):
        x, y = position
        try:
            return self._grid[y][x] is not self.WALL
        except IndexError:
            return False
