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

        a.left, a.right = i, b
        a.threaded_left = a.threaded_right = True
        c.left, c.right = b, d
        c.threaded_left = c.threaded_right = True
        e.left, e.right = d, f
        e.threaded_left = e.threaded_right = True
        g.left = f
        g.threaded_left = True
        h.left, h.right = g, i
        h.threaded_left = h.threaded_right = True
        i.right = a
        i.threaded_right = True

        self.assertEqual(root, tree.root)
    
    def test_threaded_bin_tree_from_iterable(self):
        lst = ["A", "B", "C", "D", "E"]
        c = root = ThreadedBinTreeNode("C")
        a = root.left = ThreadedBinTreeNode("A")
        b = root.left.right = ThreadedBinTreeNode("B")
        d = root.right = ThreadedBinTreeNode("D")
        e = root.right.right = ThreadedBinTreeNode("E")

        a.left = e
        a.threaded_left = True
        b.left, b.right = a, c
        b.threaded_left = b.threaded_right = True
        d.left = c
        d.threaded_left = True
        e.left, e.right = d, a
        e.threaded_left = e.threaded_right = True

        tree = ThreadedBinTree(root)
        self.assertEqual(tree, ThreadedBinTree.from_iterable(lst))

        

