import math
import argparse


def calculate_distance(x, y):
    return math.sqrt(x**2 + y**2)


def main():
    parser = argparse.ArgumentParser(description='Calculate distance using Pythagorean theorem')
    parser.add_argument('x', type=float, help='x-coordinate')
    parser.add_argument('y', type=float, help='y-coordinate')
    args = parser.parse_args()

    distance = calculate_distance(args.x, args.y)
    print(f"Distance: {distance}")


if __name__ == "__main__":
    main()