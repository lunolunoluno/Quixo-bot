import random

from agents.utils import BotClassModel, Move, Player, get_all_legal_moves, get_position_after_move
from typing import List, Tuple


class RandomBot(BotClassModel):
    def play_position(self, position: List[List[chr]], player: Player)-> Tuple[Move, float, List[List[chr]]]:
        m = random.choice(get_all_legal_moves(position, player))
        new_pos = get_position_after_move(position, m, player)
        return (m, 0.0, new_pos)