from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Initial board state (empty board)
board = "         "

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('update_board', board)
    emit('iq_update', 200)

@app.route('/new_bot/<new_iq>')
def new_bot(new_iq):
    global losses, draws, generation
    iq_update(new_iq)

    generation = 0
    gen_update()

    losses = -1
    draws = -1
    botlosses_update()
    botdraws_update()


@socketio.on('reset_board')
def handle_reset_board():
    global board
    board = "         "
    socketio.emit('update_board', board)

def update_board(new_board):
    global board
    board = new_board
    socketio.emit('update_board', board)

@app.route('/iq/<new_iq>')
def iq_update(new_iq):
    socketio.emit('iq_update', new_iq)
    return f"IQ updated to: {new_iq}"

@app.route('/consolelog/<log>')
def update_console(log):
    socketio.emit('consolelog', log)
    return f"Printed: {log}"

# Endpoint to update the board state from Python
@app.route('/update_board/<new_board_state>')
def update_board_endpoint(new_board_state):
    update_board(new_board_state)
    return f"Board updated to: {new_board_state}"

@app.route('/set_winner/<winner>')
def set_winner(winner):
    print(winner)
    if winner == "Draw":
        socketio.emit('game_winner', None)  # Emit None to indicate a draw
    else:
        socketio.emit('game_winner', winner)
    return "Winner set to " + winner

if __name__ == '__main__':
    socketio.run(app, debug=True)
