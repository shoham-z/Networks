number = input("Please enter a 5 digit number:\n")
print("you entered the number: " + number)
lst = list(number)
print("The digits of this number are: ")
string = ','.join([str(x) for x in lst])
print(string)
i = 0
for x in lst:
    lst[i] = int(lst[i])
    i = i + 1
print("The sum of this numbers is: " + str(sum(lst)))