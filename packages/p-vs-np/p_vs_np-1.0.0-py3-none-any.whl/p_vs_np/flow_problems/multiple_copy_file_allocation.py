#Multiple copy file allocation



    # Generate all possible allocations of files to storage devices




# Example usage



if __name__ == '__main__':
    import itertools
    def allocate_files(files, storage_devices):
        min_cost = float('inf')
        best_allocation = []
        allocations = list(itertools.product(storage_devices, repeat=len(files)))
        for allocation in allocations:
            total_cost = sum([allocation.count(device) for device in storage_devices])
            if total_cost < min_cost:
                min_cost = total_cost
                best_allocation = allocation
        return best_allocation
    files = ['file1', 'file2', 'file3']
    storage_devices = ['device1', 'device2', 'device3']
    allocation = allocate_files(files, storage_devices)
    print("Best Allocation:")
    for file, device in zip(files, allocation):
        print(file, ":", device)
