import sys
import math

def distance(point1, point2): 
    return math.dist(point1, point2)

def closest_pair(points, nb_points):
    sorted_by_x = sorted(points, key=lambda point: point[0]) # n log n 
    sorted_by_y = sorted(points, key=lambda point: point[1]) # n log n

    return closest_pair_recursive(sorted_by_x, sorted_by_y)

def closest_pair_recursive(sorted_by_x, sorted_by_y):
    # Base case: if there are 2 or 3 point, use brute force.
    if len(sorted_by_x) <= 40:
        return closest_distance_brute_force(sorted_by_x)
    
    left_x, right_x, left_y, right_y = split_lists(sorted_by_x, sorted_by_y)
    smallest_left = closest_pair_recursive(left_x, left_y) # T(n/2)
    smallest_right = closest_pair_recursive(right_x, right_y) # T(n/2)
    smallest = min(smallest_left, smallest_right)

    # check the strip

    strip = [] # initialize the strip. 
    mid_x = left_x[-1][0] # get the division line. 

    for point in sorted_by_y:
        if abs(point[0] - mid_x) < smallest:
            strip.append(point)
    # check the smallest distance in the strip
    smallest_distance_in_strip = check_strip_distance(strip)

    return min(smallest, smallest_distance_in_strip)

def check_strip_distance(strip):
    min_distance = float('inf') # define the minimum distance
    strip_length = len(strip)
    for i in range(len(strip)):
        for j in range(i +1, min(i + 15, strip_length)): # check max 6 points in the strip on the other side, but 15 points are checked.
            dist = distance(strip[i], strip[j]) # this ensures the time complexity is O(n)
            if dist < min_distance:
                min_distance = dist
    return min_distance

def closest_distance_brute_force(points):
    min_distance = float('inf') # O (1) for only max 3 points (small number)
    n = len(points)  

    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_distance:
                min_distance = dist
    return min_distance 

def split_lists(sorted_by_x, sorted_by_y):
    left_x = sorted_by_x[:len(sorted_by_x) // 2] # O(1) - slicing 
    right_x = sorted_by_x[len(sorted_by_x) // 2:] # O(1) - slicing
    left_y = []
    right_y = []
    # get last point of left_x, to filter out points for left_y
    ref_point = left_x[-1][0]
    for point in sorted_by_y: # O(n) -- for creating left_y and right_y
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

    closest_distance = closest_pair(coordinates, number_of_points)
    print(f"{closest_distance:.6f}")

if __name__ == "__main__":
    main()