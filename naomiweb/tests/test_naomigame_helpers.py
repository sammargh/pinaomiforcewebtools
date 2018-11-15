import unittest
from naomigame import *

class TestNAOMIGame_is_naomi_game(unittest.TestCase):

    def setUp(self):
        pass

    def test_with_valid_game(self):
        '''
        If the beginning of a file is 'NAOMI', it should be considered a valid game.
        '''
        self.assertTrue(is_naomi_game('tests/testgame.bin'))

    def test_with_invalid_game(self):
        '''
        If the beginning of a file is not 'NAOMI', it should not be cosidered a valid game.
        '''
        self.assertFalse(is_naomi_game('tests/invalidgame.bin'))

    def test_with_invalid_path(self):
        '''
        If filename leads to an invalid path, it should return false
        '''
        self.assertFalse(is_naomi_game('invalid_path'))

class TestNAOMIGame_get_game_name(unittest.TestCase):

    def setUp(self):
        pass

    def test_valid_game(self):
        '''
        If game name string exists in proper place in the file, it should be returned
        '''
        self.assertEqual(get_game_name('tests/testgame.bin'), 'JAPAN TITLE')

    def test_invalid_game(self):
        '''
        If the file doesn't contain a game name string in the right place, return a blank string
        '''
        self.assertEqual(get_game_name('tests/invalidgame.bin'), '')

    def test_invalid_path(self):
        '''
        If the path to the game is invalid, return a blank string
        '''
        self.assertEqual(get_game_name('invalid_path'), '')

if __name__ == '__main__':
    unittest.main()
