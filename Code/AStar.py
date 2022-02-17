from math import sqrt, floor
import sys
import heapq

alphabets = [letter for letter in "abcdefghijklmnopqrstuvwxyz"] # ['a', 'b', 'c', ..., 'z']
indexing = {k:v for (k,v) in zip(alphabets, [i for i in range(26)])} # {'a': 0, 'b': 1, ..., 'z': 25}

# convert a0 to (0, 0)
def get_tuple_coord(coord):
    return (int(coord[1:]), indexing[coord[0]])

# convert (0, 0) to a0
def get_alpha_coord(coord):
    return alphabets[coord[1]] + str(coord[0])
    
class Piece:
    def __init__(self, ptype, coord): 
        self.ptype = ptype
        self.coord = coord #a0
        
    # returns a list of coords as valid moves
    def get_valid_moves(self, rows, cols, obs_pos):
        return []
    
    # return if new_coord is a valid move
    # new_coord here is a tuple
    def is_valid_move(self, new_coord, rows, cols, obs_pos):
        curr_coord = get_tuple_coord(self.coord)
        return (new_coord != curr_coord) and (new_coord[0] >= 0) and (new_coord[0] < rows) and (new_coord[1] >= 0) and (new_coord[1] < cols) and (get_alpha_coord(new_coord) not in obs_pos)
    
    # return if new_coord is beyond edge of board or is obstacle
    def is_obstacle(self, new_coord, rows, cols, obs_pos):
        return (new_coord[0] < 0) or (new_coord[0] >= rows) or (new_coord[1] < 0) or (new_coord[1] >= cols) or (get_alpha_coord(new_coord) in obs_pos)
    
class King(Piece):
    def __init__(self, ptype, coord):
        super().__init__(ptype, coord)
        
    def get_valid_moves(self, rows, cols, obs_pos):
        moves = []
        curr_coord = get_tuple_coord(self.coord)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_coord = (curr_coord[0] + i, curr_coord[1] + j)
                if self.is_valid_move(new_coord, rows, cols, obs_pos):
                    moves.append(get_alpha_coord(new_coord))
        return moves

class Queen(Piece):
    def __init__(self, ptype, coord):
        super().__init__(ptype, coord)
    
    def get_valid_moves(self, rows, cols, obs_pos):
        moves = []
        curr_coord = get_tuple_coord(self.coord)
        for direction in range(8):
            for i in range(1, max(rows, cols)):
                new_coord = 0
                if direction == 0:
                    new_coord = (curr_coord[0] + i, curr_coord[1]) # south
                elif direction == 1:
                    new_coord = (curr_coord[0] + i, curr_coord[1] + i) # south-east
                elif direction == 2:
                    new_coord = (curr_coord[0], curr_coord[1] + i) # east
                elif direction == 3:
                    new_coord = (curr_coord[0] - i, curr_coord[1] + i) # north-east
                elif direction == 4:
                    new_coord = (curr_coord[0] - i, curr_coord[1]) # north
                elif direction == 5:
                    new_coord = (curr_coord[0] - i, curr_coord[1] - i) # north-west
                elif direction == 6:
                    new_coord = (curr_coord[0], curr_coord[1] - i) # west
                elif direction == 7:
                    new_coord = (curr_coord[0] + i, curr_coord[1] - i) # south-west
                # if encounter obstacle or edge of board, stop moving in this direction
                if self.is_obstacle(new_coord, rows, cols, obs_pos):
                    break
                if self.is_valid_move(new_coord, rows, cols, obs_pos):
                    moves.append(get_alpha_coord(new_coord))
        return moves

class Bishop(Piece):
    def __init__(self, ptype, coord):
        super().__init__(ptype, coord)
    
    def get_valid_moves(self, rows, cols, obs_pos):
        moves = []
        curr_coord = get_tuple_coord(self.coord)
        for direction in range(4):
            for i in range(1, max(rows, cols)):
                new_coord = 0
                if direction == 0:
                    new_coord = (curr_coord[0] + i, curr_coord[1] + i) # south-east
                elif direction == 1:
                    new_coord = (curr_coord[0] - i, curr_coord[1] + i) # north-east
                elif direction == 2:
                    new_coord = (curr_coord[0] - i, curr_coord[1] - i) # north-west
                elif direction == 3:
                    new_coord = (curr_coord[0] + i, curr_coord[1] - i) # south-west
                # if encounter obstacle or edge of board, stop moving in this direction
                if self.is_obstacle(new_coord, rows, cols, obs_pos):
                    break
                if self.is_valid_move(new_coord, rows, cols, obs_pos):
                    moves.append(get_alpha_coord(new_coord))
        return moves

class Knight(Piece):
    def __init__(self, ptype, coord):
        super().__init__(ptype, coord)
    
    def get_valid_moves(self, rows, cols, obs_pos):
        moves = []
        curr_coord = get_tuple_coord(self.coord)
        for i in [(2, 1), (2, -1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (1, -2), (-1, -2)]:
            new_coord = (curr_coord[0] + i[0], curr_coord[1] + i[1])
            if self.is_valid_move(new_coord, rows, cols, obs_pos):
                moves.append(get_alpha_coord(new_coord))
        return moves
    
class Rook(Piece):
    def __init__(self, ptype, coord):
        super().__init__(ptype, coord)
    
    def get_valid_moves(self, rows, cols, obs_pos):
        moves = []
        curr_coord = get_tuple_coord(self.coord)
        for direction in range(4):
            for i in range(1, max(rows, cols)):
                new_coord = 0
                if direction == 0:
                    new_coord = (curr_coord[0] + i, curr_coord[1]) # south
                elif direction == 1:
                    new_coord = (curr_coord[0], curr_coord[1] + i) # east
                elif direction == 2:
                    new_coord = (curr_coord[0] - i, curr_coord[1]) # north
                elif direction == 3:
                    new_coord = (curr_coord[0], curr_coord[1] - i) # west
                    # if encounter obstacle or edge of board, stop moving in this direction
                if self.is_obstacle(new_coord, rows, cols, obs_pos):
                    break
                if self.is_valid_move(new_coord, rows, cols, obs_pos):
                    moves.append(get_alpha_coord(new_coord))
        return moves

class Board:
    def __init__(self, rows, cols, obs, obs_pos, enemies, costs):
        self.rows = rows
        self.cols = cols
        self.obs = obs # number of obstacles
        self.obs_pos = obs_pos.split()
        self.grid = [[1 for y in range(cols)] for x in range(rows)]
        self.en_threat = []
        for c in costs:
            curr_coord = get_tuple_coord(c[0])
            self.grid[curr_coord[0]][curr_coord[1]] = c[1]
        for en in enemies:
            self.obs_pos.append(en.coord)
        for en in enemies:
            self.en_threat += en.get_valid_moves(self.rows, self.cols, self.obs_pos)
        self.obs_pos += self.en_threat
        self.obs_pos = set(self.obs_pos)
    
    def get_cost(self, coord):
        if coord in self.obs_pos:
            return float("inf") # defensive coding
        curr_coord = get_tuple_coord(coord)
        return self.grid[curr_coord[0]][curr_coord[1]]
            
class Node:
    def __init__(self, board, piece, goals, parents, cost):
        self.board = board
        self.piece = piece
        self.goals = goals
        self.parents = parents
        self.cost = cost
        self.depth = len(self.parents)
        self.fn = self.eval_func()
    
    def __lt__(self, other):
        return self.fn < other.fn
    
    def transition(self, action):
        new_piece = get_piece(self.piece.ptype, action)
        new_parents = self.parents + [[(self.piece.coord[0], int(self.piece.coord[1:])), (new_piece.coord[0], int(new_piece.coord[1:]))]]
        new_cost = self.cost + self.board.get_cost(action)
        return Node(self.board, new_piece, self.goals, new_parents, new_cost)
    
    def heuristic(self):
        hn = float("inf")
        curr_coord = get_tuple_coord(self.piece.coord)
        for goal in self.goals:
            goal_coord = get_tuple_coord(goal)
            # floor of eucliean_distance to nearest goal
            dist = floor(sqrt(pow(goal_coord[0] - curr_coord[0], 2) + pow(goal_coord[1] - curr_coord[1], 2)))
            if dist < hn:
                hn = dist
        return hn
    
    def eval_func(self):
        return self.cost + self.heuristic()
    
    def is_goal(self):
        return self.piece.coord in self.goals

    def get_actions(self):
        return self.piece.get_valid_moves(self.board.rows, self.board.cols, self.board.obs_pos)

def get_piece(ptype, coord):
    pieces = {"King" : lambda : King(ptype, coord), "Queen" : lambda : Queen(ptype, coord), "Bishop" : lambda : Bishop(ptype, coord), "Knight" : lambda : Knight(ptype, coord), "Rook" : lambda : Rook(ptype, coord)}
    return pieces[ptype]()

def initialise():
    test_case = []
    with open(sys.argv[1]) as f:
        test_case = f.read().split("\n")
    rows = int(test_case[0].split(":")[1])
    cols = int(test_case[1].split(":")[1])
    obs = int(test_case[2].split(":")[1])
    obs_pos = test_case[3].split(":")[1]
    costs = []
    counter = 5
    for i in test_case[5:]:
        if "Number of Enemy" in i:
            break
        cost_coord = i.split(",")
        costs.append((cost_coord[0][1:], int(cost_coord[1][:-1])))
        counter += 1
    counter += 2
    enemies = []
    for i in test_case[counter:]:
        if "Number of Own" in i:
            break
        en = i.split(",")
        enemies.append(get_piece(en[0][1:], en[1][:-1]))
        counter += 1
    counter += 2
    piece = get_piece(test_case[counter].split(",")[0][1:], test_case[counter].split(",")[1][:-1])
    counter += 1
    goals = set(test_case[counter].split(":")[1].split())
    board = Board(rows, cols, obs, obs_pos, enemies, costs)
    return [board, piece, Node(board, piece, goals, [], 0)]

def search():
    initial_state = initialise()
    board = initial_state[0]
    piece = initial_state[1]
    initial_node = initial_state[2]
    nodes_explored = 0
    reached = dict() # graph-search
    frontier = [initial_node]
    heapq.heapify(frontier)
    while len(frontier) != 0:
        current = heapq.heappop(frontier)
        nodes_explored += 1
        if current.is_goal():
            return current.parents, nodes_explored, current.cost
        for a in current.get_actions():
            next_node = current.transition(a)
            if (next_node.piece.coord not in reached) or (reached[next_node.piece.coord] > next_node.fn):
                heapq.heappush(frontier, next_node)
                reached[next_node.piece.coord] = next_node.fn
    return [], nodes_explored, 0

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned