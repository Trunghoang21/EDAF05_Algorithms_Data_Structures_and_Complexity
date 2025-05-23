# defind a class to solve the problem. 
from collections import deque

class Railway_Planner: 
    def __init__(self):
        # define the class variables. 
        self.nbr_nodes = 0 
        self.nbr_edges = 0
        self.required_flow = 0
        self.original_edges = [] # the original edges. 
        self.to_remove = []
        self.source = 0
        self.sink = 0
        

    def parse_input(self):
        N, M, C, P = map(int, input().split()) # N: number of nodes, M: number of edges, C: the required flow, P: is the numebr of edges to be removed.
    
        # read the edges
        edges = []
        for _ in range(M):
            u, v, c = map(int, input().split())
            edges.append((u, v, c))
        self.original_edges = edges


        # read the edges to be removed.
        to_remove = []
        for _ in range(P):
            to_remove.append(self.original_edges[int(input())])

        self.to_remove = to_remove # the edges to be removed.

        self.nbr_nodes = N
        self.nbr_edges = M
        self.required_flow = C
        self.sink = N - 1

    def solver(self):
        # initialzie the original graph. 
        graph = [dict() for _ in range(self.nbr_nodes)]

        # add all the edges to the graph. 
        for (u, v, c) in self.original_edges:
            graph[u][v]  = graph[v][u] = c

        # remove all the edges from the to_remove list.
        for u, v , _ in self.to_remove:
            #u, v , c = self.original_edges[i]
            graph[u][v] = graph[v][u] = 0
        
        # initialize the max_flow to 0. 
        max_flow = 0 
        flows = [[0 for _ in range(self.nbr_nodes)] for _ in range(self.nbr_nodes)] # the flow matrix. 
        
        while max_flow < self.required_flow:
            # add back one edges to the graph.
            u, v, c = self.to_remove.pop()
            #print(f"Adding back edge: {u} {v} {c}")
            graph[u][v] = graph[v][u] = c
            # add back edges to the graph.
            self.Edmonds_Karp(graph, flows)
            max_flow = sum(flows[self.source]) # calculate the max flow. 
            # update the graph with new edges.
             
        
        return (len(self.to_remove), sum(flows[self.source])) # return the number of edges to be removed and the max flow.
    
    def Edmonds_Karp(self, current_graph, flows):
        # Implement the Edmonds-Karp algorithm for finding max flow
        while True: 
            parent = self.BFS_(current_graph, flows)
            if parent[self.sink] == -1:
                break
            path_flow = float("Inf")
            s = self.sink
            # Max O(V)
            while s != self.source:
                path_flow = min(path_flow, current_graph[parent[s]][s] - flows[parent[s]][s])
                s = parent[s]
            # update the flow matrix.
            v = self.sink
            while v != self.source:
                u = parent[v]
                flows[u][v] += path_flow
                flows[v][u] -= path_flow
                v = parent[v]
        

    def BFS_(self, current_graph, flows):
        # check if the node is visited.
        visited = [False] * self.nbr_nodes
        # mark the source code as visted.
        visited[self.source] = True
        
        # the queue to store the nodes.
        queue = deque([self.source])
        # the parent of the node.
        parent = [-1] * self.nbr_nodes
        
        while queue:
            current = queue.popleft()
            for neighbor, c in current_graph[current].items():
                if visited[neighbor] is False and c - flows[current][neighbor] > 0: 
                    visited[neighbor] = True
                    queue.append(neighbor)
                    parent[neighbor] = current
                    if neighbor == self.sink:
                        return parent
        return parent
        # return the parent of each node.
def main():
    planner = Railway_Planner()
    # read the input.
    planner.parse_input()
    #planner.print()
    result = planner.solver()
    # print the result.
    print(f"{result[0]} {result[1]}")

if __name__ == "__main__":
    main()