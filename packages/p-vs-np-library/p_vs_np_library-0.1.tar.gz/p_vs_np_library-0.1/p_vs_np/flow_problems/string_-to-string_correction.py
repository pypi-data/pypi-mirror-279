#String -to-string Correction

def string_correction(str1, str2):
    m = len(str1)
    n = len(str2)

    # Initialize a table to store the minimum edit distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and column of the table
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill in the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])

    # Traverse the table to find the sequence of operations
    i = m
    j = n
    operations = []

    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(f"Replace '{str1[i - 1]}' with '{str2[j - 1]}'")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i][j - 1] + 1:
            operations.append(f"Insert '{str2[j - 1]}'")
            j -= 1
        else:
            operations.append(f"Delete '{str1[i - 1]}'")
            i -= 1

    while i > 0:
        operations.append(f"Delete '{str1[i - 1]}'")
        i -= 1

    while j > 0:
        operations.append(f"Insert '{str2[j - 1]}'")
        j -= 1

    operations.reverse()

    return dp[m][n], operations

# Example usage
str1 = "kitten"
str2 = "sitting"

distance, operations = string_correction(str1, str2)
print("Minimum Edit Distance:", distance)
print("Operations:")
for operation in operations:
    print(operation)
