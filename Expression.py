def checkRemainder(num):
    removed_num = str(num)[:-1]
    removed_num += str(int(removed_num) % 7)
    return int(removed_num) == num

num = int(input("Enter a 6-digit number: "))
print(checkRemainder(num))