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

class OrbitTree(object):

    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, node):
        if not isinstance(node, OrbitTree):
            node = OrbitTree(node)
        node.parent = self
        self.children.append(node)
        return node

    def is_child(self, data):
        for child in self.children:
            if child.data == data:
                return True
        return False

    def find(self, data):
        if self.data == data:
            return self

        for child in self.children:
            chk = child.find(data)
            if chk:
                return chk

        return None

    def depth(self):
        count = 0
        node = self
        while node is not None:
            count = count + 1
            node = node.parent

        return count

    def indirect_orbit_count(self):
        total = 0

        depth = self.depth()
        #print(depth)

        if(depth >= 1):
            total = total + depth - 1


        for child in self.children:
            total = total + child.indirect_orbit_count()

        return total

    def __repr__(self):
        parent_name = ""
        if self.parent:
            parent_name = self.parent.data

        repr = "<OrbitTree>" + self.data + "(" + str(self.depth()) + "|" + str(parent_name) + ")"
        for child in self.children:

            repr = repr + "\n" + " " + child.__repr__()

        return str(repr)

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
first_orbit = orbit_inputs[0]
orbits = OrbitTree(first_orbit[0])

for orbit_input in orbit_inputs:
    print(orbit_input)
    node = orbits.find(orbit_input[0])
    node.add_child(orbit_input[1])

orbit_count = orbits.indirect_orbit_count()
print(orbit_count)