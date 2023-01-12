# N-Puzzle-Game
Solves any 8-puzzle board when given an arbitrary starting configuration using three different search methods.

he program will be executed as follows:
$ python3 puzzle.py <method> <board>
The method argument will be one of the following. You must implement all three of them:
bfs (Breadth-First Search)
dfs (Depth-First Search)
ast (A-Star Search)
The board argument will be a comma-separated list of integers containing no spaces. For example, to use the
bread-first search strategy to solve the input board given by the starting configuration {0,8,7,6,5,4,3,2,1}, the pro-
gram will be executed like so (with no spaces between commas):
$ python3 puzzle.py bfs 0,8,7,6,5,4,3,2,1
