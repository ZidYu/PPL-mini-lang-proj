import unittest
from src.main import execute_source
class TestInterpreter(unittest.TestCase):
    def test_basic(self): self.assertEqual(execute_source('let x=5; print(x);'),['5'])
    def test_loop(self): self.assertEqual(execute_source('let x=5; while x<8: print(x); x=x+1; end'),['5','6','7'])
    def test_function(self): self.assertEqual(execute_source('function add(a,b): return a+b; end let x=add(2,3); print(x);'),['5'])
    def test_type_error(self):
        with self.assertRaises(Exception): execute_source('print("a" + true);')
if __name__=='__main__': unittest.main()
