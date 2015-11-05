import random
import re
import argparse


def height_helper(n, acc, f):
    if n == None:
        return acc

    return f(height_helper(n.left, acc+1, f), height_helper(n.right, acc+1, f))

class Tree:
    def __init__(self, root):
        self.root = root

    def setroot(self, n):
        self.root = n

    def max_height(self):
        return height_helper(self.root, 0, max)
        
    def min_height(self):
        return height_helper(self.root, 0, min)

    def search(self, k):
        x = self.root
        found = False
        pathlen = -1

        while not x == None:
            pathlen += 1
            if x.key == k:
                found = True
                break

            if k < x.key:
                x = x.left
            else:
                x = x.right

        return [found, pathlen]

class Node:
    def __init__(self, k):
        self.key    = k
        self.left   = None
        self.right  = None
        self.parent = None

    def setkey(self, k):
        self.key = k

    def setleft(self, n):
        self.left = n

    def setright(self, n):
        self.right = n

    def setparent(self, n):
        self.parent = n

def insert(T, z):
    y = None
    x = T.root

    while not x == None:
        y = x
        if z.key < x.key:
            x = x.left
        else:
            x = x.right

    z.setparent(y)
    
    if y == None:
        T.setroot(z)
    elif z.key < y.key:
        y.setleft(z)
    else:
        y.setright(z)

def makenode(k):
    return Node(k)

def maketree(root=None):
    return Tree(root)

def preorder(root):
    if not root == None:
        print root.key
        preorder(root.left)
        preorder(root.right)
