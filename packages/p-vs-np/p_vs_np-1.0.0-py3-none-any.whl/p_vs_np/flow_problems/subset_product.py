#Subset Product






# Example usage:



if __name__ == '__main__':
    def can_subset_product(nums, target):
        return subset_product(nums, target, 0)
    def subset_product(nums, target, index):
        if target == 1:
            return True
        if target < 1 or index >= len(nums):
            return False
        if nums[index] <= target and target % nums[index] == 0:
            return True
        return subset_product(nums, target // nums[index], index + 1) or subset_product(nums, target, index + 1)
    nums = [2, 3, 5, 7]
    target = 42
    result = can_subset_product(nums, target)
    if result:
        print("Subset with the product exists")
    else:
        print("Subset with the product does not exist")
