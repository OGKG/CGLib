import unittest
import math
from copy import deepcopy
from CGLib.models import Point, Vertex, Graph, Vector, Triangle, Polygon, ThreadedBinTreeNode, ThreadedBinTree


class TestModels(unittest.TestCase):
    """Test class for basic entities."""

    def test_point_creation(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2, 3.6)
        self.assertEqual(p1.coords, (1, 2))
        self.assertEqual(p2.coords, (1, 2, 3.6))

    def test_graph_vertex_add(self):
        g = Graph()
        v1 = Vertex(Point(1, 2))
        v2 = Vertex(Point(2, 1))

        g.add_vertex(v1)
        g.add_vertex(v2)

        g.add_edge(v1, v2)
        g.add_edge(v2, v1)

        self.assertEqual(len(g.edges), 1)

    def test_point_domination(self):
        a = Point(1, 2)
        b = Point(3, 4)
        c = Point(2, 2)
        self.assertTrue(b.dominating(a))
        self.assertTrue(b.dominating(c))
        self.assertFalse(a.dominating(c))

    def test_vectors(self):
        a = Vector([1, 1])
        b = Vector([0, 12])
        self.assertAlmostEqual(a.angle(b), math.pi / 4)

    def test_polygon_in(self):
        p1 = Point(1, 1)
        p2 = Point(1, -1)
        p3 = Point(-1, -1)
        p4 = Point(-1, 1)
        p = Polygon([p1, p2, p3, p4])

        p0 = Point(0, 0)
        pn = Point(1.1, 1)
        self.assertEqual(p.contains_point(p0), True)
        self.assertNotEqual(p.contains_point(pn), True)

    def test_point_centroid(self):
        p1 = Point(1, 2, 3)
        p2 = Point(1, 5, 6)
        p3 = Point(1, 2, 3)
        self.assertEqual(Point.centroid((p1, p2, p3)), Point(1, 3, 4))

        p1 = Point(1, 2, 3)
        p2 = Point(1, 5, 6)
        p3 = Point(1, 2, 3)
        p4 = Point(1, 2, 3)
        self.assertEqual(Point.centroid((p1, p2, p3, p4)), Point(1, 2.75, 3.75))

    def test_triangle_area(self):
        p1 = Point(0, 1)
        p2 = Point(0, 0)
        p3 = Point(1, 0)
        t = Triangle(p1, p2, p3)
        self.assertAlmostEqual(t.area, 0.5)

        p1 = Point(-100, 0)
        p2 = Point(0, 100)
        p3 = Point(100, 0)
        t = Triangle(p1, p2, p3)
        self.assertAlmostEqual(t.area, 10000)

    def test_polygon_area(self):
        p1 = Point(0, 0)
        p2 = Point(0, 100)
        p3 = Point(100, 100)
        p4 = Point(100, 0)
        p = Polygon((p1, p2, p3, p4))
        self.assertAlmostEqual(p.area, 10000)
        self.assertAlmostEqual(p.area, 10000)

    def test_threaded_bin_trees_eq(self):
        f = root = ThreadedBinTreeNode("F")
        b = root.left = ThreadedBinTreeNode("B")
        a = root.left.left = ThreadedBinTreeNode("A")
        d = root.left.right = ThreadedBinTreeNode("D")
        c = root.left.right.left = ThreadedBinTreeNode("C")
        e = root.left.right.right = ThreadedBinTreeNode("E")
        g = root.right = ThreadedBinTreeNode("G")
        i = root.right.right = ThreadedBinTreeNode("I")
        h = root.right.right.left = ThreadedBinTreeNode("H")

        root2 = deepcopy(root)
        tree = ThreadedBinTree(root2)

        a.prev, a.next = i, b
        b.prev, b.next = a, c
        c.prev, c.next = b, d
        d.prev, d.next = c, e
        e.prev, e.next = d, f
        f.prev, f.next = e, g
        g.prev, g.next = f, h
        h.prev, h.next = g, i
        i.prev, i.next = h, a

        self.assertEqual(root, tree.root)
    
    def test_threaded_bin_tree_from_iterable(self):
        lst = ["A", "B", "C", "D", "E"]
        c = root = ThreadedBinTreeNode("C")
        a = root.left = ThreadedBinTreeNode("A")
        b = root.left.right = ThreadedBinTreeNode("B")
        d = root.right = ThreadedBinTreeNode("D")
        e = root.right.right = ThreadedBinTreeNode("E")

        a.prev, a.next = e, b
        b.prev, b.next = a, c
        c.prev, c.next = b, d
        d.prev, d.next = c, e
        e.prev, e.next = d, a

        tree = ThreadedBinTree(root)
        self.assertEqual(tree, ThreadedBinTree.from_iterable(lst))
    
    def test_threaded_bin_tree_non_circular(self):
        b = root = ThreadedBinTreeNode("B")
        a = root.left = ThreadedBinTreeNode("A")
        c = root.right = ThreadedBinTreeNode("C")

        a.next = b
        b.prev, b.next = a, c
        c.prev = b
        
        tree = ThreadedBinTree(root)
        self.assertEqual(tree, ThreadedBinTree.from_iterable(["A", "B", "C"], circular=False))
