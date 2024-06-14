class BTreeNode:
    """
    A class to denote BTree Node
    This is a work in progress. This could be implemented in version 2  as indexing feature.

    Attributes:
        keys (list): A list of keys
        child (list): A list of child nodes
        leaf (bool): A flag indicating whether the node is a leaf node
    """
    def __init__(self, leaf=False):
        self.keys = []
        self.child = []
        self.leaf = leaf
