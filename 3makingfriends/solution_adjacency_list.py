import sys
import heapq as hq


class Graph:
    def __init__(self, nbr_nodes, nbr_edges):
        self.nbr_nodes = nbr_nodes
        self.nbr_edges = nbr_edges
        # list of lists to represent the graph
        self.graph = [[] for _ in range(nbr_nodes)]
        # for each node, an empty list is created to represent the edges.
        # the graph is represented as an adjacency list.

    def add_edge(self, u, v, w):
        # Adjust for 1-indexed nodes
        u = u - 1
        v = v - 1
        # Add edge to adjacency list (undirected graph)
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def jarnik(self, start_node=1):
        # the function finds the minimun cost of the minimum spanning tree.
        # the minium spanning tree could be found by adding the chossen edges to a list.

        # list to keep track of all the nodes in the graph.
        # define the nodes in the graph.
        nodes = [i for i in range(self.nbr_nodes)]
        # create a priority queue
        prioryty_queue = []
        # create a set to keep track of visited nodes.
        visted = set()
        # start from the first node, adjust for 1-indexed for each node.
        start_node = start_node - 1

        # add edge for the start node to the priority queue.
        for neighbor, weight in self.graph[start_node]:
            hq.heappush(prioryty_queue, (weight, (start_node, neighbor)))
        # heapush used to add the edge to the priority queue.
        # the prioritt queue is sorted by the cost (weight) of the edge i.e the first element of the tuple.

        # add the start node to the visted nodes.
        visted.add(start_node)

        # remove the frist node from the nodes list.
        nodes.remove(start_node)

        # the cost for the minimum spanning tree.
        total_cost = 0
        # loop unitl the nodes list is empty.
        while nodes or prioryty_queue:
            # get the first edge from the priority queue.
            cost, edge = hq.heappop(prioryty_queue)
            if edge[1] not in visted:
                # Add all edges from the newly visited node to the priority queue
                for neighbor, weight in self.graph[edge[1]]:
                    if neighbor not in visted:
                        hq.heappush(prioryty_queue,
                                    (weight, (edge[1], neighbor)))
                # add the edge to the visted nodes.
                visted.add(edge[1])
                # remove the edge from the nodes list.
                nodes.remove(edge[1])
                # add the cost to the total cost.
                total_cost += cost
        return total_cost

    def get_frist_node(self):
        return hq.heappop(self.priority_queue)


def main():
    # read the number of nodes and edges
    nbr_nodes, nbr_edges = map(int, sys.stdin.readline().split())
    # create the graph
    graph = Graph(nbr_nodes, nbr_edges)

    # read the edges and add them to the graph.
    for line in sys.stdin:
        u, v, w = map(int, line.split())
        graph.add_edge(u, v, w)

    # print out the minimum cost of the minimum spanning tree.
    print(f"{graph.jarnik()}")


if __name__ == "__main__":
    main()
