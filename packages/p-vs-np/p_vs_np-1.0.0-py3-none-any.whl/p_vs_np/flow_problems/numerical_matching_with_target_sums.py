#Numerical Matching With Target Sums








# Example usage:




if __name__ == '__main__':
    def can_numerical_matching(nums, target_sum):
        return numerical_matching(nums, [], target_sum)
    def numerical_matching(nums, subset, target_sum):
        if sum(subset) == target_sum:
            return True
        if sum(subset) > target_sum:
            return False
        for i in range(len(nums)):
            subset.append(nums[i])
            if numerical_matching(nums[i+1:], subset, target_sum):
                return True
            subset.pop()
        return False
    nums = [1, 2, 3, 4, 5]
    target_sum = 9
    result = can_numerical_matching(nums, target_sum)
    if result:
        print("There exists a Numerical Matching with the target sum")
    else:
        print("There does not exist a Numerical Matching with the target sum")
