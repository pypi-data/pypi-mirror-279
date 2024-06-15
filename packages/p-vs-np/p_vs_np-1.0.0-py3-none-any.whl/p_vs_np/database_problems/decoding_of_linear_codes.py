#Decoding of linear codes





# Example usage


if __name__ == '__main__':
    def hamming_decode(codeword):
        parity_matrix = [[1, 1, 0],
                         [1, 0, 1],
                         [1, 0, 0],
                         [0, 1, 1],
                         [0, 1, 0],
                         [0, 0, 1],
                         [1, 1, 1]]
        syndrome = [0, 0, 0]
        for i, bit in enumerate(codeword):
            for j in range(3):
                syndrome[j] ^= bit * parity_matrix[i][j]
        error_position = sum(bit * (2 ** i) for i, bit in enumerate(syndrome)) - 1
        if error_position >= 0:
            codeword[error_position] = 1 - codeword[error_position]
        decoded_message = [codeword[2], codeword[4], codeword[5], codeword[6]]
        return decoded_message
    codeword = [1, 0, 1, 1, 0, 0, 1]
    decoded_message = hamming_decode(codeword)
    print("Decoded Message:")
    print(decoded_message)
