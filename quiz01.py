def quiz(num):
    for i in range(1,num + 1):
        print("*" * i)
    for i in range(num - 1,0, -1):
        print("*" * i)
num = int(input("Enter Number : "))
quiz(num)