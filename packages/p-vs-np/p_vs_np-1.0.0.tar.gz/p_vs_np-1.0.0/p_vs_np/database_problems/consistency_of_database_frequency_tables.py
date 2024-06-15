#Consistency of Database Frequency Tables

    # Create an empty dictionary to store the attribute combinations and their counts

    # Iterate through each frequency table
        # Iterate through each attribute combination and its count in the table
            # Check if the attribute combination is already in the dictionary
                # If it exists, check if the count matches the existing count
                # If it doesn't exist, add it to the dictionary with its count


# Example usage


if __name__ == '__main__':
    def is_consistent(frequency_tables):
        attribute_counts = {}
        for table in frequency_tables:
            for attributes, count in table.items():
                if attributes in attribute_counts:
                    if attribute_counts[attributes] != count:
                        return False
                else:
                    attribute_counts[attributes] = count
        return True
    frequency_tables = [
        {'A': 3, 'B': 5},
        {'A': 3, 'C': 5},
        {'A': 3, 'B': 5, 'C': 7}
    ]
    result = is_consistent(frequency_tables)
    print(result)
