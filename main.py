import pygame
import numpy as np
import sys
from hypercube import generate_vertices, generate_edges
from rotation import create_rotation_matrix, rotate_points
from projection import project_points
from renderer import HypercubeRenderer
from shapes import get_available_shapes, get_shape_info, SHAPES

def main():
    # Shape selection
    print("Available shapes:")
    shapes = get_available_shapes()
    for i, shape_name in enumerate(shapes, 1):
        info = get_shape_info(shape_name)
        print(f"{i}. {shape_name.title()}: {info['description']}")
    
    try:
        shape_choice = int(input("Select shape (enter number): "))
        if shape_choice < 1 or shape_choice > len(shapes):
            print("Invalid shape selection")
            return
        selected_shape = shapes[shape_choice - 1]
    except ValueError:
        print("Please enter a valid number")
        return
    
    # Get user input for dimension
    shape_info = get_shape_info(selected_shape)
    min_dim = shape_info['min_dimension']
    try:
        n = int(input(f"Enter dimension ({min_dim}-99): "))
        if n < min_dim or n > 99:
            print(f"Dimension must be between {min_dim} and 99")
            return
    except ValueError:
        print("Please enter a valid integer")
        return
    
    # Initialize shape
    print(f"Generating {n}-dimensional {selected_shape}...")
    vertices_func = shape_info['vertices_func']
    edges_func = shape_info['edges_func']
    
    vertices = vertices_func(n)
    edges = edges_func(vertices)
    print(f"Generated {len(vertices)} vertices and {len(edges)} edges")
    print(f"Visualizing {n}-dimensional {selected_shape}")
    print("Controls:")
    print("- Mouse: Click and drag to rotate")
    print("- Spacebar: Toggle automatic rotation")
    print("- W/S: Rotate axes 0-1")
    print("- A/D: Rotate axes 1-2")
    print("- Q/E: Rotate axes 2-3")
    print("- R/F: Rotate axes 3-4")
    print("- T/G: Rotate axes 4-5")
    print("- Y/H: Rotate axes 5-6")
    print("- U/J: Rotate axes 6-7")
    print("- I/K: Rotate axes 7-8")
    print("- O/L: Rotate axes 8-9")
    print("- Z/X: Rotate axes 9-10")
    print("- C/V: Rotate axes 10-11")
    print("- B/N: Rotate axes 11-12")
    print("- M/, : Rotate axes 12-13")
    print("- ./: Rotate axes 13-14")
    print(f"\nAvailable axis pairs for dimension {n}: {min(14, n-1)}")
    
    # Initialize renderer
    renderer = HypercubeRenderer()
    
    # Rotation angles for different axis pairs
    rotation_angles = {}
    rotation_speed = 0.02
    auto_rotate = True  # Enable automatic rotation
    auto_rotation_speed = 0.01  # Speed for automatic rotation
    
    # Main loop
    running = True
    # Adjust scale based on dimension and shape type
    if selected_shape == 'hypersphere':
        scale = max(100, 400 - (n * 3))
    elif selected_shape == 'simplex':
        scale = max(80, 350 - (n * 2.5))
    elif selected_shape == 'cross_polytope':
        scale = max(90, 380 - (n * 2.8))
    else:  # hypercube
        scale = max(50, 300 - (n * 2))
    
    # Mouse rotation variables
    mouse_dragging = False
    last_mouse_pos = None
    mouse_sensitivity = 0.01
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                    auto_rotate = False  # Disable auto-rotation when using mouse
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change cursor to hand
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    mouse_dragging = False
                    last_mouse_pos = None
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor to arrow
            elif event.type == pygame.MOUSEMOTION:
                if mouse_dragging and last_mouse_pos:
                    current_mouse_pos = pygame.mouse.get_pos()
                    dx = current_mouse_pos[0] - last_mouse_pos[0]
                    dy = current_mouse_pos[1] - last_mouse_pos[1]
                    
                    # Apply mouse rotation to first two axis pairs
                    if n >= 2:
                        rotation_angles[(0, 1)] = rotation_angles.get((0, 1), 0) + dx * mouse_sensitivity
                    if n >= 3:
                        rotation_angles[(1, 2)] = rotation_angles.get((1, 2), 0) + dy * mouse_sensitivity
                    
                    last_mouse_pos = current_mouse_pos
        
        # Handle keyboard input for rotation
        keys = pygame.key.get_pressed()
        
        # Toggle automatic rotation with spacebar
        if keys[pygame.K_SPACE]:
            auto_rotate = not auto_rotate
        
        # Dynamic keyboard mapping for axis pairs
        # Define key pairs for different axis rotations
        key_mappings = [
            (pygame.K_w, pygame.K_s, 0, 1),  # W/S: axes 0-1
            (pygame.K_a, pygame.K_d, 1, 2),  # A/D: axes 1-2
            (pygame.K_q, pygame.K_e, 2, 3),  # Q/E: axes 2-3
            (pygame.K_r, pygame.K_f, 3, 4),  # R/F: axes 3-4
            (pygame.K_t, pygame.K_g, 4, 5),  # T/G: axes 4-5
            (pygame.K_y, pygame.K_h, 5, 6),  # Y/H: axes 5-6
            (pygame.K_u, pygame.K_j, 6, 7),  # U/J: axes 6-7
            (pygame.K_i, pygame.K_k, 7, 8),  # I/K: axes 7-8
            (pygame.K_o, pygame.K_l, 8, 9),  # O/L: axes 8-9
            (pygame.K_z, pygame.K_x, 9, 10), # Z/X: axes 9-10
            (pygame.K_c, pygame.K_v, 10, 11), # C/V: axes 10-11
            (pygame.K_b, pygame.K_n, 11, 12), # B/N: axes 11-12
            (pygame.K_m, pygame.K_COMMA, 12, 13), # M/,: axes 12-13
            (pygame.K_PERIOD, pygame.K_SLASH, 13, 14), # ./: axes 13-14
        ]
        
        # Apply keyboard controls for available axis pairs
        for key_pos, key_neg, axis1, axis2 in key_mappings:
            if axis1 < n and axis2 < n:
                if keys[key_pos]:
                    rotation_angles[(axis1, axis2)] = rotation_angles.get((axis1, axis2), 0) + rotation_speed
                if keys[key_neg]:
                    rotation_angles[(axis1, axis2)] = rotation_angles.get((axis1, axis2), 0) - rotation_speed
        
        # Apply automatic rotation
        if auto_rotate:
            # Rotate different axis pairs based on dimension
            # Use a dynamic approach for higher dimensions
            for i in range(min(n - 1, 15)):  # Limit to first 15 axis pairs for performance
                axis1, axis2 = i, i + 1
                if axis2 < n:
                    # Decrease rotation speed for higher dimensions
                    speed_factor = max(0.1, 1.0 - (i * 0.1))
                    rotation_angles[(axis1, axis2)] = rotation_angles.get((axis1, axis2), 0) + auto_rotation_speed * speed_factor
        
        # Apply rotations
        rotated_vertices = vertices.copy()
        for (axis1, axis2), angle in rotation_angles.items():
            if axis1 < n and axis2 < n:  # Make sure axes exist in current dimension
                rotation_matrix = create_rotation_matrix(n, axis1, axis2, angle)
                rotated_vertices = rotate_points(rotated_vertices, rotation_matrix)
        
        # Project to 2D
        projected_points = project_points(rotated_vertices)
        
        # Clear screen
        renderer.clear_screen()
        
        # Draw edges and vertices
        renderer.draw_edges(projected_points, edges, scale, selected_shape)
        renderer.draw_vertices(projected_points, scale, selected_shape)
        
        # Update display
        renderer.update_display()
        renderer.clock.tick(60)  # 60 FPS
    
    # Cleanup
    renderer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
