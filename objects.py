import json
import heapq
from math import cos, asin, sqrt
from abc import ABC, abstractmethod

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
            
    def __repr__(self) -> str:
        """
        Returns a string representation of this object.
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    
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
    
    def __lt__(self, other):
        return True if self.distance < other.distance else False
    
    def __gt__(self, other):
        return True if self.distance > other.distance else False
    
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
    

    def edges(self) -> list:
        edges = []
        
        for node, edge in self.adjacency_list.items():
            edges.append(edge)
            
        return edges
    
    
    def adj(self, source: Node) -> list:
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
                
class PQItem:
    """
    Generic object that will work with whatever
    implemention of priority queue that we will create.
    """
    def __init__(self, priority, element):
        self.priority = priority
        self.element = element
        
    def __lt__(self, other):
        return self.priority < other.priority
    
    def __gt__(self, other):
        return self.priority > other.priority
    
    def __eq__(self, other):
        if isinstance(other, PQItem):
            return (other.element == self.element)     
        return False
    
class PriorityQueue(ABC):
    @abstractmethod
    def pop(self):
        pass
    
    @abstractmethod
    def push(self, element: PQItem):
        pass
    
    @abstractmethod
    def getMin(self):
        pass
    
    @abstractmethod
    def isEmpty(self):
        pass
    
class ListPriorityQueue(PriorityQueue):
    """
    Basic priority queue implementation using a list.
    We use QuickSort to maintain its priority.
    Lowest priority will always be at the front of the queue (index 0)
    """
    def __init__(self):
        self.queue = []
        
    def pop(self):
        if self.isEmpty():
            return None

        minElement = self.queue[0]
        del self.queue[0]
        return minElement      
    
    def push(self, element: PQItem):
        self.queue.append(element)
        self.queue = self.__quickSort()
        
    def getMin(self):
        return None if self.isEmpty() else self.queue[0]
        
    def isEmpty(self):
        return len(self.queue) == 0
    
    def contains(self, node) -> bool:
        return node in self.queue
              
    def __quickSort(self, queue=None):
        if queue is None:
            queue = self.queue
            
        if len(queue) < 2:
            return queue
        
        pivot = queue[len(queue) // 2]
        left = [e for e in queue if e < pivot]
        right = [e for e in queue if e > pivot]
        
        return self.__quickSort(left) + [pivot] + self.__quickSort(right)
    
    
class MinHeap(PriorityQueue):
    """
    Binary Heap implemented in the form of a MinHeap since we are mainly using it for
    A-Star and Dijkstra's Algorithm. 1-based indexing is used. The minimum priority
    element will always be at index 1.
    """
    def __init__(self) -> None:
        self.heap = [PQItem(-100, None)]
        
    def push(self, element: PQItem) -> None:
        "Adds a new element into the heap without compromising the heap"
        self.heap.append(element)
        
        size: int = self.len()
        
        while (self.at(size) < self.atParent(size)):
            self.swap(size, self.parent(size))
            size = self.parent(size)
        
    def pop(self):
        "Remove and returns the min element from the heap without compromising the heap"
        if self.len() == 0:
            return None
        
        if self.len() == 1:
            result = self.heap[1]
            del self.heap[1]
            return result
        
        result = self.heap[1]
        self.heap[1] = self.heap[self.len()]
        del self.heap[self.len()]
        self.heapify(1)
        return result
     
    def isEmpty(self) -> bool:
        return self.len() == 1
    
    def getMin(self):
        return self.heap[1]
    
    def contains(self, node) -> bool:
        return node in self.heap
    
    def at(self, index: int):
        return self.heap[index]
    
    def atParent(self, index: int):
        return self.heap[self.parent(index)]
    
    def atLeft(self, index: int):
        if self.len() < self.left(index):
            return None
        return self.heap[self.left(index)]
    
    def atRight(self, index: int):
        if self.len() < self.right(index):
            return None
        return self.heap[self.right(index)]
        
    def parent(self, index: int) -> int:
        return index // 2
    
    def left(self, index: int) -> int:
        return 2 * index
    
    def right(self, index: int) -> int:
        return index + index + 1
    
    def isLeaf(self, index: int) -> bool:
        return ((index <= self.len())) and (index >= self.len() // 2)
            
    def swap(self, first: int, second: int) -> None:
        self.heap[first], self.heap[second] = self.heap[second], self.heap[first]
             
    def heapify(self, index: int) -> None:
        # we don't deal with leaf nodes
        if self.isLeaf(index):
            return
        
        # nothing to heapify if the element is less than both its child
        if (self.at(index) < self.atLeft(index)) and (self.at(index) < self.atRight(index)):
            return
        
        if (self.atLeft(index) < self.atRight(index)):
            self.swap(index, self.left(index))
            self.heapify(self.left(index))
            
        else:
            self.swap(index, self.right(index))
            self.heapify(self.right(index))
        
    def heapifyAll(self) -> None:
        index: int = self.len() // 2
        
        while index >= 1:
            self.heapify(index)
            index -= 1

    def len(self) -> int:
        return len(self.heap) - 1


class BSTPriorityQueue(PriorityQueue):
    
    class BSTNode(PQItem):
        def __init__(self, priority, element, left=None, right=None):
            super().__init__(priority, element)
            self.left: BSTNode = left
            self.right: BSTNode = right
            
        def push(self, element) -> None:
            if element.priority < self.priority:
                if not self.left:
                    self.left = element
                else:
                    self.left.push(element)
                    
            else:
                if not self.right:
                    self.right = element
                else:
                    self.right.push(element)
                    
        def getMin(self):
            if self.left is None:
                return self
            
            return self.left.getMin()
                    
 
    def __init__(self) -> None:
        self.root: BSTNode = None
        
    def push(self, element: BSTNode) -> None:
        if not self.root:
            self.root = element
            
        else:
            self.root.push(element)
            
    
    def pop(self):
        if self.isEmpty():
            return None
        
        if self.root.left:
            this = self.root
            
            while this.left.left is not None:
                this = this.left

    def getMin(self):
        if self.isEmpty():
            return None
        
        return self.root.getMin()

    
    def isEmpty(self) -> bool:
        return self.root is None