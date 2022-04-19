def is_5_digit_number(user_input):
    """
    this function checks if the input is a five digit number
    :param user_input: a sting from the user
    :return: true if it is a 5 digit number, false otherwise
    """
    if len(user_input) == 5 and user_input.isnumeric():
        return True
    else:
        return False


def digit_comma(user_input):
    """
    this function gets number as string and return a string with ',' between the digits
    :param user_input: a sting from the user
    :return: a string with ',' between 2 digits
    """
    string = ','.join([str(x) for x in user_input])
    return string


def user_sum(user_input):
    """
    this function gets a number as string and returns the sum of digits
    :param user_input: a string from the user
    :return: the sum of the digits
    """
    lst = list(user_input)
    sum_digits = 0
    for num in lst:
        sum_digits += int(num)
    return sum_digits


def execute_asserts():
    """
    this function is running the asserts to make sure there are no bugs
    :return: none
    """
    assert is_5_digit_number('12345') == True
    assert is_5_digit_number('abcde') == False
    assert is_5_digit_number('123456') == False
    assert is_5_digit_number('12345f') == False
    assert is_5_digit_number('abcdef') == False
    assert is_5_digit_number('1234') == False
    assert is_5_digit_number('abcd') == False
    assert user_sum('11111') == 5
    assert user_sum('93569') == 32
    assert digit_comma('11111') == '1,1,1,1,1'
    return


def main():
    execute_asserts()
    user_input = input("Please enter a 5 digit number:\n")
    is_5_digit_number(user_input)
    print("You entered the number: " + user_input)
    print("The digits of this number is: " + digit_comma(user_input))
    print("The sum of the digits is: " + str(user_sum(user_input)))


main()
