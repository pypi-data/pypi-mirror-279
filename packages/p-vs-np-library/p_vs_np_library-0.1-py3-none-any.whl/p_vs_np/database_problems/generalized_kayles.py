#Generalized Kayles


def is_winning_position(n, k, positions):
    dp = [False] * (n + 1)

    # Iterate through all positions up to n
    for i in range(1, n + 1):
        # Check if current position is a winning position
        if not dp[i]:
            continue

        # Iterate through all possible moves
        for move in range(1, k + 1):
            if i + move in positions:
                continue

            # Check if the next position is a losing position
            if i + move > n or not dp[i + move]:
                dp[i + move] = True

    return dp[n]


# Example usage
n = 10  # Number of tokens
k = 3  # Maximum number of tokens to remove in one move
positions = [2, 4, 6]  # Positions of the tokens

is_first_player_winning = is_winning_position(n, k, positions)

if is_first_player_winning:
    print("The first player has a winning strategy.")
else:
    print("The first player does not have a winning strategy.")
