#Ensemble Computation

import multiprocessing

class EnsembleComputation:
    def __init__(self, function, inputs):
        self.function = function
        self.inputs = inputs

    def compute(self):
        pool = multiprocessing.Pool()
        results = pool.map(self.function, self.inputs)
        pool.close()
        pool.join()

        return results

# Example usage
def square(x):
    return x * x

inputs = [1, 2, 3, 4, 5]

ensemble_computation = EnsembleComputation(square, inputs)
results = ensemble_computation.compute()

print("Results:")
print(results)
