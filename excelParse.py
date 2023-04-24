from distances import Graph, Address
import csv
from package import Package

# This file is here to parse the .csv files provided with the program.

file = open('WGUPS_Package_File.csv')
csvreader = csv.reader(file)

# This for loop reads each row in the WGUPS_Package_file.csv and creates a Package object.
# It also parses row 7 to be used later in the program. After that is done it adds the package object to a hashtable
# which is stored in the package.py file titled "Packages".
# Runtime: O(n^2)
for row in csvreader:
    p = Package(int(row[0]), row[1], row[5], row[2], row[4], row[6], 'At Hub')

    if row[5] != "EOD":
        p.priority = True
    if "truck 2" in row[7]:
        p.unavailable = True
        p.special = "truck 2"
    # Space complexity:
    if "Delayed" in row[7]:
        stringH = row[7]
        parseString = stringH.split()
        timeDelayed = ""
        holdString = ""
        for i in parseString:
            if "am" in i:
                timeDelayed = holdString + i
            holdString = i
        p.unavailable = True
        p.special = timeDelayed
    if "Wrong address" in row[7]:
        p.unavailable = True
        p.special = "10:20am"
    if "Must be delivered" in row[7]:
        p.special = row[7]
        p.priority = True

    Package.Packages.insert(int(row[0]), p)

# This Graph object will be used to store the distances from each address to another from the WGUPS_Distance_Table.csv
g = Graph()

file = open('WGUPS_Distance_Table.csv')
data = list(csv.reader(file))
header = data[0]

# This "startA" Address point will be the location of the hub that all trucks will be starting at and the first
# distances will be in relation to
startA = Address

# This for loop parses the WGUPS_Distance_Table.csv file for Address names and adds them to the Graph object g
# It also tests to see if any address is labeled "HUB" to store our startA address Object.
# Runtime: O(n)
for row in data[1:]:
    if "HUB" in row[1]:
        v = Address(row[0])
        v.hub = True
        g.add_address(v)
        startA = v
    else:
        v = Address(row[0])
        g.add_address(v)

# This for loop parses the WGUPS_Distance_Table.csv for distances and adds those as undirected edges to the Graph g
# object. Since the data is stored as a distance chart with the diagonal being 0. The code must account for each
# step that is added as we parse another row in the table.
# Runtime: O(n^3)
i = 2
for row in data[1:]:
    v1 = Address
    v2 = Address
    j = 2

    for v in g.adjacency_list:
        if v.label in row[0]:
            v.distance = float(row[2])
            v1 = v
            j = 2
            while j <= i:
                for v in g.adjacency_list:
                    if v.label in header[j]:
                        v2 = v
                        g.add_undirected_edge(v1, v2, float(row[j]))
                j += 1
    i += 1
