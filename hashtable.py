class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=100):
        # initialize the hash table with empty bucket list entries.
        # Runtime: O(n)
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    # Runtime: O(1)
    def insert(self, id, item):
        # get the bucket list where this item will go.
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        package = [id, item]
        bucket_list.append(package)

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    # Runtime: O(n)
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for package in bucket_list:
            if key == package[0]:
                return package[1]
        return None

    # Given the id of a package, search the hash table for the bucket that contains the id. Then search bucket list for
    # the package and return package information once found.
    def lookup(self, id):
        # get the bucket list where this key would be.
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        for package in bucket_list:
            if id == package[0]:
                return "Package Id: " + str(package[1].id) + "\n" + \
                    "Address: " + package[1].address + "\n" + \
                    "Deadline: " +package[1].deadline + "\n" + \
                    "City: " + package[1].city + "\n" + \
                    "Zip Code: " +package[1].zip + "\n" + \
                    "Weight: " +package[1].weight + "\n" + \
                    "Status: " +package[1].status
        return None

    # Removes an item with matching key from the hash table.
    # Runtime: O(1)
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)