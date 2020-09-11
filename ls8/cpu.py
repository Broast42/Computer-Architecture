"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.sp = 7
        self.fl = 0b00000000
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[self.sp] = 244
        self.running = True
        self.op = {
            0b00000000: 'NOP',
            0b00000001: 'HLT',
            0b10000010: "LDI",
            0b01000111: 'PRN',
            0b01000101: 'PUSH',
            0b01000110: 'POP',
            0b01010000: 'CALL',
            0b00010001: 'RET',
            0b01010101: 'JEQ',
            0b01011010: 'JGE',
            0b01010111: 'JGT',
            0b01011001: 'JLE',
            0b01011000: 'JLT',
            0b01010100: 'JMP',
            0b01010110: 'JNE',
            0b10000011: 'LD',
            0b01001000: 'PRA',
            0b10000100: 'ST',
            #alu instructions
            0b10101000: 'ADD',
            0b10100000: 'AND',
            0b10100111: 'CMP',
            0b01100110: 'DEC',
            0b10100011: 'DIV',
            0b01100101: 'INC',
            0b10100100: 'MOD',
            0b10100010: 'MUL',
            0b01101001: 'NOT',
            0b10101010: 'OR',
            0b10101100: 'SHL',
            0b10101101: 'SHR',
            0b10100001: 'SUB',
            0b10101011: 'XOR',
            
        }
        #op table
        self.optable = {}
        self.optable[0b00000000] = self.handel_nop
        self.optable[0b00000001] = self.handel_hlt
        self.optable[0b10000010] = self.handel_ldi
        self.optable[0b01000111] = self.handel_prn
        self.optable[0b01000101] = self.handel_push
        self.optable[0b01000110] = self.handel_pop
        self.optable[0b01010000] = self.handel_call
        self.optable[0b00010001] = self.handel_ret
        self.optable[0b01010101] = self.handel_jeq
        self.optable[0b01011010] = self.handel_jge
        self.optable[0b01010111] = self.handel_jgt
        self.optable[0b01011001] = self.handel_jle
        self.optable[0b01011000] = self.handel_jlt
        self.optable[0b01010100] = self.handel_jmp
        self.optable[0b01010110] = self.handel_jne
        self.optable[0b10000011] = self.handel_ld
        self.optable[0b01001000] = self.handel_pra
        self.optable[0b10000100] = self.handel_st


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
        
    def handel_call(self, op, a ,b):
        self.reg[self.sp] -=1
        self.ram_write(self.reg[self.sp], self.pc + 2)
        self.pc = self.reg[a]    

    def handel_ret(self, op, a, b):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
    
    def handel_jeq(self, op, a, b):
        if self.fl == 0b00000001:
            self.pc = self.reg[a]
        else:
            self.pc += (op >> 6) + 1    

    def handel_jge(self, op, a, b):
        if self.fl == 0b00000001 or self.fl == 0b00000010:
            self.pc = self.reg[a]
        else:
            self.pc += (op >> 6) + 1

    def handel_jgt(self, op, a, b):
        if self.fl == 0b00000010:
            self.pc = self.reg[a]
        else:
            self.pc += (op >> 6) + 1 

    def handel_jle(self, op, a, b):
        if self.fl == 0b00000001 or self.fl == 0b00000100:
            self.pc = self.reg[a]
        else:
            self.pc += (op >> 6) + 1

    def handel_jlt(self, op, a, b):
        if self.fl == 0b00000100:
            self.pc = self.reg[a]
        else:
            self.pc += (op >> 6) + 1 

    def handel_jmp(self, op, a, b):
        self.pc = self.reg[a] 
    
    def handel_jne(self, op, a, b):
        if self.fl != 0b00000001:
            self.pc = self.reg[a]
        else:
            self.pc += (op >> 6) + 1
    
    def handel_ld(self, op, a, b):
        
        self.reg[a] = self.ram_read(self.reg[b])
        # self.reg[self.sp] += 1
        self.pc += (op >> 6) + 1
    
    def handel_nop(self, op, a, b):
        self.pc += (op >> 6) + 1
    
    def handel_pra(self, op, a, b):
        print(chr(self.reg[a]))
        #print(self.reg[a])
        self.pc += (op >> 6) + 1
    
    def handel_st(self, op, a, b):
        self.ram_write(self.reg[a],self.reg[b])
        

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
        elif op == "AND":
            value = self.reg[reg_a] & self.reg[reg_b]
            self.reg[reg_a] = value
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "DIV":
            if self.reg[reg_b] == 0:
                print('Error: cannot divide by zero')
                self.running = False
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                print('Error: cannot divide by zero')
                self.running = False
            else:
                self.reg[reg_a] %= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "NOT":
            value = ~self.reg[reg_a]
            self.reg[reg_a] = value
        elif op == "OR":
            value = self.reg[reg_a] | self.reg[reg_b]
            self.reg[reg_a] = value
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << reg_b
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> reg_b
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "XOR":
            value = self.reg[reg_a] ^ self.reg[reg_b]
            self.reg[reg_a] = value
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
            
            #check if instruction is not in op if not print error and exit
            if ir not in self.op:
                print(f"Unknown instruction {ir}")
                sys.exit(1)
            
            # trace for debugging un-comment to test    
            # self.trace()
            
            #check if this is an alu instruction
            if (ir >> 5) & 0b00000001 == 1:
                self.alu(self.op[ir], reg_a, reg_b)
                self.pc += (ir >> 6) + 1
            else:
                #run function from optable using op as key
                #pass in reg a and b regardless of need
                self.optable[ir](ir, reg_a, reg_b)
            
            