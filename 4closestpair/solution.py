import sys 

coordinates = []

number_of_points = int (sys.stdin.readline().strip())

for i in range (number_of_points):
    x, y = map (int, sys.stdin.readline().strip().split())
    coordinates.append((x, y))

closest_distance = float('inf')

for i in range(len(coordinates)):
    for j in range (i + 1, len (coordinates)):
        distance = ((coordinates[i][0] - coordinates[j][0]) ** 2 + (coordinates[i][1] - coordinates[j][1]) ** 2) ** 0.5
        if distance < closest_distance:
            closest_distance = distance

print(f"{closest_distance:.6f}")
