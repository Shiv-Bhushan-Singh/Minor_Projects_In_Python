tasks = []

def show_menu():
    print("1. Add\n2. Remove\n3. View\n4. Exit")

while True:
    show_menu()
    choice = input("Choose: ")
    if choice == "1":
        tasks.append(input("Task: "))
    elif choice == "2":
        idx = int(input("Task number to remove: ")) - 1
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
    elif choice == "3":
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")
    elif choice == "4":
        break