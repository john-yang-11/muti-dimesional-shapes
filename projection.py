import numpy as np

def project_point(point, distance=5.0):
    """
    Convert n-dimensional point into 2D point using perspective projection.
    
    Args:
        point (numpy.ndarray): n-dimensional point
        distance (float): Distance for perspective projection
        
    Returns:
        tuple: (x, y) 2D coordinates
    """
    if len(point) <= 2:
        # If point is already 2D or less, just return the first two coordinates
        x = point[0] if len(point) > 0 else 0
        y = point[1] if len(point) > 1 else 0
        return x, y
    
    # Use perspective projection with the last coordinate as depth
    last_coordinate = point[-1]
    
    # Prevent division by zero
    if distance - last_coordinate <= 0:
        factor = 1.0
    else:
        factor = distance / (distance - last_coordinate)
    
    x = point[0] * factor
    y = point[1] * factor
    
    return x, y

def project_points(points, distance=5.0):
    """
    Project all n-dimensional points to 2D.
    
    Args:
        points (numpy.ndarray): Array of n-dimensional points
        distance (float): Distance for perspective projection
        
    Returns:
        list: List of (x, y) tuples
    """
    projected = []
    for point in points:
        x, y = project_point(point, distance)
        projected.append((x, y))
    return projected
