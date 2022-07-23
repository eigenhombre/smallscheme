class Env(object):
    """
    Provide a nested series of environments to look things up in.  If
    it's not found in the current environment, look in the parent, or
    its parent(s).  The idea is explained well in SICP, Chapter 4.
    """
    def __init__(self, parent=None):
        self.__values = {}
        self.__parent = parent

    def __setitem__(self, k, v):
        self.__values[k] = v

    def __getitem__(self, k):
        if k in self.__values:
            return self.__values[k]
        elif self.__parent is not None:
            return self.__parent[k]

    def copy(self):
        ret = Env(self.__parent)
        for k, v in self.__values.items():
            ret[k] = v
        return ret

    def tree(self):
        if self.__parent is None:
            parent = None
        else:
            parent = self.__parent.tree()
        return {"values": self.__values,
                "parent": parent}

    def __repr__(self):
        return str(self.tree())

    def __contains__(self, k):
        if k in self.__values:
            return True
        elif self.__parent:
            return k in self.__parent
        else:
            return False
