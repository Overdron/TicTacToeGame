from unittest import TestCase, main
import tictactoe

class TestGame(TestCase):
    def test_singleton(self):
        """Class "Game" uses Singleton design pattern which is available through "inst()" method"""
        self.assertEqual(tictactoe.Game.inst(), tictactoe.Game.inst(),
                         "Singleton failed, variables contain different instances.")


if __name__ == '__main__':
    main()
