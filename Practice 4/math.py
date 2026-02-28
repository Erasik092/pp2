import math

def degree_to_radian():
    """Convert degree to radian"""
    degree = float(input("Input degree: "))
    radian = math.radians(degree)
    print(f"Output radian: {radian}\n")


def trapezoid_area():
    """Calculate the area of a trapezoid"""
    height = float(input("Height: "))
    base1 = float(input("Base, first value: "))
    base2 = float(input("Base, second value: "))
    
    area = (base1 + base2) * height / 2
    print(f"Expected Output: {area}\n")


def regular_polygon_area():
    """Calculate the area of a regular polygon"""
    sides = int(input("Input number of sides: "))
    side_length = float(input("Input the length of a side: "))
    
    area = (sides * side_length ** 2) / (4 * math.tan(math.pi / sides))
    print(f"The area of the polygon is: {area}\n")


def parallelogram_area():
    """Calculate the area of a parallelogram"""
    base = float(input("Length of base: "))
    height = float(input("Height of parallelogram: "))
    
    area = base * height
    print(f"Expected Output: {area}\n")


if __name__ == "__main__":
    print("=== Math Calculations ===\n")
    
    print("Task 1: Convert degree to radian")
    degree = 15
    radian = math.radians(degree)
    print(f"Input degree: {degree}")
    print(f"Output radian: {radian:.6f}\n")
    
    print("Task 2: Calculate the area of a trapezoid")
    height = 5
    base1 = 5
    base2 = 6
    area = (base1 + base2) * height / 2
    print(f"Height: {height}")
    print(f"Base, first value: {base1}")
    print(f"Base, second value: {base2}")
    print(f"Expected Output: {area}\n")
    
    print("Task 3: Calculate the area of a regular polygon")
    sides = 4
    side_length = 25
    area = (sides * side_length ** 2) / (4 * math.tan(math.pi / sides))
    print(f"Input number of sides: {sides}")
    print(f"Input the length of a side: {side_length}")
    print(f"The area of the polygon is: {area}\n")
    
    print("Task 4: Calculate the area of a parallelogram")
    base = 5
    height = 6
    area = base * height
    print(f"Length of base: {base}")
    print(f"Height of parallelogram: {height}")
    print(f"Expected Output: {area}\n")
    
    # Uncomment below to run interactive input versions
    # degree_to_radian()
    # trapezoid_area()
    # regular_polygon_area()
    # parallelogram_area()