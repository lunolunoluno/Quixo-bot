import webbrowser
import os

from agents.utils import INITPOS, Player
from agents.randombot import RandomBot
from agents.simplebot import SimpleBot
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST"])

# list of all bots available
ai_types = {
    "Random bot": RandomBot,
    "Simple bot": SimpleBot
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

    return {
        "move": {
            "source": {"row": m.source[0], "col": m.source[1]},
            "dest": {"row": m.dest[0], "col": m.dest[1]}
        },
        "eval": eval,
        "newboard": new_pos
    }



if __name__ == "__main__":
    ui_path = os.path.join(".", "UI", "index.html")
    webbrowser.open(ui_path)

    app.run(host="127.0.0.1", port=5000)
