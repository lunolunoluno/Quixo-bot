"use strict";

const players = ["X", "O"];
const boardState = Array.from({ length: 5 }, () => Array(5).fill("")); // empty 5x5 array

let playerType = ["Human"];
let gameTurn = 0;
let humanPlayers = [true, true];
let aiTypes = [null, null];


window.onload = function () {
    const selects = [
        document.getElementById("playerType1"),
        document.getElementById("playerType2")
    ];

    fetch("http://127.0.0.1:5000/aitypes").then((response) => {
        const responseData = response.json();
        responseData.then((r) => {
            r.types.forEach((t) => {
                playerType.push(t);
            })
        }).then(() => {
            playerType.forEach((t, i) => {
                selects.forEach(select => {
                    const opt = new Option(`${i}: ${t}`, t);
                    select.add(opt);
                });
            });
        });
    }).catch(() => {
        playerType.forEach((t, i) => {
            selects.forEach(select => {
                const opt = new Option(`${i}: ${t}`, t);
                select.add(opt);
            });
        });
    });

    generateBoard();
}

function newGame() {
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            boardState[i][j] = '';
        }
    }
    gameTurn = 0;

    ["playerType1", "playerType2"].forEach((id, i) => {
        const value = document.getElementById(id).value;
        humanPlayers[i] = value === "Human";
        if (!humanPlayers[i]) {
            aiTypes[i] = value;
        } else {
            aiTypes[i] = null;
        }
    });

    updateGameInfo();
    updateBoard();
    if (!isCrtPlayerHuman()) {
        AIplay();
    }
}

function getCrtPlayer() {
    return players[gameTurn % 2];
}

function isCrtPlayerHuman() {
    return humanPlayers[gameTurn % 2];
}

function updateGameInfo(info = null) {
    if (info) {
        document.getElementById("gameInfo").innerHTML = info;
    } else {
        document.getElementById("gameInfo").innerHTML = "player '" + getCrtPlayer() + "' to play. Turn " + gameTurn + ".";
    }
}

function generateBoard() {
    let board = "<table>";
    for (let i = 0; i < 7; i++) {
        board += "<tr>";
        for (let j = 0; j < 7; j++) {
            const isOuter = (i === 0 || i === 6 || j === 0 || j === 6);
            const isPlayable = (i === 1 || i === 5 || j === 1 || j === 5);
            const cellClass = isOuter ? "outer-cell" : (isPlayable ? "playable-cell cell" : "locked-cell cell");

            board += `<td id="cell-${i}-${j}" 
                        class="${cellClass}" 
                        data-row="${i}" 
                        data-col="${j}" 
                        ></td>`;
        }
        board += "</tr>";
    }
    board += "</table>";
    document.getElementById("gameBoard").innerHTML = board;
}


function pickCube(selectedCell) {
    selectedCell.classList.add("selected-cell");

    // remove playable-cell class to all cells
    // add place-cube class to the correct outer cells
    for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 7; j++) {
            const isOuter = (i === 0 || i === 6 || j === 0 || j === 6);
            const c = document.getElementById(`cell-${i}-${j}`);
            if (isOuter) {
                c.classList.remove("selected-outer-cell");
                const row = parseInt(c.dataset.row);
                const col = parseInt(c.dataset.col);
                const selectedRow = parseInt(selectedCell.dataset.row);
                const selectedCol = parseInt(selectedCell.dataset.col);

                const sameRow = (row === selectedRow);
                const sameCol = (col === selectedCol);
                const notAdjacent = (sameRow && Math.abs(col - selectedCol) > 1) || (sameCol && Math.abs(row - selectedRow) > 1);

                // if the cell is on the same row or column but not adjacent to the selected cell
                if ((sameRow || sameCol) && notAdjacent) {
                    c.classList.add("place-cube");
                    if (isCrtPlayerHuman()) {
                        c.onclick = () => placeCube(c, sameRow);
                    }
                }
            } else {
                c.classList.remove("playable-cell");
                c.onclick = null;
            }
        }
    }
}

function placeCube(selectedOuterCell, isSameRow) {
    // the -1 is to match the index of the boardState array
    const refRow = parseInt(selectedOuterCell.dataset.row) - 1;
    const refCol = parseInt(selectedOuterCell.dataset.col) - 1;

    // place the cube
    if (isSameRow) {
        if (refCol === -1) {
            // placing the cube from the left
            for (let i = 4; i > 0; i--) {
                boardState[refRow][i] = boardState[refRow][i - 1];
            }
            boardState[refRow][0] = getCrtPlayer();
        } else {
            // placing the cube from the right
            for (let i = 0; i < 4; i++) {
                boardState[refRow][i] = boardState[refRow][i + 1];
            }
            boardState[refRow][4] = getCrtPlayer();
        }
    } else {
        if (refRow === -1) {
            // placing the cube from the top
            for (let i = 4; i > 0; i--) {
                boardState[i][refCol] = boardState[i - 1][refCol];
            }
            boardState[0][refCol] = getCrtPlayer();
        } else {
            // placing the cube from the bottom
            for (let i = 0; i < 4; i++) {
                boardState[i][refCol] = boardState[i + 1][refCol];
            }
            boardState[4][refCol] = getCrtPlayer();
        }
    }

    // reset the outer cells
    for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 7; j++) {
            const isOuter = (i === 0 || i === 6 || j === 0 || j === 6);
            const c = document.getElementById(`cell-${i}-${j}`);
            if (isOuter) {
                c.classList.remove("place-cube");
                c.onclick = null;
            }
            c.classList.remove("selected-cell");
        }
    }
    selectedOuterCell.classList.add("selected-outer-cell");

    nextTurn();
}

function nextTurn() {
    gameTurn++;
    updateGameInfo();
    updateBoard();
    const gameEnded = checkForWinner();
    if (!isCrtPlayerHuman() && !gameEnded) {
        AIplay();
    }
}

function updateBoard() {
    for (let i = 0; i < boardState.length; i++) {
        for (let j = 0; j < boardState[i].length; j++) {
            const c = document.getElementById(`cell-${i + 1}-${j + 1}`);
            c.innerHTML = boardState[i][j];

            const isPlayable = (boardState[i][j] === getCrtPlayer() || boardState[i][j] === '');
            if ((i === 0 || i === 4 || j === 0 || j === 4) && isPlayable) {
                if (isCrtPlayerHuman()) {
                    c.className = "playable-cell cell";
                    c.onclick = () => pickCube(c);
                } else {
                    c.className = "cell"
                }
            } else {
                c.className = "locked-cell cell";
            }
        }
    }
}

function checkForWinner() {
    let gameEnded = false;
    const size = 5;
    for (const player of players) {
        const winInfo = `${player} Won !`

        // Check rows
        for (let row = 0; row < size; row++) {
            if (boardState[row].every(cell => cell === player)) {
                updateGameInfo(winInfo);
                displayWinner(player, 'row', row + 1);
                gameEnded = true;
            }
        }

        // Check columns
        for (let col = 0; col < size; col++) {
            let columnWin = true;
            for (let row = 0; row < size; row++) {
                if (boardState[row][col] !== player) {
                    columnWin = false;
                    break;
                }
            }
            if (columnWin) {
                updateGameInfo(winInfo);
                displayWinner(player, 'col', col + 1);
                gameEnded = true;
            }
        }

        // Check main diagonal (top-left -> bottom-right)
        let mainDiagWin = true;
        for (let i = 0; i < size; i++) {
            if (boardState[i][i] !== player) {
                mainDiagWin = false;
                break;
            }
        }
        if (mainDiagWin) {
            updateGameInfo(winInfo);
            displayWinner(player, 'dia', 0);
            gameEnded = true;
        }

        // Check anti-diagonal (top-right -> bottom-left)
        let antiDiagWin = true;
        for (let i = 0; i < size; i++) {
            if (boardState[i][size - 1 - i] !== player) {
                antiDiagWin = false;
                break;
            }
        }
        if (antiDiagWin) {
            updateGameInfo(winInfo);
            displayWinner(player, 'dia', 1);
            gameEnded = true;
        }
    }
    return gameEnded;
}

function displayWinner(player, type, id) {
    for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 7; j++) {
            const c = document.getElementById(`cell-${i}-${j}`);
            const isOuter = (i === 0 || i === 6 || j === 0 || j === 6);
            c.onclick = null;

            if (isOuter) {
                c.className = "outer-cell";
            } else {
                c.className = "cell";
                if (type === 'row' && i === id) {
                    c.classList.add("win-cell");
                }
                if (type === 'col' && j === id) {
                    c.classList.add("win-cell");
                }
                if (type === 'dia' && id === 0 && i === j) {
                    c.classList.add("win-cell");
                }
                if (type === 'dia' && id === 1 && i + j === 6) {
                    c.classList.add("win-cell");
                }
            }
        }
    }
}

function AIplay() {
    const bodyData = {
        'ai_type': aiTypes[gameTurn % 2],
        'board': boardState,
        'player': getCrtPlayer()
    };
    fetch("http://127.0.0.1:5000/aimove", {
        method: 'POST',
        body: JSON.stringify(bodyData),
        headers: {
            "Content-Type": "application/json",
        }
    }).then((response) => {
        response.json().then((data) => {
            const s_r = data.move.source.row + 1;
            const s_c = data.move.source.col + 1; 
            const selectedCell = document.getElementById(`cell-${s_r}-${s_c}`);
            setTimeout(() => {
                pickCube(selectedCell);
            }, 500);
            
            const d_r = data.move.dest.row + 1;
            const d_c = data.move.dest.col + 1;
            let r = 0;
            let c = 0;
            if (d_r === s_r) {
                r = d_r;
                if (d_c === 1) {
                    c = 0;
                } else {
                    c = 6;
                }
            } else {
                c = d_c;
                if (d_r === 1) {
                    r = 0;
                } else {
                    r = 6;
                }
            }
            const selectedOuterCell = document.getElementById(`cell-${r}-${c}`);
            const isSameRow = (d_r === s_r)

            setTimeout(() => {
                placeCube(selectedOuterCell, isSameRow);
            }, 1000);
        });
    })
        .catch(() => alert("Error while reading AI move!"));
}

