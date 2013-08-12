


class RTCReference():
    def __init__(self, tree, node):
        self._tree = tree
        self._node = node
        pass

    
    def outports(self):
        return self._node.outports


