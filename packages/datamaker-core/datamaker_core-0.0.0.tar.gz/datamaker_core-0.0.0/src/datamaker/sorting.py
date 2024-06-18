from collections import defaultdict, deque


def topological_sort(dependencies: dict[str, list[str]]) -> list[str]:
    """Sorts a graph in topological order.

    Args:
        dependencies (dict[str, list[str]]): A dictionary where the key is a node and the value is a list of nodes that the key node depends on.

    Raises:
        ValueError: If a cycle is detected in the graph.

    Returns:
        list[str]: A list of nodes in topological order.
    """
    indegree = defaultdict(int)
    graph = defaultdict(list)

    for node, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(node)
            indegree[node] += 1

    # Queue for all nodes with no incoming edges
    zero_indegree = deque([node for node in graph if indegree[node] == 0])

    order = []
    while zero_indegree:
        node = zero_indegree.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_indegree.append(neighbor)

    # Check if there was a cycle
    if len(order) != len(set(indegree).union(set(graph))):
        raise ValueError(
            "A cycle detected in the graph, no valid topological order exists"
        )

    return order
