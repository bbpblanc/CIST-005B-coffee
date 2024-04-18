"""
Definition of the Vertex and Graph classes with basic graph related operations
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["Vertex", "Graph"]

class Vertex():
    def __init__(self, id, data, neighbors=None):
        self.id = id
        self.data = data
        self.neighbors = list()

        if neighbors:
            for n in neighbors:
                self.add(n)

    def __hash__(self):
        return self.id

    def __len__(self):
        return len(self.neighbors)

    def __eq__(self, other):
        if self is other:
            return True
        return self.id == other.id

    def __iter__(self):
        for n in self.neighbors:
            yield n

    def add(self, other):
        self.neighbors.append(other)

    def remove(self,other):
        assert isinstance(other,Vertex)
        assert other in self.neighbors
        self.neighbors.remove(other)
        assert other not in self.neighbors

    def __str__(self):
        return str(self.id) + ": [" +  ", ".join(list(map(lambda x:str(x.id),self.neighbors))) + ']'        


class Graph():
    def __init__(self,vertices=None):
        self._vertices = dict()
        if vertices:
            for v in vertices:
                assert not self._vertices.get(v.id,False)
                self._vertices[v.id] = v

    @property
    def vertices(self):
        return self._vertices.values()

    def __len__(self):
        return len(self._vertices)

    def len_edges(self):
        return sum(map(lambda x:len(x),self._vertices.values()))

    def add(self, vertex):
        assert not self._vertices.get(vertex.id,False)
        self._vertices[vertex.id] = vertex

    def __getitem__(self,key):
        return self._vertices[key]

    def __iter__(self):
        keys = sorted(self._vertices.keys())
        for k in keys:
            yield self._vertices[k]
  
    def __str__(self):
        return '[' + ", ".join(map(str,self._vertices.values())) + ']'


if __name__ == "__main__":
    vs = [Vertex(x,'E' +str(x)) for x in range(5)]
    for v in vs:
        [v.add(x) for x in vs if x != v]
    g = Graph(vs)
    g[3].remove(g[0])
    for v in g.iter_by_greater_neighbors():
        print(v)
    for v in g.iter_by_less_neighbors():
        print(v)
    print(g)
    print(g.len_edges())

"""
test_create (__main__.TestGraph.test_create) ... ok
test_getitem (__main__.TestGraph.test_getitem) ... ok
test_create (__main__.TestVertex.test_create) ... ok
test_create_with_neighbors (__main__.TestVertex.test_create_with_neighbors) ... ok
test_eq (__main__.TestVertex.test_eq) ... ok
test_iter (__main__.TestVertex.test_iter) ... ok
test_neighbors (__main__.TestVertex.test_neighbors) ... ok
test_remove (__main__.TestVertex.test_remove) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
"""