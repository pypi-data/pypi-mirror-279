#Kth Largest m-Tuple





# Example usage


if __name__ == '__main__':
    def generate_tuples(n, m):
        tuples = []
        generate_tuples_helper(n, m, [], tuples)
        return tuples
    def generate_tuples_helper(n, m, current_tuple, tuples):
        if len(current_tuple) == m:
            tuples.append(tuple(current_tuple))
            return
        for i in range(1, n + 1):
            current_tuple.append(i)
            generate_tuples_helper(n, m, current_tuple, tuples)
            current_tuple.pop()
    def kth_largest_m_tuple(n, m, k):
        tuples = generate_tuples(n, m)
        sorted_tuples = sorted(tuples, reverse=True)
        if k <= len(sorted_tuples):
            return sorted_tuples[k - 1]
        else:
            return None
    n = 3
    m = 2
    k = 4
    result = kth_largest_m_tuple(n, m, k)
    if result:
        print(f"The {k}th largest {m}-tuple for n={n} is: {result}")
    else:
        print(f"The {k}th largest {m}-tuple does not exist for n={n}")
