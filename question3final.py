import math      # For mathematical functions like tan() and pi
import turtle    # For drawing graphics

# Recursive function to draw an indented line (part of the fractal polygon)
def draw(length: float, depth: int, inward: bool = True) -> None:
    """
    Draws a fractal line segment using recursion.
    
    length: the length of the current line segment
    depth: recursion depth; if 0, draw a straight line
    inward: determines direction of indentation
    """
    if depth == 0:
        turtle.forward(length)  # Base case: draw a straight line
        return

    length /= 3.0  # Divide the segment into three parts for the fractal

    # Set angles for inward or outward indentation
    if inward:
        t1, t2 = 60, -120
    else:
        t1, t2 = -60, 120

    # Recursively draw the four sub-segments
    draw(length, depth - 1, inward)
    turtle.left(t1)
    draw(length, depth - 1, inward)
    turtle.left(t2)
    draw(length, depth - 1, inward)
    turtle.left(t1)
    draw(length, depth - 1, inward)

# Function to draw a complete fractal polygon
def draw_pattern(sides: int, side_length: float, depth: int) -> None:
    """
    Draws a recursive indented polygon.
    
    sides: number of sides in the polygon (>=3)
    side_length: length of each side in pixels
    depth: recursion depth
    """
    # Input validation
    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    if side_length <= 0:
        raise ValueError("Side length must be positive.")
    if depth < 0:
        raise ValueError("Recursion depth must be 0 or greater.")

    # Setup turtle screen
    screen = turtle.Screen()
    screen.title("Recursive Indented Polygon (Inward)")
    screen.setup(width=1000, height=800)

    turtle.hideturtle()     # Hide the turtle cursor for clean drawing
    turtle.speed(0)         # Fastest drawing speed
    turtle.pensize(2)       # Line thickness
    screen.tracer(0, 0)     # Disable animation to speed up drawing

    # Compute radius to center the polygon
    r = side_length / (2.0 * math.tan(math.pi / sides))

    # Move turtle to starting position without drawing
    turtle.penup()
    turtle.setheading(0)
    turtle.goto(-side_length / 2.0, -r)
    turtle.pendown()

    exterior_turn = 360.0 / sides  # Angle to turn at each vertex

    # Draw all sides of the polygon
    for _ in range(sides):
        draw(side_length, depth, inward=True)
        turtle.left(exterior_turn)

    # Update the screen and finish
    screen.update()
    turtle.done()

# Main function to get user input and draw the polygon
def main():
    try:
        sides = int(input("Enter the number of sides: "))
        side_length = float(input("Enter the side length (pixels): "))
        depth = int(input("Enter the recursion depth: "))
    except ValueError:
        print("Please enter valid numeric values (integers for sides/depth, number for length).")
        return

    draw_pattern(sides, side_length, depth)

# Only run main() if this script is executed directly
if __name__ == "__main__":
    main()
    
