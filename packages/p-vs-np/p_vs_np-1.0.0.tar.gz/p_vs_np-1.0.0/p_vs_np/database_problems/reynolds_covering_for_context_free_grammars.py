#Reynolds Covering For Context-Free Grammars



    # Initialize an empty set of non-terminals

    # Compute the set of terminals

    # Create a mapping of terminals to non-terminals that can generate them

    # Find the minimum set of non-terminals that cover all terminals

        # Find the terminal with maximum coverage

        # Remove the terminal from the set and remove the covering non-terminals

    # Return the minimum set of non-terminals that cover all terminals


# Example usage



if __name__ == '__main__':
    from collections import defaultdict
    def find_reynolds_cover(grammar):
        non_terminals = set(grammar.keys())
        terminals = set()
        for productions in grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol.islower():
                        terminals.add(symbol)
        terminal_coverage = defaultdict(set)
        for non_terminal, productions in grammar.items():
            for production in productions:
                for symbol in production:
                    if symbol in terminals:
                        terminal_coverage[symbol].add(non_terminal)
        while terminals:
            max_coverage = set()
            max_terminal = None
            for terminal, cover in terminal_coverage.items():
                if len(cover) > len(max_coverage):
                    max_coverage = cover
                    max_terminal = terminal
            terminals.remove(max_terminal)
            non_terminals -= max_coverage
        return non_terminals
    grammar = {
        'S': ['aSb', ''],
        'A': ['aA', 'b']
    }
    reynolds_cover = find_reynolds_cover(grammar)
    print(f"Reynolds Cover: {reynolds_cover}")
