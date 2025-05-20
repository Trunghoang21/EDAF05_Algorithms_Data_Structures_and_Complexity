from collections import deque


def main():
    global C, parent, sink, source, N

    N, C, edges, remove, graph = parse_input()
    parent = [-1]*N
    source = 0
    sink = N-1

    it, max_flow = solver(edges, remove, graph)
    print(str(it) + " " + str(max_flow))


def parse_input():
    N, M, C, P = list(map(int, input().split(" ")))
    edges = [list(map(int, input().split(" "))) for _ in range(M)]
    graph = [dict() for _ in range(N)]
    remove = [int(input()) for _ in range(P)]

    for u, v, c in edges:
        graph[u][v] = graph[v][u] = c

    return N, C, edges, remove, graph


def solver(edges, remove, graph):
    for i in remove:
        u, v, c = edges[i]
        graph[u][v] = graph[v][u] = 0

    max_flow = 0
    flows = [[0 for _ in range(N)] for _ in range(N)]
    while max_flow < C:
        u, v, c = edges[remove.pop()]
        graph[u][v] = graph[v][u] = c
        max_flow += FF(graph, flows)

    return len(remove), max_flow


# Ford-Fulkerson/Edmond-Karp O(CE)

# Edmonds-Karp: O(|VE^2| + |CE|)
def FF(graph, flows):
    new_flow = 0
    while BFS(graph, flows):
        path_flow = float("Inf")
        s = sink
        # Max O(V)
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s] - flows[parent[s]][s])
            s = parent[s]
        new_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            flows[u][v] += path_flow
            flows[v][u] = flows[u][v]
            v = parent[v]
    return new_flow


# O(E + V) => O(E)
def BFS(graph, flows):
    queue = deque([source])
    visited = [False]*N

    visited[source] = True
    while queue:
        current = queue.popleft()
        for neighbor, c in graph[current].items():
            if visited[neighbor] is False and c - flows[current][neighbor] > 0:
                visited[neighbor] = True
                queue.append(neighbor)
                parent[neighbor] = current
                if neighbor is sink:
                    return True
    return visited[sink]


if __name__ == "__main__":
    main()