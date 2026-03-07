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