from enum import Enum
from utils import NodeTypes
from plot_tree import plot_tree


class Tree:
    def __init__(self, initial_node):
        self.initial_node = initial_node
        self.list_nodes = []
        self.max_depth = None

    def convert_to_dict_list(self):
        self.initial_node.name = 0
        current_name = 1
        result = {0: []}
        nodes_to_expand = [self.initial_node]
        while len(nodes_to_expand) > 0:
            expanded_node = nodes_to_expand.pop()
            if len(expanded_node.children_nodes) > 0:
                for child_node in expanded_node.children_nodes:
                    child_node.name = current_name
                    current_name += 1
                result[expanded_node.name] = [
                    child.name for child in expanded_node.children_nodes
                ]
            nodes_to_expand += expanded_node.children_nodes
        return result


class Node:
    def __init__(self, value, parent_node, from_action, node_type, children_nodes=[]):
        self.value = value
        self.from_action = from_action
        self.children_nodes = []
        self.node_type = node_type
        self.name = None

        self.parent_node = parent_node
        if parent_node != None:  # only for initial node in theory
            self.parent_node.add_child_node(self)
            self.depth = parent_node.depth + 1
        else:
            self.depth = 0

    def add_children_nodes(self, children):
        self.children_nodes += children

    def add_child_node(self, child):
        self.children_nodes.append(child)

    def update_value(self, new_value):
        self.value = new_value


if __name__ == "__main__":
    a = Node(1, None, None, NodeTypes.max)
    b = Node(2, a, None, NodeTypes.max)
    c = Node(3, a, None, NodeTypes.max)
    d = Node(4, b, None, NodeTypes.max)
    e = Node(5, b, None, NodeTypes.max)
    f = Node(6, b, None, NodeTypes.max)
    f = Node(7, e, None, NodeTypes.max)

    tree = Tree(a)
    dict_list = tree.convert_to_dict_list()
    plot_tree(dict_list)
