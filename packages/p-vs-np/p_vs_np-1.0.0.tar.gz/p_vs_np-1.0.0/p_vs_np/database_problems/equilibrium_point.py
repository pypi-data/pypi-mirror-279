#Equilibrium Point








# Example usage


if __name__ == '__main__':
    def equilibrium_point(arr):
        total_sum = sum(arr)
        left_sum = 0
        for i in range(len(arr)):
            total_sum -= arr[i]
            if left_sum == total_sum:
                return i
            left_sum += arr[i]
        return -1
    array = [1, 2, 3, 4, 5, 5, 1, 1]
    equilibrium = equilibrium_point(array)
    if equilibrium != -1:
        print("Equilibrium point found at index", equilibrium)
    else:
        print("No equilibrium point found in the array.")
