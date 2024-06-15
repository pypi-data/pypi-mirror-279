#Domatic Number

        # Check if S is a dominating set for G



if __name__ == '__main__':
    def domatic_number(G, k):
        def is_dominating_set(G, S):
            pass
        def backtrack(G, S, k, curr):
            if len(S) == k:
                if all(is_dominating_set(G, S[i]) for i in range(k)):
                    return True
                else:
                    return False
            for v in range(curr, len(G)):
                S.append(v)
                if backtrack(G, S, k, v+1):
                    return True
                S.pop()
            return False
        min_domatic_number = float('inf')
        for k in range(k, len(G)):
            for S in itertools.combinations(range(len(G)), k):
                if backtrack(G, list(S), k, 0):
                    min_domatic_number = min(min_domatic_number, k)
                    break
        if min_domatic_number == float('inf'):
            return -1
        return min_domatic_number
