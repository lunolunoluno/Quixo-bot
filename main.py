import webbrowser
import os
import math
import time

 
from tqdm import tqdm

from agents.utils import INITPOS, Move, Player, bitboard_play_move, convert_bitboard_to_position, get_position_after_move, convert_position_to_bitboard, print_pos, get_all_legal_moves
from agents.randombot import RandomBot
from agents.simplebot import SimpleBot
from agents.simplebotv2 import SimpleBotV2
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST"])

# list of all bots available
ai_types = {
    "Random bot": RandomBot,
    "Simple bot": SimpleBot,
    "Simple bot v2": SimpleBotV2
}

@app.get("/aitypes")
def get_ai_types():
    return {"types": list(ai_types.keys())}


@app.post("/aimove")
def get_ai_move():
    data = request.get_json()
    ai_t = data["ai_type"]
    position = data['board']
    player = Player.X if data['player'] == Player.X.name else Player.O

    bot = ai_types[ai_t]()
    m, eval, new_pos = bot.play(position, player)
    if math.isinf(eval):
        eval = math.copysign(1, eval) * 1000

    return {
        "move": {
            "source": {"row": m.source[0], "col": m.source[1]},
            "dest": {"row": m.dest[0], "col": m.dest[1]}
        },
        "eval": eval,
        "newboard": new_pos
    }

@app.post("/playmove")
def make_move():
    data = request.get_json()
    position = data["board"]
    m_source = (data["source_row"], data["source_col"])
    m_dest = (data["dest_row"], data["dest_col"])
    move = Move(m_source, m_dest)
    player = Player.X if data['player'] == Player.X.name else Player.O

    new_pos = get_position_after_move(position, move, player)
    return {"newboard": new_pos}



if __name__ == "__main__":
    ui_path = os.path.join(".", "UI", "index.html")
    webbrowser.open(ui_path)

    app.run(host="127.0.0.1", port=5000)

    # pos = [
    #     ['', '', 'O', 'O', ''],
    #     ['', 'X', 'O', '', ''],
    #     ['X', 'X', 'X', 'O', 'X'],
    #     ['O', 'X', '', '', ''],
    #     ['', 'O', 'X', '', '']
    # ]
    # print_pos(pos)
    # moves = []
    # nb_x_moves = 0
    # for p in Player:
    #     ms = get_all_legal_moves(pos, p)
    #     moves += ms
    #     print(p.name, len(ms))
    # nb_x_moves = len(moves) - len(ms)
    # print(f"{len(moves)} moves ({nb_x_moves} X, {len(moves) - nb_x_moves} O)")


    # tot_tot_pos_time = 0
    # tot_tot_bb_time = 0
    # tot_avg_diff = 0
    # for t in tqdm(range(1000)):
    #     tot_pos_time = 0
    #     tot_bb_time = 0
    #     tot_diff = 0
    #     for i, move in enumerate(moves):
    #         player = Player.X if i < nb_x_moves else Player.O
    #         print(f"{i}: {player.name} from {move.source} to {move.dest}, ", end='')

    #         move_type = 'row' if move.source[0] == move.dest[0] else 'col'
    #         print(f"type: {move_type}, ", end='')

    #         start = time.time()
    #         pos_after = get_position_after_move(pos, move, player)
    #         end = time.time()
    #         pos_time = end - start

    #         start = time.time()
    #         bb = convert_position_to_bitboard(pos)
    #         bb_after = bitboard_play_move(bb, move, player)
    #         end = time.time()
    #         bb_time = end - start

    #         tot_pos_time += pos_time
    #         tot_bb_time += bb_time

    #         correct = bb_after == convert_position_to_bitboard(pos_after)
    #         faster = bb_time < pos_time
    #         tot_diff += bb_time - pos_time
    #         print(f"pos time: {pos_time}s, bb time: {bb_time}s, correct: {correct}, faster: {faster}")
    #     print(f"total pos time: {tot_pos_time}s, total bb time: {tot_bb_time}s, diff: {tot_bb_time - tot_pos_time}s, avg diff: {tot_diff/len(moves)}")
    #     tot_tot_pos_time += tot_pos_time
    #     tot_tot_bb_time += tot_bb_time
    #     tot_avg_diff += tot_diff/len(moves)
    # print(f"total pos time: {tot_tot_pos_time}s, total bb time: {tot_tot_bb_time}s, diff: {tot_tot_bb_time - tot_tot_pos_time}s, avg diff: {tot_avg_diff/1000}")

    

