class Address:

    # Constructor for a new Address object. All vertex objects start with a distance of positive infinity.
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')


class Graph:

    # Constructor for a new Graph object.
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    # Add an Address object to the adjacency_list.
    # Runtime: O(1)
    def add_address(self, new_address):
        self.adjacency_list[new_address] = []

    # Add distance from one address in the adjacency_list to another and store it in edge_weights.
    # Runtime: O(1)
    def add_directed_edge(self, from_address, to_address, weight=1.0):
        self.edge_weights[(from_address, to_address)] = weight
        self.adjacency_list[from_address].append(to_address)

    # Add distance going in either direction from one address in the adjacency_list to another and store it in
    # edge_weights.
    # Runtime: O(1)
    def add_undirected_edge(self, address_a, address_b, weight=1.0):
        self.add_directed_edge(address_a, address_b, weight)
        self.add_directed_edge(address_b, address_a, weight)
