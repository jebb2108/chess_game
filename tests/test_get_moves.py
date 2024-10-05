from board import Board
from chess_pieces import Pawn, Color, Queen
from board import Board
from main import GamePlay



def test_turn_into_piece_successfully():
    # Arrange
    pawn = Pawn(1, 0, Color.black)
    pawn.back_or_forth = -1
    main = GamePlay()
    board = Board()
    main.board = board
    board.change_its_position(pawn, (0, 0))

    # Act
    pawn._turn_into_piece(main.board, 'queen')

    # Assert
    assert isinstance(main.board.board[pawn.y][pawn.x], Queen)
    assert main.board.board[pawn.y][pawn.x].color == Color.black
    assert main.board.board[pawn.y][pawn.x].y == pawn.y
    assert main.board.board[pawn.y][pawn.x].x == pawn.x


def test_pawn_memory_when_enemy_passing():
    # Arrange
    main = GamePlay()
    board = Board()
    main.board = board

    # Create two pawns, one white and one black
    white_pawn = Pawn(3, 0, Color.white)
    black_pawn = Pawn(1, 1, Color.black)
    white_pawn.back_or_forth = -1
    black_pawn.back_or_forth = 1

    # Place the pawns on the board
    board.change_its_position(white_pawn, (2, 0))
    board.change_its_position(black_pawn, (3, 1))

    # Act
    white_pawn._move_object(board, (2, 1))  # White pawn moves to the same position as black pawn

    # Assert
    assert white_pawn.memory  # Check that white pawn's memory is not empty
    assert len(white_pawn.memory) == 1  # Check that white pawn's memory contains only one move
    assert white_pawn.memory[0][0] == black_pawn  # Check that the move in white pawn's memory is the black pawn
    assert white_pawn.memory[0][1] == (3, 0)  # Check that the move in white pawn's memory is to the correct position

