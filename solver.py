import pygame
import sys
import random
from board import *


class Solver:
    """Solves given board state"""

    class Node:
        """Single search node in a solver"""

        def __init__(self, board, parent, move):
            self.board = board
            self.parent = parent
            self.move = move
            self.children = []

            if self.parent is None:
                self.num_moves = self.y_coordinate = 0
            else:
                self.num_moves = self.y_coordinate = self.parent.num_moves + 1

            self.x_coordinate = -1
            self.modifier = 0

            self.thread = None
            self.offset = 0
            self.ancestor = self
            self.change = self.shift = 0
            self.left_sibling = None
            self.number = 1
            self.number_tested = 0

            # For on buffer processing:
            self.x_screen = None
            self.y_screen = None

        def __gt__(self, other):
            """Done to break comparing ties"""
            return True

        # Following methods are for tree_draw
        def left(self):
            return self.thread or len(self.children) and self.children[0]

        def right(self):
            return self.thread or len(self.children) and self.children[-1]

        def left_brother(self):
            n = None
            if self.parent:
                for node in self.parent.children:
                    if node == self:
                        return n
                    else:
                        n = node
            return n

        def get_lmost_sibling(self):
            if not self.left_sibling and self.parent and self != \
                    self.parent.children[0]:
                self.left_sibling = self.parent.children[0]
            return self.left_sibling

        leftmost_sibling = property(get_lmost_sibling)

    def __init__(self, board, depth_limit):
        self.init_state = self.Node(board, None, None)
        self.nodes = []
        self.num_tested = 0
        self.depth_limit = depth_limit

        self.history = {}
        self.list = []

    def next_node(self):
        """ chooses the next node to be tested from the list of
            untested node, removing it from the list and returning it
        """
        s = random.choice(self.nodes)
        if s.parent is not None:
            parent = s.parent
            parent.children += [s]
        self.nodes.remove(s)
        return s

    def generate_children(self, node):
        """creates and returns a list of all possible node children"""
        move = ['left', 'up', 'down', 'right']
        children = []
        for m in move:
            b = node.board.copy()
            if b.move_blank(m):
                s = self.Node(b, node, m)
                children += [s]
        return children

    def used(self, node):
        """checks if a node's board has been previously visited"""
        board = node.board
        node = node.parent
        while node is not None:
            if node.board == board:
                return True
            node = node.parent
        return False

    def can_add(self, node):
        """checks if it is possible to add a node to self.nodes"""
        if self.depth_limit < node.num_moves and self.depth_limit != -1:
            return False
        elif self.used(node):
            return False
        else:
            return True

    def add_node(self, new_node):
        self.nodes += [new_node]

    def add_nodes(self, new_nodes):
        for s in new_nodes:
            if self.can_add(s):
                self.add_node(s)

    def create_history(self, node):
        """ adds all the states the searcher tests to a dictionary while solving a problem
            to store the data
        """
        self.list += [node]
        if node.num_moves not in self.history:
            self.history[node.num_moves] = [node]
        else:
            self.history[node.num_moves] += [node]

    def solution(self):
        """Solves the slide puzzle"""
        self.add_node(self.init_state)

        while len(self.nodes) > 0:
            mousePosition = pygame.mouse.get_pos()
            # Makes exiting the loop possible while attempting to solve
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 970 < mousePosition[0] < 1040 and 645 < mousePosition[1] < 715:
                        return None

            s = self.next_node()
            self.create_history(s)
            s.number_tested = self.num_tested
            self.num_tested += 1
            if s.board.tiles == s.board.goal_tiles:
                return s
            else:
                children = self.generate_children(s)
                self.add_nodes(children)
        return None


class BFSolver(Solver):
    """A class that uses breadth first search"""
    def next_node(self):
        s = self.nodes[0]

        if s.parent is not None:
            parent = s.parent
            parent.children += [s]

        self.states.remove(s)
        return s


class DFSolver(Solver):
    """A class that uses depth first search"""
    def next_node(self):
        s = self.nodes[-1]

        if s.parent is not None:
            parent = s.parent
            parent.children += [s]

        self.nodes.remove(s)
        return s


class GreedySolver(Solver):
    """Class that uses greedy search"""
    def __init__(self, board, heuristic):
        super().__init__(board, -1)
        self.heuristic = heuristic

    def priority(self, node):
        return -1 * self.heuristic(node)

    def add_node(self, new_node):
        self.nodes += [[self.priority(new_node), new_node]]

    def next_node(self):
        s = max(self.nodes)

        if s[-1].parent is not None:
            parent = s[-1].parent
            parent.children += [s[-1]]

        self.nodes.remove(s)
        return s[-1]


class AStarSolver(GreedySolver):
    """class that uses A* search"""
    def priority(self, node):
        return -1 * (self.heuristic(node) + node.num_moves)


def h1(node):
    """ a heuristic function that always returns 0 """
    return node.board.get_heuristic("h1")


def h2(node):
    """ Takes a state and returns the number of misplaced tiles"""
    return node.board.get_heuristic("h2")


def h3(node):
    """Takes a state and returns the Manhattan distance each tile is from its goal tile"""
    return node.board.get_heuristic("h3")


def create_solver(board, algorithm, param):
    searcher = None

    if algorithm == 'Random':
        searcher = Solver(board, param)
    elif algorithm == 'BFS':
        searcher = BFSolver(board, param)
    elif algorithm == 'DFS':
        searcher = DFSolver(board, param)
    elif algorithm == 'Greedy':
        searcher = GreedySolver(board, param)
    elif algorithm == 'A*':
        searcher = AStarSolver(board, param)

    return searcher
