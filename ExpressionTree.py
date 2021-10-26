from __future__ import absolute_import

import re
from Node import Node
from Stack import Stack

# The Binary Tree Class
# WARNING: Supports only numbers and operators

class ExpressionTree():
    def __init__(self):
        self.root = None
        self.__ordered_data = []

    def __is_root_or_self(self, node):
        if node in "DEFAULT":
            return self.root
        else:
            return node

    def levelorder(self, node="DEFAULT"):
        node = self.__is_root_or_self(node)

        return []

