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
    def test_bottom_winner(self):
        self.assertEqual(
            ttt.winner(
                [[self.EMPTY, self.X, self.EMPTY],
                [self.EMPTY, self.X, self.EMPTY],
                [self.O, self.O, self.O]]
            ),
            self.O,
            "Checked bottom horizontal victory correctfully"
        )
    

if __name__ == '__main__':
    unittest.main()