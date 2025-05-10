# Python program to find minimum distance between points
import sys
import math

# Function to compute Euclidean distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Function to find the minimum distance in the strip
def stripClosest(strip, d):
    min_dist = d

    # Sort points in the strip by their y-coordinate
    strip.sort(key=lambda point: point[1])

    # Compare each point in the strip
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j][1] - strip[i][1]) < min_dist:
                min_dist = min(min_dist, distance(strip[i], strip[j]))
            else:
                break

    return min_dist

# Divide and conquer function to find the minimum distance
def minDistUtil(points, left, right):
    
    # Base case brute force for 2 or fewer points
    if right - left <= 2:
        min_dist = float('inf')
        for i in range(left, right):
            for j in range(i + 1, right):
                min_dist = min(min_dist, distance(points[i], points[j]))
        return min_dist

    # Find the midpoint
    mid = (left + right) // 2
    mid_x = points[mid][0]

    # Recursively find the minimum distances
    # in the left and right halves
    dl = minDistUtil(points, left, mid)
    dr = minDistUtil(points, mid, right)

    d = min(dl, dr)

    # Build the strip of points within distance d from the midl
    strip = []
    for i in range(left, right):
        if abs(points[i][0] - mid_x) < d:
            strip.append(points[i])

    # Find the minimum distance in the strip
    stripDist = stripClosest(strip, d)

    return min(d, stripDist)

# Function to find the closest pair of points
def minDistance(points):
    n = len(points)

    # Sort points by x-coordinate
    points.sort(key=lambda point: point[0])

    return minDistUtil(points, 0, n)

if __name__ == '__main__':
    
    coordinates = []

    number_of_points = int (sys.stdin.readline().strip())

    for i in range (number_of_points):
        x, y = map (int, sys.stdin.readline().strip().split())
        coordinates.append((x, y))

    

    res = minDistance(coordinates)

    # Output the result with 6 decimal places
    print(f"{res:.6f}")