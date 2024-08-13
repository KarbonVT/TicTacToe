from flask import Blueprint, render_template
from flask_socketio import SocketIO, emit
import game

views = Blueprint(__name__, "views")
board="XXO----XX"

@views.route("/")
def home():
    return render_template("index.html", board)

@SocketIO.on('connect')
def handle_connect():
    emit('update_board', board)

@SocketIO.on('update_board')
def handle_update_board(data):
    global board
    board = data
    emit('update_board', board, broadcast=True)