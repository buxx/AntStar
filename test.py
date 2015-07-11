from antstar.Ant import Ant
from antstar.Grid import Grid
import time

grid_text = """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1 1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 1 0 1 1 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 0 1 1 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 0 1 1 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 S 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
"""

grid = Grid.from_string(grid_text)
ant = Ant(start_position=grid.get_start_position(),
          end_position=grid.get_end_position(),
          grid=grid)

grid.print(ant)
while ant.get_position() != grid.get_end_position():
    time.sleep(0.3)
    ant.move()
    print('')
    grid.print(ant)
