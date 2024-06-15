#Regular Grammar Inequivalence

    # Generate the languages for both grammars

    # Check if the languages are different


    # Initialize the language as an empty set

    # Iterate through each production rule
            # Generate the words by expanding the production rules

            # Add the generated words to the language



    # Base case: If the production is empty, return an empty word


    # Expand the non-terminals in the production

            # Recursively generate words for each non-terminal

            # Concatenate the generated words with the remaining production

            # The symbol is a terminal, so append it to each word



# Example usage




if __name__ == '__main__':
    def are_regular_grammars_inequivalent(grammar1, grammar2):
        language1 = generate_language(grammar1)
        language2 = generate_language(grammar2)
        if language1 != language2:
            return True
        else:
            return False
    def generate_language(grammar):
        language = set()
        for non_terminal, productions in grammar.items():
            for production in productions:
                words = generate_words(grammar, production)
                language.update(words)
        return language
    def generate_words(grammar, production):
        if production == '':
            return ['']
        words = []
        for symbol in production:
            if symbol in grammar:
                non_terminal_productions = grammar[symbol]
                non_terminal_words = generate_words(grammar, non_terminal_productions[0])
                words = [word + remaining for word in non_terminal_words for remaining in generate_words(grammar, production[1:])]
            else:
                words = [word + symbol for word in words]
        return words
    grammar1 = {
        'S': ['aS', 'bA', ''],
        'A': ['aA', 'bB'],
        'B': ['bB', 'b']
    }
    grammar2 = {
        'S': ['aS', 'bS', ''],
        'A': ['aA', 'bB'],
        'B': ['bB', 'b']
    }
    inequivalent = are_regular_grammars_inequivalent(grammar1, grammar2)
    print(f"Inequivalent: {inequivalent}")
