#Set Packing


    # Sort sets by decreasing order of size



# Example usage:



if __name__ == '__main__':
    def set_packing(sets):
        selected_sets = []
        sorted_sets = sorted(sets, key=len, reverse=True)
        for s in sorted_sets:
            if all(not set_.intersection(s) for set_ in selected_sets):
                selected_sets.append(s)
        return selected_sets
    sets = [
        {1, 2, 3},
        {2, 3, 4},
        {4, 5, 6},
        {6, 7, 8},
        {8, 9, 10}
    ]
    selected_sets = set_packing(sets)
    print("Selected Sets:")
    for s in selected_sets:
        print(s)
