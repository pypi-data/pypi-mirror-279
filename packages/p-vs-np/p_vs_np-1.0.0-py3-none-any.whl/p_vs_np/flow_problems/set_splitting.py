#Set Splitting











# Example usage:



if __name__ == '__main__':
    def set_splitting(set_):
        total_sum = sum(set_)
        if total_sum % 2 != 0:
            return False
        target_sum = total_sum // 2
        def backtrack(curr_set, curr_sum, start):
            if curr_sum == target_sum:
                return True
            if curr_sum > target_sum or start >= len(set_):
                return False
            for i in range(start, len(set_)):
                if set_[i] not in curr_set:
                    curr_set.add(set_[i])
                    curr_sum += set_[i]
                    if backtrack(curr_set, curr_sum, i + 1):
                        return True
                    curr_set.remove(set_[i])
                    curr_sum -= set_[i]
            return False
        return backtrack(set(), 0, 0)
    set_ = {1, 2, 3, 4, 5, 6}
    if set_splitting(set_):
        print("Set can be split into two equal-sum subsets.")
    else:
        print("Set cannot be split into two equal-sum subsets.")
