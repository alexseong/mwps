from __future__ import absolute_import

import re
from ExpressionTree import ExpressionTree
from Stack import Stack

OPERATORS = {'+', '-', '*', '/', '(', ')', '^'}
PRIORITY = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}

class EquationConverter():
    def __init__(self, equation="DEFAULT"):
        self.original_equation = equation
        self.tree = ExpressionTree()
        self.equals_what = None

    def show_expression_tree(self):
        print(self.tree.levelorder())
