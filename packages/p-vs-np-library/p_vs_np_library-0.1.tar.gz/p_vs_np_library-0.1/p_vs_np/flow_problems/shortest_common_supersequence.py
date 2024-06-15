#Shortest Common Supersequence

def shortest_common_supersequence(s1, s2):
    m = len(s1)
    n = len(s2)

    # Create a table to store the lengths of the shortest common supersequences
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the table using dynamic programming
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1)

    # Reconstruct the shortest common supersequence
    supersequence = ""
    i, j = m, n

    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            supersequence = s1[i - 1] + supersequence
            i -= 1
            j -= 1
        elif dp[i - 1][j] + 1 == dp[i][j]:
            supersequence = s1[i - 1] + supersequence
            i -= 1
        else:
            supersequence = s2[j - 1] + supersequence
            j -= 1

    while i > 0:
        supersequence = s1[i - 1] + supersequence
        i -= 1

    while j > 0:
        supersequence = s2[j - 1] + supersequence
        j -= 1

    return supersequence

# Example usage
s1 = "AGGTAB"
s2 = "GXTXAYB"

result = shortest_common_supersequence(s1, s2)
print("Shortest Common Supersequence:", result)

