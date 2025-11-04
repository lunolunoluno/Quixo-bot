# QUIXO BOT
This is an attempt at making an AI that plays the game [Quixo](https://boardgamegeek.com/wiki/page/thing:3190).

Note: Quixo is a [solved game](https://arxiv.org/abs/2007.15895). 

## Game rules

Each turn, a player chooses a cube and moves it according to the following rules. In no event can a player miss their turn.

- Choosing a cube: The player chooses and takes a blank cube, or one with their symbol on it, from the board’s periphery. In the first round, the players have no choice but to take a blank cube. If the cube taken is blank, it must always be replaced by a cube with the player’s symbol on the top face.
- Replacing the cube: The player can choose at which end of the incomplete rows made when a cube is taken, the cube is to be replaced. The player add its cube at the end of one of the incompleted rows, pushing the rest of the row into the hole created when the player took its cube. You can never replace the cube just played back in the position from which it was taken.

END OF GAME: The winner is the player to make a horizontal, vertical or diagonal line with 5 cubes bearing their symbol. 

[Source](https://cdn.1j1ju.com/medias/a8/5e/26-quixo-rulebook.pdf)

# Start

To start the project, run the following command:

```sh
python3 main.py 
```

# Bot created

## Random

> implemented in `agents/randombot.py`

This bot will play a random move from all the legal moves available. 

## Simple

> implemented in `agents/simplebot.py`

This is bot uses a simple implementation of the [Negamax](https://www.chessprogramming.org/Negamax) algorithm for move search and the evaluation of a position is defined as `the sum of all of current player's pieces` - `the sum of all of the opponent's pieces` + `some random noise`.

Since there is no optimization implemented on the Negamax algorithm, the max depth is 3, as a higher depth takes too long.
The random noise applied to the evaluation function is to avoid having the bot playing the same move in the same positions but the random noise is small enough so that a move with a lower evaluation shouldn't be promoted because of this noise. 

