import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

def preprocess(current_board):
    int_str = []

    x_count = sum(1 for cell in current_board if cell.upper() == "X")
    o_count = sum(1 for cell in current_board if cell.upper() == "O")
    xIsNext = True
    if x_count > o_count:
        xIsNext = False
    else:
        xIsNext = True

    if xIsNext is True:
        for cell in current_board:
            if cell.upper() == "X":
                int_str.append(1)
            elif cell.upper() == "O":
                int_str.append(0)
            else:
                int_str.append(2)  # Empty cell marker
    else:
        for cell in current_board:
            if cell.upper() == "X":
                int_str.append(0)
            elif cell.upper() == "O":
                int_str.append(1)
            else:
                int_str.append(2)  # Empty cell marker
    
    return np.array(int_str, dtype=np.float32)

class TicTacToeAI():
    def __init__(self):
        self.data = []  # To store game data
        self.current_board = []  # Current board state
        self.model = None  # Initialize model attribute

    def collect_data(self, board, next_marker_position):
        # Collect game data
        self.data.append((board, next_marker_position))

    def train_model(self):
        # Prepare data for training
        inputs = []
        targets = []

        for board, next_marker_position in self.data:
            inputs.append(preprocess(board))
            targets.append(next_marker_position)

        inputs = torch.tensor(inputs)
        targets = torch.tensor(targets, dtype=torch.long)

        # Define neural network model with two hidden layers
        self.model = nn.Sequential(
            nn.Linear(len(board), 64),
            nn.ReLU(),
            nn.Linear(64, 32),  # Second hidden layer with 32 neurons
            nn.ReLU(),
            nn.Linear(32, 9)   # Output layer with 9 neurons for positions
        )

        # Define loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        # Training loop
        num_epochs = 200
        for epoch in range(num_epochs):
            optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

    def predict_next_position(self, current_board):
        # If board is empty and first gen, pick a random position
        if self.model is None:
            numbers = list(range(9))
            random.shuffle(numbers)
            return numbers

        # Preprocess current board state
        inputs = torch.tensor([preprocess(current_board)])

        # Predict the next position
        with torch.no_grad():
            outputs = self.model(inputs)
            # Get indices sorted by tensor values in descending order
            sorted_indices = torch.argsort(outputs, descending=True)

            # Convert sorted indices to a list
            sorted_indices_list = sorted_indices.squeeze().tolist()

            return sorted_indices_list
