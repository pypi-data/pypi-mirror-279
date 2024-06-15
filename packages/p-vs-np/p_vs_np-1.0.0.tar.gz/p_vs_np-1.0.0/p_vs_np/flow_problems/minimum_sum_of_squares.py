#Minimum Sum of Squares




# Example usage:



if __name__ == '__main__':
    def minimum_sum_of_squares(numbers):
        n = len(numbers)
        memo = [float('inf')] * (n + 1)
        memo[0] = 0
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                memo[i] = min(memo[i], memo[i - j] + numbers[i - 1] ** 2)
        return memo[n]
    numbers = [2, 3, 4, 5]
    minimum_sum = minimum_sum_of_squares(numbers)
    print("Minimum Sum of Squares:", minimum_sum)
