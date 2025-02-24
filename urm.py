class URM:
    def __init__(self, program):
        self.program = program
        self.registers = {}  
        self.pc = 0          # Program Counter (0-based)
        
        self.instructions = {
            "Z": self.instr_Z,
            "S": self.instr_S,
            "T": self.instr_T,
            "J": self.instr_J
        }
        
    def get_register(self, n):
        return self.registers.get(n, 0)

    def set_register(self, n, value):
        self.registers[n] = value 

    def instr_Z(self, n):
        self.set_register(n, 0)
        self.pc += 1

    def instr_S(self, n):
        self.set_register(n, self.get_register(n) + 1)
        self.pc += 1

    def instr_T(self, m, n):
        self.set_register(n, self.get_register(m))
        self.pc += 1

    def instr_J(self, m, n, q):
        if self.get_register(m) == self.get_register(n):
            self.pc = q - 1
        else:
            self.pc += 1

    def execute(self):
        while self.pc < len(self.program):
            instr = self.program[self.pc]
            op = instr[0]
            operands = instr[1:]
            # Debug
            print(f"Instruction {self.pc + 1}: {instr} | Registers: {self.registers}")
            if op in self.instructions:
                self.instructions[op](*operands)
            else:
                raise ValueError(f"Unrecognized instruction: {op}")

        print("Final state of registers:")
        print(self.registers)

def main():
    program = [
        ("J", 1, 2, 6),
        ("S", 2),
        ("S", 3),
        ("J", 1, 2, 6),
        ("J", 1, 1, 2),
        ("T", 3, 1)
    ]
    
    machine = URM(program)
    
    initial_registers = {1: 9, 2: 7, 3: 0, 4: 0, 5: 0}
    for reg, value in initial_registers.items():
        machine.set_register(reg, value)
    
    print("Initial configuration:", machine.registers)
    machine.execute()

if __name__ == "__main__":
    main()