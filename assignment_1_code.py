"""
Assignment 1 Part B for COMS 4223 Neworks, Crowds, and the Web
"""

import networkx as nx 
from typing import List

### Exercise 2

def exercise2_1() -> int:
    """
    return 42
    """
    return 42


def exercise2_2() -> List[int]:
    """
    Return a list of all odd numbers between 50 and 150.
    """
    return list(range(51,150,2))

### Exercise 3

def exercise3_1(p: str) -> nx.Graph:
    """
    load p, the path to the txt file (for this assignment, "ca-GrQc.txt")
    as an undirected networkx graph. 

    return the graph
    """
    g = nx.Graph()

    with open(p, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue

            node1, node2 = map(int, line.split())
            g.add_edge(node1, node2)

    return g

def exercise3_2(g: nx.Graph) -> tuple[int, int]:
    """
    given a graph g, return a tuple of integers in the following order:
    1. the maximum degree in the network
    2. the minimum degree in the network
    """
    degrees = [degree for node, degree in g.degree()]

    return (max(degrees), min(degrees))

def exercise3_3(g: nx.Graph) -> tuple[
        float,
        float,
        float,
        float,
        float,
    ]: 
    """
    given a graph g, return a tuple of the following in order:
    - Percentage of authors with only 1 coauthor.
    - Percentage of authors with 10 or fewer coauthors.
    - Percentage of authors with 20 or fewer coauthors.
    - Percentage of authors with 40 or fewer coauthors.
    - Percentage of authors with 80 or fewer coauthors.
    
    represent each percentage as a decimal
    """
    degrees = [degree for node, degree in g.degree()]
    total = len(degrees)

    only_1 = sum(1 for degree in degrees if degree == 1) / total
    at_most_10 = sum(1 for degree in degrees if degree <= 10) / total
    at_most_20 = sum(1 for degree in degrees if degree <= 20) / total
    at_most_40 = sum(1 for degree in degrees if degree <= 40) / total
    at_most_80 = sum(1 for degree in degrees if degree <= 80) / total

    return (only_1, at_most_10, at_most_20, at_most_40, at_most_80)


### Exercise 4

def exercise4_1(g: nx.Graph, n1: int, n2: int) -> bool:
    """
    given a graph g and two nodes n1 and n2 in g,
    return True if n1 and n2 have a strong tie else False
    """
    if not g.has_edge(n1, n2):
        return False

    return any(nx.common_neighbors(g, n1, n2))

def exercise4_2(g: nx.Graph) -> tuple[int, int, int]:
    """
    Given a graph g, return a tuple of the following 3 values:
    - Number of edges 
    - Number of strong ties
    - Number of weak ties
    """
    strong_ties = 0
    weak_ties = 0

    for n1, n2 in g.edges():
        if exercise4_1(g, n1, n2):
            strong_ties += 1
        else:
            weak_ties += 1

    return (g.number_of_edges(), strong_ties, weak_ties)

def exercise4_3(g: nx.Graph) -> tuple[int, int, int, int]:
    """
    Takes the graph g as an input and returns a tuple of the following 4 values:
    - The number of connected components in the graph
    - The number of nodes in the largest connected component in the graph
    - The number of connected components in the graph, if you removed all weak ties.
    - The number of nodes in the largest connected component in the graph, if you removed all weak ties.
    """
    components = list(nx.connected_components(g))
    num_components = len(components)
    largest_component = max(len(component) for component in components)

    strong_graph = nx.Graph()
    strong_graph.add_nodes_from(g.nodes())

    for n1, n2 in g.edges():
        if exercise4_1(g, n1, n2):
            strong_graph.add_edge(n1, n2)

    strong_components = list(nx.connected_components(strong_graph))
    num_strong_components = len(strong_components)
    largest_strong_component = max(
        len(component) for component in strong_components
    )

    return (
        num_components,
        largest_component,
        num_strong_components,
        largest_strong_component,
    )


if __name__ == "__main__":
    print(exercise2_1()) # expected output: 42
    print(exercise2_2()) # expected output: 51 53 55 ... 149
    g = exercise3_1('ca-GrQc.txt')
    output_3_2 = exercise3_2(g)
    print(output_3_2)
    if len(output_3_2) != 2:
        raise ValueError("Output of exercise3_2 should be a tuple of 2 integers")
    output_3_3 = exercise3_3(g)
    print(output_3_3)
    if len(output_3_3) != 5:
        raise ValueError("Output of exercise3_3 should be a list of 5 floats")
    print(exercise4_1(g, 3466, 937)) # expected output: True
    print(exercise4_1(g, 3466, 14924)) # expected output: False
    output_4_2 = exercise4_2(g)
    if len(output_4_2) != 3:
        raise ValueError("Output of exercise4_2 should be a tuple of 3 integers")
    output_4_3 = exercise4_3(g)
    if len(output_4_3) != 4:
        raise ValueError("Output of exercise4_3 should be a tuple of 4 integers")
