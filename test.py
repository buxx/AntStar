import time

from antstar.Ant import Ant
from antstar.GlueWallAntBrain import GlueWallAntBrain
from antstar.Grid import Grid


brains = [GlueWallAntBrain]#, DirectionByPassAntBrain]

grids = {
    'Map A': """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 # # # 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 # 0 # # 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # 0 # # # # # # # # # 0
0 0 0 0 0 0 0 # # # 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 # # # # # # # 0 0 0 0
0 0 0 0 0 0 0 # 0 # # 0 0 0 0 # 0 0 0 0
0 0 0 0 0 0 0 # 0 # # 0 0 0 0 # 0 0 0 0
0 0 0 0 0 0 0 # 0 # # 0 0 0 0 # 0 0 0 0
0 0 0 0 0 0 0 # 0 # # 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 # # # # # 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 0 0 0 0 0 0 0 S 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
""",
    'Map B': """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 S 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 # 0 # 0 0 0 0 # 0 0 0
0 0 0 0 0 0 0 0 0 0 # 0 # 0 0 # 0 0 0 0
0 0 0 0 0 0 0 0 0 # 0 # 0 # 0 # 0 0 0 0
0 0 0 0 0 0 0 0 0 0 # 0 # 0 # 0 # 0 0 0
0 0 0 0 0 0 0 0 0 # 0 # 0 # 0 # 0 # 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 # 0 # 0 # 0 # 0 # 0
0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
""",
    'Map C': """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 S 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 # # 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 # 0 # # 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # 0 # 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 X 0 # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # # # # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
""",
    'Map D': """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 # # 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 # # X # # 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # 0 # 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # # # # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 S 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
""",
    'Map E': """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 # # 0 0 0 0 0 0 0 0 0 # 0 0 0 0
0 0 0 0 0 # # 0 0 0 0 0 0 0 # # 0 0 0 0
0 0 0 0 0 0 # 0 0 0 0 0 0 # # 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 0 0 # 0 0 0 0 0 0
0 0 0 0 0 0 0 # # 0 0 0 # 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 # # X # # 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 # # # 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # # # # # # 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 0 0 # 0 0 0 0 0 0 0
0 0 0 0 0 0 0 # 0 0 S 0 # 0 0 0 0 0 0 0
0 0 0 0 0 0 # 0 0 0 0 0 0 # 0 0 0 0 0 0
0 0 0 0 0 # 0 0 0 0 0 0 0 # 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
""",
    'Map F': """
# # # # # # # # # # # # # # # # # # # # # #
# 0 0 0 0 # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 X 0 # # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 0 # # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 # # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 # # # 0 0 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 # 0 # # 0 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 # # 0 # # 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 0 # # 0 # # # # # # # # # 0 #
# 0 # 0 0 0 0 0 # 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 0 # # # # # # # # # 0 0 0 0 #
# 0 # 0 0 0 0 0 # 0 # # 0 0 0 0 # 0 0 0 0 #
# 0 # 0 0 0 0 0 # 0 # # 0 0 0 0 # 0 0 0 0 #
# 0 # 0 0 0 0 0 # 0 # # 0 0 0 0 # 0 0 0 0 #
# 0 # 0 0 0 0 0 # 0 # # 0 0 0 0 0 0 0 0 0 #
# 0 # 0 0 0 0 0 # 0 # # # # # 0 0 0 0 0 0 #
# 0 # 0 0 0 0 0 # 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 # # # # # # # 0 0 0 0 0 0 0 0 0 0 0 0 #
# 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 S 0 #
# 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 #
# # # # # # # # # # # # # # # # # # # # # #
""",
}

for grid_name in grids:
    for brain_class in brains:

        try:

            grid_text = grids[grid_name]

            grid = Grid.from_string(grid_text)
            ant = Ant(start_position=grid.get_start_position(),
                      end_position=grid.get_end_position(),
                      grid=grid,
                      brain=brain_class)

            print('%s with %s' % (grid_name, brain_class.__name__))
            grid.print(ant)
            steps = 0
            while ant.get_position() != grid.get_end_position() and steps < 200:
                time.sleep(0.1)
                ant.move()
                steps += 1
                print('')
                print('%s with %s (step %s)' % (grid_name, brain_class.__name__, str(steps)))
                grid.print(ant)

        except KeyboardInterrupt:
            pass
