from math import pi
from .models import Point, ThreadedBinTree


def preparata(points):
    points.sort()

    # Find first three non-collinear points
    i = 2
    while Point.direction(points[0], points[1], points[i]) == 0:
        i += 1
    
    # Insert 3rd point in the correct position
    point3 = points[i]
    del points[i]
    points.insert(2, point3)

    hulls, trees, left_paths, right_paths, deleted_points = [], [], [], [], []

    # Construct the initial hull clockwise, starting from the leftmost point
    hull = [points[0]] + sorted(points[1:3], key=lambda p: -p.polar_angle_with(points[0]))
    hulls.append(hull)

    for point in points[3:]:
        tree = ThreadedBinTree.from_iterable(hull)
        trees.append(tree)

        left_supporting_path = find_path_to_supporting_point(tree, point, search_left_supporting=True)
        right_supporting_path = find_path_to_supporting_point(tree, point, search_left_supporting=False)
        left_paths.append(left_supporting_path)
        right_paths.append(right_supporting_path)
        
        left_i = hull.index(left_supporting_path[-1])
        right_i = hull.index(right_supporting_path[-1])
        
        # Drop the points from exclusive range (right, left) and insert the new point between right and left.
        deleted_points.append(hull[right_i+1:] if left_i < right_i else hull[right_i+1:left_i])
        hull = hull[:right_i+1] + [point] + ([] if left_i < right_i else hull[left_i:])
        hulls.append(hull)
    
    yield hulls[0], trees[0]
    yield left_paths, right_paths
    yield deleted_points
    yield hulls[1:], trees[1:]
    yield hull


def find_path_to_supporting_point(tree, point, search_left_supporting):
    path = []
    node, prev = tree.root, None
    
    while prev != node:
        prev = node
        path.append(node.data)
        node = find_next_node(node, point, search_left_supporting)
    
    return path


def find_next_node(node, point, search_left_supporting):

    # [0, 2*pi) polar angle in coordinate system with axis node.data -> point (rotated against x axis by rot)
    def polar_angle(p):
        rot = point.ccw_polar_angle_with(node.data)
        angle = p.ccw_polar_angle_with(node.data)
        return angle - rot + (2 * pi if angle < rot else 0)

    angles = polar_angle(node.left.data), polar_angle(node.right.data)
    angle1 = min(angles)
    angle2 = max(angles)

    convex_or_reflex = 0 < angle1 <= pi <= angle2 < 2 * pi

    # Convex
    if convex_or_reflex and angle2 < angle1 + pi:
        return node.right if search_left_supporting else node.left
    
    # Reflex
    if convex_or_reflex and angle2 > angle1 + pi:
        return node.left if search_left_supporting else node.right

    # Left supporting
    if 0 <= angle1 < angle2 < pi:
        return node if search_left_supporting else node.left
    
    # Right supporting
    if angle1 == 0:
        angle1 = 2 * pi
        angle1, angle2 = angle2, angle1
    
    if pi < angle1 < angle2 <= 2 * pi:
        return node.right if search_left_supporting else node
