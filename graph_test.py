
from graph import *
import unittest

class TestVertex(unittest.TestCase):
    def test_create(self):
        for data in [None, 3, 'abc', [2,0], Vertex(3,3)]:
            v = Vertex(2,data)
            self.assertEqual(v.id, 2)
            self.assertIs(v.data, data)
            self.assertEqual(len(v),0)

    def test_neighbors(self):
        vs = [Vertex(x,x) for x in range(5)]
        for n in vs[1:]:
            vs[0].add(n)

        self.assertEqual(len(vs[0]),len(vs)-1)
        self.assertEqual(len(vs[0].neighbors),len(vs)-1)

        for n in vs[1:]:
            self.assertEqual(len(n),0)
            self.assertTrue(n in vs[0].neighbors)

    def test_create_with_neighbors(self):
        vs = [Vertex(x,x) for x in range(5)]
        v = Vertex(2,2,vs)

        self.assertEqual(len(v),len(vs))
        for x in v.neighbors:
            self.assertTrue(x in vs)

    def test_iter(self):
        vs = [Vertex(x,x) for x in range(5)]
        v = Vertex(2,2,vs)
        for x in v:
            self.assertTrue(x in vs)

    def test_eq(self):
        v1 = Vertex(2,2)
        v2 = Vertex(3,5)
        v3 = v1
        v4 = Vertex(2,5)

        self.assertFalse(v1 == v2)
        self.assertTrue(v1 == v1)
        self.assertTrue(v1 == v3)
        self.assertTrue(v1 == v4)

    def test_remove(self):
        vs = [Vertex(x,x) for x in range(5)]
        for n in vs[1:]:
            vs[0].add(n)

        self.assertEqual(len(vs[0]), len(vs)-1)
        for n in vs[1:]:
            self.assertTrue(n in vs[0])
            vs[0].remove(n)
            self.assertFalse(n in vs[0])

        self.assertEqual(len(vs[0]), 0)


class TestGraph(unittest.TestCase):
    def test_create(self):
        vs = [Vertex(x,x) for x in range(5)]
        g = Graph()

        self.assertEqual(len(g),0)
        self.assertEqual(len(g.vertices),0)

        for v in vs:
            g.add(v)
        self.assertEqual(len(g),len(vs))
        self.assertEqual(len(g.vertices),len(vs))
        self.assertEqual(g.len_edges(),0)

        g2 = Graph(vs)
        self.assertEqual(len(g),len(vs))
        self.assertEqual(len(g.vertices),len(vs))
        vs[2].add(vs[3])
        vs[3].add(vs[4])
        self.assertEqual(g2.len_edges(),2)

    def test_getitem(self):
        vs = [Vertex(x,x) for x in range(5)]
        g1 = Graph(vs)

        for idx,_ in enumerate(vs):
            self.assertTrue(g1[idx] in vs)

        v = Vertex(10,10)
        self.assertEqual(hash(v),v.id)
        with self.assertRaises(KeyError):
            g1[v]
    

if __name__ == "__main__":
    unittest.main(argv=['ignore'], exit=False, verbosity=2)