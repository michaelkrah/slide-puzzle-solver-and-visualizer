"""
Node positioning algorithm for trees
For source and explanation see:
http://dirk.jivas.de/papers/buchheim02improving.pdf
and
https://llimllib.github.io/pymag-trees/
"""
import math

# Global functions for node positioning algorithm
MINDISTANCE = 1
MAXDEPTH = math.inf  # Infinity


def position_tree(node):
    """Main node positioning function, takes as input the root node, always returns True"""
    if node is not None:
        n = first_walk(node, 0)
        second_walk(n, 0, 0)
        return True
    else:
        return True


def first_walk(node, level):
    if len(node.children) == 0:
        if node.leftmost_sibling:
            node.x_coordinate = node.left_brother().x_coordinate + MINDISTANCE
        else:
            node.x_coordinate = 0

    else:
        default_ancestor = node.children[0]
        for successor in node.children:
            first_walk(successor, level + 1)
            default_ancestor = apportion(successor, default_ancestor, level)

        execute_shifts(node)

        midpoint = (node.children[0].x_coordinate + node.children[-1].x_coordinate) / 2

        ell = node.children[0]
        arr = node.children[-1]
        left_brother = node.left_brother()

        if left_brother:
            node.x_coordinate = left_brother.x_coordinate + MINDISTANCE
            node.modifier = node.x_coordinate - midpoint
        else:
            node.x_coordinate = midpoint
    return node


def second_walk(node, modifier, depth):
    node.x_coordinate += modifier
    node.y_coordinate = depth

    for child in node.children:
        second_walk(child, modifier + node.modifier, depth + 1)


def apportion(node, default_ancestor, level):
    node_child = node.left_brother()
    # in short for inner, out short for outer, l short for left, r short for right
    if node_child is not None:
        node_in_r = node_out_r = node
        node_in_l = node_child
        node_out_l = node.leftmost_sibling
        shift_in_r = shift_out_r = node.modifier
        shift_in_l = node_in_l.modifier
        shift_out_l = node_out_l.modifier
        while node_in_l.right() and node_in_r.left():
            node_in_l = node_in_l.right()
            node_in_r = node_in_r.left()
            node_out_l = node_out_l.left()
            node_out_r = node_out_r.right()
            node_out_r.ancestor = node

            shift = (node_in_l.x_coordinate + shift_in_l) - (node_in_r.x_coordinate + shift_in_r) + MINDISTANCE
            if shift > 0:
                a = ancestor(node_in_l, node, default_ancestor)
                move_subtree(a, node, shift)
                shift_in_r = shift_in_r + shift
                shift_out_r = shift_out_r + shift
            shift_in_l += node_in_l.modifier
            shift_in_r += node_in_r.modifier
            shift_out_l += node_out_l.modifier
            shift_out_r += node_out_r.modifier
        if node_in_l.right() and not node_out_r.right():
            node_out_r.thread = node_in_l.right()
            node_out_r.modifier += shift_in_l - shift_out_r
        else:
            if node_in_r.left() and not node_out_l.left():
                node_out_l.thread = node_in_r.left()
                node_out_l.modifier += shift_in_r - shift_out_r
            default_ancestor = node
    return default_ancestor


def ancestor(node_in_l, node, default_ancestor):
    if node_in_l.ancestor in node.parent.children:
        return node_in_l.ancestor
    else:
        return default_ancestor


def move_subtree(child_l, child_r, shift):
    subtrees = child_r.number - child_l.number
    child_r.change -= shift / subtrees
    child_r.shift += shift
    child_l.change += shift / subtrees
    child_r.x_coordinate += shift
    child_r.modifier += shift


def execute_shifts(node):
    shift = change = 0
    for child in node.children[::-1]:
        child.x_coordinate += shift
        child.modifier += shift
        change += child.change
        shift += child.shift + change


def num_ordering(history):
    """ Goes through the dictionary of the tree
        and order siblings from 1-n"""
    for histKey in history:
        for i in range(0, len(history[histKey])):

            node = history[histKey][i]

            if node.parent is None:
                break

            siblings = node.parent.children
            siblings.sort(key=sibling_sort)
            count = 1
            for m in siblings:
                if node.move == m.move:
                    node.number = count
                count += 1

def sibling_sort(children):
    """Order of child nodes is determined based on the move taken to get from parent to child"""
    sibling_order = {'left': 0, 'up': 1, 'down': 2, 'right': 3}
    return sibling_order[children.move]
