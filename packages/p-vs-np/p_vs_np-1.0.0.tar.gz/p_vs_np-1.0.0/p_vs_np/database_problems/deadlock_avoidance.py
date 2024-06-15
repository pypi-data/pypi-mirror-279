#Deadlock Avoidance









    # Check if the initial state is safe

    # Try to allocate resources to processes

            # Check if the new state is safe



# Example usage
    # Example resource allocation and maximum demand

    # Perform deadlock avoidance


if __name__ == '__main__':
    from collections import defaultdict
    def is_safe_state(available, allocation, need):
        processes = len(allocation)
        resources = len(available)
        work = available[:]
        finish = [False] * processes
        sequence = []
        while True:
            found = False
            for p in range(processes):
                if not finish[p] and all(need[p][r] <= work[r] for r in range(resources)):
                    work = [work[r] + allocation[p][r] for r in range(resources)]
                    finish[p] = True
                    sequence.append(p)
                    found = True
            if not found:
                break
        return all(finish)
    def deadlock_avoidance(available, allocation, maximum):
        processes = len(allocation)
        resources = len(available)
        need = [[maximum[p][r] - allocation[p][r] for r in range(resources)] for p in range(processes)]
        if not is_safe_state(available, allocation, need):
            return False, []
        for p in range(processes):
            if all(available[r] >= need[p][r] for r in range(resources)):
                available = [available[r] + allocation[p][r] for r in range(resources)]
                allocation[p] = [0] * resources
                if not is_safe_state(available, allocation, need):
                    return False, []
        return True, available
    if __name__ == "__main__":
        available = [3, 1, 2]
        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]
        safe, available = deadlock_avoidance(available, allocation, maximum)
        if safe:
            print("No deadlock detected. Available resources:", available)
        else:
            print("Deadlock detected. System is in an unsafe state.")
