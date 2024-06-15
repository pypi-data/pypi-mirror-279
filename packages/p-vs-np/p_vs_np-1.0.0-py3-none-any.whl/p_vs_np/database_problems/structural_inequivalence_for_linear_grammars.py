#Structural Inequivalence For Linear Grammars

    # Check if the number of non-terminals is different

    # Check if the production rules for each non-terminal are the same



# Example usage



if __name__ == '__main__':
    def are_linear_grammars_structurally_equivalent(grammar1, grammar2):
        if len(grammar1) != len(grammar2):
            return False
        for non_terminal in grammar1:
            if non_terminal not in grammar2:
                return False
            if grammar1[non_terminal] != grammar2[non_terminal]:
                return False
        return True
    grammar1 = {
        'S': ['aA', 'bB', ''],
        'A': ['aA', 'a'],
        'B': ['bB', 'b']
    }
    grammar2 = {
        'S': ['aA', 'bB', ''],
        'A': ['aA', 'a'],
        'B': ['bB', 'b']
    }
    equivalent = are_linear_grammars_structurally_equivalent(grammar1, grammar2)
    print(f"Structurally Equivalent: {equivalent}")
