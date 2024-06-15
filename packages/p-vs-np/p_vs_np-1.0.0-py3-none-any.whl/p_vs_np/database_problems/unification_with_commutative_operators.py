#Unification with commutative operators






# Example usage


if __name__ == '__main__':
    def unify(expression1, expression2):
        if expression1 == expression2:
            return True
        elif isinstance(expression1, str) and expression1.isalpha():
            return True
        elif isinstance(expression2, str) and expression2.isalpha():
            return True
        elif isinstance(expression1, list) and isinstance(expression2, list):
            if len(expression1) != len(expression2):
                return False
            for i in range(len(expression1)):
                if not unify(expression1[i], expression2[i]):
                    return False
            return True
        else:
            return False
    exp1 = ['+', 'x', 'y']
    exp2 = ['+', 'y', 'x']
    result = unify(exp1, exp2)
    if result:
        print("Expressions can be unified.")
    else:
        print("Expressions cannot be unified.")
