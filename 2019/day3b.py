# --- Part Two ---
#
# It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.
#
# To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where
# the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value
# from the first time it visits that position when calculating the total value of a specific intersection.
#
# The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location,
# including the intersection being considered. Again consider the example from above:
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
# In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first
# wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.
#
# However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only
# 7+6+2 = 15, a total of 15+15 = 30 steps.
#
# Here are the best steps for the extra examples from above:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
#
# What is the fewest combined steps the wires must take to reach an intersection?


tests = [
    ["R4,U8", "U4,R8", 8, 16],
    ["R8,U5,L5,D3", "U7,R6,D4,L4", 6, 0],
    ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159, 610],
    ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135, 410]
]

with open("day3.txt") as f:
    line1 = f.readline()
    line2 = f.readline()

tests.append([line1, line2, 0, 0])

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

tests = [tests[4]]
for test in tests:
    line1 = convert_line_vectors_to_points(test[0].split(","))
    line2 = convert_line_vectors_to_points(test[1].split(","))
    check_value = test[3]


    print("Test:")
    # print(line1)
    # print(line2)
    dist_a = 0
    dist_b = 0

    pairs = {}
    matches = []
    lengths = []
    for i in range(0, len(line1)-1):
        p1 = line1[i]
        p2 = line1[i + 1]

        dist_a = dist_a + abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
        dist_b = 0

        for j in range(0, len(line2)-1):

            p3 = line2[j]
            p4 = line2[j+1]


            dist_b = dist_b + abs(p4[0] - p3[0]) + abs(p4[1] - p3[1])
            print(p1, p2, p3, p4, dist_a, dist_b)
            pint = check_intersection(p1, p2, p3, p4)


            # print("Match", pint, match_dist_a)

            if pint[0] is not None and pint[1] is not None:
                distance = abs(pint[0]) + abs(pint[1])

                match_dist_a = dist_a - (abs((p2[0] - pint[0])) + abs((p2[1] - pint[1])))
                match_dist_b = dist_b - (abs((p4[0] - pint[0])) + abs((p4[1] - pint[1])))

                matches.append(distance)
                lengths.append(match_dist_a + match_dist_b)

                if (match_dist_a + match_dist_b) not in pairs:
                    pairs[match_dist_a + match_dist_b] = []
                pairs[match_dist_a + match_dist_b].append(distance)
                print("Match", pint, match_dist_a, match_dist_b)


    tmp = [abs(m) for m in matches]
    closest_distance = min(tmp)

    print("Mat:", matches)
    print("Len:", lengths)
    min_length = min(lengths)

    print("pairs:", pairs)
    print("min len", min_length, "dist is", pairs[min_length])
    print("Closest:", check_value, closest_distance)
    if check_value == closest_distance:
        print("Test pass!")
