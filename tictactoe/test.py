import unittest
import tictactoe as ttt

class TestWinnerMethod(unittest.TestCase):
    X = ttt.X
    EMPTY = ttt.EMPTY
    O = ttt.O
    board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    
    def test_vertical_winner(self):
        self.assertEqual(
            ttt.winner(
                [[self.EMPTY, self.X, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY]]
            ),
            self.X,
            "Checked middle vertical victory correctfully"
        )
    def test_bottom_horizontal_winner(self):
        self.assertEqual(
            ttt.winner(
                [[self.EMPTY, self.X, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY],
                [self.O, self.O, self.O]]
            ),
            self.O,
            "Checked bottom horizontal victory correctfully"
        )
    def test_no_winner(self):
        self.assertEqual(
            ttt.winner(
                [[self.EMPTY, self.O, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY]]
            ),
            None
        )
    
    def test_diagonal_victory(self):
        self.assertEqual(
            ttt.winner(
                [[self.X, self.O, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY],
                [self.EMPTY, self.X, self.X]]
            ),
            self.X
        )
    def test_diagonal_victory2(self):
        self.assertEqual(
            ttt.winner(
                [[self.EMPTY, self.O, self.O],
                [self.EMPTY, self.O, self.EMPTY],
                [self.O, self.X, self.X]]
            ),
            self.O
        )

if __name__ == '__main__':
    unittest.main()