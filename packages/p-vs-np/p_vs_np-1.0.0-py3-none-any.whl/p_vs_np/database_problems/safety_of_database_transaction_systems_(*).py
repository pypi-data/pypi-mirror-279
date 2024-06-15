#Safety of Database Transaction Systems(*)


    # Generate all possible permutations of the transactions

    # Check if any permutation results in an equivalent serial history



    # Use itertools library to generate all permutations of T


    # Execute transactions serially and return the resulting history
        # Execute the transaction and update the history


    # Execute a single transaction and return the list of operations
    # You would need to implement the logic specific to your transaction system
    # Here, I'm assuming a simple list-based representation of the history


    # Compare the two histories and check if they are equivalent
    # You would need to implement the logic specific to your transaction system
    # Here, I'm assuming a simple list-based representation of the history


# Example usage


if __name__ == '__main__':
    def is_serializable(T, H):
        permutations = get_permutations(T)
        for permutation in permutations:
            serial_history = execute_serially(permutation)
            if is_equivalent(H, serial_history):
                return True
        return False
    def get_permutations(T):
        from itertools import permutations
        return permutations(T)
    def execute_serially(transactions):
        history = []
        for transaction in transactions:
            history += execute_transaction(transaction)
        return history
    def execute_transaction(transaction):
        return transaction
    def is_equivalent(history1, history2):
        return history1 == history2
    transactions = ['T1', 'T2', 'T3']  # List of transactions T
    history = ['A', 'B', 'C']  # Transaction history H
    result = is_serializable(transactions, history)
    print(result)
