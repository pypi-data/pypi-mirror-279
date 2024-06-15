#Composite Number



    # Check divisibility up to the square root of n


# Example usage
    # Example number

    # Check if the number is composite

    # Print the result


if __name__ == '__main__':
    import math
    def is_composite_number(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return True
        return False
    if __name__ == '__main__':
        number = 15
        result = is_composite_number(number)
        if result:
            print(f"The number {number} is composite.")
        else:
            print(f"The number {number} is not composite.")
