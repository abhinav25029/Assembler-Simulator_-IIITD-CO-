
def regval(val):

    if val == "zero": return 0
    elif val == "ra": return 1
    elif val == "sp": return 2
    elif val == "gp": return 3
    elif val == "tp": return 4
    elif val == "t0": return 5
    elif val == "t1": return 6
    elif val == "t2": return 7
    elif val == "s0" or val == "fp": return 8
    elif val == "s1": return 9
    elif val == "a0": return 10
    elif val == "a1": return 11
    elif val == "a2": return 12
    elif val == "a3": return 13
    elif val == "a4": return 14
    elif val == "a5": return 15
    elif val == "a6": return 16
    elif val == "a7": return 17
    elif val == "s2": return 18
    elif val == "s3": return 19
    elif val == "s4": return 20
    elif val == "s5": return 21
    elif val == "s6": return 22
    elif val == "s7": return 23
    elif val == "s8": return 24
    elif val == "s9": return 25
    elif val == "s10": return 26
    elif val == "s11": return 27
    elif val == "t3": return 28
    elif val == "t4": return 29
    elif val == "t5": return 30
    elif val == "t6": return 31



def r_type(ins,rs2,rs1,rd):

    x=""

    if ins=="add":
        x+="0000000"
        x+=format(regval(rs2),'05b')
        x+=format(regval(rs1),'05b')
        x+="000"
        x+=format(regval(rd),'05b')
        x+="0110011"

    elif ins=="sub":
        x+="0100000"
        x+=format(regval(rs2),'05b')
        x+=format(regval(rs1),'05b')
        x+="000"
        x+=format(regval(rd),'05b')
        x+="0110011"

    elif ins=="slt":
        x+="0000000"
        x+=format(regval(rs2),'05b')
        x+=format(regval(rs1),'05b')
        x+="010"
        x+=format(regval(rd),'05b')
        x+="0110011"

    elif ins=="sltu":
        x+="0000000"
        x+=format(regval(rs2),'05b')
        x+=format(regval(rs1),'05b')
        x+="011"
        x+=format(regval(rd),'05b')
        x+="0110011"

    print(x)


# ---------- BEQ ----------
def b_type(ins,imm_int,rs2,rs1):

    imm_bin = format(imm_int & 0x1FFF,'013b')

    x=(imm_bin[0]+imm_bin[2:8]+
       format(regval(rs2),'05b')+
       format(regval(rs1),'05b')+
       "000"+
       imm_bin[8:12]+
       imm_bin[1]+
       "1100011")

    print(x)



def bltu_type(imm_int,rs2,rs1):

    imm_bin=format(imm_int & 0x1FFF,'013b')

    x=(imm_bin[0]+imm_bin[2:8]+
       format(regval(rs2),'05b')+
       format(regval(rs1),'05b')+
       "110"+
       imm_bin[8:12]+
       imm_bin[1]+
       "1100011")

    print(x)



def bgeu_type(imm_int,rs2,rs1):

    imm_bin=format(imm_int & 0x1FFF,'013b')

    x=(imm_bin[0]+imm_bin[2:8]+
       format(regval(rs2),'05b')+
       format(regval(rs1),'05b')+
       "111"+
       imm_bin[8:12]+
       imm_bin[1]+
       "1100011")

    print(x)



def lui_type(rd,imm):

    x=format(int(imm),'020b')+format(regval(rd),'05b')+"0110111"
    print(x)


def auipc_type(rd,imm):

    x=format(int(imm),'020b')+format(regval(rd),'05b')+"0010111"
    print(x)


def jal_type(rd,imm):

    imm_bin=format(int(imm),'021b')

    x=(imm_bin[0]+imm_bin[10:20]+imm_bin[9]+imm_bin[1:9]+
       format(regval(rd),'05b')+"1101111")

    print(x)



def sw_type(rs2,mem):

    imm,rs1=mem.split("(")
    rs1=rs1.replace(")","")

    imm_bin=format(int(imm),'012b')

    x=(imm_bin[0:7]+
       format(regval(rs2),'05b')+
       format(regval(rs1),'05b')+
       "010"+
       imm_bin[7:12]+
       "0100011")

    print(x)


with open("riscv_program.txt") as f:
    x=f.readlines()

l=[]
j=0

for i in x:
    i=i.strip()
    i=i.replace(","," ")
    i=i+" "+str(j)
    j=j+1
    l.append(i)



for i in l:

    k=i.split(" ")

    # R TYPE
    if k[0] in ["add","sub","slt","sltu"]:
        r_type(k[0],k[3],k[2],k[1])

    # BEQ
    elif k[0]=="beq":

        if k[3].isdigit():
            imm=int(k[3])

        else:
            store=k[3]
            current_idx=k[4]

            for u in l:
                z=u.split(" ")
                if z[0]==store+":":
                    label_idx=z[5]

            imm=(int(label_idx)-int(current_idx))*4

        b_type(k[0],imm,k[2],k[1])

    # BLTU
    elif k[0]=="bltu":

        if k[3].isdigit():
            imm=int(k[3])

        else:
            store=k[3]
            current_idx=k[4]

            for u in l:
                z=u.split(" ")
                if z[0]==store+":":
                    label_idx=z[5]

            imm=(int(label_idx)-int(current_idx))*4

        bltu_type(imm,k[2],k[1])

    # BGEU
    elif k[0]=="bgeu":

        if k[3].isdigit():
            imm=int(k[3])

        else:
            store=k[3]
            current_idx=k[4]

            for u in l:
                z=u.split(" ")
                if z[0]==store+":":
                    label_idx=z[5]

            imm=(int(label_idx)-int(current_idx))*4

        bgeu_type(imm,k[2],k[1])

    # U TYPE
    elif k[0]=="lui":
        lui_type(k[1],k[2])

    elif k[0]=="auipc":
        auipc_type(k[1],k[2])

    # J TYPE
    elif k[0]=="jal":
        jal_type(k[1],k[2])

    # S TYPE
    elif k[0]=="sw":
        sw_type(k[1],k[2])

REGISTERS = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
    "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111",     
    "fp": "01000", "a0": "01010", "a1": "01011", "a2": "01100", 
    "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000", 
    "a7": "10001", "s0": "01000", "s1": "01001", "s2": "10010",
    "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110",
    "s7": "10111", "s8": "11000", "s9": "11001", "s10": "11010",
    "s11": "11011"
}

I_TYPE_OPCODES = {
    "lw":    {"opcode": "0000011", "funct3": "010"},
    "addi":  {"opcode": "0010011", "funct3": "000"},
    "sltiu": {"opcode": "0010011", "funct3": "011"},
    "jalr":  {"opcode": "1100111", "funct3": "000"}
}

B_TYPE_OPCODES = {
    "beq":   {"opcode": "1100011", "funct3": "000"},
    "bne":   {"opcode": "1100011", "funct3": "001"},
    "blt":   {"opcode": "1100011", "funct3": "100"},
    "bge":   {"opcode": "1100011", "funct3": "101"}
}

R_TYPE_FUNCT3 = {
    "sll": "001", 
    "xor": "100",
    "srl": "101", 
    "or":  "110", 
    "and": "111"
}

def int_to_bin(val, bits):
    if val < 0:
        val = 2**bits + val
    binary = bin(val)
    binary = binary.replace("0b", "")
    while len(binary) < bits:
        binary = "0" + binary
    return binary

def process_r_type(instruction_str):
    parts = instruction_str.split()
    opcode_str = parts[0]
    rd = parts[1]
    rs1 = parts[2]
    rs2 = parts[3]

    opcode = "0110011" 
    funct7 = "0000000" 
    funct3 = R_TYPE_FUNCT3[opcode_str] 
    rd_bin = REGISTERS[rd]
    rs1_bin = REGISTERS[rs1]
    rs2_bin = REGISTERS[rs2]
    
    return funct7 + rs2_bin + rs1_bin + funct3 + rd_bin + opcode

def process_i_type(instruction_str):
    parts = instruction_str.split()
    opcode_1 = parts[0]

    if opcode_1 == "lw":
        rd = parts[1]
        imm_str, rs1_d = parts[2].split("(")
        rs1 = rs1_d.replace(")", "")
    else:
        rd = parts[1]
        rs1 = parts[2]
        imm_str = parts[3]

    imm = int(imm_str)

    opcode = I_TYPE_OPCODES[opcode_1]["opcode"]
    funct3 = I_TYPE_OPCODES[opcode_1]["funct3"]
    rd_bin = REGISTERS[rd]
    rs1_bin = REGISTERS[rs1]
    imm_bin = int_to_bin(imm, 12)

    return imm_bin + rs1_bin + funct3 + rd_bin + opcode

def process_b_type(instruction, imm):
    parts = instruction.split() 
    opcode_2 = parts[0]
    rs1 = parts[1]
    rs2 = parts[2]
    imm = int(imm)

    opcode = B_TYPE_OPCODES[opcode_2]["opcode"]
    funct3 = B_TYPE_OPCODES[opcode_2]["funct3"]
    rs1_bin = REGISTERS[rs1]
    rs2_bin = REGISTERS[rs2]
    
    b_imm = int_to_bin(imm, 13) 

    imm_12 = b_imm[0]               
    imm_10_5 = b_imm[2:8]           
    imm_4_1 = b_imm[8:12]           
    imm_11 = b_imm[1]               
    
    part1 = imm_12 + imm_10_5
    part2 = imm_4_1 + imm_11

    return part1 + rs2_bin + rs1_bin + funct3 + part2 + opcode


print("RISC-V ASSEMBLER")

with open("riscv_program1.txt") as f:
    x = f.readlines()

instruction_list = []

idx = 0 
for i in x:
    if not i.strip(): 
        continue
    i = i.strip()
    i = i.replace(","," ")
    i = i+" "+str(idx)
    idx = idx+1
    instruction_list.append(i)

for instruction in instruction_list:
    decoded = instruction.split()
    
    if decoded[0].endswith(":"):
        clean_instruction = instruction.split(":", 1)[1].strip()
        decoded = clean_instruction.split()
    else:
        clean_instruction = instruction

    if not decoded:
        continue

    opcode = decoded[0]
    
    if opcode in ["lw", "addi", "sltiu", "jalr"]:
        binary_result = process_i_type(clean_instruction)
        print(binary_result)

    elif opcode in ["xor", "sll", "srl", "or", "and"]:
        binary_result = process_r_type(clean_instruction)
        print(binary_result)

    elif opcode in ["bge", "blt", "bne", "beq"]:
        store = decoded[3]
        current_idx = decoded[-1]

        if store.lstrip('-').isdigit():
            imm = int(store)
        else:
            for i in instruction_list:
                p = i.split()
                if p[0] == store + ":":
                    label_idx = p[-1] 
                    break 
            imm = (int(label_idx) - int(current_idx)) * 4
        
        bit_value = process_b_type(clean_instruction, imm)
        print(bit_value)





















    

















































































    























































