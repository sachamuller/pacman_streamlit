from enum import Enum
from utils import NodeType


class Tree:
    def __init__(self, initial_node):
        self.initial_node = initial_node
        self.list_nodes = []
        self.max_depth = None

        self.build_list_nodes()
        self.get_max_depth()

    def fill_nodes_coordinates(self):
        bottom_layer = self.get_nodes_with_same_depth(self.max_depth)
        bottom_layer_per_parents = self.group_nodes_per_parents(bottom_layer)
        x = 0
        for parent in bottom_layer_per_parents.keys():
            for node in bottom_layer_per_parents[parent]:
                node.x_coordinate = x
                x += 1
        # damn it's hard to plot a tree ??

    def build_list_nodes(self):
        nodes_to_expand = [self.initial_node]
        while len(nodes_to_expand) > 0:
            expanded_node = nodes_to_expand.pop()
            self.list_nodes.append(expanded_node)
            nodes_to_expand += expanded_node.children_nodes

    def get_nodes_with_same_depth(self, depth):
        result = []
        for node in self.list_nodes:
            if node.depth == depth:
                result.append(node)
        return result

    def get_max_depth(self):
        for node in self.list_nodes:
            if self.max_depth == None or node.depth > self.max_depth:
                self.max_depth = node.depth

    def group_nodes_per_parents(self, nodes_sublist):
        result = {}
        for node in nodes_sublist:
            if node.parent_node in result:
                result[node.parent_node].append(node)
            else:
                result[node.parent_node] = [node]
        return result


class Node:
    def __init__(self, value, parent_node, from_action, node_type, children_nodes=[]):
        self.value = value
        self.parent_node = parent_node
        self.from_action = from_action
        self.children_nodes = []
        self.depth = parent_node.depth + 1
        self.x_coordinate = None
        self.node_type = node_type

    def add_children_nodes(self, children):
        self.children_nodes += children
