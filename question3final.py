import math
import turtle
 
def draw(length: float, depth: int, inward: bool = True) -> None:
    if depth == 0:
        turtle.forward(length)
        return
 
    length /= 3.0
 
    if inward:
        t1, t2 = 60, -120
    else:
        t1, t2 = -60, 120
 
    draw(length, depth - 1, inward)
    turtle.left(t1)
    draw(length, depth - 1, inward)
    turtle.left(t2)
    draw(length, depth - 1, inward)
    turtle.left(t1)
    draw(length, depth - 1, inward)
 
def draw_pattern(sides: int, side_length: float, depth: int) -> None:
    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    if side_length <= 0:
        raise ValueError("Side length must be positive.")
    if depth < 0:
        raise ValueError("Recursion depth must be 0 or greater.")
 
    screen = turtle.Screen()
    screen.title("Recursive Indented Polygon (Inward)")
    screen.setup(width=1000, height=800)
 
    turtle.hideturtle()
    turtle.speed(0)
    turtle.pensize(2)
    screen.tracer(0, 0)
 
    r = side_length / (2.0 * math.tan(math.pi / sides))
 
    turtle.penup()
    turtle.setheading(0)    
    turtle.goto(-side_length / 2.0, -r)
    turtle.pendown()
 
    exterior_turn = 360.0 / sides
 
    for _ in range(sides):
        draw(side_length, depth, inward=True)
        turtle.left(exterior_turn)
 
    screen.update()
    turtle.done()
 
def main():
    try:
        sides = int(input("Enter the number of sides: "))
        side_length = float(input("Enter the side length (pixels): "))
        depth = int(input("Enter the recursion depth: "))
    except ValueError:
        print("Please enter valid numeric values (integers for sides/depth, number for length).")
        return
 
    draw_pattern(sides, side_length, depth)
 
if __name__ == "__main__":
    main()

    