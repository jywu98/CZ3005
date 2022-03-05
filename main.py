choice = -1
while (choice < 4):
    print("1. Task 1")
    print("2. Task 2")
    print("3. Task 3")
    print("4. Exit")
    choice = int(input("Enter selection: "))

    if choice == 1:
        exec(open("task1.py").read())
    elif choice == 2:
        exec(open("task2.py").read())
    elif choice == 3:
        exec(open("task3.py").read())
    elif choice == 4:
        exit()
