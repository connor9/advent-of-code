# --- Day 6: Universal Orbit Map ---
#
# You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves
# transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example,
# you and Santa. You download a map of the local orbits (your puzzle input).
#
# Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object.
# An orbit looks roughly like this:
#
#                   \
#                    \
#                     |
#                     |
# AAA--> o            o <--BBB
#                     |
#                     |
#                    /
#                   /
#
# In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is
# only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit
# around AAA".
#
# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To
# verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like
# the one shown above) and indirect orbits.
#
# Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A
# orbits B, B orbits C, and C orbits D, then A indirectly orbits D.
#
# For example, suppose you have the following map:
#
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
#
# Visually, the above map of orbits looks like this:
#
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I
#
# In this visual representation, when two objects are connected by a line, the one on the right directly orbits the
# one on the left.
#
# Here, we can count the total number of orbits as follows:
#
#     D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
#     L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
#     COM orbits nothing.
#
# The total number of direct and indirect orbits in this example is 42.
#
# What is the total number of direct and indirect orbits in your map data?
# --- Part Two ---
#
# Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).
#
# You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets
# you move from any object to an object orbiting or orbited by that object.
#
# For example, suppose you have the following map:
#
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN
#
# Visually, the above map of orbits looks like this:
#
#                           YOU
#                          /
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#
# In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4
# orbital transfers are required:
#
#     K to J
#     J to E
#     E to D
#     D to I
#
# Afterward, the map of orbits looks like this:
#
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#                  \
#                   YOU
#
# What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN
# is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)
#

class OrbitHash(object):

    def __init__(self):
        self.orbits = {}

    def add_orbit(self, a, b):
        if a not in self.orbits:
            self.orbits[a] = []
        if b not in self.orbits:
            self.orbits[b] = []

        self.orbits[a].append(b)

    def parent_map(self, key, parent_map_data):
        for a, b in self.orbits.items():
            if key in b:
                tmp_map = parent_map_data
                tmp_map.append(a)
                return self.parent_map(a, tmp_map)

        return parent_map_data

    def depth(self, key, depth=0):
        for a, b in self.orbits.items():
            if key in b:
                return self.depth(a, depth+1)
        return depth

    def indirect_orbits_count(self):
        total = 0

        for k in self.orbits:
            depth = self.depth(k)
            total = total + depth

        return total

test = ("""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""", 42)

print("Test:", test)

def parse_input(data):
    parsed_input = [i.split(")") for i in data.split("\n")]
    return parsed_input

with open("day6.txt") as f:
    real_data = f.read()

#real_data = test[0]

orbit_inputs = parse_input(real_data)

# Add root orbit
orbits = OrbitHash()
for orbit_input in orbit_inputs:
    orbits.add_orbit(orbit_input[0], orbit_input[1])

# Part 1
#count = orbits.indirect_orbits_count()
#print(count)

# Part 2

you_tree = orbits.parent_map('YOU', [])
print("YOU:", you_tree)
san_tree = orbits.parent_map('SAN', [])
print("SAN:", san_tree)

# At this point the two lists above represent all the orbits that the specified body follows.
# If we reverse these orbits we can simply walk through the lists until the orbits diverge.
# At that point we know the unique orbits that we need to transfer down and the up

you_tree.reverse()
san_tree.reverse()

merge_index = 0

while True:
    if you_tree[merge_index] != san_tree[merge_index]:
        break
    merge_index = merge_index + 1

transfers = (len(you_tree) - merge_index) + (len(san_tree) - merge_index)
print(transfers)

