import numpy as np
import requests
import time
import random
from minmax import get_best_move


class Game:
    def __init__(self, id):
        self.id = id
        self.board = np.full((3, 3), "-", dtype=str)
        self.iq = 200

        # Randomly have AI move first
        if random.choice([0,1]) == 1:
            self.move_ai()

    def output(self):
        # Flatten the array and convert elements to strings
        flat_arr = self.board.flatten()
        str_arr = [str(item) if str(item) != '-' else '-' for item in flat_arr]

        # Join the elements into a single string
        return ''.join(str_arr)

    def _check_winner(self):
        # Check rows and columns for a winner
        for i in range(self.board.shape[0]):
            if np.all(self.board[i, :] == self.board[i, 0]) and self.board[i, 0] != "-":
                return self.board[i, 0]
            if np.all(self.board[:, i] == self.board[0, i]) and self.board[0, i] != "-":
                return self.board[0, i]

        # Check diagonals for a winner
        if np.all(np.diag(self.board) == self.board[0, 0]) and self.board[0, 0] != "-":
            return self.board[0, 0]
        if np.all(np.diag(np.fliplr(self.board)) == self.board[0, -1]) and self.board[0, -1] != "-":
            return self.board[0, -1]

        # Check for a draw (no empty spots left)
        if '-' not in self.board:
            return "Draw"

        # No winner and game is not a draw
        return None

    def _display_winner(self):
        winner = self._check_winner()
        requests.get('http://127.0.0.1:5000/gen')
        if winner == "X":
            url = 'http://127.0.0.1:5000//set_winner/' + "Karbon"
            requests.get(url)
            return("Karbon")
        elif winner == "O":
            url = 'http://127.0.0.1:5000//set_winner/' + "Bot"
            requests.get(url)
            return("Bot")
        else:
            url = 'http://127.0.0.1:5000//set_winner/' + "Draw"
            requests.get(url)
            return("Draw")
        
    def update(self):
        # Update flask using websockets
        new_board = self.output()
        print(new_board)
        url = 'http://127.0.0.1:5000/update_board/' + new_board
        # Send the HTTP request
        response = requests.get(url)
        # Print the response from the server
        print(response.text)

        if self._check_winner() is not None:
            self._display_winner()

            self.board = np.full((3, 3), "-", dtype=str)
            if random.choice([0,1]) == 1:
                time.sleep(3)
                self.move_ai()
            self.iq = random.randint(20, 200)
            url = 'http://127.0.0.1:5000/iq/' + str(self.iq)
            response = requests.get(url)

            return
        
    def board_list(self):
        converted_board = []
        for row in range(self.board.shape[0]):
            for column in range(self.board.shape[0]):
                if self.board[(row, column)] == "X":
                    converted_board.append(-1)
                elif self.board[(row, column)] == "O":
                    converted_board.append(1)
                else:
                    converted_board.append(0)
        return converted_board
    
    def random_ai_move(self):
        # Find all empty positions
        empty_positions = [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == "-"]
        
        # Choose a random empty position
        if empty_positions:
            move = random.choice(empty_positions)
            self.board[move[0], move[1]] = "O"
        self.update()

        print("Made a random move")

        
    def move_ai(self):
        # Make ai move
        #predictions = self.ai.predict_next_position(self.output())
        #for idx in predictions:
        #    if self.output()[idx] == "-":
        #        row = idx // 3
        #        col = idx % 3
        #        self.board[row, col] = "O"
        #        break
        move = get_best_move(self.board_list())
        accuracy = self.iq * .78
        if accuracy >= 100:
            self.board[move[0], move[1]] = "O"
        else:
            if accuracy < random.randint(0,100):
                self.random_ai_move()
            else:
                self.board[move[0], move[1]] = "O"
        self.update()
            
    def move(self, marker, coordinates):
        # Check if spot is empty
        if self.board[coordinates[0], coordinates[1]] == "-":

            # Send current flattened board to AI model and correct position
            #current_board = self.output()
            #next_pos = coordinates[0] + coordinates[1]*3
            #self.ai.collect_data(current_board, next_pos)
            #self.ai.train_model()

            self.board[coordinates[0], coordinates[1]] = marker

            # Update flask using websockets
            new_board = self.output()
            print(new_board)
            url = 'http://127.0.0.1:5000/update_board/' + new_board
            # Send the HTTP request
            response = requests.get(url)
            # Print the response from the server
            print(response.text)

            if self._check_winner() is not None:
                self.update()
            else:
                self.move_ai()
        return None
