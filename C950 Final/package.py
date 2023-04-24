import hashtable
import datetime


class Package:
    # Static hashtable of Package objects that can be called upon
    Packages = hashtable.HashTable()

    # Constructor used in excelParse to add packages to hashtable
    def __init__(self, id, address, deadline, city, zip, weight, status):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status
        self.special = ""
        self.unavailable = False
        self.priority = False
        self.distance = float('inf')
        self.timeDelivered = datetime.datetime
        self.truckRequired = ""
