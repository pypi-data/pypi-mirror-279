#K - Relevancy



    # Generate all possible subsets of X with cardinality <= K

        # Check if the condition holds for all m-tuples y_bar
                # A counterexample found, X' is not K-relevant

    # No counterexample found, X' is K-relevant


    # Generate the m-tuples y_bar, you need to implement this function
    # based on the specific requirements of your problem

    # For demonstration purposes, a dummy generator is provided


# Example usage


if __name__ == '__main__':
    from itertools import combinations
    def is_k_relevant(X, K):
        subsets = [set(combo) for r in range(K + 1) for combo in combinations(X, r)]
        for X_prime in subsets:
            for y_bar in m_tuple_generator():
                if any(x_bar.dot(y_bar) > b for x_bar, b in X_prime):
                    return False
        return True
    def m_tuple_generator():
        yield [1, 2, 3]
        yield [-1, 0, 1]
        yield [0.5, 0.5, 0.5]
    X = [([1, 2, 3], 10), ([-1, 0, 1], 5), ([2, 2, 2], 8), ([3, 2, 1], 7)]
    K = 2
    result = is_k_relevant(X, K)
    print(f"Is there a subset X' with cardinality <= {K} that satisfies the condition? {result}")
