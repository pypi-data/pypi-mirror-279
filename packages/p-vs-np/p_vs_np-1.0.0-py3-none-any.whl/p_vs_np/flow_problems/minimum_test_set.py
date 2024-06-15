#Minimum Test Set








# Example usage:



if __name__ == '__main__':
    def minimum_test_set(elements, pairs):
        covered_pairs = set()
        minimum_test_set = []
        while len(covered_pairs) < len(pairs):
            max_covered_count = 0
            max_covered_element = None
            for element in elements:
                covered_count = sum(1 for pair in pairs if element in pair and pair not in covered_pairs)
                if covered_count > max_covered_count:
                    max_covered_count = covered_count
                    max_covered_element = element
            if max_covered_element is None:
                break
            minimum_test_set.append(max_covered_element)
            covered_pairs.update(pair for pair in pairs if max_covered_element in pair)
        return minimum_test_set
    elements = {1, 2, 3, 4, 5}
    pairs = [
        {1, 2},
        {1, 3},
        {2, 3},
        {3, 4},
        {4, 5}
    ]
    test_set = minimum_test_set(elements, pairs)
    print("Minimum Test Set:")
    print(test_set)
