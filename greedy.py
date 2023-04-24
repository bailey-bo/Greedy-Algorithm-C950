import trackTime
from distances import Address
from package import Package
from datetime import time, timedelta


# This is a Greedy Algorithm used to find a short path for our packages.
# Runtime: O(n^3)
def greedyAlgorithm(g, start_vertex):
    # These are the different variables that will be used throughout the program to store relevant data.
    # Important ones to note are startDateTime to track when packages are delivered, truck1/2/3 Packages List
    # that will be used to store the order of packages for each truck.
    startTime = time(hour=8, minute=0, second=0)
    startDateTime = trackTime.parse_time(startTime)
    unvisited_queue = []
    packagesDelivered = 0
    packagesOrder = []
    truck1 = True
    truck1Packages = []
    truck2 = False
    truck2Packages = []
    truck3 = False
    truck3Packages = []
    priorityEmpty = False
    truck1Distance = 0
    truck2Distance = 0
    truck3Distance = 0
    truck1TimeFinsh = trackTime.parse_time(startTime)
    truck2TimeFinsh = trackTime.parse_time(startTime)

    # This loop parses each bucket in the Packages Hashtable and adds each package stored to the unvisited queue list
    # Runtime: O(n)
    for v in Package.Packages.table:
        for i in range(0, len(v)):
            unvisited_queue.append(v[i][1])

    # This for loop parses the unvisited queue list and adds any packages that must be delivered together as priority.
    # It adds the package with special instructions as well as any number that is referenced in the note as long as it
    # is separated by a comma.
    # Runtime: O(n^3)
    for p in unvisited_queue:
        if "Must be delivered" in p.special:
            str1 = p.special
            parsed = str1.split(',')
            for p in parsed:
                id = ""
                for digit in p:
                    if digit.isdigit():
                        id = id + digit
                Package.Packages.search(int(id)).priority = True

    # This is the start of the algorithm, it will continue until all packages in the unvisited queue are delivered.
    # Runtime: O(n^2)
    while len(unvisited_queue) > 0:

        # These are different variables that will be used throughout the program to store relevant data.
        nextTruck = False
        smallest_index = 0
        smallestDistance = 100
        nextAddress = Address

        # This sections starts with a Boolean to check if there are any priority packages that need to be delivered.
        # After, it parses the unvisited_queue for any package that has been marked as priority. Then it finds the
        # corresponding address that the package needs to be delivered at in the g Graph object. Finally, it returns
        # the smallest_index of unvisited queue that has the smallest distance to our current address. If no packages
        # are marked as priority, it sets priorityEmpty to True.
        # Runtime: O(n^2)
        if priorityEmpty == False:
            for i in range(0, len(unvisited_queue)):
                if unvisited_queue[i].priority == True and unvisited_queue[i].unavailable == False:
                    for address in g.adjacency_list:
                        if unvisited_queue[i].address in address.label:
                            priorityDistance = address.distance
                            if priorityDistance < smallestDistance:
                                smallestDistance = priorityDistance
                                smallest_index = i
                                unvisited_queue[i].distance = priorityDistance
                                nextAddress = address
            if smallestDistance == 100:
                priorityEmpty = True

        # This sections starts with a Boolean to check if there are no priority packages that need to be delivered.
        # After, it parses the unvisited_queue for all packages as long as they are not marked as unavailable. Then
        # it finds the corresponding address that the package needs to be delivered at in the g Graph object. Finally,
        # it returns the smallest_index of unvisited queue that has the smallest distance to our current address.
        # Runtime: O(n^2)
        if priorityEmpty == True:
            for i in range(0, len(unvisited_queue)):
                if unvisited_queue[i].unavailable == False:
                    for address in g.adjacency_list:
                        if unvisited_queue[i].address in address.label:
                            priorityDistance = address.distance
                            if priorityDistance < smallestDistance:
                                smallestDistance = priorityDistance
                                smallest_index = i
                                unvisited_queue[i].distance = priorityDistance
                                nextAddress = address

        # Pop the current package from the unvisited queue list.
        current_package = unvisited_queue.pop(smallest_index)

        # Convert the distance to deliver the package to minutes at conversion of 18mph. Then add that to startDateTime
        # and set the package time delivered to this updated time. Set the status of the package as delivered. Add a
        # package to the delivered list and add the package id to the order list.
        addMin = (current_package.distance / 18) * 60
        startDateTime = startDateTime + timedelta(minutes=addMin)
        current_package.timeDelivered = startDateTime
        current_package.status = "Delivered"
        packagesDelivered += 1
        packagesOrder.append(current_package.id)

        # Boolean to check which truck is currently being loaded. Adds the current package id to the correct truck list.
        # Also adds the distance traveled to deliver that package to the correct truck.
        if truck1 == True:
            truck1Packages.append(current_package)
            truck1Distance += current_package.distance
        if truck2 == True:
            truck2Packages.append(current_package)
            truck2Distance += current_package.distance
        if truck3 == True:
            truck3Packages.append(current_package)
            truck3Distance += current_package.distance

        # If 16 packages are loaded into a truck nextTruck = True and the next truck starts being loaded.
        if packagesDelivered % 16 == 0:
            nextTruck = True

        # If nextTruck is True, and truck2 is done loading, start loading packages into truck3
        if nextTruck == True and truck2 == True:
            truck2 = False
            truck3 = True

        # If nextTruck is True, and truck1 is done loading, start loading packages into truck2. Also, if a package
        # had to be loaded into truck 2, make it available and add it to the priority queue.
        # Runtime: O(n)
        if nextTruck == True and truck2 != True and truck3 != True:
            truck2 = True
            truck1 = False
            for v in unvisited_queue:
                if v.special == "truck 2":
                    v.unavailable = False
                    if v.priority == True:
                        priorityEmpty = False

        # If nextTruck is True, and we are loading packages into a new truck. Check to see if any delayed packages are
        # now at the hub. Change the status of these packages to available and if any of them are priority packages, set
        # priorityEmpty to False.
        # Runtime: O(n)
        if nextTruck == True:
            for v in unvisited_queue:
                if "am" in v.special:
                    parseTime = trackTime.parse_string(v.special)
                    if parseTime <= startDateTime and v.unavailable == True:
                        v.unavailable = False
                        if v.priority == True:
                            priorityEmpty = False
                        if v.special == "10:20am":
                            v.address = "410 S State St"

        # This for loop allows packages that need to be delivered by a certain deadline to have priority first, and then
        # trucks that need to be delivered on truck 2 can be added to the priority queue.
        if priorityEmpty == True and truck2 == True:
            for v in unvisited_queue:
                if v.special == "truck 2":
                    v.priority = True
                    priorityEmpty = False

        # When the program has finished loading all the packages in a truck. To start loading the next truck,
        # loop for each address in g and set the distance of that address to the g.edge_weight between that address
        # and the hub. If a truck is still in route, loops for each address in g and sets the distance of that
        # address to the g.edge_weight between that address and the current address the most recent package was
        # delivered to.
        # Runtime: O(n)
        if nextTruck == True:
            packagesOrder.append("HUB")
            for address in g.adjacency_list:
                address.distance = g.edge_weights[start_vertex, address]
                if truck2 == True:
                    truck1TimeFinsh = startDateTime
                if truck3 == True:
                    truck2TimeFinsh = startDateTime
        else:
            for address in g.adjacency_list:
                address.distance = g.edge_weights[nextAddress, address]
    print(packagesOrder)

    # Function returns each truck's order of packages to be delivered and the total distance traveled for that truck.
    truck3TimeFinsh = startDateTime
    return truck1Packages, truck1Distance, truck2Packages, truck2Distance, truck3Packages, truck3Distance, truck1TimeFinsh, truck2TimeFinsh, truck3TimeFinsh


# Function designed to return the status of all packages at the time of checkTime.
def printAllPackages(T1, T2, T3, checkTime):
    # If you enter "EOD" you will get the status of all packages at the end of the day after the Greedy Algorithm
    # has fully run.
    if checkTime == "EOD":
        print("ID, Address, City, Zip, Deadline, Weight, Special Notes, Status, Delivery Time")
        for p in Package.Packages.table:
            for i in range(0, len(p)):
                currentPackage = p[i][1]
                print(str(currentPackage.id) + ",", currentPackage.address + ",", currentPackage.city + ",",
                      currentPackage.zip + ",", currentPackage.deadline + ",", currentPackage.weight + ",",
                      currentPackage.special + ",", currentPackage.status + ",", currentPackage.timeDelivered)

    # With the time entered, loop through all the packages and check the status of each package at that time. If
    # the package has been delivered, print an extra value of the time of delivery. If package is still at the
    # hub or en route, set the status of the package accordingly.
    if checkTime != "EOD":
        parseTime = trackTime.parse_string(checkTime)
        for p in Package.Packages.table:
            for i in range(0, len(p)):
                currentPackage = p[i][1]
                currentPackage.status = "At Hub"
                if T1.timeDone >= parseTime:
                    if currentPackage in T1.packages:
                        currentPackage.status = "En Route"
                if T1.timeDone <= parseTime <= T2.timeDone:
                    if currentPackage in T2.packages:
                        currentPackage.status = "En Route"
                if T2.timeDone <= parseTime:
                    if currentPackage in T3.packages:
                        currentPackage.status = "En Route"
                if currentPackage.timeDelivered <= parseTime:
                    currentPackage.status = "Delivered"
                if currentPackage.status == "Delivered":
                    print(str(currentPackage.id) + ",", currentPackage.address + ",", currentPackage.city + ",",
                          currentPackage.zip + ",", currentPackage.deadline + ",", currentPackage.weight + ",",
                          currentPackage.special + ",", currentPackage.status, ",", currentPackage.timeDelivered)
                if currentPackage.status != "Delivered":
                    print(str(currentPackage.id) + ",", currentPackage.address + ",", currentPackage.city + ",",
                          currentPackage.zip + ",", currentPackage.deadline + ",", currentPackage.weight + ",",
                          currentPackage.special + ",", currentPackage.status)


# Function designed to return the status of one package with id at the time of checkTime.
# Runtime: O(n)
def printPackage(T1, T2, T3, checkTime, id):
    # With the time entered, find the package at the given id and the status of delivery at that time. If
    # the package has been delivered, print an extra value of the time of delivery. If package is still at the
    # hub or en route, set the status of the package accordingly.
    # Runtime: O(n)
    parseTime = trackTime.parse_string(checkTime)
    print("ID, Address, City, Zip, Deadline, Weight, Special Notes, Status, Delivery Time")
    for p in Package.Packages.table:
        for i in range(0, len(p)):
            currentPackage = p[i][1]
            if str(currentPackage.id) == id:
                currentPackage.status = "At Hub"
                if T1.timeDone >= parseTime:
                    if currentPackage in T1.packages:
                        currentPackage.status = "En Route"
                if T1.timeDone <= parseTime <= T2.timeDone:
                    if currentPackage in T2.packages:
                        currentPackage.status = "En Route"
                if T2.timeDone <= parseTime:
                    if currentPackage in T3.packages:
                        currentPackage.status = "En Route"
                if currentPackage.timeDelivered <= parseTime:
                    currentPackage.status = "Delivered"
                if currentPackage.status == "Delivered":
                    print(str(currentPackage.id) + ",", currentPackage.address + ",", currentPackage.city + ",",
                          currentPackage.zip + ",", currentPackage.deadline + ",", currentPackage.weight + ",",
                          currentPackage.special + ",", currentPackage.status, ",", currentPackage.timeDelivered)
                if currentPackage.status != "Delivered":
                    print(str(currentPackage.id) + ",", currentPackage.address + ",", currentPackage.city + ",",
                          currentPackage.zip + ",", currentPackage.deadline + ",", currentPackage.weight + ",",
                          currentPackage.special + ",", currentPackage.status)

def resetPackages():
    for p in Package.Packages.table:
        for i in range(0, len(p)):
            currentPackage = p[i][1]
            currentPackage.status = "At Hub"
