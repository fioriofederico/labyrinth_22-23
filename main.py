from utilities.menuOption import menuOption

def main_menu():
    print("Main Menu:")
    print("1. Create maze")
    print("2. Upload image")
    print("3. Upload JSON")
    menu = menuOption()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_maze()
    elif choice == 2:
        upload_image(menu)
    elif choice == 3:
        upload_json(menu)
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def create_maze(menu):
    size = int(input("Enter the size of the maze: "))
    start = None
    while start != "0":
        start = input("Enter the starting point (or 0 to finish): ")
        if start != "0":
            print("You entered:", start)
    goal = input("Enter the goal point: ")
    print("Goal:", goal)
    add_breadcrumbs = None
    while add_breadcrumbs != "0":
        add_breadcrumbs = input("Do you want to add breadcrumbs? (yes/no or 0 to finish): ")
        if add_breadcrumbs == "yes":
            print("Breadcrumbs added.")
        elif add_breadcrumbs == "no":
            print("Breadcrumbs not added.")
        else:
            print("Invalid choice. Please try again.")

def upload_image(menu):
    path = input("Enter the path of the image on tiff: ")
    menu.ImageInput(path)

def upload_json(menu):
    path = input("Enter the path of the json file: ")
    menu.JsonInput(path)

if __name__ == "__main__":
    main_menu()
