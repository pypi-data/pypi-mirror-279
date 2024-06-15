#Geometric Steiner Tree

def geometric_steiner_tree(points, terminals):
    def dist(p1, p2):
        # Euclidean distance function
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def closest_point(point):
        min_dist = float("inf")
        closest = None
        for p in points:
            if p not in terminals:
                d = dist(point, p)
                if d < min_dist:
                    min_dist = d
                    closest = p
        return closest

    tree = []
    for terminal in terminals:
        closest = closest_point(terminal)
        if closest:
            tree.append((terminal, closest))
            terminals.append(closest)
    return tree
