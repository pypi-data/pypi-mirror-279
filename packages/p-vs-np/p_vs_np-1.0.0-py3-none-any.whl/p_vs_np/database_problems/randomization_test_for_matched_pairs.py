#Randomization test for matched pairs


    # Calculate the observed difference

    # Generate random permutations and calculate the difference for each permutation

    # Calculate the p-value


# Example usage
    # Define your matched pairs as a list of tuples

    # Run the randomization test

    # Print the results

if __name__ == '__main__':
    import random
    def randomization_test(matched_pairs):
        observed_diff = sum(x - y for x, y in matched_pairs)
        permutation_diffs = []
        num_permutations = 1000  # Number of random permutations to generate (adjust as needed)
        for _ in range(num_permutations):
            random.shuffle(matched_pairs)
            diff = sum(x - y for x, y in matched_pairs)
            permutation_diffs.append(diff)
        num_extreme = sum(diff >= observed_diff for diff in permutation_diffs)
        p_value = (num_extreme + 1) / (num_permutations + 1)
        return observed_diff, p_value
    if __name__ == '__main__':
        matched_pairs = [(2, 5), (4, 8), (3, 6), (1, 4), (7, 9)]
        observed_diff, p_value = randomization_test(matched_pairs)
        print("Observed Difference:", observed_diff)
        print("p-value:", p_value)
