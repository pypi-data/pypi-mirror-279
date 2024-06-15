#ETOL Grammar Non-Emptiness

    # Create a set to keep track of visited non-terminals

    # Perform depth-first search starting from the start symbol

    # Check if any non-terminal was visited, indicating non-emptiness


    # Base case: symbol is a terminal, stop recursion

    # Mark the symbol as visited

    # Recursively visit the production rules


# Example usage


if __name__ == '__main__':
    def is_etol_grammar_non_empty(grammar):
        visited = set()
        dfs(grammar, grammar['start_symbol'], visited)
        return bool(visited)
    def dfs(grammar, symbol, visited):
        if symbol not in grammar:
            return
        visited.add(symbol)
        for production in grammar[symbol]:
            for token in production:
                dfs(grammar, token, visited)
    grammar = {
        'start_symbol': 'S',
        'S': ['aA', 'bB'],
        'A': ['aA', ''],
        'B': ['bB', '']
    }
    etol_non_empty = is_etol_grammar_non_empty(grammar)
    print(f"ETOL Grammar Non-Emptiness: {etol_non_empty}")
