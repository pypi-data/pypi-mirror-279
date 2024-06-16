from cwstorm.deserializer import deserialize
from collections import Counter


def walk(node, func, result):
    """
    Walk the graph and apply a function to each node.

    If the function returns True, the node is added to the result list.
    """
    for child in node.children:
        if child.is_original(node):
            if func(child):
                result.append(child)
            walk(child, func, result)
    return result


def _cycle_check(node, visited, rec_stack):
    """
    Do the work for cycle detection.
    """
    if node not in visited:
        visited.add(node)
        rec_stack.add(node)

        for child in node.children:
            if child not in visited and _cycle_check(child, visited, rec_stack):
                return True
            elif child in rec_stack:
                # If the child is in the recursion stack, it means we found a cycle.
                return True

        rec_stack.remove(node)
    return False


def has_cycle(root):
    """
    Detect cycles in the graph.
    """
    visited = set()
    rec_stack = set()
    return _cycle_check(root, visited, rec_stack)


def longest_path(sink):
    """
    Find the longest path from the job.
    """

    def topological_sort(node, visited, stack):
        visited.add(node)
        for child in node.children:
            if child not in visited:
                topological_sort(child, visited, stack)
        stack.append(node)

    def find_longest_path(stack):
        # Init all distances to the minimum possible value
        dist = {node: float("-inf") for node in stack}
        # Distance to the sink node from itself is 0
        dist[sink] = 0

        while stack:
            node = stack.pop()
            # Update dists for all children
            for child in node.children:
                if dist[child] < dist[node] + 1:
                    dist[child] = dist[node] + 1

        return max(dist.values())

    # Topological sort the graph
    visited = set()
    stack = []
    topological_sort(sink, visited, stack)

    # Find the longest path using the topologically sorted nodes
    return find_longest_path(stack)


def validate(data):
    """
    Validate a dict that represents a job.
    """

    result = {"input_info": [], "job_info": []}

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    node_types = [node["data"]["type"] for node in nodes]
    type_counts = Counter(node_types)
    type_counts = {f"{k.capitalize()} nodes": v for k, v in type_counts.items()}

    element_counts = {"Nodes": len(nodes), "Edges": len(edges)}
    counts_list = list(element_counts.items())
    counts_list += type_counts.items()
    result["input_info"] = counts_list

    job = deserialize(data)

    num_connected_nodes = job.count_descendents() + 1
    num_connected_nodes_okay = len(nodes) == (num_connected_nodes)

    source_nodes = []
    walk(job, lambda x: len(x.children) == 0, source_nodes)
    num_source_nodes = len(source_nodes)

    longest = longest_path(job)

    density = 0
    if len(nodes) > 1:
        density = len(edges) / (len(nodes) * (len(nodes) - 1))

    has_cycle_ = has_cycle(job)

    job_params = [
        ["Name", job.name(), True],
        ["Schema version", job.schema_version(), True],
        ["Comment", job.comment(), True],
        ["Project", job.project(), True],
        ["Location", job.location(), True],
        ["Author", job.author(), True],
    ]
    job_params.append(["Source nodes", num_source_nodes, num_source_nodes > 0])
    job_params.append(["Connected nodes", num_connected_nodes, num_connected_nodes_okay])
    job_params.append(["Longest path", longest, longest > 0])
    job_params.append(["Density", density, density > 0])
    job_params.append(["Has cycle", has_cycle_, not has_cycle_])

    result["job_info"] = job_params

    return result
