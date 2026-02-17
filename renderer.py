import pygame
import numpy as np

class HypercubeRenderer:
    def __init__(self, width=800, height=600):
        """Initialize pygame window and settings."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("N-Dimensional Shape Visualizer")
        self.clock = pygame.time.Clock()
        self.background_color = (0, 0, 0)  # Black
        
        # Shape-specific colors
        self.shape_colors = {
            'hypercube': {
                'vertex': (255, 255, 255),  # White
                'edge': (100, 200, 255)     # Light blue
            },
            'simplex': {
                'vertex': (255, 200, 100),  # Orange
                'edge': (255, 150, 50)      # Dark orange
            },
            'cross_polytope': {
                'vertex': (100, 255, 200),  # Cyan
                'edge': (50, 200, 150)      # Dark cyan
            },
            'hypersphere': {
                'vertex': (255, 100, 255),  # Magenta
                'edge': (200, 50, 200)      # Dark magenta
            }
        }
        
        self.vertex_radius = 4
        
    def clear_screen(self):
        """Clear the screen with background color."""
        self.screen.fill(self.background_color)
        
    def world_to_screen(self, x, y, scale=100):
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            x, y: World coordinates
            scale: Scaling factor to fit the hypercube on screen
            
        Returns:
            tuple: Screen coordinates (screen_x, screen_y)
        """
        screen_x = int(x * scale + self.width / 2)
        screen_y = int(y * scale + self.height / 2)
        return screen_x, screen_y
        
    def draw_vertices(self, points, scale=100, shape_type='hypercube'):
        """
        Draw small circles at each projected point with shape-specific colors.
        
        Args:
            points: List of (x, y) tuples representing projected vertices
            scale: Scaling factor
            shape_type: Type of shape for color selection
        """
        colors = self.shape_colors.get(shape_type, self.shape_colors['hypercube'])
        vertex_color = colors['vertex']
        
        # Adjust vertex size based on shape type
        if shape_type == 'hypersphere':
            vertex_radius = 2  # Smaller points for hypersphere
        elif shape_type == 'simplex':
            vertex_radius = 5  # Larger points for simplex
        else:
            vertex_radius = self.vertex_radius
            
        for x, y in points:
            screen_x, screen_y = self.world_to_screen(x, y, scale)
            pygame.draw.circle(self.screen, vertex_color, 
                             (screen_x, screen_y), vertex_radius)
            
    def draw_edges(self, points, edges, scale=100, shape_type='hypercube'):
        """
        Draw lines between connected vertices with shape-specific colors.
        
        Args:
            points: List of (x, y) tuples representing projected vertices
            edges: List of tuples representing edge connections
            scale: Scaling factor
            shape_type: Type of shape for color selection
        """
        colors = self.shape_colors.get(shape_type, self.shape_colors['hypercube'])
        edge_color = colors['edge']
        
        # Adjust edge thickness based on shape type
        if shape_type == 'hypersphere':
            edge_thickness = 1  # Thinner edges for hypersphere
        elif shape_type == 'simplex':
            edge_thickness = 3  # Thicker edges for simplex
        else:
            edge_thickness = 2
            
        for edge in edges:
            vertex1_idx, vertex2_idx = edge
            x1, y1 = points[vertex1_idx]
            x2, y2 = points[vertex2_idx]
            
            screen_x1, screen_y1 = self.world_to_screen(x1, y1, scale)
            screen_x2, screen_y2 = self.world_to_screen(x2, y2, scale)
            
            pygame.draw.line(self.screen, edge_color,
                           (screen_x1, screen_y1), (screen_x2, screen_y2), edge_thickness)
            
    def update_display(self):
        """Update the pygame display."""
        pygame.display.flip()
        
    def quit(self):
        """Quit pygame."""
        pygame.quit()
