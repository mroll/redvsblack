import random
import argparse


def height(n):
    h = 0

    x = n
    while not nullnode(x.parent):
        h += 1
        x = x.parent

    return h

def height_helper(n, acc, f):
    if nullnode(n):
        return acc

    return f(height_helper(n.left, acc+1, f), height_helper(n.right, acc+1, f))

class Tnil:
    def __init__(self):
        self.color = "black"

def left_rotate(T, x):
    y = x.right
    x.right = y.left

    if not nullnode(y.left):
        y.left.parent = x
    y.parent = x.parent

    if nullnode(x.parent):
        T.root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y

    y.left = x
    x.parent = y

def right_rotate(T, x):
    y = x.left
    x.left = y.right

    if not nullnode(y.right):
        y.right.parent = x
    y.parent = x.parent

    if nullnode(x.parent):
        T.root = y
    elif x == x.parent.right:
        x.parent.right = y
    else:
        x.parent.left = y

    y.right = x
    x.parent = y

def set_color(col, *nodes):
    for n in nodes:
        n.color = col

def set_red(*nodes):
    set_color("red", *nodes)

def set_black(*nodes):
    set_color("black", *nodes)

def grandparent(n):
    if not nullnode(n.parent):
        return n.parent.parent

def uncle(n):
    if not nullnode(grandparent(n)):
        if is_lchild(n.parent):
            return grandparent(n).right
        else:
            return grandparent(n).left

def recolor_and_recurse(n):
    set_black(n.parent, uncle(n))
    set_red(grandparent(n))

    return grandparent(n)

def is_lchild(n):
    if not nullnode(n):
        if n == n.parent.left:
            return True
    return False

def is_rchild(n):
    if not nullnode(n):
        if n == n.parent.right:
            return True
    return False

def are_lchildren(*nodes):
    if nodes:
        return reduce(lambda x,y: x and y, map(is_lchild, nodes))

def are_rchildren(*nodes):
    if nodes:
        return reduce(lambda x,y: x and y, map(is_rchild, nodes))

def rotate_for(n):
    if is_rchild(n):
        return left_rotate
    else:
        return right_rotate

def nodes_between_helper(lower, upper, nodes):
    if upper == lower:
        return nodes + [upper]

    if height(lower) <= height(upper):
        return []

    return nodes_between_helper(lower.parent, upper, [lower] + nodes)

# This returns an inclusive list
def nodes_between(lower, upper):
    if nullnode(upper) or nullnode(lower):
        return []

    return nodes_between_helper(lower, upper, [])

def are_aligned(x, y):
    if are_lchildren(*nodes_between(x, y.left)):
        return True
    elif are_rchildren(*nodes_between(x, y.right)):
        return True
    else:
        return False

def realign(T, n):
    op = rotate_for(n)
    n = n.parent
    op(T, n)

    return n

def balance(T, n):
    set_black(n.parent)
    set_red(grandparent(n))

    rotate_for(n)(T, grandparent(n))

    return n

def rb_insert_fixup(T, n):
    while n.parent.color == "red":
        y = uncle(n)
        if y.color == "red":
            n = recolor_and_recurse(n)
        else:
            if not are_aligned(n, grandparent(n)):
                n = realign(T, n)
            n = balance(T, n)

    set_black(T.root)

class RBTree:
    def __init__(self, root=None):
        self.nil  = Tnil()
        if root == None:
            self.root = self.nil
        else:
            self.root = root

    def max_height(self):
        return height_helper(self.root, 0, max)
        
    def min_height(self):
        return height_helper(self.root, 0, min)

    def search(self, k):
        x = self.root
        found = False
        pathlen = -1

        while not nullnode(x):
            pathlen += 1
            if x.key == k:
                found = True
                break

            if k < x.key:
                x = x.left
            else:
                x = x.right

        return [found, pathlen]

def insert(T, n):
    y = T.nil
    x = T.root

    while not x == T.nil:
        y = x
        if n.key < x.key:
            x = x.left
        else:
            x = x.right

    n.parent = y

    if y == T.nil:
        T.root = n
    elif n.key < y.key:
        y.left = n
    else:
        y.right = n

    n.left = T.nil
    n.right = T.nil
    n.color = "red"

    rb_insert_fixup(T, n)

def nullnode(n):
    return isinstance(n, Tnil) or (n == None)

class Node:
    def __init__(self, k):
        self.key    = k
        self.left   = None
        self.right  = None
        self.parent = None
        self.color  = None

    def setkey(self, k):
        self.key = k

    def setleft(self, n):
        self.left = n

    def setright(self, n):
        self.right = n

    def setparent(self, n):
        self.parent = n

def print_node(n):
    print "{}: {}".format(n.key, n.color)

def preorder(f, root):
    if not nullnode(root):
        f(root)
        preorder(f, root.left)
        preorder(f, root.right)

def makenode(x):
    return Node(x)

def maketree(root=None):
    return RBTree(root)
