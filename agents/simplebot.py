import random

from agents.utils import BotClassModel, Move, Player, get_all_legal_moves, get_position_after_move, convert_position_to_string, get_opposite_player, check_for_winner
from typing import List, Tuple


class SimpleBot(BotClassModel):
    analyzed_positions = {}

    def play_position(self, position: List[List[chr]], player: Player)-> Tuple[Move, float, List[List[chr]]]:
        e, m = self.__get_best_move(position, player)
        new_pos = get_position_after_move(position, m, player)
        return (m, e, new_pos)
    
    def __get_best_move(self, position: List[List[chr]], player: Player) -> Tuple[float, Move]:
        def __negamax(depth: int, pos: List[List[chr]], pl: Player) -> Tuple[float, Move]:
            if depth == 0:
                pos_str = convert_position_to_string(pos, pl)
                if pos_str in self.analyzed_positions:
                    return (self.analyzed_positions[pos_str], Move((0,0), (0,0)))
                else:
                    score = self.__evaluate_position(pos, pl)
                    self.analyzed_positions[pos_str] = score
                    return (score, Move((0,0), (0,0)))
                
            max = float('-inf')
            best_move = Move((0,0), (0,0))
            moves = get_all_legal_moves(pos, pl)
            for m in moves:
                neg_score, _ = __negamax(depth - 1, get_position_after_move(pos, m, pl), get_opposite_player(pl))
                score = -neg_score
                if score > max:
                    max = score
                    best_move = m
                if max == float('inf'):
                    break
            return max, best_move
        return __negamax(3, position, player)
    
    def __evaluate_position(self, position: List[List[chr]], player: Player) -> float:
        winner = check_for_winner(position, player)
        if winner == player:
            return float('inf')
        elif winner == get_opposite_player(player):
            return float('-inf')
        else:
            pos_str = convert_position_to_string(position, player)[1:]
            nb_player = pos_str.count(player.name)
            nb_opp = pos_str.count(get_opposite_player(player).name)
            return (nb_player - nb_opp) + random.random()