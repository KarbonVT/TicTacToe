import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Step 1: Collecting data
# For simplicity, we'll create a small synthetic dataset
# In practice, you would collect real game data
def create_dataset():
    # Example dataset of board states and corresponding moves
    data = [
        (np.array([["x", "", ""], ["", "o", ""], ["", "", ""]]), (0, 1)),
        (np.array([["x", "o", "x"], ["o", "x", "o"], ["o", "x", ""]]), (2, 2)),
        (np.array([["", "", ""], ["", "x", ""], ["o", "", ""]]), (0, 2)),
        # Add more data here
    ]
    return data

# Step 2: Preprocessing data
def preprocess_data(data):
    X = []
    y = []
    for board, move in data:
        board_flat = board.flatten()
        board_encoded = [(1 if x == "x" else 2 if x == "o" else 0) for x in board_flat]
        X.append(board_encoded)
        y.append(move[0] * 3 + move[1])  # Convert (row, col) to a single integer
    return np.array(X), np.array(y)

data = create_dataset()
X, y = preprocess_data(data)
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.long)

# Step 3: Defining the model
class TicTacToeModel(nn.Module):
    def __init__(self):
        super(TicTacToeModel, self).__init__()
        self.fc1 = nn.Linear(9, 128)
        self.fc2 = nn.Linear(128, 9)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = TicTacToeModel()

# Step 4: Training the model
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Step 5: Evaluating the model
def predict_move(model, board):
    board_flat = board.flatten()
    board_encoded = [(1 if x == "x" else 2 if x == "o" else 0) for x in board_flat]
    board_tensor = torch.tensor(board_encoded, dtype=torch.float32)
    output = model(board_tensor)
    move = torch.argmax(output).item()
    return divmod(move, 3)

# Example usage
test_board = np.array([["x", "o", "x"], ["o", "x", "o"], ["o", "x", ""]])
predicted_move = predict_move(model, test_board)
print(f"Predicted move: {predicted_move}")
