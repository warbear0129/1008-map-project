from abc import ABC, abstractmethod
from objects import *
import heapq

class Algorithm(ABC):
    """
    Abstract class for algorithm object.
    Ensures output and parameters are consistent whenever we add new algorithms
    """
    def __init__(self, source: Node, destination: Node, graph: Graph, queue: PriorityQueue = None) -> None:
        self.source = source
        self.destination = destination
        self.graph = graph
        self.queue = queue
               
    @abstractmethod
    def getPath(self) -> list:
        pass           
    
    
class Dijkstra(Algorithm):
    """
    Class for the normal Dijkstra Algorithm.
    Queue takes in any implementation of a PriorityQueue.
    At the moment we have:
        1) List-based priority queue 
        2) Binary heap
        3) BST
    """
    name = "Classic Dijkstra Algorithm"
    distance = {}
    edgeTo = {}
    queue = MinHeap()

    def __init__(self, source: Node, destination: Node, graph: Graph, queue: PriorityQueue = None) -> None:
        super().__init__(source, destination, graph, queue)
        
        for node in self.graph.adjacency_list:
            self.distance[node] = float('inf')
            self.edgeTo[node] = None
            self.queue.push(PQItem(self.source.distanceTo(node), node))
                
        self.distance[self.source] = 0.0
                            
        while not self.queue.isEmpty():
            current_node = self.queue.pop().element
            
            for edge in self.graph.adj(current_node):
                    distance = self.distance[current_node] + edge.distance
                    
                    if edge.destination not in self.distance:
                        self.distance[edge.destination] = distance
                        self.edgeTo[edge.destination] = edge
                        
                    else:
                        if distance < self.distance[edge.destination]:
                            self.distance[edge.destination] = distance
                            self.edgeTo[edge.destination] = edge
 
    def getPath(self) -> list:
        if not self.edgeTo[self.destination]:
            return []
        
        path = []
        edge = self.edgeTo[self.destination]
        
        while edge is not None:
            path.append(edge)
            edge = self.edgeTo[edge.source]
            
        return path
        
            
    
class DijkstraNoPQ(Algorithm):
    
    name = "Dijkstra Without Priority Queue"
    path = {}
    
    def __init__(self, source: Node, destination: Node, graph: Graph, queue: PriorityQueue = None) -> None:
        super().__init__(source, destination, graph, queue)
        
        # Keep track of visited nodes
        seen = set()
        
        current_node: Node = self.source
        
        # paths will store our visited nodes and their relaxed weight value
        # the first key is an Edge object representing the source_node with distance of zero
        self.path = {current_node: Edge(source=None,
                                        destination=current_node,
                                        distance=0.0)}

        # we just want to find the shortest route between source and destination
        while current_node != self.destination:
            seen.add(current_node)
            
            for edge in self.graph.adj(current_node):
                curr_distance: float = edge.distance + self.path[current_node].distance

                if edge.destination not in self.path:
                    self.path[edge.destination] = edge
                    self.path[edge.destination].distance = curr_distance

                else:
                    if self.path[edge.destination].distance > curr_distance:
                        self.path[edge.destination] = edge
                        self.path[edge.destination].distance = curr_distance

            next_edges = {node: self.path[node] for node in self.path if node not in seen}

            if not next_edges:
                self.path = {}
                return 

            current_node = min(next_edges, key = lambda k: next_edges[k].distance)
            
    def getPath(self) -> list:
        shortest_path = []
        current_node = self.destination
        while current_node is not None:
            shortest_path.append(self.path[current_node])
            current_node = self.path[current_node].source

        return shortest_path[::-1]
    
   
    
class AStar(Algorithm):
    
    name = "A-Star Algorithm"
    visited = []
    path = {}
    
    def __init__(self, source: Node, destination: Node, graph: Graph, queue: PriorityQueue = None) -> None:
        super().__init__(source, destination, graph, queue)
        
        # Push into the source node into queue with F-score = 0
        self.queue.push(PQItem(0, self.source))
        
        while not self.queue.isEmpty():
            
            # Retrieve the Node with the lowest F-score
            current_node = self.queue.pop().element
            
            # Mark it as visited
            self.visited_nodes.append(current_node)
            
            # If we found our destination, return
            if (current_node == self.destination):
                return
            
            # Enumerate through all the adjacent nodes
            for edge in self.graph.adj(current_node):
                next_node = edge.destination
                
                # ignore any visited nodes
                if next_node in self.visited:
                    continue
                
                if self.queue.contains(next_node):
                    temp_g = self.__g(current_node) + edge.distance
               
                
                if self.queue.contains(next_node) and self.__g(next_node) < curr_cost:
                    continue
                
                if next_node in self.visited_nodes and self.__g(next_node) < curr_cost:
                    continue
                                   
    def getPath(self) -> list:
        return self.path
                   
    
    def __g(self, node):
        return self.source.distanceTo(node)
    
    def __h(self, node):
        return self.destination.distanceTo(node)
                        

class IanAStar(Algorithm):
    """
    For our search algorithm we went with the a*star algorithm as the added heuristic will allow us to find our shortest path in a
    smarter and more efficient way.
    We used transfer cost as a heuristic, and we keep track of how many times the route changes bus services.
    A threshold is set to prefer routes with less transferring.
    This brings us with two benefits; one is that it mimics the reality of the situation where transferring busses is time consuming and undesirable.
    The second is that we will not look at every path, but only those that contains the smaller number of transfers that we want.
    This means less paths traversed and a faster search time.
    """
    name = "Ian's A-Star Algorithm"
    
    def __init__(self, source: Node, destination: Node, graph: Graph, queue: PriorityQueue = None) -> None:
        self.source = source
        self.destination = destination
        self.graph = graph
        self.queue = []
    
    
    def getPath(self) -> list:
        seen = set()
        # maintain a queue of paths
        queue = []
        # push the first path into the queue
        heapq.heappush(queue, (0, 0, 0, [(self.source.id, None)]))
        while queue:
            # get the first path from the queue
            (curr_cost, curr_distance, curr_transfers, path) = heapq.heappop(queue)

            # get the last node from the path
            (node, curr_service) = path[-1]

            # path found


            if node == self.destination:
                return (curr_distance, path)
            if (node, curr_service) in seen:
                continue

            seen.add((node, curr_service))
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            for edge in self.graph.adj(node):
                (adjacent, service), distance = (edge.destination, edge.bus_service), edge.distance
                new_path = list(path)
                new_path.append((adjacent, service))
                new_distance = curr_distance + distance
                new_cost = distance + curr_cost
                new_transfers = curr_transfers
                if curr_service != service:
                    new_cost += 10
                    new_transfers += 1
                new_cost += 0.5

                heapq.heappush(queue, (new_cost, new_distance, new_transfers, new_path))
                
        return []
        
        
            
        
        
        