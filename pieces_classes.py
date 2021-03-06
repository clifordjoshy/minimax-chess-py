import pygame
import sys
import os

if getattr(sys, 'frozen', False):       #for pyinstaller resource
    Path = sys._MEIPASS              
else:
    Path = os.path.dirname(__file__) 



BOARD_DIMENSION = 8
BLACK_KING_POS = (4, 0)
WHITE_KING_POS = (4, 7)


def is_available(x, y, side, board_state):
    if 0 <= x < BOARD_DIMENSION and 0 <= y < BOARD_DIMENSION:
        if board_state[x][y] is None or board_state[x][y].dir_coeff != side:
            # either empty or opponents piece
            return True
    return False


def get_if_checked(side, board, black=None, white=None):
    king = None
    if black is None:
        black = [(x, y) for x in range(8) for y in range(8) if board[x][y] is not None and board[x][y].color == 'b']
    if white is None:
        white = [(x, y) for x in range(8) for y in range(8) if board[x][y] is not None and board[x][y].color == 'w']

    if side == 'w':
        check_for = black
        for piece in white:
            if board[piece[0]][piece[1]].__class__.__name__ == "King":
                king = piece

    else:
        check_for = white
        for piece in black:
            if board[piece[0]][piece[1]].__class__.__name__ == "King":
                king = piece

    for piece_pos in check_for:
        if board[piece_pos[0]][piece_pos[1]].__class__.__name__ != "King":
            # if statement prevents infinite recursion between opposite king checks. King check can't happen.
            if king in board[piece_pos[0]][piece_pos[1]].get_moves(piece_pos, board):
                return king

    return None


class Pawn:
    def __init__(self, color):
        self.dir_coeff = 1 if color == 'b' else -1  # black playing down the board\
        self.color = color
        self.image = pygame.image.load(os.path.join(Path, "resources/pawn_" + color + ".png"))
        self.points = 1 if color == 'b' else -1
        self.double_step_row = 1 if color == 'b' else 6
        self.promotion_row = 0 if color == 'w' else 7

    def get_moves(self, position, board_state):
        valid_moves = []
        if board_state[position[0]][position[1] + self.dir_coeff] is None: # stops being pawn at end. Avoid is_available
            if position[1] + self.dir_coeff != self.promotion_row:
                valid_moves.append((position[0], position[1] + self.dir_coeff))
            else:       # promotion
                valid_moves.append((position[0], position[1] + self.dir_coeff, Queen))
                valid_moves.append((position[0], position[1] + self.dir_coeff, Knight))
                valid_moves.append((position[0], position[1] + self.dir_coeff, Rook))
                valid_moves.append((position[0], position[1] + self.dir_coeff, Bishop))

            # second one only if first is available
            if position[1] == self.double_step_row and board_state[position[0]][position[1] + 2 * self.dir_coeff] is None:
                valid_moves.append((position[0], position[1] + 2 * self.dir_coeff))

        if is_available(position[0] - 1, position[1] + self.dir_coeff, self.dir_coeff, board_state) and \
                board_state[position[0] - 1][position[1] + self.dir_coeff] is not None:
            if position[1]+self.dir_coeff != self.promotion_row:
                valid_moves.append((position[0] - 1, position[1] + self.dir_coeff))
            else:
                valid_moves.append((position[0] - 1, position[1] + self.dir_coeff, Queen))
                valid_moves.append((position[0] - 1, position[1] + self.dir_coeff, Knight))
                valid_moves.append((position[0] - 1, position[1] + self.dir_coeff, Rook))
                valid_moves.append((position[0] - 1, position[1] + self.dir_coeff, Bishop))

        if is_available(position[0] + 1, position[1] + self.dir_coeff, self.dir_coeff, board_state) and \
                board_state[position[0] + 1][position[1] + self.dir_coeff] is not None:
            if position[1] + self.dir_coeff != self.promotion_row:
                valid_moves.append((position[0] + 1, position[1] + self.dir_coeff))
            else:
                valid_moves.append((position[0] + 1, position[1] + self.dir_coeff, Queen))
                valid_moves.append((position[0] + 1, position[1] + self.dir_coeff, Knight))
                valid_moves.append((position[0] + 1, position[1] + self.dir_coeff, Rook))
                valid_moves.append((position[0] + 1, position[1] + self.dir_coeff, Bishop))

        return valid_moves


class Rook:
    def __init__(self, color):
        self.dir_coeff = 1 if color == "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load(os.path.join(Path, "resources/rook_" + color + ".png"))
        self.points = 5 if color =='b' else -5
        self.can_castle = True

    def get_moves(self, position, board_state):
        valid_moves = []

        # horizontal scanning
        for i in range(1, position[0] + 1):
            if is_available(position[0] - i, position[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] - i, position[1]))
                if board_state[position[0] - i][position[1]] is not None:
                    break  # cant go through pieces
            else:
                break  # encountered own side pieces
        for i in range(position[0] + 1, BOARD_DIMENSION):
            if is_available(i, position[1], self.dir_coeff, board_state):
                valid_moves.append((i, position[1]))
                if board_state[i][position[1]] is not None:
                    break
            else:
                break

        # vertical scanning
        for i in range(1, position[1] + 1):
            if is_available(position[0], position[1] - i, self.dir_coeff, board_state):
                valid_moves.append((position[0], position[1] - i))
                if board_state[position[0]][position[1] - i] is not None:
                    break
            else:
                break
        for i in range(position[1] + 1, BOARD_DIMENSION):
            if is_available(position[0], i, self.dir_coeff, board_state):
                valid_moves.append((position[0], i))
                if board_state[position[0]][i] is not None:
                    break
            else:
                break

        return valid_moves


class Knight:
    def __init__(self, color):
        self.dir_coeff = 1 if color == "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load(os.path.join(Path, "resources/knight_" + color + ".png"))
        self.points = 3 if color =='b' else -3

    def get_moves(self, position, board_state):
        valid_moves = []

        move_increments = [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for update in move_increments:
            if is_available(position[0] + update[0], position[1] + update[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] + update[0], position[1] + update[1]))
        return valid_moves


class Bishop:
    def __init__(self, color):
        self.dir_coeff = 1 if color == "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load(os.path.join(Path, "resources/bishop_" + color + ".png"))
        self.points = 3 if color == 'b' else -3

    def get_moves(self, position, board_state):
        valid_moves = []
        pos_x = position[0] + 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y += 1

        pos_x = position[0] - 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y -= 1

        pos_x = position[0] - 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y += 1

        pos_x = position[0] + 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y -= 1

        return valid_moves


class Queen:
    def __init__(self, color):
        self.dir_coeff = 1 if color == "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load(os.path.join(Path, "resources/queen_" + color + ".png"))
        self.points = 10 if color == 'b' else -10

    def get_moves(self, position, board_state):  # rook + bishop
        valid_moves = []

        # horizontal scanning
        for i in range(1, position[0] + 1):
            if is_available(position[0] - i, position[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] - i, position[1]))
                if board_state[position[0] - i][position[1]] is not None:
                    break  # cant go through pieces
            else:
                break  # encountered own side pieces
        for i in range(position[0] + 1, BOARD_DIMENSION):
            if is_available(i, position[1], self.dir_coeff, board_state):
                valid_moves.append((i, position[1]))
                if board_state[i][position[1]] is not None:
                    break
            else:
                break

        # vertical scanning
        for i in range(1, position[1] + 1):
            if is_available(position[0], position[1] - i, self.dir_coeff, board_state):
                valid_moves.append((position[0], position[1] - i))
                if board_state[position[0]][position[1] - i] is not None:
                    break
            else:
                break
        for i in range(position[1] + 1, BOARD_DIMENSION):
            if is_available(position[0], i, self.dir_coeff, board_state):
                valid_moves.append((position[0], i))
                if board_state[position[0]][i] is not None:
                    break
            else:
                break

        # diagonal scanning
        pos_x = position[0] + 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y += 1

        pos_x = position[0] - 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y -= 1

        pos_x = position[0] - 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y += 1

        pos_x = position[0] + 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y -= 1

        return valid_moves


class King:
    def __init__(self, color):
        self.dir_coeff = 1 if color == "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load(os.path.join(Path, "resources/king_" + color + ".png"))
        self.points = 100 if color == 'b' else -100
        self.can_castle = True

    def get_moves(self, position, board_state):
        valid_moves = []
        move_increments = [(-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]

        for update in move_increments:
            if is_available(position[0] + update[0], position[1] + update[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] + update[0], position[1] + update[1]))

        if self.can_castle:
            # castling
            pos = BLACK_KING_POS if self.color == 'b' else WHITE_KING_POS
            if board_state[1][pos[1]] is None and board_state[2][pos[1]] is None and board_state[3][pos[1]] is None:
                if board_state[0][pos[1]] is not None and board_state[0][pos[1]].__class__.__name__ == "Rook" and \
                        board_state[0][pos[1]].can_castle and get_if_checked(self.color, board_state) is None:
                    valid_moves.append((2, pos[1]))
            if board_state[5][pos[1]] is None and board_state[6][pos[1]] is None:
                if board_state[7][pos[1]] is not None and board_state[7][pos[1]].__class__.__name__ == "Rook" and \
                        board_state[7][pos[1]].can_castle and get_if_checked(self.color, board_state) is None:
                    valid_moves.append((6, pos[1]))

        return valid_moves
