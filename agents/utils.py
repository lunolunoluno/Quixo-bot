from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass

# CLASSES
# =========================================

@dataclass
class Move():
    source: Tuple[int, int]
    dest: Tuple[int, int]

class Player(Enum):
    X = 1
    O = 2

class BotClassModel:
    def play(self, position: List[List[chr]], player: Player) -> Tuple[Move, float, List[List[chr]]]:
        move, eval, new_pos = self.play_position(position, player)
        return (move, eval, new_pos)

# CONST
# =========================================

INITPOS = [['' for _ in range(5)] for _ in range(5)]

# FUNCTIONS
# =========================================

def get_opposite_player(player: Player) -> Player:
    return Player.X if player == Player.O else Player.O

def get_all_legal_moves(position: List[List[chr]], player: Player) -> List[Move]:
    moves = []
    for i, row in enumerate(position):
        for j, cell in enumerate(row):  
            notplayer = get_opposite_player(player)
            if cell is not notplayer.name:
                if i == 0 or i == 4 or j == 0 or j == 4:
                    source = (i, j)
                    if i != 0:
                        moves.append(Move(source, (0, j)))
                    if i != 4:
                        moves.append(Move(source, (4, j)))
                    if j != 0:
                        moves.append(Move(source, (i, 0)))
                    if j != 4:
                        moves.append(Move(source, (i, 4)))

    return moves

def get_position_after_move(position: List[List[chr]], move: Move, player: Player) -> List[List[chr]]:  
    new_pos = [row[:] for row in position]  # make a copy to avoid modifying in place
    src_r, src_c = move.source
    dst_r, dst_c = move.dest
    value = player.name

    # same row
    if src_r == dst_r:
        row = new_pos[src_r]
        if src_c < dst_c:
            # shift left to right
            for j in range(src_c, dst_c):
                row[j] = row[j + 1]
        else:
            # shift right to left
            for j in range(src_c, dst_c, -1):
                row[j] = row[j - 1]
        row[dst_c] = value

    # same column
    elif src_c == dst_c:
        if src_r < dst_r:
            # shift up to down
            for i in range(src_r, dst_r):
                new_pos[i][src_c] = new_pos[i + 1][src_c]
        else:
            # shift down to up
            for i in range(src_r, dst_r, -1):
                new_pos[i][src_c] = new_pos[i - 1][src_c]
        new_pos[dst_r][src_c] = value

    else:
        raise ValueError("Source and destination must be in the same row or column")

    return new_pos


def convert_position_to_string(position: List[List[chr]], player: Player) -> str:
    string_pos = player.name
    string_pos += "".join([
        '.' if c=='' else c for row in position for c in row
    ])
    return string_pos


def convert_position_to_bitboard(position: List[List[chr]]) -> int:
    bit_x = int(''.join('1' if c==Player.X.name else '0' for row in position for c in row), 2)
    bit_o = int(''.join('1' if c==Player.O.name else '0' for row in position for c in row), 2)
    bit_board = bit_o | (bit_x << 32)
    return bit_board


def convert_bitboard_to_position(bitboard: int) -> List[List[chr]]:
    bit_o_str = format((0xffffffff & bitboard), '025b')
    bit_x_str = format((bitboard >> 32), '025b')
    pos = [['' for _ in range(5)] for _ in range(5)]
    for i, (os, xs) in enumerate(zip(bit_o_str, bit_x_str)):
        if os == '1':
            pos[i // 5][i % 5] = "O"
        if xs == '1':
            pos[i // 5][i % 5] = "X"
    return pos


def bitboard_play_move(bitboard: int, move: Move, player: Player) -> int:
    start = 24 - (move.source[0] * 5 + move.source[1])
    end = 24 - (move.dest[0] * 5 + move.dest[1])
    # row move
    if move.source[0] == move.dest[0]:
        # Right-pushing move
        if move.source[1] > move.dest[1]:
            bb_shift_area = ((1 << (end - start + 1)) - 1) << start
            bb_shift_area = bb_shift_area | (bb_shift_area << 32)
            # shift all bits of the area to the right
            bb_after_shift = (bitboard & ~bb_shift_area) | ((bitboard & bb_shift_area) >> 1) & bb_shift_area
            
        # Left-pushing move
        if move.source[1] < move.dest[1]:
            bb_shift_area = ((1 << (start - end + 1)) - 1) << end
            bb_shift_area = bb_shift_area | (bb_shift_area << 32)
            # shift all bits of the area to the left
            bb_after_shift = (bitboard & ~bb_shift_area) | ((bitboard & bb_shift_area) << 1) & bb_shift_area

        # set to 1 the bit that represent the new piece/moved piece
        bb_after_shift |= (1 << end) if player == Player.O else (1 << end + 32)
        return bb_after_shift
    
    # column move
    if move.source[1] == move.dest[1]:
        col_id_reversed = 4 - move.source[1]
        start_row_id_reversed = 4 - move.source[0]
        end_row_id_reversed = 4 - move.dest[0]

        # Down-pushing move
        if move.source[0] > move.dest[0]:
            bb_shift_area = 0
            for i in range(start_row_id_reversed * 5, (end_row_id_reversed + 1) * 5, 5):
                bb_shift_area |= (1 << i + col_id_reversed)
            bb_shift_area = bb_shift_area | (bb_shift_area << 32)
            # shift all bits of the area down
            bb_after_shift = (bitboard & ~bb_shift_area) | (((bitboard & bb_shift_area) >> 5) & bb_shift_area)
        
        # Up-pushing move
        if move.source[0] < move.dest[0]:
            bb_shift_area = 0
            for i in range(end_row_id_reversed * 5, (start_row_id_reversed + 1) * 5, 5):
                bb_shift_area |= (1 << i + col_id_reversed)
            bb_shift_area = bb_shift_area | (bb_shift_area << 32)
            # shift all bits of the area up
            bb_after_shift = (bitboard & ~bb_shift_area) | (((bitboard & bb_shift_area) << 5) & bb_shift_area)

        # set to 1 the bit that represent the new piece/moved piece
        bb_after_shift |= (1 << end) if player == Player.O else (1 << end + 32)
        return bb_after_shift

    return 0


def check_for_winner(position: List[List[chr]], player: Player) -> Optional[Player]:
    # Start with the opponent because if a player creates two lines with distinct symbols in a single turn, 
    # then the opponent is the winner
    players = [get_opposite_player(player), player]
    for player in players:
        # check row
        for row in position:
            if all(cell == player.name for cell in row):
                return player

        # check column
        for col in range(5):
            if all(position[row][col] == player.name for row in range(5)):
                return player

        # check main diagonal (top-left -> bottom-right)
        if all(position[i][i] == player.name for i in range(5)):
            return player

        # check anti-diagonal (top-right -> bottom-left)
        if all(position[i][5 - 1 - i] == player.name for i in range(5)):
            return player
    return None


def check_for_winner_bitboard(bitboard: int, player: Player) -> Optional[Player]:
    bits_o = (0xffffffff & bitboard)
    bits_x = (bitboard >> 32)
    def __is_winning(bits: int) -> bool:
        # Check rows
        for i in range(0, 25, 5):
            check_row_area = ((1 << 5) - 1) << i
            if check_row_area & bits == check_row_area:
                return True
        # Check for column
        check_col_areas = [
            0x108421,
            0x210842, 
            0x421084,
            0x842108,
            0x1084210
        ]
        for area in check_col_areas:
            if area & bits == area:
                return True
        # Check diagonals
        if bits & 0x1041041 == 0x1041041:
            # Main diagonal
            return True
        if bits & 0x111110 == 0x111110:
            # Anti diagonal
            return True
        return False
    if player == Player.O:
        if __is_winning(bits_x):
            return Player.X
        if __is_winning(bits_o):
            return Player.O
    else:
        if __is_winning(bits_o):
            return Player.O
        if __is_winning(bits_x):
            return Player.X
    return None


def print_pos(position: List[List[chr]]) -> None:
    print("_"*11)
    for row in position:
        row_str = "|"
        row_str += "|".join([' ' if c == '' else c for c in row])
        print(row_str + "|")

