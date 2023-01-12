import argparse
import timeit
import resource
from collections import deque
from heapq import heappush, heappop, heapify

class State:
    def __init__(self, state, parent, move, depth, cost, key):

        self.state = state

        self.parent = parent

        self.move = move

        self.depth = depth

        self.cost = cost

        self.key = key

        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map


goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_node = State
initial_state = list()
nodes_expanded = 0
max_search_depth = 0
moves = list()

up_restricted = {0,1,2}
down_restricted = {6,7,8}
left_restricted = {0,3,6}
right_restricted = {2,5,8}


def bfs(initial_state):
    global goal_node, max_search_depth

    frontier = deque([State(initial_state, None, None, 0, 0, 0)])
    start_node = State(initial_state, None, None, 0, 0, 0)
    #frontier_checker = deque()
    #frontier_checker.append(start_node.map)
    explored = set()

    while frontier:
        current_node = frontier.popleft()
        #frontier_checker.popleft()
        explored.add(current_node.map)

        if current_node.state == goal_state:
            goal_node = current_node
            return True

        neighbors = expand(current_node)

        for node in neighbors:
            if node.map not in explored:
                frontier.append(node)
                #frontier_checker.append(node.map)
                explored.add(node.map)

                if node.depth > max_search_depth:
                    max_search_depth = node.depth
    return False

def dfs(initial_state):
    global goal_node, max_search_depth

    stack =  list([State(initial_state, None, None, 0, 0, 0)])
    explored = set()

    while stack:
        current_node = stack.pop()
        explored.add(current_node.map)

        if current_node.state == goal_state:
            goal_node = current_node
            return True

        neighbors = reversed(expand(current_node))

        for node in neighbors:
            if node.map not in explored:
                stack.append(node)
                explored.add(node.map)

                if node.depth > max_search_depth:
                    max_search_depth = node.depth
    return False

def ast(initial_state):
    global goal_node, max_search_depth

    heap = list()
    explored = set()
    heap_checker = {}

    key = h(initial_state)
    start_node = State(initial_state, None, None, 0, 0, 0)
    entry = (key, start_node)

    heappush(heap, entry)
    heap_checker[start_node.map] = entry

    while heap:
        current_node = heappop(heap)
        explored.add(current_node[1].map)

        if current_node[1].state == goal_state:
            goal_node = current_node[1]
            return True

        neighbors = expand(current_node[1])

        for node in neighbors:
            node.key = node.cost + h(node.state)
            entry = (node.key, node)

            if node.map not in explored:
                heappush(heap, entry)
                explored.add(node.map)
                heap_checker[node.map] = entry

                if node.depth > max_search_depth:
                    max_search_depth += 1

            elif node.map in heap_checker and node.key < heap_checker[node.map][1].key:
                heap_index = heap.index((heap_checker[node.map][1].key, heap_checker[node.map][1]))

                #re-insert into heap with new key(cost)
                heap[int(heap_index)] = entry
                heap_checker[node.map] = entry
                heapify(heap)

    return False

def h(state):
    h = 0

    for i in range(1, 9):
        board_i = state.index(i)
        goal_i = goal_state.index(i)
        h += abs(board_i % 3 - goal_i % 3) + abs(board_i // 3 - goal_i // 3)

    return h

def expand(node):
    global nodes_expanded
    nodes_expanded += 1

    neighbors = []
    neighbors.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    node_list = []

    for node in neighbors:
        if node.state != None:
            node_list.append(node)

    return node_list

def move(state, action):
    global up_restricted, down_restricted, left_restricted, right_restricted

    new_state = state[:]
    key_index = new_state.index(0)
    #up
    if action == 1:
        if key_index not in up_restricted:
            temp = new_state[key_index - 3]
            new_state[key_index-3] = new_state[key_index]
            new_state[key_index] = temp

            return new_state
        else:
            return None

    if action == 2:
        if key_index not in down_restricted:
            temp = new_state[key_index + 3]
            new_state[key_index + 3] = new_state[key_index]
            new_state[key_index] = temp

            return new_state
        else:
            return None

    if action == 3:
        if key_index not in left_restricted:
            temp = new_state[key_index - 1]
            new_state[key_index - 1] = new_state[key_index]
            new_state[key_index] = temp

            return new_state
        else:
            return None

    if action == 4:
        if key_index not in right_restricted:
            temp = new_state[key_index + 1]
            new_state[key_index + 1] = new_state[key_index]
            new_state[key_index] = temp

            return new_state
        else:
            return None

def backtrace():
    current_node = goal_node

    while initial_state != current_node.state:
        if current_node.move == 1:
            movement = 'Up'
        elif current_node.move == 2:
            movement = 'Down'
        elif current_node.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'

        moves.insert(0, movement)
        current_node = current_node.parent

    return moves

def output(time, start_ram):
    global moves
    moves = backtrace()

    file = open('output.txt', 'w')

    file.write("path_to_goal: " + str(moves))
    file.write("\ncost_of_path: " + str(len(moves)))
    file.write("\nnodes_expanded: " + str(nodes_expanded))
    file.write("\nsearch_depth: " + str(goal_node.depth))
    file.write("\nmax_search_depth: " + str(max_search_depth))
    file.write("\nrunning_time: " + format(time, '.8f'))
    file.write("\nmax_ram_usage: " + format((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram)/(2**20), '.8f'))
    file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('algorithm')
    parser.add_argument('board')
    args = parser.parse_args()

    #create list for the intial State
    board = args.board.split(",")

    for element in board:
        initial_state.append(int(element))

    function = function_map[args.algorithm]
    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    start = timeit.default_timer()
    frontier = function(initial_state)
    stop = timeit.default_timer()

    output(stop-start, dfs_start_ram)

function_map = {'bfs':bfs, 'dfs':dfs, 'ast':ast}

if __name__ == '__main__':
    main()
