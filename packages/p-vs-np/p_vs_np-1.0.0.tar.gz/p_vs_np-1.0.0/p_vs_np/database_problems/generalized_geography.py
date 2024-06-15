#Generalized Geography


# Function to check if a word is valid

# Function to determine the next valid word

# List of countries and cities

# Game loop
    # Print the previous word

    # Get the next valid word

    # Print the next word and update the previous word

    # Remove the word from the list

    # Ask for user input to continue the game

if __name__ == '__main__':
    import random
    def is_valid_word(word, prev_word):
        if prev_word is None:
            return True
        return word[0].lower() == prev_word[-1].lower()
    def get_next_word(words, prev_word):
        valid_words = [word for word in words if is_valid_word(word, prev_word)]
        if valid_words:
            return random.choice(valid_words)
        return None
    words = ["Argentina", "Australia", "Austria", "Brazil", "Bahrain", "Belgium",
             "Canada", "China", "Colombia", "Croatia", "Denmark", "Dubai", "Egypt",
             "Ecuador", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
             "India", "Indonesia", "Ireland", "Italy", "Japan", "Jordan", "Kenya",
             "Kuwait", "Lebanon", "Luxembourg", "Malaysia", "Mexico", "Morocco",
             "Netherlands", "New Zealand", "Norway", "Oman", "Pakistan", "Panama",
             "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
             "Saudi Arabia", "Singapore", "South Africa", "Spain", "Sweden",
             "Switzerland", "Thailand", "Turkey", "Ukraine", "United Arab Emirates",
             "United Kingdom", "United States", "Uruguay", "Venezuela", "Vietnam",
             "Yemen", "Zambia", "Zimbabwe"]
    prev_word = None
    while True:
        if prev_word is not None:
            print("Previous word:", prev_word)
        next_word = get_next_word(words, prev_word)
        if next_word is None:
            print("No valid word. Game over!")
            break
        print("Next word:", next_word)
        prev_word = next_word
        words.remove(next_word)
        choice = input("Enter any key to continue (or 'q' to quit): ")
        if choice.lower() == "q":
            break
