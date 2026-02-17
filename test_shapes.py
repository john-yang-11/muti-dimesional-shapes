#!/usr/bin/env python3
"""
Test script for the shape visualizer functionality.
"""

from shapes import get_available_shapes, get_shape_info, SHAPES
import numpy as np

def test_shape_generation():
    """Test that all shapes can be generated correctly."""
    print("Testing shape generation...")
    
    shapes = get_available_shapes()
    
    for shape_name in shapes:
        info = get_shape_info(shape_name)
        print(f"\nTesting {shape_name}:")
        
        # Test with dimension 3
        n = 3
        vertices_func = info['vertices_func']
        edges_func = info['edges_func']
        
        try:
            vertices = vertices_func(n)
            edges = edges_func(vertices)
            
            print(f"  Dimension {n}: {len(vertices)} vertices, {len(edges)} edges")
            
            # Verify vertex dimensions
            assert vertices.shape[1] == n, f"Wrong vertex dimension for {shape_name}"
            
            # Verify edge format
            for edge in edges:
                assert len(edge) == 2, f"Invalid edge format for {shape_name}"
                assert edge[0] < len(vertices) and edge[1] < len(vertices), f"Invalid edge indices for {shape_name}"
            
            print(f"  ✓ {shape_name} passed tests")
            
        except Exception as e:
            print(f"  ✗ {shape_name} failed: {e}")
            return False
    
    print("\nAll shape generation tests passed!")
    return True

def test_shape_info():
    """Test shape info retrieval."""
    print("\nTesting shape info...")
    
    shapes = get_available_shapes()
    print(f"Available shapes: {shapes}")
    
    for shape_name in shapes:
        info = get_shape_info(shape_name)
        assert info is not None, f"No info found for {shape_name}"
        assert 'vertices_func' in info, f"No vertices_func for {shape_name}"
        assert 'edges_func' in info, f"No edges_func for {shape_name}"
        assert 'min_dimension' in info, f"No min_dimension for {shape_name}"
        print(f"  ✓ {shape_name} info valid")
    
    print("Shape info tests passed!")
    return True

if __name__ == "__main__":
    success = True
    success &= test_shape_info()
    success &= test_shape_generation()
    
    if success:
        print("\n🎉 All tests passed! The shape visualizer is ready to use.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
