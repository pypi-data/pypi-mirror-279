import chess
import random
import abc

from torrechess import utils

class BaseHeuristicEngine(abc.ABC):
    """
    Base class for all heuristic engines.
    """
    def __init__(self, name):
        self.name = name
    
    @abc.abstractmethod
    def play_move_on_chessboard(self, board: chess.Board) -> chess.Move:
        pass

###############################################################################

class TorreEngineRandom(BaseHeuristicEngine):
    """
    Plays a random legal move.
    """
    def __init__(self):
        super().__init__("TorreEngineRandom")
    
    def play_move_on_chessboard(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        chosen_move = random.choice(legal_moves)
        board.push(chosen_move)
        return chosen_move

class TorreEngineRandomCapture(BaseHeuristicEngine):
    """
    Plays a random legal capture move if available.
    If no capture move is available, plays a random legal move.
    """
    def __init__(self):
        super().__init__("TorreEngineRandomCapture")
    
    def play_move_on_chessboard(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        capture_moves = [move for move in legal_moves if board.is_capture(move)]
        
        if capture_moves:
            chosen_move = random.choice(capture_moves)
        else:
            chosen_move = random.choice(legal_moves)
        
        board.push(chosen_move)
        return chosen_move

class TorreEngineRandomCheck(BaseHeuristicEngine):
    """
    Plays a random legal check move if available.
    If no check move is available, plays a random legal move.
    """
    def __init__(self):
        super().__init__("TorreEngineRandomCheck")
    
    def play_move_on_chessboard(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        check_moves = [move for move in legal_moves if board.gives_check(move)]
        
        if check_moves:
            chosen_move = random.choice(check_moves)
        else:
            chosen_move = random.choice(legal_moves)
        
        board.push(chosen_move)
        return chosen_move

class TorreEngineMaterialNextMove(BaseHeuristicEngine):
    """
    Plays the move that results in the best material balance for the current player.
    Material balance is positive if white is ahead, negative if black is ahead.
    """
    def __init__(self):
        super().__init__("TorreEngineMaterialNextMove")
    
    def play_move_on_chessboard(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        best_material_balance = float('-inf') if board.turn == chess.WHITE else float('inf')
        best_moves = []

        for move in legal_moves:
            board.push(move)
            material_balance = utils.get_material_balance(board)
            board.pop()

            if board.turn == chess.WHITE:
                if material_balance > best_material_balance:
                    best_material_balance = material_balance
                    best_moves = [move]
                elif material_balance == best_material_balance:
                    best_moves.append(move)
            else:
                if material_balance < best_material_balance:
                    best_material_balance = material_balance
                    best_moves = [move]
                elif material_balance == best_material_balance:
                    best_moves.append(move)

        best_move = random.choice(best_moves) if best_moves else None

        if best_move is not None:
            board.push(best_move)
        
        return best_move
