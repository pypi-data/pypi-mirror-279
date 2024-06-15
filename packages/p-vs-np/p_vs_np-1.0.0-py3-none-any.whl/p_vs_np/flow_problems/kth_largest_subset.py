#Kth Largest Subset







# Example usage:




if __name__ == '__main__':
    def kth_largest_subset(numbers, k):
        subsets = []
        generate_subsets(numbers, [], subsets)
        subsets.sort(key=lambda x: sum(x), reverse=True)
        if k > len(subsets):
            return None
        return subsets[k - 1]
    def generate_subsets(numbers, current_subset, subsets):
        subsets.append(current_subset[:])
        for i in range(len(numbers)):
            current_subset.append(numbers[i])
            generate_subsets(numbers[i+1:], current_subset, subsets)
            current_subset.pop()
    numbers = [2, 4, 6, 8]
    k = 2
    kth_largest = kth_largest_subset(numbers, k)
    if kth_largest is None:
        print("No kth largest subset found.")
    else:
        print(f"The {k}th largest subset:", kth_largest)
