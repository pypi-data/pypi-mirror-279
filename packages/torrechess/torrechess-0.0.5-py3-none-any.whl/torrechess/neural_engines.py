import chess
import os
import torch
from torch import nn
import torch.nn.functional as F
from torrechess.utils import chessboard_to_tensorboard_29x8x8
from torrechess.utils import get_uci_move_by_index

class _nn_29_1858_v0(nn.Module):
    def __init__(self, channels=29, num_of_layers=12, fc_hidden_size=64):
        super(_nn_29_1858_v0, self).__init__()
        kernel_size = 3
        padding = 1
        features = 64
        groups = 1
        
        self.channels = channels  # Save the number of channels for later use

        self.relu = nn.ReLU()
        
        # Initialize convolutional layers and batch normalization
        self.conv_layers = self._make_layers(nn.Conv2d, features, kernel_size, num_of_layers, padding, groups)
        self.batch_norms = nn.ModuleList([
            nn.BatchNorm2d(features) for _ in range(num_of_layers)
        ])
        
        # Final convolutional layer
        self.final_conv = nn.Conv2d(in_channels=features, out_channels=64, kernel_size=kernel_size, padding=padding, groups=groups, bias=False)
        
        # Fully connected layer 1
        self.fc1 = nn.Linear(features, fc_hidden_size)

        # Fully connected layer 2
        self.fc2 = nn.Linear(fc_hidden_size, fc_hidden_size)
        
        # Output layer
        self.output_layer = nn.Linear(fc_hidden_size, 1858)
        
        # Weight initialization
        self._initialize_weights()

    def _make_layers(self, block, features, kernel_size, num_of_layers, padding=1, groups=1, bias=False):
        layers = []
        in_channels = self.channels  # Set the initial number of input channels
        for _ in range(num_of_layers):
            layers.append(block(in_channels=in_channels, out_channels=features, kernel_size=kernel_size, padding=padding, groups=groups, bias=bias))
            in_channels = features  # Update the number of input channels for the next layer
        return nn.Sequential(*layers)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.BatchNorm2d):
                if isinstance(m, nn.Conv2d):
                    nn.init.kaiming_normal_(m.weight.data)
                elif isinstance(m, nn.BatchNorm2d):
                    m.weight.data.fill_(1)
                    m.bias.data.zero_()
        # Initialize weights for fully connected layers
        nn.init.kaiming_normal_(self.fc1.weight)
        nn.init.zeros_(self.fc1.bias)
        nn.init.kaiming_normal_(self.fc2.weight)
        nn.init.zeros_(self.fc2.bias)
        nn.init.kaiming_normal_(self.output_layer.weight)
        nn.init.zeros_(self.output_layer.bias)

    def forward(self, x):
        # Initial convolutional layers
        out = self.relu(self.batch_norms[0](self.conv_layers[0](x)))
        for i in range(1, len(self.conv_layers)):
            out = self.relu(self.batch_norms[i](self.conv_layers[i](out)))
        # Final convolutional layer
        out = self.final_conv(out)
        # Global average pooling
        out = F.avg_pool2d(out, out.size()[2:]).view(out.size(0), -1)
        # Fully connected layer1
        out = self.relu(self.fc1(out))
        # Fully connected layer 2
        out = self.relu(self.fc2(out))
        # Output layer
        out = self.output_layer(out)
        return out

class TorreEngineNN_29_1858_v0():
    name = "TorreEngineNN_29_1858_v0"
    
    def __init__(self, model_path="_nn_29_1858_v0.pth", device="auto"):
        """
        Initialize the neural network and load the state dictionary.
        """
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.model = _nn_29_1858_v0()  # Create an instance of the model

        # If model dictionary does not exist, initialize a new model and save it
        if os.path.isfile(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Model loaded from {model_path}")
        else:
            self.model = _nn_29_1858_v0()
            torch.save(self.model.state_dict(), model_path)
            print(f"Model file not found. Initialized and saved a new model to {model_path}")

        self.model.to(self.device)
        self.model.eval()
    
    def play_move_on_chessboard(self, board: chess.Board, prevent_illegal_move: bool = True) -> chess.Move:
        """
        Evaluate the position with the neural network and play the most probable move.
        """
        board_tensor = chessboard_to_tensorboard_29x8x8(board, mirror_if_black=False)
        board_tensor = board_tensor.to(self.device)

        with torch.no_grad():
            output_layer_1858 = self.model(board_tensor.unsqueeze(0))  # Get the output from the model

        # Sort the moves by their probability in descending order
        sorted_move_indices = torch.argsort(output_layer_1858, descending=True).squeeze().tolist()

        # Initialize best_move to None
        best_move = None

        if prevent_illegal_move:
            # Iterate through the sorted moves and find the first legal move
            for move_idx in sorted_move_indices:
                best_move_candidate = get_uci_move_by_index(move_idx)  # Convert index to UCI move
                if chess.Move.from_uci(best_move_candidate) in board.legal_moves:  # Check if the move is legal
                    best_move = best_move_candidate
                    board.push_uci(best_move)  # Play the move on the board
                    break
        else:
            # If not preventing illegal moves, take the top move
            best_move = get_uci_move_by_index(sorted_move_indices[0])
            board.push_uci(best_move)  # Play the move on the board

        # Return the move object
        return chess.Move.from_uci(best_move)

    def evaluate_moves_probabilities(self, board: chess.Board) -> torch.Tensor:
        """
        Evaluate the given board position using the neural network.
        """
        board_tensor = chessboard_to_tensorboard_29x8x8(board, mirror_if_black=False)
        board_tensor = board_tensor.to(self.device)

        with torch.no_grad():
            output_layer_1858 = self.model(board_tensor.unsqueeze(0))  # Get the output from the model
        
        return output_layer_1858
