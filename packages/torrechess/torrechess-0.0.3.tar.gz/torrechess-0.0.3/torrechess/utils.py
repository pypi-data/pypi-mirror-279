import chess
import chess.pgn
import collections

def pgn_from_chessboard(board:chess.Board, white_name:str="White", black_name:str="Black") -> str:
    """
    Generate a PGN from a chess.Board.
    """
    game = chess.pgn.Game()

    # Undo all moves.
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())

    game.setup(board)
    node = game

    # Replay all moves.
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)

    # Define headers of PGN game
    game.headers["White"] = white_name
    game.headers["Black"] = black_name
    game.headers["Result"] = board.result()
    
    return str(game)
