# tests/test_module.py
import unittest
from mypackage import module

class TestModule(unittest.TestCase):
    def test_function(self):
        self.assertEqual(module.function_to_test(), 'expected result')

if __name__ == '__main__':
    unittest.main()
