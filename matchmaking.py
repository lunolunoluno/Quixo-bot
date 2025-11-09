import argparse

from tqdm import tqdm
from agents.utils import INITPOS, BotClassModel, Player, check_for_winner, print_pos
from agents.randombot import RandomBot
from agents.simplebot import SimpleBot
from agents.simplebotv2 import SimpleBotV2

bot_list = {
    "random": RandomBot,
    "simple": SimpleBot,
    "simplev2": SimpleBotV2
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    bots_list_str = ', '.join(list(bot_list.keys()))
    parser.add_argument("player_x", help=f"Bot playing 'X'. Must be one of the following values: {bots_list_str}", type=str)
    parser.add_argument("player_o", help=f"Bot playing 'O'. Must be one of the following values: {bots_list_str}", type=str)
    parser.add_argument("nb_games", help="Number of games played between the bots (100 by default).", type=int, nargs='?', default=100)
    parser.add_argument('debug', help='Show debug informations.', type=bool, nargs='?', default=False)
    args = parser.parse_args()

    assert args.player_x in bot_list.keys(), f"{args.player_x} not in [{bots_list_str}]"
    assert args.player_o in bot_list.keys(), f"{args.player_o} not in [{bots_list_str}]"
    debug = args.debug
    print("Debug:", debug)

    p_x: BotClassModel = bot_list[args.player_x]()
    p_o: BotClassModel = bot_list[args.player_o]()
    res = {'x_win': 0, 'o_win': 0, 'draw': 0}
    for i in tqdm(range(args.nb_games)):
        pos = INITPOS
        winner = None
        game_turn = 0
        # the game_turn < 100 codition is here in case a game is too long and bots keep repeating the same moves
        while winner is None and game_turn < 100:
            _, _, pos = p_x.play(pos, Player.X)
            if debug:
                print_pos(pos)
            winner = check_for_winner(pos, Player.X) 
            if winner is not None:
                break
            _, _, pos = p_o.play(pos, Player.O)
            if debug:
                print_pos(pos)
            winner = check_for_winner(pos, Player.O) 
        
        if winner == Player.X:
            res['x_win'] += 1
        elif winner == Player.O:
            res['o_win'] += 1
        else:
            res['draw'] += 1
        
        if debug:
            print(f"{winner.name} Won!")
        
    print(f"Results for {args.nb_games} games:")
    print(f"X wins: {res['x_win']}")
    print(f"O wins: {res['o_win']}")
    print(f"Draws: {res['draw']}")
        
