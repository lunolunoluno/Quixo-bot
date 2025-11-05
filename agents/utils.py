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


def check_for_winner(position: List[List[chr]]) -> Optional[Player]:
    for player in Player:
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


def print_pos(position: List[List[chr]]) -> None:
    print("_"*11)
    for row in position:
        row_str = "|"
        row_str += "|".join([' ' if c == '' else c for c in row])
        print(row_str + "|")

