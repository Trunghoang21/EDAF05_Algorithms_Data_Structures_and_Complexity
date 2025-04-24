import sys
import heapq as hq


class Graph:
    def __init__(self, nbr_nodes, nbr_edges):
        self.nbr_nodes = nbr_nodes
        self.nbr_edges = nbr_edges
        # list of lists to represent the graph
        self.graph = [[0] * nbr_nodes for _ in range(nbr_nodes)]

    def add_edge(self, u, v, w):
        self.graph[u-1][v-1] = w
        # self.graph[v-1][u-1] = w # undirected graph
        # add the edge to the graph

    def jarnik(self, start_node=1):
        # list to keep track of all the nodes in the graph.
        # define the nodes in the graph.
        nodes = [i for i in range(self.nbr_nodes)]
        # create a priority queue
        prioryty_queue = []
        # create a set to keep track of visited nodes.
        visted = set()
        # start from the first node
        start_node = start_node - 1
        # add edge to the priority queue
        for i in range(self.nbr_nodes):
            if self.graph[start_node][i] != 0:
                # heapush adds the edge to the priority queue
                hq.heappush(prioryty_queue,
                            (self.graph[start_node][i], (start_node, i)))
            if self.graph[i][start_node] != 0:
                hq.heappush(prioryty_queue,
                            (self.graph[i][start_node], (start_node, i)))
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
                # add the edge to the priority queue.
                for i in range(self.nbr_nodes):
                    if self.graph[edge[1]][i] != 0 and i not in visted:
                        hq.heappush(prioryty_queue,
                                    (self.graph[edge[1]][i], (edge[1], i)))
                # add the edge to the priority queue.
                for i in range(self.nbr_nodes):
                    if self.graph[i][edge[1]] != 0 and i not in visted:
                        hq.heappush(prioryty_queue,
                                    (self.graph[i][edge[1]], (edge[1], i)))

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
    graph = Graph(nbr_nodes, nbr_edges)

    for line in sys.stdin:
        u, v, w = map(int, line.split())
        graph.add_edge(u, v, w)

    print(f"{graph.jarnik()}")


if __name__ == "__main__":
    main()
