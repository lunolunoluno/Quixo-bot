import random

from agents.utils import BotClassModel, Move, Player, bitboard_play_move, check_for_winner_bitboard, convert_bitboard_to_position, convert_position_to_bitboard, get_all_legal_moves, get_position_after_move, convert_position_to_string, get_opposite_player, check_for_winner
from typing import List, Tuple


class SimpleBotV2(BotClassModel):
    analyzed_positions = {}

    def play_position(self, position: List[List[chr]], player: Player)-> Tuple[Move, float, List[List[chr]]]:
        e, m = self.__get_best_move(convert_position_to_bitboard(position), player)
        new_pos = get_position_after_move(position, m, player)
        return (m, e, new_pos)
    
    def __get_best_move(self, position_bb: int, player: Player) -> Tuple[float, Move]:
        def __negamax(depth: int, pos: int, pl: Player) -> Tuple[float, Move]:
            if depth == 0:
                if pos in self.analyzed_positions:
                    return (self.analyzed_positions[pos], Move((0,0), (0,0)))
                else:
                    score = self.__evaluate_position(pos, pl)
                    self.analyzed_positions[pos] = score
                    return (score, Move((0,0), (0,0)))
                
            max = float('-inf')
            best_move = Move((0,0), (0,0))
            moves = get_all_legal_moves(convert_bitboard_to_position(pos), pl) # would be better if get_all_legal_moves could be directly from a bitboard
            for m in moves:
                neg_score, _ = __negamax(depth - 1, bitboard_play_move(pos, m, pl), get_opposite_player(pl))
                score = -neg_score
                if score > max:
                    max = score
                    best_move = m
                if max == float('inf'):
                    break
            return max, best_move
        return __negamax(3, position_bb, player)
    
    def __evaluate_position(self, position_bb: int, player: Player) -> float:
        winner = check_for_winner_bitboard(position_bb, player)
        if winner == player:
            return float('inf')
        elif winner == get_opposite_player(player):
            return float('-inf')
        else:
            nb_o = bin(0xffffffff & position_bb).count("1")
            nb_x = bin(position_bb >> 32).count("1")
            eval = nb_x - nb_o if player == Player.X else nb_o - nb_x
            return eval + random.random()