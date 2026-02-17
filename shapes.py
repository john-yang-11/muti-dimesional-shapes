import numpy as np

def generate_simplex_vertices(n):
    """
    Generate vertices of an n-dimensional simplex (n-simplex has n+1 vertices).
    
    Args:
        n (int): Dimension of the simplex
        
    Returns:
        numpy.ndarray: Array of shape (n+1, n) containing simplex vertices
    """
    vertices = np.zeros((n + 1, n))
    
    # Generate simplex vertices using standard construction
    # First vertex at origin, others along coordinate axes
    for i in range(n + 1):
        if i == 0:
            # First vertex at (-1, -1, -1, ..., -1)
            vertices[i] = -1
        else:
            # Subsequent vertices have one coordinate = n, others = -1
            vertices[i] = -1
            vertices[i, i-1] = n
    
    # Normalize to fit in unit cube-like space
    vertices = vertices / n
    
    return vertices

def generate_simplex_edges(vertices):
    """
    Generate edges of a simplex by connecting all vertices (complete graph).
    
    Args:
        vertices (numpy.ndarray): Array of simplex vertices
        
    Returns:
        list: List of tuples representing edge connections
    """
    num_vertices = vertices.shape[0]
    edges = []
    
    # In a simplex, every vertex connects to every other vertex
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            edges.append((i, j))
    
    return edges

def generate_cross_polytope_vertices(n):
    """
    Generate vertices of an n-dimensional cross polytope (2n vertices).
    
    Args:
        n (int): Dimension of the cross polytope
        
    Returns:
        numpy.ndarray: Array of shape (2n, n) containing cross polytope vertices
    """
    vertices = np.zeros((2 * n, n))
    
    # Generate vertices: unit vectors in positive and negative directions
    for i in range(n):
        # Positive unit vector
        vertices[2 * i] = np.zeros(n)
        vertices[2 * i, i] = 1
        
        # Negative unit vector
        vertices[2 * i + 1] = np.zeros(n)
        vertices[2 * i + 1, i] = -1
    
    return vertices

def generate_cross_polytope_edges(vertices):
    """
    Generate edges of a cross polytope by connecting non-opposite vertices.
    
    Args:
        vertices (numpy.ndarray): Array of cross polytope vertices
        
    Returns:
        list: List of tuples representing edge connections
    """
    n = vertices.shape[1]
    num_vertices = vertices.shape[0]
    edges = []
    
    # In a cross polytope, each vertex connects to all others except its opposite
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            # Check if vertices are not opposites
            # Opposite vertices are pairs (0, n), (1, n+1), ..., (n-1, 2n-1)
            is_opposite = False
            for k in range(n):
                if (i == 2 * k and j == 2 * k + 1) or (i == 2 * k + 1 and j == 2 * k):
                    is_opposite = True
                    break
            
            if not is_opposite:
                edges.append((i, j))
    
    return edges

def generate_hypersphere_points(n, num_points=100):
    """
    Generate points on the surface of an n-dimensional hypersphere.
    
    Args:
        n (int): Dimension of the hypersphere
        num_points (int): Number of points to generate
        
    Returns:
        numpy.ndarray: Array of shape (num_points, n) containing hypersphere points
    """
    if n == 1:
        # 1D "sphere" is just two points
        points = np.array([[-1], [1]])
        return points
    
    # Generate random points from normal distribution
    points = np.random.normal(0, 1, (num_points, n))
    
    # Normalize each point to unit distance from origin
    norms = np.linalg.norm(points, axis=1, keepdims=True)
    points = points / norms
    
    return points

def generate_hypersphere_edges(vertices, max_distance=0.5):
    """
    Generate edges for hypersphere visualization by connecting nearby points.
    
    Args:
        vertices (numpy.ndarray): Array of hypersphere points
        max_distance (float): Maximum distance between connected points
        
    Returns:
        list: List of tuples representing edge connections
    """
    num_points = vertices.shape[0]
    edges = []
    
    # Connect points that are close to each other
    for i in range(num_points):
        for j in range(i + 1, num_points):
            distance = np.linalg.norm(vertices[i] - vertices[j])
            if distance <= max_distance:
                edges.append((i, j))
    
    return edges

# Shape registry for easy access
SHAPES = {
    'hypercube': {
        'vertices_func': lambda n: __import__('hypercube').generate_vertices(n),
        'edges_func': lambda vertices: __import__('hypercube').generate_edges(vertices),
        'min_dimension': 2,
        'description': 'N-dimensional hypercube (2^n vertices)'
    },
    'simplex': {
        'vertices_func': generate_simplex_vertices,
        'edges_func': generate_simplex_edges,
        'min_dimension': 2,
        'description': 'N-dimensional simplex (n+1 vertices)'
    },
    'cross_polytope': {
        'vertices_func': generate_cross_polytope_vertices,
        'edges_func': generate_cross_polytope_edges,
        'min_dimension': 2,
        'description': 'N-dimensional cross polytope (2n vertices)'
    },
    'hypersphere': {
        'vertices_func': lambda n: generate_hypersphere_points(n, num_points=min(50, 2**n)),
        'edges_func': lambda vertices: generate_hypersphere_edges(vertices, max_distance=0.3),
        'min_dimension': 2,
        'description': 'N-dimensional hypersphere (point cloud)'
    }
}

def get_available_shapes():
    """Get list of available shape names."""
    return list(SHAPES.keys())

def get_shape_info(shape_name):
    """Get information about a specific shape."""
    return SHAPES.get(shape_name, None)
