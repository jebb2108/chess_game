from chess_pieces import Empty, Color, Pawn, Knight, Queen
from unittest.mock import patch


class TestPawnTransformation:
    @patch('builtins.input', return_value='queen')
    def test_pawn_transformation_to_selected_piece(self, mock_input):
        board = [[Empty() for _ in range(8)] for _ in range(8)]
        pawn = Pawn(0, 0, Color.white)
        pawn._turn_into_piece(board, 'queen')
        assert isinstance(board[0][0], Queen)
        assert board[0][0].color == Color.white

    @patch('builtins.input', side_effect=['invalid', 'knight'])
    def test_invalid_response_handling(self, mock_input):
        board = [[Empty() for _ in range(8)] for _ in range(8)]
        pawn = Pawn(0, 0, Color.white)
        pawn._turn_into_piece(board, 'knight')
        assert isinstance(board[0][0], Knight)
        assert board[0][0].color == Color.white

    def test_invalid_color_handling(self):
        board = [[Empty() for _ in range(8)] for _ in range(8)]
        pawn = Pawn(0, 0, 3)  # Invalid color
        pawn._turn_into_piece(board, 'queen')
        assert isinstance(board[0][0], Empty)