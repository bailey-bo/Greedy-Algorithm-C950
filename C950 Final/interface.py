import excelParse
import greedy
import time
from truck import Truck

# This is the dashboard/ interface that will run when the program starts
def interface_program():
    # Prompt user for input to use the dashboard. While loop continues until user chooses to close the program by
    # entering "4".
    # Runtime: O(1)
    global Truck1, Truck2, Truck3
    start = time.time()
    packages_order = greedy.greedyAlgorithm(excelParse.g, excelParse.startA)
    Truck1 = Truck(packages_order[0], packages_order[1], packages_order[6])
    Truck2 = Truck(packages_order[2], packages_order[3], packages_order[7])
    Truck3 = Truck(packages_order[4], packages_order[5], packages_order[8])
    greedy.resetPackages()
    end = time.time()
    print("Time to run greedy algorithm and assign values to Trucks:")
    print(end - start)

    menu = ""
    while menu != "4":
        menu = input('\nPlease choose from one of the following menu options:\n'
                     '1. Print All Package Status and Total Mileage\n'
                     '2. Get a Single Package Status with a Time\n'
                     '3. Get All Package Status with a Time\n'
                     '4. Exit the Program\n')

        # If user enters "1", print status of all packages in their current state.
        # Runtime: O(1)
        if menu == "1":
            greedy.printAllPackages(Truck1, Truck2, Truck3, "EOD")
            print("Truck 1 " + str(round(Truck1.distance, 2)) + " miles")
            print("Truck 2 " + str(round(Truck2.distance, 2)) + " miles")
            print("Truck 3 " + str(round(Truck3.distance, 2)) + " miles")

        # If user enters "2", ask user for a given time and package ID . Run printPackage up to that certain time
        # and return status of package at given id. Exception will occur if correct format of time is not entered.
        # Runtime: O(1)
        elif menu == "2":
            menuTime = input("Please enter a time in HH:MMam format\n")
            menuId = input("Please enter a package ID number\n")
            try:
                greedy.printPackage(Truck1, Truck2, Truck3, menuTime, menuId)

            except ValueError:
                print("Sorry... input not recognized, please try again")

        # If user enters "3", ask user for a given time. Run printAllPackages at that current time and update package
        # data. Exception will occur if correct format of time is not entered.
        # Runtime: O(1)
        elif menu == "3":
            menuTime = input("Please enter a time in HH:MMam format\n")
            try:
                greedy.printAllPackages(Truck1, Truck2, Truck3, menuTime)

            except ValueError:
                print("Sorry... input not recognized, please try again")

        # Exception if user does not enter a valid choice from the options given.
        # Runtime: O(1)
        else:
            if menu != "4":
                print("Sorry... input not recognized, please try again")
