import functools as f
from .models import Point, Graph


def slab(g: Graph, dot: Point):
    """Stripe method for dot localization."""
    separators = sorted(set(map(lambda x: x[1], g.vertices)))
    separators = [float("-inf")] + separators + [float("inf")]
    slabs = []
    for separ in range(len(separators) - 1):
        slabs.append((separators[separ], separators[separ + 1]))
    yield slabs
    table = first_stage(slabs, g)
    yield table
    slab = find_slab(slabs, dot)
    yield slab
    edges_to_check = sorted_edges_in_slab(table[slab], slab)
    yield check_edges(edges_to_check, dot)


def edge_value_in_y(edge, y):
    x1, y1 = edge.v1.point.coords
    x2, y2 = edge.v2.point.coords

    return (x2 - x1) * (y - y1) / (y2 - y1) + x1


def sorted_edges_in_slab(edges, slab):
    slab_median = sum(slab) / 2
    return sorted(edges, key=f.partial(edge_value_in_y, y=slab_median))


def edge_in_slab(self, slab):
    """True if edge y projection overlaps slab y region."""
    return (
        self.v1.point.y <= slab[0]
        and self.v2.point.y >= slab[1]
        or self.v2.point.y <= slab[0]
        and self.v1.point.y >= slab[1]
    )


def position_dot_edge(dot, edge):
    """Vector magic...

    * / -> positive(dot in left)
    / * -> negative(dor in right)
    * is on / -> 0
    """
    x1, y1 = edge.v1.point.coords
    x2, y2 = edge.v2.point.coords
    x3, y3 = dot.coords

    return (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)


def first_stage(slabs, g: Graph):
    """Return list of tuples (lower, upper) bounds for each slabs."""
    ans = {}
    for slab in slabs:
        ans.update({slab: list(filter(lambda x: edge_in_slab(x, slab), g.edges))})
    return ans


def dot_in_slab(dot, slab):
    """True if dot.y is in horizontal slab."""
    return slab[0] < dot.y <= slab[1]


def find_slab(slabs, dot):
    """Return slab in which dot is located from slab list."""
    return filter(lambda x: dot_in_slab(dot, x), slabs).__next__()


def dot_between_edges(dot, edges):
    """True if dot is in left of one edge and right of another."""
    return position_dot_edge(dot, edges[0]) * position_dot_edge(dot, edges[1]) < 0


def check_edges(edges, dot):
    """Return pair of edges, if dot is between them."""
    tuples = []
    for edge in range(len(edges) - 1):
        tuples.append((edges[edge], edges[edge + 1]))
    ans = filter(lambda x: dot_between_edges(dot, x), tuples).__next__()
    return list(ans)
