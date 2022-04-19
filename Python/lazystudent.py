import os.path
import sys


# page 125


def count_lines(file):
    """
        this function counts how many lines are in the file and returns the amount of lines
        arg:
            file - the file path
        """
    to_count = open(file, 'r')
    line_count = 0
    for line in to_count:
        if line != "\n":
            line_count += 1
    to_count.close()
    return line_count


def is_valid(line):
    """
        this function gets a line from the file and returns 1 if the exercise format is valid, otherwise 0
        arg:
            line - line from the file as string
        """
    lst = line.split()
    if len(lst) == 3:
        if lst[1] == '+' or lst[1] == '-' or lst[1] == '*' or lst[1] == '/':
            if lst[0].isdigit() and lst[2].isdigit():
                if isinstance(int(lst[0]), int) and int(lst[0]) > 0:
                    if isinstance(int(lst[2]), int) and int(lst[0]) > 0:
                        return 1
    return 0


def add(num1, num2):
    """
        this function adds two numbers and return the answer
        args:
            num1 - the first number
            num2 - the second number
        """
    return num1 + num2


def sub(num1, num2):
    """
        this function subtracts two numbers and return the answer
        args:
            num1 - the first number
            num2 - the second number
        """
    return num1 - num2


def multiply(num1, num2):
    """
        this function multiplies two numbers and return the answer
        args:
            num1 - the first number
            num2 - the second number
        """
    if num1 == 0 or num2 == 0:
        return 0
    else:
        return num1 * num2


def divide(num1, num2):
    """
        this function divides two numbers and return the answer
        args:
            num1 - the first number
            num2 - the second number
        """
    if num2 == 0:
        return "CANT DIVIDE BY ZERO"
    return num1 / num2


def asserts():
    """
    this function perform all the asserts to assure integrity
    """
    assert is_valid("3 + 5") == 1
    assert is_valid("3 - 5") == 1
    assert is_valid("3 * 5") == 1
    assert is_valid("3 / 5") == 1
    assert is_valid("3 +5") == 0
    assert is_valid("3+ 5") == 0
    assert is_valid("3+5") == 0
    assert is_valid("3 + 5.5") == 0
    assert is_valid("3.2 + 5") == 0
    assert is_valid("3.7 + 5.1") == 0
    assert add(1, 4) == 5
    assert add(124, 53121) == 53245
    assert sub(3, 5) == -2
    assert sub(12, 4) == 8
    assert multiply(3, 6) == 18
    assert multiply(55, 8) == 440
    assert divide(128, 5) == 25.6
    assert divide(55, 5) == 11


def main():
    asserts()
    calculate()


def calculate():
    if os.path.exists((sys.argv[1])) and os.path.exists((sys.argv[2])):
        homework = open(sys.argv[1], 'r')
        solution = open(sys.argv[2], 'w')
        for line in homework:
            if line != "\n":
                if is_valid(line):
                    solu = 0
                    (num1, ch, num2) = tuple(line.split())
                    if ch == '+':
                        solu = add(int(num1), int(num2))
                    elif ch == '-':
                        solu = sub(int(num1), int(num2))
                    elif ch == '*':
                        solu = multiply(int(num1), int(num2))
                    elif ch == '/':
                        solu = divide(int(num1), int(num2))
                    if any(c.isalpha() for c in str(solu)):
                        solution.writelines(str(solu) + "\n")
                    else:
                        solution.writelines(num1 + " " + ch + " " + num2 + " = " + str(solu) + "\n")
                else:
                    solution.writelines("UNSUPPORTED FORMAT!\n")
    else:
        print("Two parameters required for the program to run.")


if __name__ == "__main__":
    main()
