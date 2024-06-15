#External Macro Data Compression




# Example usage



if __name__ == '__main__':
    def external_macro_data_compression(D, C, h, B):
        total_length = len(D) + len(C)
        pointer_count = D.count('p') + C.count('p')
        if total_length + (h - 1) * pointer_count <= B:
            return True
        return False
    D = "abcppdepp"
    C = "ppab"
    h = 2
    B = 15
    result = external_macro_data_compression(D, C, h, B)
    if result:
        print("There exists a valid configuration.")
    else:
        print("No valid configuration exists.")
