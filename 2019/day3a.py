# --- Day 3: Crossed Wires ---
#
# The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush
# back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.
#
# Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and
# extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of
# text (your puzzle input).
#
# The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the
# intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for
# this measurement. While the wires do technically cross right at the central port where they both start, this point
# does not count, nor does a wire count as crossing with itself.
#
# For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8,
# up 5, left 5, and finally down 3:
#
# ...........
# ...........
# ...........
# ....+----+.
# ....|....|.
# ....|....|.
# ....|....|.
# .........|.
# .o-------+.
# ...........
#
# Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:
#
# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
#
# These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance
# is 3 + 3 = 6.
#
# Here are a few more examples:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
#
# What is the Manhattan distance from the central port to the closest intersection?

tests = [
    ["R4,U8", "U4,R8", 8, 0],
    ["R8,U5,L5,D3", "U7,R6,D4,L4", 6, 0],
    ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159, 610],
    ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135, 410]
]

with open("day3.txt") as f:
    line1 = f.readline()
    line2 = f.readline()

tests.append([line1, line2, 0])

#print(tests)

test = tests[0]

def convert_line_vectors_to_points(line):
    pos = (0, 0)

    points = []
    points.append(pos)

    for vec in line:
        direc = vec[0]
        dist = int(vec[1:])

        px = pos[0]
        py = pos[1]

        if direc == 'L' or direc == 'D':
            dist = dist*-1

        if direc == 'U' or direc == 'D':
            py = py + dist
        else:
            px = px + dist

        p = (px, py)
        points.append(p)

        pos = p

    return points


def check_intersection(p1, p2, p3, p4):
    px = None
    py = None
    try:
        denom = ((p4[0] - p3[0])*(p1[1] - p2[1])) - ((p1[0] - p2[0])*(p4[1] - p3[1]))
        num_x = ((p3[1] - p4[1])*(p1[0] - p3[0]) + (p4[0] - p3[0])*(p1[1] - p3[1]))
        ta = num_x / denom
        tb = ((p1[1] - p2[1]) * (p1[0] - p3[0]) + (p2[0] - p1[0]) * (p1[1] - p3[1])) / denom

        if ta >= 0 and ta <= 1 and tb >= 0 and tb <= 1:
            px = int(p1[0] + ta*(p2[0] - p1[0]))
            py = int(p1[1] + ta * (p2[1] - p1[1]))
    except:
        pass
    if px == 0 and py == 0:
        return None, None

    return px, py

#tests = [tests[1]]
for test in tests:
    line1 = convert_line_vectors_to_points(test[0].split(","))
    line2 = convert_line_vectors_to_points(test[1].split(","))
    check_value = test[2]

    print("Test:")
    # print(line1)
    # print(line2)

    matches = []
    # n^2 search - could improve with https://www.hackerearth.com/practice/math/geometry/line-intersection-using-bentley-ottmann-algorithm/tutorial/
    for i in range(0, len(line1)-1):
        for j in range(0, len(line2)-1):
            p1 = line1[i]
            p2 = line1[i+1]
            p3 = line2[j]
            p4 = line2[j+1]

            # print(p1, p2, p3, p4)
            pint = check_intersection(p1, p2, p3, p4)
            # print("Match", pint)

            if pint[0] is not None and pint[1] is not None:
                distance = abs(pint[0]) + abs(pint[1])
                matches.append(distance)
                #print("Match", pint)


    tmp = [abs(m) for m in matches]
    closest_distance = min(tmp)

    print(matches)
    print("Closest:", check_value, closest_distance)
    if check_value == closest_distance:
        print("Test pass!")

#

def convert_line_vectors_to_populated_grid(grid, max_size, line, check):
    pos = (0, 0)

    mid_point = int(max_size / 2)

    for vec in line:
       # print(vec)
        direc = vec[0]
        dist = int(vec[1:])

        px = pos[0]
        py = pos[1]

        if direc == 'L' or direc == 'D':
            dist = dist*-1

        if direc == 'U' or direc == 'D':
            py = py + dist
        else:
            px = px + dist


        p = (px, py)
        #print("pos->p", pos, p)

        xstride = 1
        if pos[0] > p[0]:
            xstride = -1
        ystride = 1
        if pos[1] > p[1]:
            ystride = -1

        for x in range(pos[0], p[0]+xstride, xstride):
            for y in range(pos[1], p[1]+ystride, ystride):
                #print(x, y)
                xpos = x + mid_point
                ypos = ((max_size-1)-y)-mid_point
                #print(xpos, ypos)
                if(grid[ypos][xpos] == "1" and check == "2"):
                    grid[ypos][xpos] = "X"
                    print("cross:", x, y)
                else:
                    grid[ypos][xpos] = check

        pos = p

    grid[max_size-1-mid_point][mid_point] = 'o'
    return grid


test = tests[2]
max_size = 480
grid = [['.' for j in range(0, max_size)] for i in range(0, max_size)]

grid1 = convert_line_vectors_to_populated_grid(grid, max_size, test[0].split(","), "1")
grid2 = convert_line_vectors_to_populated_grid(grid, max_size, test[1].split(","), "2")
# for row in grid1:
#     print(row)

with open("shape.txt","w") as f:
    for row in grid1:
        f.write("".join(row))