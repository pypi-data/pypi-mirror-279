#Isomorphic Spanning Tree

from collections import defaultdict

def isomorphic_spanning_tree(n, edges, target_tree):
    def dfs(v, visited, tree):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                tree.append((v, neighbor))
                dfs(neighbor, visited, tree)

    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append(v)
        graph[v].append(u)

    def backtrack(tree, visited):
        if len(visited) == n:
            if tree == target_tree:
                return True
            else:
                return False
        for u, v, w in edges:
            if (u, v) not in tree and (v, u) not in tree and u in visited and v not in visited:
                tree.append((u, v))
                visited.add(v)
                if backtrack(tree, visited):
                    return True
                tree.pop()
                visited.remove(v)
            if (v, u) not in tree and (u, v) not in tree and v in visited and u not in visited:
                tree.append((v, u))
                visited.add(u)
                if backtrack(tree, visited):
                    return True
                tree.pop()
                visited.remove(u)
        return False

    visited = set()
    tree = []
    dfs(0, visited, tree)
    if backtrack(tree, visited):
        return tree
    else:
        return None
