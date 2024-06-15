#Regular Expression Substitution



# Example usage


if __name__ == '__main__':
    import re
    def regular_expression_substitution(s, t, pattern, substitution):
        regex = re.compile(pattern)
        result = regex.sub(substitution, s)
        return result == t
    s = "abcxyzdef"
    t = "xyz"
    pattern = "abc(.*?)def"
    substitution = "xyz"
    result = regular_expression_substitution(s, t, pattern, substitution)
    if result:
        print("The substitution rule can transform the string.")
    else:
        print("The substitution rule cannot transform the string.")
