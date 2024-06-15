#Internal Macro Data Compression




# Example usage


if __name__ == '__main__':
    def internal_macro_data_compression(s, h, B):
        pointer_count = s.count('p')
        total_length = len(s) + (h - 1) * pointer_count
        if total_length <= B:
            return True
        return False
    s = "ppabcpp"
    h = 2
    B = 10
    result = internal_macro_data_compression(s, h, B)
    if result:
        print("There exists a valid configuration.")
    else:
        print("No valid configuration exists.")
