"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 226
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.op = {
            'HLT': 0b00000001,
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'MUL': 0b10100010,
        }

    def ram_read(self, mar):
        return self.ram[mar]   

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        #try- open file and loop through its contents
        try:
            with open(filename) as f:
                for i in f:
                    # split out comments
                    splited = i.split('#')
                    # remove white spaces
                    value = splited[0].strip()
                    #continue on empty value before comments
                    if value == '':
                        continue
                    #update ram at address with value
                    self.ram_write(address, int(value, 2))
                    #increment address
                    address += 1
        #handle exception
        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # print(self.ram)
        while self.running is True:
            ir = self.ram[self.pc]
            if ir == self.op['LDI']:
                reg_num = self.ram_read(self.pc + 1)
                reg_val = self.ram_read(self.pc +2)
                self.reg[reg_num] = reg_val
                self.pc += (ir >> 6) + 1
            elif ir == self.op['PRN']:
                reg_num = self.ram_read(self.pc + 1)
                print(self.reg[reg_num])
                self.pc += (ir >> 6) + 1
            elif ir == self.op['HLT']:
                self.running = False
                self.pc += (ir >> 6) + 1
            elif ir == self.op['MUL']:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu('MUL', reg_a, reg_b)
                self.pc += (ir >> 6) + 1
            else:
                print(f"Unknown instruction {ir}")
                sys.exit(1)
