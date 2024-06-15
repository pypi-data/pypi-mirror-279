#Shapley-Shubik voting power

from itertools import permutations

def calculate_shapley_shubik(players, weights):
    n = len(players)
    total_weight = sum(weights)
    shapley_shubik = {}

    for player in players:
        shapley_shubik[player] = 0

    for perm in permutations(players):
        cumulative_weight = 0
        for i, player in enumerate(perm, start=1):
            cumulative_weight += weights[player]
            if cumulative_weight > total_weight / 2:
                shapley_shubik[player] += 1
                break

    for player in players:
        shapley_shubik[player] /= n

    return shapley_shubik

# Example usage
players = ['Alice', 'Bob', 'Charlie']
weights = [3, 2, 5]

voting_power = calculate_shapley_shubik(players, weights)

print("Shapley-Shubik Voting Power:")
for player, power in voting_power.items():
    print(player + ": " + str(power))
