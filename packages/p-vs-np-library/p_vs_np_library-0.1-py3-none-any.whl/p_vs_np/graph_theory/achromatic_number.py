#Achromatic Number

def achromatic_number(graph, k):
    vertices = set(range(len(graph)))
    color_counts = [0] * k
    for vertex in vertices:
        for neighbor in vertices:
            if graph[vertex][neighbor]:
                color_counts[vertex % k] += 1
    return min(color_counts)

graph = [[0, 1, 1, 1],
         [1, 0, 1, 0],
         [1, 1, 0, 1],
         [1, 0, 1, 0]]
k = 3

print("Achromatic number is: ", achromatic_number(graph, k))
