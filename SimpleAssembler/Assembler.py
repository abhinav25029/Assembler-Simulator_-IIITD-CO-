#CO- project assembler
import sys

registers = {
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7, "s0": 8, "fp": 8,
    "s1": 9, "a0": 10, "a1": 11, "a2": 12, "a3": 13,
    "a4": 14, "a5": 15, "a6": 16, "a7": 17,
    "s2": 18, "s3": 19, "s4": 20, "s5": 21,
    "s6": 22, "s7": 23, "s8": 24, "s9": 25,
    "s10": 26, "s11": 27,
    "t3": 28, "t4": 29, "t5": 30, "t6": 31
}

#convert to binary fnc
def convert_bin(val, bits):     
    b = bin(val)[2:]     
    while len(b) <bits:     
        b = "0"+b
    return b

# U type instruction format:
#  imm[31:12]       rd         opcode
#      20            5           7
def U1_lui(parts):
    opcode = "0110111"
    r_des = parts[1]
    
    try:
        imm_val = int(parts[2])
    except:
        print("Invalid imm val")
        sys.exit()
    
    if r_des not in registers:
        print("Invalid register",r_des)
        sys.exit()
        
    reg_num = registers[r_des]
    imm_bin = convert_bin(imm_val,20)
    bin_reg = convert_bin(reg_num,5)
    output = imm_bin + bin_reg + opcode
    return output

def U2_auipc(parts):
    opcode = "0010111"
    r_des = parts[1]
    
    try:
        imm_val = int(parts[2])
    except:
        print("Invalid imm val")
        sys.exit()
        
    reg_num = registers[r_des]
    imm_bin = convert_bin(imm_val,20)
    bin_reg = convert_bin(reg_num,5) 
    output  = imm_bin +bin_reg+opcode
    return output

# J type instruction format:
#  imm[20] | imm[10:1] | imm[11] | imm[19:12] | rd | opcode
def J_jal(parts):
    opcode ="1101111"
    r_des = parts[1]
    
    try:
        imm_val = int(parts[2])
    except:
        print("Invalid imm val")
        sys.exit()
        
    reg_num = registers[r_des]
    imm_bin = convert_bin(imm_val,21)
    bin_reg = convert_bin(reg_num,5)
    output = (imm_bin[0]+ imm_bin[10:20]+ imm_bin[9]+ imm_bin[1:9]+
              bin_reg+opcode)
    return output

# S type instruction format:
#  imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
def S_sw(parts):
    opcode = "0100011"
    rs2 = parts[1]
    funct3 = "010"
    imm , rs1 = parts[2].split('(')
    rs1 = rs1.replace(")","")
    
    r1 = registers[rs1]
    r2 = registers[rs2]
    imm_val = int(imm)
    imm_bin = convert_bin(imm_val,12)
    bin_r1 = convert_bin(r1,5)
    bin_r2= convert_bin(r2,5)
    output = (imm_bin[0:7] + bin_r2+bin_r1+funct3+ imm_bin[7:12]
                +opcode)
    return output


# B type instructuon format:
#  imm[12] | imm[10:5] | rs2 | rs1 | funct3 | imm[4:1] | imm[11] | opcode
def B_bltu(parts):
    funct3= "110"
    opcode ="1100011" 
    rs1 = parts[1]
    rs2 = parts[2]
    off = int(parts[3])
    
    rs1 = registers[rs1]
    rs2 = registers[rs2]
    imm_bin= convert_bin(off,13)
    bin_rs1 = convert_bin(rs1,5)
    bin_rs2 = convert_bin(rs2,5)
    output = (imm_bin[0]+imm_bin[2:8]+bin_rs2+bin_rs1+funct3+
              imm_bin[8:12]+imm_bin[1]+opcode)
    return output

def B_bgeu(parts):
    opcode ="1100011"
    funct3="111"
    rs1 = registers[parts[1]]
    rs2 = registers[parts[2]]
    off = int(parts[3])
    bin_rs1 = convert_bin(rs1,5)
    bin_rs2 = convert_bin(rs2,5)
    imm_bin = convert_bin(off,13)
    output = (imm_bin[0]+imm_bin[2:8]+bin_rs2+bin_rs1+funct3+imm_bin[8:12]
              +imm_bin[1]+opcode)
    return output

if __name__ == "__main__":
    
    if len(sys.arv)<3:
        print("IndexError")
        sys.exit()
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        lines = f.readlines()
        
    halt = False
    for i in lines:
        x = i.replace(","," ").split()
        if x==["beq", "zero","zero","0"]:
            halt = True
        if not halt:
            print("Virtual halt missing instr..")
            sys.exit()
        
    pc =0
    labels={}
    output = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        
        if ":" in line:
            line = line.split(":")[1].strip()
        
        if line!= "":
            pc = pc+4
            
        parts = line.replace(",", " ").split()
        instruction = parts[0]
        
        if instruction in ["bltu","bgeu","jal"]:
            if not parts[-1].isdigit():
                label = parts[-1]
                
                if label not in labels:
                    print("undefined label",label)
                    sys.exit()
                    
                offset = labels[label] - pc
                parts[-1] = str(offset)
        
        if instruction == "lui":
            binary = U1_lui(parts)

        elif instruction == "auipc":
            binary = U2_auipc(parts)

        elif instruction == "jal":
            binary = J_jal(parts)

        elif instruction == "sw":
            binary = S_sw(parts)

        elif instruction == "bltu":
            binary = B_bltu(parts)

        elif instruction == "bgeu":
            binary = B_bgeu(parts)

        else:
            print("Invalid instruction given",instruction)
            sys.exit()

        output.append(binary)
        pc = pc+4
        
    with open(output_file, "w") as f:
        for line in output:
            f.write(line + "\n")



def regval(val):

    if val == "zero": 
        return 0
    elif val == "ra": 
        return 1
    elif val == "sp": 
        return 2
    elif val == "gp": 
        return 3
    elif val == "tp": 
        return 4
    elif val == "t0": 
        return 5
    elif val == "t1": 
        return 6
    elif val == "t2": 
        return 7
    elif val == "s0" or val == "fp": 
        return 8
    elif val == "s1": 
        return 9
    elif val == "a0": 
        return 10
    elif val == "a1": 
        return 11
    elif val == "a2": 
        return 12
    elif val == "a3": 
        return 13
    elif val == "a4": 
        return 14
    elif val == "a5": 
        return 15
    elif val == "a6": 
        return 16
    elif val == "a7": 
        return 17
    elif val == "s2": 
        return 18
    elif val == "s3": 
        return 19
    elif val == "s4": 
        return 20
    elif val == "s5": 
        return 21
    elif val == "s6": 
        return 22
    elif val == "s7": 
        return 23
    elif val == "s8": 
        return 24
    elif val == "s9": 
        return 25
    elif val == "s10": 
        return 26
    elif val == "s11": 
        return 27
    elif val == "t3": 
        return 28
    elif val == "t4": 
        return 29
    elif val == "t5": 
        return 30
    elif val == "t6": 
        return 31

#funct7 rs2 rs1 funct3 rd opcode

def r_type(ins,rs2,rs1,rd):
    x = ""
    if ins == "add":
        x = x+"0000000"

        rs2call = regval(rs2)
        rs2bin = format(rs2call, '05b')
        x = x+rs2bin

        rs1call = regval(rs1)
        rs1bin = format(rs1call, '05b')
        x = x+rs1bin

        x = x+"000"

        rdcall = regval(rd)
        rdbin = format(rdcall, '05b')
        x = x+rdbin
        
        x = x+"0110011"
    
    elif ins == "sub":
        x = x+"0100000"

        rs2call = regval(rs2)
        rs2bin = format(rs2call, '05b')
        x = x+rs2bin

        rs1call = regval(rs1)
        rs1bin = format(rs1call, '05b')
        x = x+rs1bin

        x = x+"000"

        rdcall = regval(rd)
        rdbin = format(rdcall, '05b')
        x = x+rdbin
        
        x = x+"0110011"


    elif ins == "slt":
        x = x+"0000000"

        rs2call = regval(rs2)
        rs2bin = format(rs2call, '05b')
        x = x+rs2bin

        rs1call = regval(rs1)
        rs1bin = format(rs1call, '05b')
        x = x+rs1bin

        x = x+"010"

        rdcall = regval(rd)
        rdbin = format(rdcall, '05b')
        x = x+rdbin
        
        x = x+"0110011"

    elif ins == "sltu":

        x = x+"0000000"

        rs2call = regval(rs2)
        rs2bin = format(rs2call, '05b')
        x = x+rs2bin

        rs1call = regval(rs1)
        rs1bin = format(rs1call, '05b')
        x = x+rs1bin

        x = x+"011"

        rdcall = regval(rd)
        rdbin = format(rdcall, '05b')
        x = x+rdbin
        
        x = x+"0110011"
    print(x)

#imm[12] imm[10:5] rs2 rs1 funct3 imm[4:1] imm[11] opcode

def b_type(ins,imm_int,rs2,rs1):
    x = ""
    if ins == "beq":
        imm_bin = format(imm_int & 0x1FFF, '013b')
        x = x+imm_bin[0]
        x = x+imm_bin[2:8]

        rs2call = regval(rs2)
        rs2bin = format(rs2call, '05b')
        x = x+rs2bin

        rs1call = regval(rs1)
        rs1bin = format(rs1call, '05b')
        x = x+rs1bin

        x = x+"000"

        x = x+imm_bin[8:12]
        x = x+imm_bin[1]

        x = x+"1100011"
    print(x)

with open("riscv_program.txt") as f:
    x = f.readlines()

l = []
j = 0 
for i in x:
    i = i.strip()
    i = i.replace(","," ")
    i = i+" "+str(j)
    j = j+1
    l.append(i)
    

#add,sub,sub2,slt,sltu,beq

for i in l:
    k = i.split(" ")


    if k[0] in ["add","sub","slt","sltu"]:
        r_type(k[0],k[3],k[2],k[1])
    elif k[1] in ["add","sub","slt","sltu"]:
        r_type(k[1],k[4],k[3],k[2])


    if k[0] in ["beq"]:
        if k[3].isdigit():
            imm = int(k[3])
        else:
            store = k[3]
            current_idx = k[4]
            for u in l:
                z = u.split(" ")

                if z[0] == store+":":
                    label_idx = z[5]
            imm = (int(label_idx) - int(current_idx))*4
        b_type(k[0],imm,k[2],k[1])

    elif k[1] in ["beq"]:
        if k[4].isdigit():
            imm = int(k[4])
        else:
            store = k[4]
            current_idx = k[5]
            for u in l:
                z = u.split(" ")
                if z[0] == store+":":
                    label_idx = z[5]
            imm = (int(label_idx) - int(current_idx))*4
        b_type(k[1],imm,k[3],k[2])
    

