#Programs with formally recursive procedures


    # Parse procedure declarations

    # Parse procedure calls

    # Check if any procedure is formally recursive


# Example usage






if __name__ == '__main__':
    import re
    def is_formally_recursive(program):
        pattern = r'procedure\s+(\w+)\('
        procedure_declarations = re.findall(pattern, program)
        pattern = r'\b(\w+)\('
        procedure_calls = re.findall(pattern, program)
        for procedure in procedure_declarations:
            if procedure in procedure_calls:
                return True
        return False
    program = """
    procedure foo()
        bar()
    end
    procedure bar()
        foo()
    end
    procedure baz()
        qux()
    end
    procedure qux()
        print("Hello!")
    end
    """
    if is_formally_recursive(program):
        print("The program contains formally recursive procedures.")
    else:
        print("The program does not contain formally recursive procedures.")
