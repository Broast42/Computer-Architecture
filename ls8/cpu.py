"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.sp = 7
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[self.sp] = 244
        self.running = True
        self.op = {
            0b00000001: 'HLT',
            0b10000010: "LDI",
            0b01000111: 'PRN',
            0b10100010: 'MUL',
            0b01000101: 'PUSH',
            0b01000110: 'POP',
        }
        #op table
        self.optable = {}
        self.optable[0b00000001] = self.handel_hlt
        self.optable[0b10000010] = self.handel_ldi
        self.optable[0b01000111] = self.handel_prn
        self.optable[0b01000101] = self.handel_push
        self.optable[0b01000110] = self.handel_pop

    #ram 
    def ram_read(self, mar):
        return self.ram[mar]   

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    
    #op handelers
    def handel_hlt(self, op, a, b):
        self.running = False
        self.pc += (op >> 6) + 1
    
    def handel_ldi(self, op, a, b):
        self.reg[a] = b
        self.pc += (op >> 6) + 1
    
    def handel_prn(self, op, a, b):
        print(self.reg[a])
        self.pc += (op >> 6) + 1
    
    def handel_push(self, op, a, b):
        #grab value in register a
        value = self.reg[a]
        #decrement sp register
        self.reg[self.sp] -= 1
        #write value to memory at sp location
        self.ram_write(self.reg[self.sp], value)
        #increment pc accordingly
        self.pc += (op >> 6) + 1
    
    def handel_pop(self, op, a, b):
        #write value in memory at sp to given register
        value = self.ram_read(self.reg[self.sp])
        self.reg[a] = value
        #increment sp and pc accordingly
        self.reg[self.sp] += 1
        self.pc += (op >> 6) + 1
        


    #load function
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

    # alu handle function
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
            #grab the next instruction plus the next two
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc +2)

            #check if this is an alu instruction
            if (ir >> 5) & 0b00000001 == 1:
                self.alu(self.op[ir], reg_a, reg_b)
                self.pc += (ir >> 6) + 1
            else:
                #run function from optable using op as key
                #pass in reg a and b regardless of need
                self.optable[ir](ir, reg_a, reg_b)
            
            ### Original if else code ###
            # ir = self.ram_read(self.pc)
            # if ir == self.op['LDI']:
            #     reg_num = self.ram_read(self.pc + 1)
            #     reg_val = self.ram_read(self.pc +2)
            #     self.reg[reg_num] = reg_val
            #     self.pc += (ir >> 6) + 1
            # elif ir == self.op['PRN']:
            #     reg_num = self.ram_read(self.pc + 1)
            #     print(self.reg[reg_num])
            #     self.pc += (ir >> 6) + 1
            # elif ir == self.op['HLT']:
            #     self.running = False
            #     self.pc += (ir >> 6) + 1
            # elif ir == self.op['MUL']:
            #     reg_a = self.ram_read(self.pc + 1)
            #     reg_b = self.ram_read(self.pc + 2)
            #     self.alu('MUL', reg_a, reg_b)
            #     self.pc += (ir >> 6) + 1
            # else:
            #     print(f"Unknown instruction {ir}")
            #     sys.exit(1)
