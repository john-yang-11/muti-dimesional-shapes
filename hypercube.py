import numpy as np

def generate_vertices(n):
    """
    Generate all vertices of an n-dimensional hypercube.
    
    Args:
        n (int): Dimension of the hypercube
        
    Returns:
        numpy.ndarray: Array of shape (2^n, n) containing all vertices
    """
    num_vertices = 2 ** n
    vertices = np.zeros((num_vertices, n))
    
    for i in range(num_vertices):
        # Convert i to binary representation and map to -1, 1
        binary_str = format(i, f'0{n}b')
        vertex = []
        for bit in binary_str:
            vertex.append(-1 if bit == '0' else 1)
        vertices[i] = vertex
    
    return vertices

def generate_edges(vertices):
    """
    Generate edges of the hypercube by connecting vertices that differ in exactly one coordinate.
    
    Args:
        vertices (numpy.ndarray): Array of vertices
        
    Returns:
        list: List of tuples representing edge connections (vertex_index1, vertex_index2)
    """
    n = vertices.shape[1]
    num_vertices = vertices.shape[0]
    edges = []
    
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            # Count how many coordinates differ
            diff_count = np.sum(vertices[i] != vertices[j])
            if diff_count == 1:
                edges.append((i, j))
    
    return edges
