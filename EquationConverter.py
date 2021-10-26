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

    def __filter_equation(self, equation):
        equation_equals = ""

        # Clean the equation
        try:
            equation_equals = re.search(r"([a-z]+(\s+)?=|=(\s+)?[a-z]+)", equation).group(1)
            equation_equals = re.sub("=", "", equation_equals)
        except:
            pass
        
        equation = re.sub(r"([a-z]+(\s+)?=|=(\s+)?[a-z]+)", "", equation)

        return equation.replace(' ', ""), equation_equals.replace(' ', "")


    def __infix_to_postfix(self):
        filtered_expresseion, equation_equals = self.__filter_equation(self.original_equation)
        self.equals_what = equation_equals

        stack = Stack()
        output = ""

        split_expression = re.findall(r"(\d*\.?\d+|[^0-9])", filtered_expresseion)
        for char in split_expression:
            if char not in OPERATORS:
                output += char
            elif char == '(':
                stack.push(char)
            elif char == ')':
                while not stack.isEmpty() and stack.peek() != '(':
                    output += ' '
                    output += stack.pop()
                stack.pop()
            else:
                output += ' '
                while not stack.isEmpty() and stack.peek() != '(' and PRIORITY[char] < PRIORITY[stack.peek()]:
                    output += stack.pop()

                stack.push(char)

        while not stack.isEmpty():
            output += ' '
            output += stack.pop()

        return output

    def __get_postfix_from_infix(self):
        return self.__infix_to_postfix()

    def __fill_tree(self):
        try:
            self.tree.tree_from_postfix(self.postfix_expression)
        except:
            pass        

    def eqset(self, equation="DEFAULT"):
        self.original_equation = equation
        self.postfix_expression = self.__get_postfix_from_infix()
        self.__fill_tree()

    



