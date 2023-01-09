# Board Class

class Board:
    """Board Data Class"""

    def __init__(self, size):
        """Initializes the board class"""
        self.size = size
        self.tiles = [[''] * size for x in range(size)]
        self.goal_tiles = [[''] * size for x in range(size)]

        self.blank_r = 0
        self.blank_c = 0

        count = 0
        for r in range(size):
            for c in range(size):
                self.tiles[r][c] = self.goal_tiles[r][c] = str(count)
                count += 1

    def __repr__(self):
        """Representation of the Board class"""
        lengthTwo = (self.size > 3)
        rep = ''
        for r in range(self.size):
            for c in range(self.size):
                if self.tiles[r][c] == '0':
                    rep += '_ '
                    if lengthTwo:
                        rep += ' '
                else:
                    rep += self.tiles[r][c] + ' '
                    if len(self.tiles[r][c]) == 1 and lengthTwo:
                        rep += ' '
            rep += '\n'
        return rep

    def __eq__(self, other):
        """Compares if tow board objects are the same"""
        return self.tiles == other.tiles

    def list_creator(self):
        """creates and returns a list of digits that corresponds to the current
            contents of the called Board object’s tiles attribute
        """
        lst = []
        for r in range(self.size):
            for c in range(self.size):
                lst += [str(self.tiles[r][c])]

        return lst

    def place_tiles(self, lst):
        """Changes the board to the list shown, can be a list of ints or strings"""
        # Makes sure all numbers in the list
        assert (len(lst) == (self.size ** 2))
        for i in range(self.size ** 2):
            assert (str(i) in lst or i in lst)

        count = 0
        for r in range(self.size):
            for c in range(self.size):
                self.tiles[r][c] = str(lst[count])
                if lst[count] == '0':
                    self.blank_r = r
                    self.blank_c = c
                count += 1

        count = 0
        for r in range(self.size):
            for c in range(self.size):
                self.tiles[r][c] = str(lst[count])
                if lst[count] == '0':
                    self.blank_r = r
                    self.blank_c = c
                count += 1

    def move_blank(self, direction):
        """ takes as input a string direction that specifies the direction
            in which the blank should move, and attempts to modify the
            contents of the called Board object accordingly
        """
        if direction == 'up':
            if self.blank_r == 0:
                return False
            else:
                tile = self.tiles[self.blank_r - 1][self.blank_c]
                self.tiles[self.blank_r - 1][self.blank_c] = '0'
                self.tiles[self.blank_r][self.blank_c] = tile
                self.blank_r -= 1
                return True
        elif direction == 'down':
            if self.blank_r == (self.size - 1):
                return False
            else:
                tile = self.tiles[self.blank_r + 1][self.blank_c]
                self.tiles[self.blank_r + 1][self.blank_c] = '0'
                self.tiles[self.blank_r][self.blank_c] = tile
                self.blank_r += 1
                return True
        elif direction == 'left':
            if self.blank_c == 0:
                return False
            else:
                tile = self.tiles[self.blank_r][self.blank_c - 1]
                self.tiles[self.blank_r][self.blank_c - 1] = '0'
                self.tiles[self.blank_r][self.blank_c] = tile
                self.blank_c -= 1
                return True
        elif direction == 'right':
            if self.blank_c == (self.size - 1):
                return False
            else:
                tile = self.tiles[self.blank_r][self.blank_c + 1]
                self.tiles[self.blank_r][self.blank_c + 1] = '0'
                self.tiles[self.blank_r][self.blank_c] = tile
                self.blank_c += 1
                return True
        else:
            return False

    def copy(self):
        """creates a copy to the current board state"""
        b2 = Board(self.size)
        move = self.list_creator()
        b2.place_tiles(move)
        return b2

    def valid_move(self, row, col):
        """Returns the direction the piece located at position (row, col) can be moved. If no move possible, returns None"""
        if col != 0 and self.tiles[row][col - 1] == '0':
            return 'right'
        if col != (self.size - 1) and self.tiles[row][col + 1] == '0':
            return 'left'
        if row != 0 and self.tiles[row - 1][col] == '0':
            return 'down'
        if row != (self.size - 1) and self.tiles[row + 1][col] == '0':
            return 'up'

        return None

    # For heuristics:

    def get_heuristic(self, heuristic):
        if heuristic == "h1":
            return 0
        elif heuristic == "h2":
            return self.num_misplaced()
        elif heuristic == "h3":
            return self.length_from_target()

    def num_misplaced(self):
        """ counts and returns the number of tiles in the called Board object
            that are not where they should be in the goal state
        """
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.tiles[r][c] != '0':
                    if self.tiles[r][c] != self.goal_tiles[r][c]:
                        count += 1
        return count

    def length_from_target(self):
        """ Finds how far each tile is from goal state (Manhattan distance)"""
        count = 0
        r_current = -1
        c_current = -1
        r_goal = -1
        c_goal = -1
        for i in range(1, self.size ** 2):
            for r in range(self.size):
                for c in range(self.size):
                    if self.tiles[r][c] == str(i):
                        r_current = r
                        c_current = c
            for r in range(3):
                for c in range(3):
                    if self.goal_tiles[r][c] == str(i):
                        r_goal = r
                        c_goal = c

            count += (abs(r_goal - r_current) + abs(c_goal - c_current))

        return count
