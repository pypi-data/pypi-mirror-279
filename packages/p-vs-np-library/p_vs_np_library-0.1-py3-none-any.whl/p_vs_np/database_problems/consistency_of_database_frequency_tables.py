#Consistency of Database Frequency Tables

def is_consistent(frequency_tables):
    # Create an empty dictionary to store the attribute combinations and their counts
    attribute_counts = {}

    # Iterate through each frequency table
    for table in frequency_tables:
        # Iterate through each attribute combination and its count in the table
        for attributes, count in table.items():
            # Check if the attribute combination is already in the dictionary
            if attributes in attribute_counts:
                # If it exists, check if the count matches the existing count
                if attribute_counts[attributes] != count:
                    return False
            else:
                # If it doesn't exist, add it to the dictionary with its count
                attribute_counts[attributes] = count

    return True

# Example usage
frequency_tables = [
    {'A': 3, 'B': 5},
    {'A': 3, 'C': 5},
    {'A': 3, 'B': 5, 'C': 7}
]

result = is_consistent(frequency_tables)
print(result)
