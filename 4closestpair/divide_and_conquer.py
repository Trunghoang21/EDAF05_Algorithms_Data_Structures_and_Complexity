import sys
import math

def distance(point1, point2): 
    return math.dist(point1, point2)

def closest_pair(points, nb_points):
    sorted_by_x = sorted(points, key=lambda point: point[0])
    sorted_by_y = sorted(points, key=lambda point: point[1])

    return closest_pair_recursive(sorted_by_x, sorted_by_y)

def closest_pair_recursive(sorted_by_x, sorted_by_y):
    # Base case: if there are 2 or 3 point, use brute force.
    if len(sorted_by_x) <= 3:
        return closest_distance_brute_force(sorted_by_x)
    
    left_x, right_x, left_y, right_y = split_lists(sorted_by_x, sorted_by_y)
    smallest_left = closest_pair_recursive(left_x, left_y)
    smallest_right = closest_pair_recursive(right_x, right_y)
    smallest = min(smallest_left, smallest_right)

    # check the strip

    # to do, check how to create the strip contains points of the left side and the rigth side
    # check how to create the split lines maybe
    return smallest

def closest_distance_brute_force(points):
    min_distance = float('inf')
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_distance:
                min_distance = dist
    return min_distance 

def split_lists(sorted_by_x, sorted_by_y):
    left_x = sorted_by_x[:len(sorted_by_x) // 2]
    right_x = sorted_by_x[len(sorted_by_x) // 2:]
    left_y = []
    right_y = []
    # get last point of left_x, to filter out points for left_y
    ref_point = left_x[-1][0]
    for point in sorted_by_y:
        if point[0] <= ref_point:
            left_y.append(point)
        else:
            right_y.append(point) 
    return left_x, right_x, left_y, right_y

def main():
    coordinates = []
    number_of_points = int(sys.stdin.readline().strip())

    for _ in range(number_of_points):
        x, y = map(int, sys.stdin.readline().strip().split())
        coordinates.append((x, y))

    #print(f"The coordinates are {coordinates}")
    #print(f"Number of points: {number_of_points}")

    closest_distance = closest_pair(coordinates, number_of_points)
    print(f"{closest_distance:.6f}")

if __name__ == "__main__":
    main()