# initializes a 2d array with the given input file, # of rows, and # of columns
def init_matrix(file, rows, cols):
    matrix = [[0 for r in range(cols)] for y in range(rows)]
    for rowIndex, line in enumerate(file):
        token_list = line.split()
        for columnIndex, token in enumerate(token_list):
            matrix[rowIndex][columnIndex] = token
    return matrix


# returns column index of a passed in terminal or non-terminal character
def column_index(char):
    switch = {
        'i': 0, '+': 1, '-': 2,
        '*': 3, '/': 4, '(': 5,
        ')': 6, '$': 7, 'E': 8,
        'T': 9, 'F': 10
    }
    return switch.get(char, -1)


# determines whether or not an input string is valid (using LR parser algorithm)
def trace(input_string, parsing_table, cfg):
    stack = []
    index = 0
    # read initial value
    current_token = input_string[index]
    # push initial state
    stack.append(0)
    print("Stack contains: ", stack)

    while True:
        top = stack.pop()
        value = str(parsing_table[int(top)][column_index(current_token)])
        # if value is a digit, push 3 values onto stack
        if value.isdigit():
            stack.extend((top, current_token, value))
            current_token = input_string[index]
        else:
            # if leading character is an S, push 3 items and read next character from input string
            if value[0] == 'S':
                stack.extend((top, current_token, value[1:]))
                index += 1
                current_token = input_string[index]
            # if leading character is an R, push left index and pop 2*(length of rhs of rule) items off the stack
            elif value[0] == 'R':
                stack.append(top)
                rule = cfg[int(value[1:])-1]
                for i in range(2*len(rule[4:])):
                    stack.pop()
                current_token = rule[0]
            # if the value is 'acc', the input string is valid
            elif value == "acc":
                return True
            # else we've reached whitespace, so reject
            else:
                return False

        print("Stack contains: ", stack)


# driver function
def main():
    parsing_table = init_matrix(open("/Users/Blake/PycharmProjects/LRparser/ParsingTable.txt", "r"), 16, 11)
    input_strings_file = open("/Users/Blake/PycharmProjects/LRparser/InputStrings.txt", "r")
    cfg_file = open("/Users/Blake/PycharmProjects/LRparser/CFGs.txt", "r")
    cfg = [line.strip('\n') for line in cfg_file.readlines()]

    for current_line in input_strings_file:
        current_line = current_line.strip('\n')
        print("***** TRACING " + current_line + " *****")
        if trace(current_line, parsing_table, cfg):
            print("\nRESULT: " + current_line + " was Accepted\n")
        else:
            print("\nRESULT: " + current_line + " was Rejected\n")


main()