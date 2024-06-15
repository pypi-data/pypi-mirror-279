#Bin Packing





# Example usage

if __name__ == '__main__':
    def first_fit(bin_capacity, items):
        bins = [[]]
        for item in items:
            assigned = False
            for bin in bins:
                if sum(bin) + item <= bin_capacity:
                    bin.append(item)
                    assigned = True
                    break
            if not assigned:
                bins.append([item])
        return bins
    def bin_packing(bin_capacity, items):
        items.sort(reverse=True)  # Sort items in descending order
        return first_fit(bin_capacity, items)
    bin_capacity = 10
    items = [4, 5, 6, 7, 8, 9, 10]
    bins = bin_packing(bin_capacity, items)
    print(f"Items: {items}")
    print(f"Bin Capacity: {bin_capacity}")
    print(f"Number of Bins Required: {len(bins)}")
    print("Bins:")
    for i, bin in enumerate(bins):
        print(f"Bin {i + 1}: {bin}")
