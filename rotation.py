import numpy as np

def create_rotation_matrix(n, axis1, axis2, theta):
    """
    Create an n x n rotation matrix that rotates points in the plane defined by axis1 and axis2.
    
    Args:
        n (int): Dimension of the space
        axis1 (int): First axis of rotation plane
        axis2 (int): Second axis of rotation plane
        theta (float): Rotation angle in radians
        
    Returns:
        numpy.ndarray: n x n rotation matrix
    """
    # Start with identity matrix
    R = np.eye(n)
    
    # Modify the rotation plane
    R[axis1, axis1] = np.cos(theta)
    R[axis2, axis2] = np.cos(theta)
    R[axis1, axis2] = -np.sin(theta)
    R[axis2, axis1] = np.sin(theta)
    
    return R

def rotate_points(points, rotation_matrix):
    """
    Apply rotation matrix to all vertices.
    
    Args:
        points (numpy.ndarray): Array of points to rotate
        rotation_matrix (numpy.ndarray): Rotation matrix
        
    Returns:
        numpy.ndarray: Rotated points
    """
    return np.dot(points, rotation_matrix.T)
