# initializes a 2d array with the given input file, # of rows, and # of columns
def init_matrix(file, rows, cols):
    matrix = [[0 for r in range(cols)] for y in range(rows)]
    for rowIndex, line in enumerate(file):
        token_list = line.split()
        for columnIndex, token in enumerate(token_list):
            matrix[rowIndex][columnIndex] = token
    return matrix


# determines whether or not an input string is valid (using LR parser algorithm)
def trace(input_string, parsing_table, cfg):
    stack = []
    index = 0
    current_token = input_string[index]
    stack.append(0)
    for element in stack:
        top = stack.pop()
        value = str(parsing_table[top][current_token])
        if value.isdigit():
            stack.extend((top, current_token, value))
        else:
            if value[0] == 'S':
                stack.extend((top, current_token, value[1:]))
                index += 1
                current_token = input_string[index]
            elif value[0] == 'R':
                stack.extend(top)
                rule = cfg[int(value[1:])-1]
                for i in range(len(rule[4:])):
                    stack.pop()
            elif value == "acc":
                return True
            else:
                return False


# driver function
def main():
    parsing_table = init_matrix(open("/Users/Blake/PycharmProjects/LRparser/ParsingTable.txt", "r"), 16, 11)
    input_strings_file = "/Users/Blake/PycharmProjects/LRparser/InputStrings.txt"
    cfg_file = open("/Users/Blake/PycharmProjects/LRparser/CFGs.txt", "r")
    cfg = [line.strip('\n') for line in cfg_file.readlines()]

    with open(input_strings_file) as file:
        current_string = file.readlines()
        if trace(current_string, parsing_table, cfg):
            print("accepted")
        else:
            print("rejected")


main()