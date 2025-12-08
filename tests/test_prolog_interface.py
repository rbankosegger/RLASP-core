import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Framework imports
from policy import RandomPolicy
from utils import PrologInterface

class TestPrologInterface(unittest.TestCase):

    def test_simple_query_1(self):

        prolog_knowledge_base = ['p(a)','q(b)']
        prolog_query = 'p(X)'

        expected_response = [{'X':'a'}]

        p = PrologInterface()

        actual_response = p.run_query(prolog_knowledge_base, prolog_query)

        self.assertEqual(expected_response, actual_response)

    def test_simple_query_2(self):

        prolog_knowledge_base = ['p(a)','q(b)', 'q(c)', 's(c)',
                                 'p(X) :- q(X), \\+ s(X)']
        prolog_query = 'p(X)'

        expected_response = [{'X':'a'}, {'X':'b'}]

        p = PrologInterface()

        actual_response = p.run_query(prolog_knowledge_base, prolog_query)

        self.assertEqual(expected_response, actual_response)

    def test_query_reset(self):

        prolog_knowledge_base_1 = ['p(1)']
        prolog_knowledge_base_2 = ['p(2)', 'p(3)']
        prolog_query = 'p(X)'

        p = PrologInterface()

        response_1 = p.run_query(prolog_knowledge_base_1, prolog_query)
        response_2 = p.run_query(prolog_knowledge_base_2, prolog_query)

        self.assertEqual([{'X':1}],response_1)
        self.assertEqual([{'X':2},{'X':3}],response_2)

    def test_query_with_two_atoms(self):

        kb = ['p(1)', 'p(2)', 'p(3)', 'q(2,a)', 'q(3,b)']
        qu = 'p(X), q(X,Y)'

        p = PrologInterface()

        response = p.run_query(kb,qu)

        self.assertEqual([{'X':2,'Y':'a'},{'X':3,'Y':'b'}], response)
