from utilities.menuOption import menuOption

def main_menu():
    print("Main Menu:")
    print("1. Create maze")
    print("2. Upload image")
    print("3. Upload JSON")
    menu = menuOption()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_maze(menu)
    elif choice == 2:
        upload_image(menu)
    elif choice == 3:
        upload_json(menu)
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def create_maze(menu):
    height = int(input("Insert the height of the maze: "))
    width = int(input("Insert the width of the maze: "))
    startPoint = []
    start = list(map(int, input("Insert the start point as a list: ").split()))
    startPoint.append(start)
    while True:
        add_start = input("Do you want to add another start point? (yes/no): ")
        if add_start == 'no':
            break
        start = list(map(int, input("Insert the start point as a list: ").split()))
        startPoint.append(start)
    goal = list(map(int, input("Insert the goal point as a list: ").split()))

    breadcrumps = []
    add_breadcrumps = int(input("Do you want to add breadcrumps? (0/1): "))
    while add_breadcrumps:
        bc = list(map(int, input("Insert the breadcrump (x y weight): ").split()))
        breadcrumps.append(bc)
        add_breadcrumps = int(input("Do you want to add another breadcrump? (0/1): "))
    menu.GenerateInput(height, width, startPoint, goal, breadcrumps)

def upload_image(menu):
    path = input("Enter the path of the image on tiff: ")
    menu.ImageInput(path)

def upload_json(menu):
    path = input("Enter the path of the json file: ")
    menu.JsonInput(path)

if __name__ == "__main__":
    main_menu()
