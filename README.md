# N-Dimensional Shape Visualizer

A Python application that visualizes various n-dimensional shapes including hypercubes, simplices, cross polytopes, and hyperspheres from 2 to 99 dimensions using pygame.

## Features

- Support for multiple n-dimensional shapes:
  - **Hypercube**: N-dimensional cube (2^n vertices)
  - **Simplex**: N-dimensional triangle/tetrahedron (n+1 vertices)
  - **Cross Polytope**: N-dimensional octahedron (2n vertices)
  - **Hypersphere**: N-dimensional sphere (point cloud)
- Dimensions from 2 to 99
- Interactive rotation controls
- Automatic rotation mode
- Perspective projection for n-dimensional visualization
- Shape-specific colors and rendering styles
- Dynamic scaling based on dimension and shape type

## Requirements

- Python 3.x
- pygame
- numpy

## Installation

```bash
pip install pygame numpy
```

## Usage

Run the application:

```bash
python main.py
```

1. Select a shape from the menu (1-4)
2. Enter a dimension between the minimum and 99

## Controls

- **Mouse**: Click and drag to rotate (horizontal drag rotates axes 0-1, vertical drag rotates axes 1-2)
- **Spacebar**: Toggle automatic rotation
- **W/S**: Rotate axes 0-1
- **A/D**: Rotate axes 1-2  
- **Q/E**: Rotate axes 2-3
- **R/F**: Rotate axes 3-4
- **T/G**: Rotate axes 4-5
- **Y/H**: Rotate axes 5-6
- **U/J**: Rotate axes 6-7
- **I/K**: Rotate axes 7-8
- **O/L**: Rotate axes 8-9
- **Z/X**: Rotate axes 9-10
- **C/V**: Rotate axes 10-11
- **B/N**: Rotate axes 11-12
- **M/,**: Rotate axes 12-13
- **./:** Rotate axes 13-14

## Shape Characteristics

### Hypercube (White/Light Blue)
- Vertices: 2^n
- Edges: n * 2^(n-1)
- Classic cube extended to n dimensions

### Simplex (Orange/Dark Orange)
- Vertices: n+1
- Edges: n(n+1)/2 (complete graph)
- Triangle extended to n dimensions

### Cross Polytope (Cyan/Dark Cyan)
- Vertices: 2n
- Edges: 2n(n-1)
- Octahedron extended to n dimensions

### Hypersphere (Magenta/Dark Magenta)
- Points: Variable (up to 50 or 2^n, whichever is smaller)
- Edges: Between nearby points
- Point cloud approximation of n-dimensional sphere

## Performance Notes

- Higher dimensions (50+) may have reduced performance due to the exponential increase in vertices and edges
- A 99-dimensional hypercube has 2^99 vertices (theoretically) - the visualization uses mathematical generation but actual rendering is optimized
- Automatic rotation is limited to the first 15 axis pairs for performance reasons
- Hyperspheres use adaptive point counts for better performance

## Files

- `main.py`: Main application loop and user interface
- `shapes.py`: Shape generation for all supported shapes
- `hypercube.py`: Hypercube vertex and edge generation (legacy)
- `rotation.py`: N-dimensional rotation matrices
- `projection.py`: N-dimensional to 2D projection
- `renderer.py`: Pygame rendering engine with shape-specific styling
