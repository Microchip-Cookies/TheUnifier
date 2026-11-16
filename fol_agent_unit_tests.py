import fol_agent
from typing import Any
import unittest

class TestUnificationUnits(unittest.TestCase):

    def test_symbol_type(self):
        symbols = {
            'predicates': ['Knows'],
            'functions': ['King'],
            'variables': ['x', 'y'],
            'constants': ['John', 'Bill']
        }
        with self.assertRaises(ValueError,):
            fol_agent._symbol_type('Knows', symbols)
        with self.assertRaises(ValueError):
            fol_agent._symbol_type('King', symbols)
        with self.assertRaises(ValueError):
            fol_agent._symbol_type('Drag Queen', symbols)
        with self.assertRaises(ValueError):
            fol_agent._symbol_type(['Drag Queen', 'x'], symbols)
        self.assertEqual('predicate', fol_agent._symbol_type(['Knows', 'x', 'John'], symbols), "['Knows', 'x', 'John'] should return 'predicate'")
        self.assertEqual('function', fol_agent._symbol_type(['King', 'x', 'John'], symbols), "['King', 'x', 'John'] should return 'function'")
        self.assertEqual('variable', fol_agent._symbol_type('x', symbols), "'x' should return 'variable'")
        self.assertEqual('variable', fol_agent._symbol_type('y', symbols), "'x' should return 'variable'")
        self.assertEqual('constant', fol_agent._symbol_type('John', symbols), "'John' should return 'constant'")
        self.assertEqual('constant', fol_agent._symbol_type('Bill', symbols), "'Bill' should return 'constant'")

    def test_get_unifier(self):
        symbols = {
            'predicates': ['Knows', 'Likes'],
            'functions': ['Father', 'Sibling'],
            'variables': ['x', 'y', 'p', 'q', 'r'],
            'constants': ['Sophia', 'James']
        }
        pred = ['Knows', 'p', 'q']
        func = ['Father', 'r']
        pred2 = ['Likes', ['Father', 'p'], 'q']

        self.assertEqual(['x', 'y'], fol_agent._get_unifier('x', 'y', symbols), "Vars 'x' and 'y' should return ['x', 'y']")
        self.assertEqual(['y', 'x'], fol_agent._get_unifier('y', 'x', symbols), "Vars 'y' and 'x' should return ['y', 'x']")
        self.assertEqual(['y', 'James'], fol_agent._get_unifier('y', 'James', symbols), "Var 'y' and const 'James' should return ['y', 'James']")
        self.assertEqual(['y', 'Sophia'], fol_agent._get_unifier('Sophia', 'y', symbols), "Const 'Sophia' and Var 'y' should return ['y', 'Sophia']")
        self.assertEqual(['x', pred], fol_agent._get_unifier(pred, 'x', symbols), "A predicate and var 'x' should return ['x', predicate]")
        self.assertEqual(['x', pred], fol_agent._get_unifier('x', pred, symbols), "A predicate and var 'x' should return ['x', predicate]")
        self.assertEqual(['x', func], fol_agent._get_unifier(func, 'x', symbols), "A function and a variable 'x' should return ['x', function]")
        self.assertEqual(['x', func], fol_agent._get_unifier('x', func, symbols), "A function and a variable 'x' should return ['x', function]")
        self.assertEqual(None, fol_agent._get_unifier('Sophia', 'James', symbols), "Two constants should return None")
        self.assertEqual(None, fol_agent._get_unifier('Sophia', pred, symbols), "A constant and a predicate should return None")
        self.assertEqual(None, fol_agent._get_unifier(pred, 'Sophia', symbols), "A constant and a predicate should return None")
        self.assertEqual(None, fol_agent._get_unifier('Sophia', func, symbols), "A constant and a function should return None")
        self.assertEqual(None, fol_agent._get_unifier(func, 'Sophia', symbols), "A constant and a function should return None")
        # Test for var in func/pred
        self.assertEqual(None, fol_agent._get_unifier('p', pred2, symbols), "Cannot unify a variable with a function containing that variable")
        self.assertEqual(None, fol_agent._get_unifier('q', pred2, symbols), "Cannot unify a variable with a function containing that variable")


    def test_contains_var(self):
        expr_1 = ['Father', 'x', 'y']
        expr_2 = ['Father', 'p', 'q']
        expr_3 = ['Father', ['Brother', 'x', 'y'], 'q']
        expr_4 = ['Father', 'p', ['Brother', 'Tom', 'x']]
        expr_5 = ['Father', 'p', ['Brother', 'Tom', 'y']]
        expr_6 = ['Knows', ['Father', ['Brother', 'Maria', 'Sayed']], ['Boss', 'x', 'y']]

        self.assertTrue(fol_agent._contains_var('x', expr_1), f'{expr_1} does contain "x"')
        self.assertFalse(fol_agent._contains_var('x', expr_2), f'{expr_2} does not contain "x"')
        self.assertTrue(fol_agent._contains_var('x', expr_3), f'{expr_3} does contain "x"')
        self.assertTrue(fol_agent._contains_var('x', expr_4), f'{expr_4} does contain "x"')
        self.assertFalse(fol_agent._contains_var('x', expr_5), f'{expr_5} does not contain "x"')
        self.assertTrue(fol_agent._contains_var('x', expr_6), f'{expr_6} does contain "x"')

    def test_substitute(self):
        expr_1 = ['Mother', 'y']
        expr_2 = ['Mother', ['Mother', 'y']]
        expr_3 = ['Mother', ['Mother', ['Mother', 'y']]]
        expr_4 = ['Knows', ['Mother', ['Mother', ['Mother', 'y']]], 'y']

        sub_1 = ['y', 'Sayed']

        expect_1 = ['Mother', 'Sayed']
        expect_2 = ['Mother', ['Mother', 'Sayed']]
        expect_3 = ['Mother', ['Mother', ['Mother', 'Sayed']]]
        expect_4 = ['Knows', ['Mother', ['Mother', ['Mother', 'Sayed']]], 'Sayed']

        fol_agent._substitute(sub_1, expr_1)
        self.assertEqual(expect_1, expr_1)

        fol_agent._substitute(sub_1, expr_2)
        self.assertEqual(expect_2, expr_2)

        fol_agent._substitute(sub_1, expr_3)
        self.assertEqual(expect_3, expr_3)

        fol_agent._substitute(sub_1, expr_4)
        self.assertEqual(expect_4, expr_4)


    def test_compose_subs(self):
        subs = [['x', ['Mother', 'z']]]
        new_sub = ['z', 'John']
        expected_subs = [['x', ['Mother', 'John']], ['z', 'John']]
        fol_agent._compose_subs(new_sub, subs)
        self.assertEqual(expected_subs, subs, f'Expected {expected_subs}\nReceived {subs}')

if __name__ == '__main__':
    unittest.main()