import math

class URM:
    def __init__(self, program):
        self.program = program
        self.registers = {}  
        self.pc = 0  # Program Counter (0-based)
        
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
            print(f"Instruction {self.pc + 1}: {instr} | Registers before: {self.registers}")
            if op in self.instructions:
                self.instructions[op](*operands)
            else:
                raise ValueError(f"Unrecognized instruction: {op}")
            print(f"Registers after: {self.registers}\n")
        print("Final state of registers:", self.registers)

    def godel_number(self):
        def beta(instr):
            if instr[0] == "Z":
                return [4 * instr[1] - 1]
            elif instr[0] == "S":
                return [4 * instr[1]]
            elif instr[0] == "T":
                return [4 * instr[1] + 1, instr[2]]
            elif instr[0] == "J":
                return [4 * instr[1] + 2, instr[2], instr[3]]
            raise ValueError(f"Unrecognized instruction for encoding: {instr}")

        def prime(n):
            """ Find the n-th prime number """
            primes = [2]
            num = 3
            while len(primes) < n:
                if all(num % p != 0 for p in primes):
                    primes.append(num)
                num += 2
            return primes[-1]
        
        beta_values = []
        for instr in self.program:
            beta_values.extend(beta(instr))
        
        # Kleene's τ function: multiplication of primes raised to the beta values
        tau_value = 1
        for i, b in enumerate(beta_values):
            tau_value *= prime(i + 1) ** b  # p_(i+1)^beta_i
        
        return tau_value

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
    print("Gödel number of the program:", machine.godel_number())

if __name__ == "__main__":
    main()