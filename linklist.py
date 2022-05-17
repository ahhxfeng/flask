#! /bin/env python
# coding=utf--8

__author__ = "TF00"


class Node():
    def __init__(self, item):
        self.item = item
        self.next = None


class SingleLinklist(object):
    def __init__(self):
        self._head = None


if __name__ == '__main__':
    """init singlist head node"""

    singlelist = SingleLinklist()
    """init other node"""

    node1 = Node(1)
    node2 = Node(2)
    """ connect node """
    singlelist._head = node1
    node1.next = node2
    """read node item"""

    print("Node1 : {}".format(singlelist._head.item))
    print("Node2 : {}".format(singlelist._head.next.item))
