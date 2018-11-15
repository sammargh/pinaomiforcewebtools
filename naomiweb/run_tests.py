import unittest

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('tests', pattern='test_*.py')
    unittest.TextTestRunner().run(tests)
