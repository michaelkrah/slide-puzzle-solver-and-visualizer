import math

import pygame
from pygame import *

from solver import *
from tree_draw import *

display_width = 1080
display_height = 720
fps = 30
fps_clock = pygame.time.Clock()
buffer = pygame.display.set_mode((display_width, display_height))
pygame.font.init()

# global vars:

grey = (50, 50, 50)
dark_grey = (44, 44, 44)
darker_grey = (24, 24, 24)
light_blue = (116, 185, 255)
blue = (28, 93, 153)
white = (255, 255, 255)
red = (255, 82, 82)
green = (82, 255, 82)
yellow = (255, 255, 82)


class Screen:
    def __init__(self, board_size=3, board_pixels=540, board_center=(720, 360)):
        """Class for what is currently occurring on the screen"""
        self.board = Board(board_size)
        self.board_pixels = board_pixels
        self.board_center = board_center

        self.solution_root = None
        self.solution = None
        self.tree_coords_chosen = False

    def set_board(self, board_size):
        self.board = Board(board_size)
        self.draw_board(self.board, self.board_center, self.board_pixels)

    def draw_screen(self):
        buffer.fill(grey)
        if side_bar.side_type == "board":
            title = pygame.font.SysFont('Montserrat', 100).render('Slide Puzzle', True, white)
            buffer.blit(title, (510, 10))
            self.draw_board(self.board, self.board_center, self.board_pixels)
            self.draw_board_buttons()
        else:
            self.calculate_tree_coords()
            self.draw_tree()
        side_bar.draw_side()

    def set_type(self, side_type):
        buffer.fill(grey)
        if side_type == "board":
            self.draw_board(self.board, self.board_center, self.board_pixels)
            self.draw_board_buttons()
        else:
            self.calculate_tree_coords()
            self.draw_tree()
        side_bar.set_type(side_type)

    def draw_board(self, board, centerpoint, dimension):
        """creates board object in main buffer given a board object, an int dimension, and a tuple centerpoint,
        given in form (x, y)"""
        size = board.size
        font_board = pygame.font.SysFont("Times New Roman", int((dimension / size) // 2))
        for r in range(size):
            for c in range(size):
                if board.tiles[r][c] == '0':
                    pygame.draw.rect(buffer, light_blue, ((centerpoint[0] - (dimension / 2)) + ((dimension / size) * c),
                                                          (centerpoint[1] - (dimension / 2)) + ((dimension / size) * r),
                                                          dimension / size, dimension / size))
                else:
                    pygame.draw.rect(buffer, light_blue, ((centerpoint[0] - (dimension / 2)) + ((dimension / size) * c),
                                                          (centerpoint[1] - (dimension / 2)) + ((dimension / size) * r),
                                                          dimension / size, dimension / size))
                    pygame.draw.rect(buffer, blue, ((centerpoint[0] - (dimension / 2)) + ((dimension / size) * c) +
                                                    ((dimension / size) // 60), (centerpoint[1] - (dimension / 2)) +
                                                    ((dimension / size) * r) + ((dimension / size) // 60),
                                                    dimension / size - ((dimension / size) // 30),
                                                    dimension / size - ((dimension / size) // 30)))
                    number = font_board.render(board.tiles[r][c], True, white)
                    if len(board.tiles[r][c]) == 2:  # For centering numbers
                        n = 4.2
                    else:
                        n = 2.6
                    buffer.blit(number, (((centerpoint[0] - (dimension / 2)) + ((dimension / size) * c)) +
                                         ((dimension / size) / n),
                                         (centerpoint[1] - (dimension / 2)) + ((dimension / size) * r)
                                         + ((dimension / size) / 4)))

    def draw_board_buttons(self):
        """Draws the buttons for the board"""
        font_board = pygame.font.SysFont("Times New Roman", 30)
        # Mix
        pygame.draw.rect(buffer, darker_grey,
                         (self.board_center[0] + 45, self.board_center[1] + self.board_pixels // 2 + 10, 180, 70))

        pygame.draw.rect(buffer, darker_grey,
                         (self.board_center[0] - 225, self.board_center[1] + self.board_pixels // 2 + 10, 180, 70))

        mix = font_board.render('Mix', True, white)
        buffer.blit(mix, (self.board_center[0] - 255 + 95, self.board_center[1] + self.board_pixels // 2 + 10 + 15))
        solve = font_board.render('Solve', True, white)
        buffer.blit(solve, (self.board_center[0] + 45 + 55, self.board_center[1] + self.board_pixels // 2 + 10 + 15))

        pygame.draw.rect(buffer, darker_grey, (
        self.board_center[0] - self.board_pixels // 2 - 80, self.board_center[1] + self.board_pixels // 2 - 70, 70, 70))
        pygame.draw.rect(buffer, darker_grey, (
        self.board_center[0] - self.board_pixels // 2 - 80, self.board_center[1] + self.board_pixels // 2 - 150, 70,
        70))
        pygame.draw.rect(buffer, darker_grey, (
        self.board_center[0] - self.board_pixels // 2 - 80, self.board_center[1] + self.board_pixels // 2 - 230, 70,
        70))

        three = font_board.render('3', True, white)
        buffer.blit(three, (
        self.board_center[0] - self.board_pixels // 2 - 54, self.board_center[1] + self.board_pixels // 2 - 215))
        four = font_board.render('4', True, white)
        buffer.blit(four, (
        self.board_center[0] - self.board_pixels // 2 - 54, self.board_center[1] + self.board_pixels // 2 - 135))
        five = font_board.render('5', True, white)
        buffer.blit(five, (
        self.board_center[0] - self.board_pixels // 2 - 54, self.board_center[1] + self.board_pixels // 2 - 55))

    def mix_board(self, num_moves):
        directions = ['left', 'right', 'up', 'down']
        count = 0
        time_per = fps // 3
        for i in range(num_moves):
            choice = random.choice(directions)
            if self.board.move_blank(choice):
                piece = [self.board.blank_r, self.board.blank_c]

                if count < 12:
                    self.move_tile(choice, piece[0], piece[1], time_per)
                else:
                    self.move_tile(choice, piece[0], piece[1], 1)
                if time_per > 4:
                    time_per = int(time_per - 3)

                count += 1

    def solve_board(self):
        starting_board = Board(self.board.size)
        starting_board.place_tiles(self.board.list_creator())
        # starting_node = State(starting_board, None, "init")
        if side_bar.algorithm == 'Random' or side_bar.algorithm == 'DFS' or side_bar.algorithm == 'BFS':
            searcher = create_solver(starting_board, side_bar.algorithm, side_bar.max_depth)
        else:
            searcher = create_solver(starting_board, side_bar.algorithm, side_bar.parameter)

        if side_bar.algorithm is None:
            return None

        sol = None

        self.tree_coords_chosen = False
        sol = searcher.solution()
        self.solution = searcher
        self.solution_root = sol
        return sol

    def solve_board_display(self, solution):
        if solution.parent is None:
            return
        else:
            self.solve_board_display(solution.parent)
            self.board.move_blank(solution.move)
            piece = [self.board.blank_r, self.board.blank_c]
            self.move_tile(solution.move, piece[0], piece[1], fps // 3)

    def move_board(self, pos_x, pos_y):
        # Converts pixel chosen to the board coordinate
        top_left = [self.board_center[0] - self.board_pixels // 2, self.board_center[1] - self.board_pixels // 2]
        row = math.floor((pos_y - top_left[1]) / (self.board_pixels / self.board.size))
        col = math.floor((pos_x - top_left[0]) / (self.board_pixels / self.board.size))

        # Checks if there piece selected can be moved and then updates piece
        move = self.board.valid_move(row, col)
        if move:
            self.board.move_blank(move)
            self.move_tile(move, row, col, fps // 3)

    def move_tile(self, move, tile_row, tile_col, time):
        distance = self.board_pixels // self.board.size
        font_board = pygame.font.SysFont("Times New Roman", int((self.board_pixels / self.board.size) // 2))

        if move == "right":
            velocity = [-distance / time, 0]
            pos = [tile_row, tile_col - 1]
        elif move == "left":
            velocity = [distance / time, 0]
            pos = [tile_row, tile_col + 1]
        elif move == "up":
            velocity = [0, distance / time]
            pos = [tile_row + 1, tile_col]
        elif move == "down":
            velocity = [0, -distance / time]
            pos = [tile_row - 1, tile_col]

        top_left = [self.board_center[0] - self.board_pixels // 2, self.board_center[1] - self.board_pixels // 2]

        x = x_1 = top_left[0] + ((self.board_pixels / self.board.size) * tile_col)
        y = y_1 = top_left[1] + ((self.board_pixels / self.board.size) * tile_row)

        for i in range(1, time + 1):
            check_quit()
            x += velocity[0]
            y += velocity[1]

            # Updates the board every frame
            pygame.draw.rect(buffer, light_blue,
                             (x_1, y_1, self.board_pixels / self.board.size, self.board_pixels / self.board.size))
            pygame.draw.rect(buffer, blue, (
            x + ((self.board_pixels / self.board.size) // 60), y + ((self.board_pixels / self.board.size) // 60),
            self.board_pixels / self.board.size - ((self.board_pixels / self.board.size) // 30),
            self.board_pixels / self.board.size - ((self.board_pixels / self.board.size) // 30)))
            number = font_board.render(self.board.tiles[pos[0]][pos[1]], True, white)
            if len(self.board.tiles[pos[0]][pos[1]]) == 2:
                n = 4.2
            else:
                n = 2.6
            buffer.blit(number, (
            x + ((self.board_pixels / self.board.size) / n), y + ((self.board_pixels / self.board.size) / 4)
            , self.board_pixels / self.board.size, self.board_pixels / self.board.size))

            pygame.display.flip()
            fps_clock.tick(fps)

        self.draw_board(self.board, self.board_center, self.board_pixels)

    def calculate_tree_coords(self):
        """calculate tree coords"""
        if self.solution is not None and not self.tree_coords_chosen:
            num_ordering(self.solution.history)
            position_tree(self.solution.history[0][0])
            self.tree_coords_chosen = True

    def draw_tree(self):
        # if self.solution is None:
        #     return None

        x_corner = 240 - screen_state.offset_x
        y_corner = 80 - screen_state.offset_y
        x_length = 820 * screen_state.scale_x
        y_length = 620 * screen_state.scale_y

        if self.solution is None:
            return None

        root = self.solution.history[0][0]

        root.yScreen = y_corner + 0
        root.xScreen = x_corner + x_length // 2
        self.draw_node(root)

        length = len(self.solution.history[0])
        long_row = 0

        for i in range(len(self.solution.history)):
            if len(self.solution.history[i]) > length:
                length = len(self.solution.history[i])
                long_row = i

        max_coord = self.solution.history[long_row][-1].x_coordinate
        least_coord = self.solution.history[long_row][0].x_coordinate
        for j in self.solution.history:
            for k in self.solution.history[j]:
                if k.x_coordinate > max_coord:
                    max_coord = k.x_coordinate
                if k.x_coordinate < least_coord:
                    least_coord = k.x_coordinate
                if k.board.tiles == k.board.goal_tiles:
                    goal_state = k

        for l in range(1, len(self.solution.history)):
            for m in self.solution.history[l]:
                if max_coord != 0:
                    m.xScreen = (((m.x_coordinate + -least_coord) / (
                                max_coord + abs(least_coord))) * x_length) + x_corner
                else:
                    m.xScreen = root.xScreen
                m.yScreen = ((m.num_moves / len(self.solution.history)) * y_length) + y_corner
                self.draw_line(m)

        for l in range(0, len(self.solution.history)):
            for m in self.solution.history[l]:
                self.draw_node(m)
        if side_bar.line_property == "Default" and side_bar.node_property == "Default":
            self.draw_goal(goal_state)

    def draw_node(self, point):
        size_x = 5 * screen_state.scale_x
        size_y = 5 * screen_state.scale_y

        if side_bar.node_property == "Default":
            pygame.draw.rect(buffer, red, (175 + 5, 140 + 10, 25, 25))
        elif side_bar.node_property == "Order":
            pygame.draw.rect(buffer, red, (175 + 5, 190 + 10, 25, 25))
        elif side_bar.node_property == "Depth":
            pygame.draw.rect(buffer, red, (175 + 5, 240 + 10, 25, 25))
        elif side_bar.node_property == "Board":
            pygame.draw.rect(buffer, red, (175 + 5, 290 + 10, 25, 25))

        if side_bar.node_property == "Default":
            buffer.fill(red, ((point.xScreen - math.ceil((size_y * screen_state.node_scale) / 2), point.yScreen - math.ceil((size_y * screen_state.node_scale) / 2)), (size_y * screen_state.node_scale, size_y * screen_state.node_scale)))
        elif side_bar.node_property == "Order":
            """draw order nodes were chosen in """
            buffer.fill(red, ((point.xScreen - math.ceil((size_y * screen_state.node_scale) / 2), point.yScreen - math.ceil((size_y * screen_state.node_scale) / 2)), (size_y * screen_state.node_scale, size_y * screen_state.node_scale)))
            num = pygame.font.SysFont("Times New Roman", int(5 * screen_state.scale_y * screen_state.node_scale)).render(str(point.number_tested), True, white)
            n = 0
            if len(str(point.number_tested)) == 1:
                n = .5
            buffer.blit(num, (point.xScreen - math.ceil((size_y * screen_state.node_scale) / 2) * (1-n), point.yScreen - math.ceil((size_y * screen_state.node_scale) / 2)))
        elif side_bar.node_property == "Depth":
            """Draw depth"""
        elif side_bar.node_property == "Board":
            self.draw_board(point.board, (point.xScreen, point.yScreen), size_y * screen_state.node_scale)

    def draw_line(self, point):
        if point.parent is not None:
            color_line = red
            if side_bar.line_property == "Multi":
                if point.move == "left":
                    color_line = green
                elif point.move == "right":
                    color_line = yellow
                elif point.move == "up":
                    color_line = blue
                elif point.move == "down":
                    color_line = red
            size_x = 5 * screen_state.scale_x
            size_y = 5 * screen_state.scale_y

            if side_bar.node_property != "Board":
                pygame.draw.line(buffer, color_line, (point.xScreen, point.yScreen),
                                 (point.parent.xScreen, point.parent.yScreen))
            else:
                pygame.draw.line(buffer, color_line, (point.xScreen, point.yScreen),
                                 (point.parent.xScreen, point.parent.yScreen))

    def draw_goal(self, point):
        size_x = 5 * screen_state.scale_x
        size_y = 5 * screen_state.scale_y
        while point.parent is not None:
            pygame.draw.line(buffer, green, (point.xScreen, point.yScreen),
                             (point.parent.xScreen, point.parent.yScreen))
            buffer.fill(green,
                        ((point.xScreen - math.ceil((size_y * screen_state.node_scale) / 2), point.yScreen - math.ceil((size_y * screen_state.node_scale) / 2)),
                         (size_y * screen_state.node_scale, size_y * screen_state.node_scale)))
            point = point.parent
        buffer.fill(green,
                    ((point.xScreen - math.ceil((size_y * screen_state.node_scale) / 2), point.yScreen - math.ceil((size_y * screen_state.node_scale) / 2)),
                     (size_y * screen_state.node_scale, size_y * screen_state.node_scale)))


class ScreenState:
    def __init__(self):
        """Class to record current screen parameters"""
        self.offset_x = 0
        self.offset_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.panning_state = False
        self.world_x = self.world_y = 0
        self.screen_x = self.screen_y = 0
        self.start_pan_x = self.start_pan_y = 0
        self.algorithm_menu = True
        self.searcher = None
        self.mouse_down = False
        self.node_scale = 1

    def world_to_screen(self, world_x, world_y):
        screen_x = int(world_x - self.offset_x) * self.scale_x
        screen_y = int(world_y - self.offset_y) * self.scale_y
        return [screen_x, screen_y]

    def screen_to_world(self, screen_x, screen_y):
        world_x = screen_x / self.scale_x + self.offset_x
        world_y = screen_y / self.scale_y + self.offset_y
        return [world_x, world_y]

    def reset(self):
        self.offset_x = 0
        self.offset_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.node_scale = 1


class SideBar:
    def __init__(self, side_type="board", algorithm="Random", parameter=h1, max_depth=20, node_property="Default",
                 line_property="Default"):
        """Class to record current algorithm properties"""
        self.side_type = side_type
        self.font_title = pygame.font.SysFont("Times New Roman", 40)
        self.font_descriptor = pygame.font.SysFont("Times New Roman", 30)
        self.algorithm = algorithm
        self.parameter = parameter
        self.max_depth = max_depth
        self.node_property = node_property
        self.line_property = line_property

    def set_type(self, side_type):
        self.side_type = side_type
        self.draw_side()

    def set_state(self, algo):
        self.algorithm = algo
        self.draw_state()

    def draw_state(self):
        starting_height = 150
        for i in ['Random:', 'BFS:', 'DFS:', 'Greedy:', 'A*:']:
            pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5, 35, 35))
            starting_height += 50

        if self.algorithm == 'Random':
            pygame.draw.rect(buffer, red, (175 + 5, 150 + 10, 25, 25))
        elif self.algorithm == 'BFS':
            pygame.draw.rect(buffer, red, (175 + 5, 200 + 10, 25, 25))
        elif self.algorithm == 'DFS':
            pygame.draw.rect(buffer, red, (175 + 5, 250 + 10, 25, 25))
        elif self.algorithm == 'Greedy':
            pygame.draw.rect(buffer, red, (175 + 5, 300 + 10, 25, 25))
        elif self.algorithm == 'A*':
            pygame.draw.rect(buffer, red, (175 + 5, 350 + 10, 25, 25))

    def set_parameter(self, param):
        self.parameter = param
        self.draw_parameter()

    def draw_parameter(self):
        starting_height = 570
        for i in ['H1:', 'H2:', 'H3:']:
            pygame.draw.rect(buffer, darker_grey, (175, starting_height, 35, 35))
            starting_height += 50

            if self.parameter == h1:
                pygame.draw.rect(buffer, red, (175 + 5, 570 + 5, 25, 25))
            elif self.parameter == h2:
                pygame.draw.rect(buffer, red, (175 + 5, 620 + 5, 25, 25))
            elif self.parameter == h3:
                pygame.draw.rect(buffer, red, (175 + 5, 670 + 5, 25, 25))

    def set_depth(self, depth):
        self.max_depth = depth
        self.draw_depth()

    def draw_depth(self):
        """Draws the depth slider"""
        x = (self.max_depth * 3 + 10) + 1
        pygame.draw.rect(buffer, dark_grey, (0, 515, 220, 50))

        pygame.draw.rect(buffer, darker_grey, (10, 535, 150, 5))
        pygame.draw.circle(buffer, white, (x, 537), 10, 10)
        num = self.font_descriptor.render(str(self.max_depth), True, white)
        buffer.blit(num, (175, 520))

    def draw_offset(self):
        offset = self.font_descriptor.render(
            "(" + str(int(screen_state.offset_x)) + ", " + str(int(screen_state.offset_y)) + ")", True, white)
        buffer.blit(offset, (65, 570))
        scale = self.font_descriptor.render(str(round(screen_state.scale_x, 2)), True, white)
        buffer.blit(scale, (165, 620))

    def set_node_property(self, node_property):
        self.node_property = node_property
        self.draw_node_property()

    def draw_node_property(self):
        starting_height = 140
        for i in ['Node:', 'Node Order:', 'Board:']:
            pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5, 35, 35))
            starting_height += 50

        if self.node_property == "Default":
            pygame.draw.rect(buffer, red, (175 + 5, 140 + 10, 25, 25))
        elif self.node_property == "Order":
            pygame.draw.rect(buffer, red, (175 + 5, 190 + 10, 25, 25))
        elif self.node_property == "Board":
            pygame.draw.rect(buffer, red, (175 + 5, 240 + 10, 25, 25))

    def set_line_property(self, line_property):
        self.line_property = line_property
        self.draw_line_property()

    def draw_line_property(self):
        starting_height = 410
        for i in ["Single:", "Multi:"]:
            pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5, 35, 35))
            starting_height += 50

        if self.line_property == "Default":
            pygame.draw.rect(buffer, red, (175 + 5, 410 + 10, 25, 25))
        elif self.line_property == "Multi":
            pygame.draw.rect(buffer, red, (175 + 5, 460 + 10, 25, 25))

    def reset_tree(self):
        self.node_property = "Default"
        self.line_property = "Default"
        screen_state.reset()

    def draw_side(self):
        """Draws to buffer the sidebar needed when changing types"""
        pygame.draw.rect(buffer, dark_grey, (0, 0, 220, 720))
        if self.side_type == "board":
            self.draw_side_board()
        else:
            self.draw_side_tree()

    def draw_side_board(self):
        """Draws the sidebar for the board screen state"""
        pygame.draw.rect(buffer, darker_grey, (110, 0, 110, 70))
        board_text = self.font_title.render("Board", True, white)
        buffer.blit(board_text, (5, 10))
        tree_text = self.font_title.render("Tree", True, white)
        buffer.blit(tree_text, (130, 10))
        algorithm = self.font_title.render('Algorithm', True, white)
        buffer.blit(algorithm, (28, 80))
        starting_height = 150
        for i in ['Random:', 'BFS:', 'DFS:', 'Greedy:', 'A*:']:
            algo = self.font_descriptor.render(i, True, white)
            buffer.blit(algo, (10, starting_height))
            pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5, 35, 35))
            starting_height += 50
        self.draw_state()

        heuristic = self.font_title.render('Heuristic', True, white)
        buffer.blit(heuristic, (28, 420))
        algo = self.font_descriptor.render("Depth:", True, white)
        buffer.blit(algo, (10, 480))
        starting_height = 570
        for i in ['H1:', 'H2:', 'H3:']:
            algo = self.font_descriptor.render(i, True, white)
            buffer.blit(algo, (10, starting_height))
            pygame.draw.rect(buffer, darker_grey, (175, starting_height, 35, 35))
            starting_height += 50
        self.draw_parameter()

        self.draw_depth()

    def draw_side_tree(self):
        """Draws the sidebar for the tree screen state"""
        pygame.draw.rect(buffer, darker_grey, (0, 0, 110, 70))
        board_text = self.font_title.render("Board", True, white)
        buffer.blit(board_text, (5, 10))
        tree_text = self.font_title.render("Tree", True, white)
        buffer.blit(tree_text, (130, 10))

        node = self.font_title.render('Node Type', True, white)
        buffer.blit(node, (23, 80))
        starting_height = 140
        for i in ['Node:', 'Node Order:', 'Board:']:
            title = self.font_descriptor.render(i, True, white)
            buffer.blit(title, (10, starting_height))
            pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5, 35, 35))
            starting_height += 50

        node_scale = self.font_descriptor.render("Node Scale:", True, white)
        buffer.blit(node_scale, (10, starting_height))
        scale_node = self.font_descriptor.render(str(round(screen_state.node_scale, 1)), True, white)
        buffer.blit(scale_node, (160, starting_height))

        line = self.font_title.render('Line Type', True, white)
        buffer.blit(line, (23, 350))
        starting_height = 410
        for i in ["Single:", "Multi:"]:
            title = self.font_descriptor.render(i, True, white)
            buffer.blit(title, (10, starting_height))
            pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5, 35, 35))
            starting_height += 50

        line = self.font_title.render('Screen', True, white)
        buffer.blit(line, (40, 510))
        starting_height = 570
        for i in ["Pos:", "Scale:", "Reset:"]:
            title = self.font_descriptor.render(i, True, white)
            buffer.blit(title, (10, starting_height))
            starting_height += 50
        pygame.draw.rect(buffer, darker_grey, (175, starting_height + 5 - 50, 35, 35))
        self.draw_node_property()
        self.draw_line_property()

        self.draw_offset()


screen = Screen()
side_bar = SideBar()
screen_state = ScreenState()


def check_quit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)


def main():
    """Main game loop and setup"""
    pygame.init()
    pygame.display.set_caption('Slide Puzzle')

    buffer.fill(grey)

    screen.draw_screen()
    running = True
    while running:

        check_quit()
        for event in pygame.event.get():

            mouse_position = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen_state.mouse_down = True
                screen_state.start_pan_x = mouse_position[0]
                screen_state.start_pan_y = mouse_position[1]
                screen_state.panning_state = True

                if 0 <= mouse_position[0] < 110 and 0 <= mouse_position[1] < 70:
                    # clicked board
                    screen.set_type("board")
                    side_bar.reset_tree()

                if 110 <= mouse_position[0] < 220 and 0 <= mouse_position[1] < 70:
                    # clicked tree
                    screen.set_type("tree")

                if 175 <= mouse_position[0] < 210 and 155 <= mouse_position[1] < 190 and side_bar.side_type == "board":
                    side_bar.set_state("Random")

                if 175 <= mouse_position[0] < 210 and 205 <= mouse_position[1] < 240 and side_bar.side_type == "board":
                    side_bar.set_state("BFS")

                if 175 <= mouse_position[0] < 210 and 255 <= mouse_position[1] < 290 and side_bar.side_type == "board":
                    side_bar.set_state("DFS")

                if 175 <= mouse_position[0] < 210 and 305 <= mouse_position[1] < 340 and side_bar.side_type == "board":
                    side_bar.set_state("Greedy")

                if 175 <= mouse_position[0] < 210 and 355 <= mouse_position[1] < 390 and side_bar.side_type == "board":
                    side_bar.set_state("A*")

                if 175 <= mouse_position[0] < 210 and 570 <= mouse_position[1] < 605 and side_bar.side_type == "board":
                    side_bar.set_parameter(h1)

                if 175 <= mouse_position[0] < 210 and 620 <= mouse_position[1] < 655 and side_bar.side_type == "board":
                    side_bar.set_parameter(h2)

                if 175 <= mouse_position[0] < 210 and 670 <= mouse_position[1] < 705 and side_bar.side_type == "board":
                    side_bar.set_parameter(h3)

                if 175 <= mouse_position[0] < 210 and 145 <= mouse_position[1] < 180 and side_bar.side_type == "tree":
                    side_bar.set_node_property("Default")

                if 175 <= mouse_position[0] < 210 and 195 <= mouse_position[1] < 230 and side_bar.side_type == "tree":
                    side_bar.set_node_property("Order")

                if 175 <= mouse_position[0] < 210 and 245 <= mouse_position[1] < 280 and side_bar.side_type == "tree":
                    side_bar.set_node_property("Board")

                if 175 <= mouse_position[0] < 210 and 415 <= mouse_position[1] < 445 and side_bar.side_type == "tree":
                    side_bar.set_line_property("Default")

                if 175 <= mouse_position[0] < 210 and 460 <= mouse_position[1] < 495 and side_bar.side_type == "tree":
                    print("here")
                    side_bar.set_line_property("Multi")

                if 175 <= mouse_position[0] < 210 and 675 <= mouse_position[1] <= 705 and side_bar.side_type == "tree":
                    screen_state.reset()

                if 450 <= mouse_position[0] < 990 and 90 <= mouse_position[1] < 630 and side_bar.side_type == "board":
                    screen.move_board(mouse_position[0], mouse_position[1])

                if 495 <= mouse_position[0] < 675 and 640 <= mouse_position[1] < 710 and side_bar.side_type == "board":
                    screen.mix_board(random.randint(30, 60))

                if 765 <= mouse_position[0] < 945 and 640 <= mouse_position[1] < 710 and side_bar.side_type == "board":

                    X = pygame.font.SysFont('Montserrat', 100).render('X', True, red)
                    pygame.draw.rect(buffer, grey, (220, 655, 250, 70))
                    buffer.blit(X, (970, 645))
                    pygame.display.flip()
                    solution = screen.solve_board()
                    pygame.draw.rect(buffer, grey, (970, 645, 70, 70))
                    pygame.display.flip()
                    if solution is not None:
                        screen.solve_board_display(solution)
                    else:
                        result = pygame.font.SysFont('Times New Roman', 30).render('No solution reached', True, white)
                        buffer.blit(result, (220, 655))

                if 370 <= mouse_position[0] < 440 and 400 <= mouse_position[1] < 470 and side_bar.side_type == "board":
                    screen.set_board(3)
                if 370 <= mouse_position[0] < 440 and 480 <= mouse_position[1] < 550 and side_bar.side_type == "board":
                    screen.set_board(4)
                if 370 <= mouse_position[0] < 440 and 560 <= mouse_position[1] < 630 and side_bar.side_type == "board":
                    screen.set_board(5)

            mouse_prezoom_x, mouse_prezoom_y = screen_state.screen_to_world(mouse_position[0], mouse_position[1])

            if keys[pygame.K_e] and side_bar.side_type == "tree":
                if screen_state.scale_x < 10:
                    if screen_state.scale_x * 1.01 > 10:
                        screen_state.scale_x = 10
                        screen_state.scale_y = 10
                    else:
                        screen_state.scale_x *= 1.01
                        screen_state.scale_y *= 1.01

            if keys[pygame.K_q] and side_bar.side_type == "tree":
                if .4 < screen_state.scale_x:
                    screen_state.scale_x *= 0.99
                    screen_state.scale_y *= 0.99

            if keys[pygame.K_c] and side_bar.side_type == "tree":
                if screen_state.scale_x < 10:
                    screen_state.scale_x *= 1.01

            if keys[pygame.K_z] and side_bar.side_type == "tree":
                if .4 < screen_state.scale_x:
                    screen_state.scale_x *= 0.99

            if keys[pygame.K_d] and side_bar.side_type == "tree":
                if screen_state.node_scale < 100:
                    if screen_state.node_scale * 1.05 > 100:
                        screen_state.node_scale = 100
                    else:
                        screen_state.node_scale *= 1.05

            if keys[pygame.K_a] and side_bar.side_type == "tree":
                if 0.1 < screen_state.node_scale:
                    screen_state.node_scale *= 0.95

            mouse_postzoom_x, mouse_postzoom_y = screen_state.screen_to_world(mouse_position[0], mouse_position[1])

            if side_bar.side_type == "tree":
                screen_state.offset_x += mouse_prezoom_x - mouse_postzoom_x
                screen_state.offset_y += mouse_prezoom_y - mouse_postzoom_y

            if event.type == pygame.MOUSEBUTTONUP:
                screen_state.mouse_down = False
                screen_state.panning_state = False

            if 10 < mouse_position[0] < 160 and 515 < mouse_position[1] < 565 and side_bar.side_type == "board" and screen_state.mouse_down:
                # Click on the slider for depth
                depth = math.ceil((mouse_position[0] - 10) / 3)
                side_bar.set_depth(depth)

            if screen_state.panning_state and side_bar.side_type == "tree":
                screen_state.offset_x -= (mouse_position[0] - screen_state.start_pan_x) / screen_state.scale_x
                screen_state.offset_y -= (mouse_position[1] - screen_state.start_pan_y) / screen_state.scale_y
                screen_state.start_pan_x = mouse_position[0]
                screen_state.start_pan_y = mouse_position[1]

            if keys[pygame.K_m]:
                screen_state.reset()
                side_bar.board_scale = 1

            if side_bar.side_type == "tree":
                buffer.fill(grey)
                screen.draw_tree()
                side_bar.draw_side()

        # Updates buffer after every action
        pygame.display.update()
        fps_clock.tick(fps)


# Press the blue button in the gutter to run the script.
if __name__ == '__main__':
    main()
