#Optimal Linear Arrangement

import numpy as np
from munkres import Munkres

# Example pairwise distances between elements
distances = np.array([[0, 10, 15, 20],
                     [10, 0, 35, 25],
                     [15, 35, 0, 30],
                     [20, 25, 30, 0]])

# Create an instance of the Munkres class
munkres = Munkres()

# Solve the assignment problem and get the indices of the optimal linear arrangement
indices = munkres.compute(distances)

# Print the optimal linear arrangement
print([i+1 for i, j in indices])
