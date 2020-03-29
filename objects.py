import json
import heapq
from math import cos, asin, sqrt

class Node:
    def __init__(self, id=None, name=None, description=None, lat=None, long=None, type=None, data=None):
        """
        Constructor for Node object. You can call this by passing the values of each field seperately 
        or you can pass in a dictionary containing all fields and their respective values.
        
        Arguments:
            id          -- a string representing the postal code, bus stop code or MRT station of the node
            name        -- a string representing name of the node
            description -- a string representing description of the node
            lat         -- a float representing the latitude of the node
            long        -- a float representing the longitude of the node
            type        -- a string representing the type of the node, can be HDB, Bus Stop or Mrt Station
            data        -- dict containing all the above fields and their respective values
        """
        if not data is None:
            self.id = data["id"]
            self.name = data["name"]
            self.description = data["description"]
            self.lat = data["lat"]
            self.long = data["long"]
            self.type = data["type"]
        
        else:
            self.id = id
            self.name = name
            self.description = description
            self.lat = lat
            self.long = long
            self.type = type
        
    def __repr__(self):
        """
        Returns a string representation of this object.
        """
        return str(self.__dict__)
    
    def __eq__(self, other):
        """
        Check if two Node objects are equal. 
        
        Arguments:
            other -- the target node object to compare to
            
        Returns:
            True if two object have the same values for every fields
            False otherwise
        """
        if isinstance(other, Node):
            return ((self.id == other.id) and 
                    (self.lat == other.lat) and 
                    (self.long == other.long) and 
                    (self.type == other.type) and
                    (self.name == other.name) and
                    (self.description == other.description))
        
        return False
    
    def __hash__(self) -> int:
        """
        Return hash for this Node object.
        This is needed to use this Node object as a key in a dictionary

        Returns:
            int representing the hash of this object
        """
        return hash((self.id, self.lat, self.long, self.type, self.name, self.description))
    
    def distanceTo(self, other) -> float:
        """
        Calculates the distance between two node objects

        Arguments:
            other -- the target node object to calculate distance 

        Returns:
            Float representation of the distance between the two node objects in kilometers, rounded to two decimal places
        """
        lat1, lon1 = self.lat, self.long
        lat2, lon2 = other.lat, other.long

        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return round(12742 * asin(sqrt(a)), 2)

class Edge:
    def __init__(self, source=None, destination=None, distance=None, bus_service=None, type=None, data=None):
        """
        Constructor for Edge object. You can call this by passing the values of each field seperately 
        or you can pass in a dictionary containing all fields and their respective values.

        Arguments:
            source      -- a node object representing the source node
            destination -- a node object representing the destination node
            distance    -- a float representing the distance between source and destination
            bus_service -- a string representation of the bus service of the route. 
                           0 is used if it is not a bus route
            type        -- a string representing the type of the edge, can be Walk, MRT or Bus
            data        -- dict containing all the above fields and their respective values
        """
        if not data is None:
            self.source = data["source"]
            self.distance = data["distance"]
            self.destination = data["destination"]
            self.bus_service = data["bus_service"]
            self.type = data["type"]
        
        else:
            self.source = source
            self.distance = distance
            self.destination = destination
            self.bus_service = bus_service
            self.type = type
            
    def __repr__(self):
        """
        Returns a string representation of this object.
        """
        return str(self.__dict__)
    
    def __eq__(self, other):
        """
        Check if two Edge objects are equal. 

        Arguments:
            other -- the target node object to compare to

        Returns:
            True if two object have the same values for every fields
            False otherwise
        """
        if isinstance(other, Edge):
            return ((self.source == other.source) and
                   (self.destination == other.destination) and
                   (self.distance == other.distance) and
                   (self.type == other.type) and
                   (self.bus_service == other.bus_service))
            
        return False
    
    def __hash__(self) -> int:
        """
        Return hash for this Node object.
        This is needed to use this Node object as a key in a dictionary

        Returns:
            int representing the hash of this object
        """
        return hash((self.source, self.destination, self.distance, self.type, self.bus_service))
        
class Graph:
    adjacency_list = {}
    
    def __init__(self, data):
        """
        Constructor for Graph object. Pass in a list of dictionaries that represents the adjacency list.

        Arguments:
            data -- list of dict representing the adjacency list
        """
        
        for dic in data:
            source_node = Node(id=dic["source_id"],
                               name=dic["source_name"],
                               description=dic["source_description"],
                               lat=dic["source_lat"],
                               long=dic["source_long"],
                               type=dic["source_type"])
            dest_node = Node(id=dic["destination_id"],
                             name=dic["destination_name"],
                             description=dic["destination_description"],
                             lat=dic["destination_lat"],
                             long=dic["destination_long"],
                             type=dic["destination_type"])
            edge = Edge(source=source_node,
                        destination=dest_node,
                        distance=dic["distance"],
                        bus_service=dic["bus_service"],
                        type=dic["edge_type"])
            
            self.addEdge(edge)
            
    def __repr__(self) -> str:
        """
        Returns a string representation of this object.
        """
        return str(self.adjacency_list)
               
    def isNeighbour(self, this, other) -> bool:
        """
        Check if edge already exists in the graph
        Criteria for 'already exist' are:
            Same source and destination
            Same type (eg. walk/bus/mrt)

        Arguments:
            this  -- node object representing the source node
            other -- node object representing the destination node

        Returns:
            True if edge exist in the graph already
            False otherwise
        """
        for edge in self.adjacency_list[this]:
            if edge.destination == other:
                return True
            
        return False
    
    
    def addEdge(self, edge) -> None:
        """
        Add an Edge object to the graph

        Arguments:
            edge -- Edge object to add to the graph

        Returns:
            None
        """
        if (edge.source in self.adjacency_list):
            if not self.isNeighbour(edge.source, edge.destination):
                self.adjacency_list[edge.source].append(edge)
                
        else:
            self.adjacency_list[edge.source] = []
            self.adjacency_list[edge.source].append(edge)
            
    def vertices(self) -> list:
        """
        Returns a list of id representing all possible sources in the adjacency list

        Returns:
            List of string id
        """
        return list(self.adjacency_list.keys())
    
    
    def adj(self, source) -> list:
        """
        Returns a list edges that are adjacent to the source node.
        If source node is not in the adjacency list, will return an empty list

        Returns:
            List of all edge objects adjacent to the source node
            Empty list if source node not in adjacency list
        """
        if source not in self.adjacency_list:
            return []
        
        return self.adjacency_list[source]
                
    def getPath(self, source_node, destination_node) -> list:
        """
        Computes shortest path from source_node to destination_node.
        
        Arguments:
            source_node      -- Node object representing the starting point of the route
            destination_node -- Node object representing the ending point of the route

        Returns:
            List of edge objects representing the shortest path from source_node to destination_node.
            Empty list if there is no possible routes between the two nodes.
        """
        
        # Keep track of visited nodes
        seen = set()
        
        # paths will store our visited nodes and their relaxed weight value
        # the first key is an Edge object representing the source_node with distance of zero
        paths = {source_node: Edge(source=None,
                                   destination=source_node,
                                   distance=0.0)}
        current_node = source_node
        
        while current_node != destination_node:
            seen.add(current_node)
            
            for edge in self.adj(current_node):
            
                curr_distance = edge.distance + paths[current_node].distance

                if edge.destination not in paths:
                    paths[edge.destination] = edge
                    paths[edge.destination].distance = curr_distance
                
                else:
                    if paths[edge.destination].distance > curr_distance:
                        paths[edge.destination] = edge
                        paths[edge.destination].distance = curr_distance
                    
            next_edges = {node: paths[node] for node in paths if node not in seen}
            
            if not next_edges:
                return []
            
            current_node = min(next_edges, key = lambda k: next_edges[k].distance)
            
        shortest_path = []
        while current_node is not None:
            shortest_path.append(paths[current_node])
            current_node = paths[current_node].source
        
        return shortest_path