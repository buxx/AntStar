# AntStar
Python lib to find path in 2d environment to an objective, with limited around information

##  Example

for a given map:

```
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
```

Where ``0`` is free way, ``1`` a wall, ``S`` the start point of our ant and ``X`` the objective.

[![AntStar exemple gif](https://raw.githubusercontent.com/buxx/AntStar/master/doc/antstar.gif)](https://raw.githubusercontent.com/buxx/AntStar/master/doc/antstar.gif) 
