# --- Part Two ---
#
# The air conditioner comes online! Its cold air feels good for a while, but then the TEST alarms start to go off.
# Since the air conditioner can't vent its heat anywhere but back into the spacecraft, it's actually making the air
# inside the ship warmer.
#
# Instead, you'll need to use the TEST to extend the thermal radiators. Fortunately, the diagnostic program (your
# puzzle input) is already equipped for this. Unfortunately, your Intcode computer is not.
#
# Your computer is only missing a few opcodes:
#
#     Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#     Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#     Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#     Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#
# Like all instructions, these instructions need to support parameter modes as described above.
#
# Normally, after an instruction is finished, the instruction pointer increases by the number of values in that
# instruction. However, if the instruction modifies the instruction pointer, that value is used and the instruction
# pointer is not automatically increased.
#
# For example, here are several programs that take one input, compare it to the value 8, and then produce one output:
#
#     3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
#     3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
#     3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
#     3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
#
# Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was non-zero:
#
#     3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
#     3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)
#
# Here's a larger example:
#
# 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
# 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
# 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
#
# The above example program uses an input instruction to ask for a single number. The program will then output 999 if
# the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is
# greater than 8.
#
# This time, when the TEST diagnostic program runs its input instruction to get the ID of the system to test,
# provide it 5, the ID for the ship's thermal radiator controller. This diagnostic test suite only outputs one
# number, the diagnostic code.
#
# What is the diagnostic code for system ID 5?
#

import queue

OP_ADD = 1
OP_MULT = 2
OP_READ = 3
OP_READ_AND_HALT = 33
OP_PRINT = 4
OP_JMP_IF_TRUE = 5
OP_JMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8
OP_ADJ_REL = 9
OP_HALT = 99

PARAM_MODE_POSITION = 0
PARAM_MODE_IMMEDIATE = 1
PARAM_MODE_RELATIVE = 2

def parse_program(input_string):
    instructions_data = [int(i.replace("\n", "").strip()) for i in input_string.split(",")]
    return instructions_data

def read_program(filename):
    # Parse input file as a list of integers
    with open(filename) as f:
        instructions_data = parse_program(f.read())

    return instructions_data


class IntcodeComputer:
    def __init__(self, inputs=None):
        self.instruction_counter = 0
        self.memory = []

        self.reset()

        self.inputs = queue.Queue()
        self.outputs = []

        self.halted = False
        self.paused = False

        self.relative_base = 0
        self.memory_expand_size = 16000

        if inputs is not None:
            self.inputs = list(inputs)

    def reset(self):
        self.instruction_counter = 0
        self.memory = []

    def load_memory(self, memory):
        self.memory = list(memory)
        # Load extra memory
        for i in range(0, self.memory_expand_size):
            self.memory.append(0)

    def add_input(self, input):
        # print("In:", input)
        self.inputs.put(input)

    def get_output(self):
        return self.outputs.pop()

    def step(self):
        instruction = self.memory[self.instruction_counter]

        parameter_modes = [PARAM_MODE_POSITION, PARAM_MODE_POSITION, PARAM_MODE_POSITION]

        opcode = None
        if instruction < 100:
            opcode = instruction
        else:
            opcode = instruction % 100
            parameter_modes[0] = ((instruction - opcode) // 100) % 10
            parameter_modes[1] = (((instruction - opcode) // 100) - parameter_modes[0]) // 10

        #print("opcode", opcode, "param_modes", parameter_modes)
        # print("Step:", opcode, self.instruction_counter, self.memory)

        parameter_count = 3

        if opcode == OP_ADD or opcode == OP_MULT or opcode == OP_EQ or opcode == OP_LT or opcode == OP_JMP_IF_FALSE or opcode == OP_JMP_IF_TRUE:

            mem_a = self.memory[self.instruction_counter + 1]

            if parameter_modes[0] == PARAM_MODE_IMMEDIATE:
                val_a = mem_a
            elif parameter_modes[0] == PARAM_MODE_RELATIVE:
                val_a = self.memory[mem_a + self.relative_base]
            else:
                val_a = self.memory[mem_a]

            mem_b = self.memory[self.instruction_counter + 2]
            if parameter_modes[1] == PARAM_MODE_IMMEDIATE:
                val_b = mem_b
            elif parameter_modes[1] == PARAM_MODE_RELATIVE:
                val_b = self.memory[mem_b + self.relative_base]
            else:
                val_b = self.memory[mem_b]



            if opcode == OP_ADD:
                mem_c = self.memory[self.instruction_counter + 3]
                self.memory[mem_c] = val_a + val_b
            elif opcode == OP_MULT:
                mem_c = self.memory[self.instruction_counter + 3]
                self.memory[mem_c] = val_a * val_b
            elif opcode == OP_EQ:
                mem_c = self.memory[self.instruction_counter + 3]
                # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                if val_a == val_b:
                    self.memory[mem_c] = 1
                else:
                    self.memory[mem_c] = 0
            elif opcode == OP_LT:
                mem_c = self.memory[self.instruction_counter + 3]
                # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                if val_a < val_b:
                    self.memory[mem_c] = 1
                else:
                    self.memory[mem_c] = 0
            elif opcode == OP_JMP_IF_TRUE:
                parameter_count = 2
                if val_a != 0:
                    self.instruction_counter = val_b
                    return opcode
            elif opcode == OP_JMP_IF_FALSE:
                parameter_count = 2
                if val_a == 0:
                    self.instruction_counter = val_b
                    return opcode

        elif opcode == OP_ADJ_REL:
            parameter_count = 1

            adj_value = self.memory[self.instruction_counter + 1]
            self.relative_base = self.relative_base + adj_value
            print("rel:", adj_value, self.relative_base)
        elif opcode == OP_READ:
            parameter_count = 1

            # if self.inputs is None:
            #     value = int(input())
            # else:
            #     value = self.inputs[self.input_counter]
            #     self.input_counter = self.input_counter + 1
            #     print("Fake in:", value)

            if self.inputs.qsize() == 0:
                self.paused = True
                return OP_READ_AND_HALT

            value = self.inputs.get()

            mem_add = self.memory[self.instruction_counter + 1]

            if parameter_modes[0] == PARAM_MODE_RELATIVE:
                reg = mem_add + self.relative_base
            else:
                reg = mem_add

            self.memory[reg] = value

        elif opcode == OP_PRINT:
            parameter_count = 1

            reg = self.memory[self.instruction_counter + 1]
            if parameter_modes[0] == PARAM_MODE_IMMEDIATE:
                value = reg
            elif parameter_modes[0] == PARAM_MODE_RELATIVE:
                value = self.memory[reg + self.relative_base]
            else:
                value = self.memory[reg]

            self.outputs.append(value)
            print("Output:", value, "IC:", self.instruction_counter)

        elif opcode == OP_HALT:
            self.halted = True
            return opcode
        else:
            print(opcode, self.instruction_counter)
            raise Exception("Invalid Opcode")

        self.instruction_counter = self.instruction_counter + parameter_count + 1

        return opcode

    def run(self):
        while True:
            opcode = self.step()
            # print("Step:", opcode, self.instruction_counter, self.memory)
            if opcode == OP_HALT or opcode == OP_READ_AND_HALT:
                break
