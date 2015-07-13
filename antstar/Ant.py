from antstar.AntFeeler import AntFeeler
from antstar.DirectionByPassAntBrain import DirectionByPassAntBrain
from antstar.geometry import direction_modifiers


class Ant:

    def __init__(self, start_position, end_position, grid, brain=DirectionByPassAntBrain):
        self._position = start_position
        self._feeler = AntFeeler(self, grid)
        home_vector = (-(start_position[0] - end_position[0]), -(start_position[1] - end_position[1]))
        self._brain = brain(self, home_vector)

    def get_position(self):
        return self._position

    def move_to(self, direction):
        vector = direction_modifiers[direction]
        self._brain.update_home_vector_with_vector(vector)
        self._position = (self._position[0] + vector[0], self._position[1] + vector[1])
        self._brain.has_moved()

    def get_feeler(self):
        return self._feeler

    def move(self):
        self._brain.advance()

    def get_bypass_memory(self):
        return self._brain.get_memory_since_blocked()
