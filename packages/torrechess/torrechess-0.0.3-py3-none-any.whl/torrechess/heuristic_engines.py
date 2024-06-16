import chess
import random
import abc

class BaseHeuristicEngine(abc.ABC):
    """
    Base class for all heuristic engines.
    """
    def __init__(self, name):
        self.name = name
    
    @abc.abstractmethod
    def play_move_on_board(self, board: chess.Board) -> chess.Move:
        pass

###############################################################################

class TorreEngineRandom(BaseHeuristicEngine):
    """
    Plays a random legal move.
    """
    def __init__(self):
        super().__init__("TorreEngineRandom")
    
    def play_move_on_board(self, board: chess.Board) -> chess.Move:
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
    
    def play_move_on_board(self, board: chess.Board) -> chess.Move:
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
    
    def play_move_on_board(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        check_moves = [move for move in legal_moves if board.gives_check(move)]
        
        if check_moves:
            chosen_move = random.choice(check_moves)
        else:
            chosen_move = random.choice(legal_moves)
        
        board.push(chosen_move)
        return chosen_move
