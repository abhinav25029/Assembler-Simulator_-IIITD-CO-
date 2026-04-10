import sys

reg=[]


for i in range(32):
    reg.append(0)

reg[2]=0x0000017C


#the memory regions dictionary
data ={}
stack={}



#bit extraction
def get_bits(ins,hi,lo):

    start_idx=31-hi


    end_idx= 31-lo+1

    return ins[start_idx:end_idx]

#this func is used to convert bin. str. to signed no. 
def signed(b):
    n=int(b,2)
    length_of_b=len(b)

    if n>=(1<<(length_of_b-1)):
        n=n-(1<<length_of_b)

    return n

# this func treats int as 32 bit bin. no. 
def sign32(n):
    n=n&0xFFFFFFFF


    if n>=0x80000000:
        n=n-0x100000000

    return n

# for testcases with memory dump error
def data_mem(addr):


    if addr%4!=0:
        return False
        

    if addr>=0x00010000 and addr<0x00010080:
        return True
        
    if addr>=0x00000100 and addr<0x00000180:
        return True
        

    return False

#decoding function
def decode(ins):

    op=get_bits(ins,6,0)
    f3=get_bits(ins,14,12)
    f7=get_bits(ins,31,25)
    
    rd_string=get_bits(ins,11,7)
    rd=int(rd_string,2)
    
    rs1_string=get_bits(ins,19,15)
    rs1=int(rs1_string,2)
    
    rs2_string=get_bits(ins,24,20)
    rs2=int(rs2_string,2)


    # R-type

    if op=="0110011":

        if f3=="000":

            if f7=="0000000":

                return("add",rd,rs1,rs2)
            
            elif f7=="0100000":

                return("sub",rd,rs1,rs2)
            
        elif f3=="001":

            return("sll",rd,rs1,rs2)
        
        elif f3=="010":

            return("slt",rd,rs1,rs2)
        
        elif f3=="011":

            return("sltu",rd,rs1,rs2)
        
        elif f3=="100":

            return("xor",rd,rs1,rs2)
        
        elif f3=="101":

            return("srl",rd,rs1,rs2)
        
        elif f3=="110":

            return("or",rd,rs1,rs2)
        
        elif f3=="111":

            return("and",rd,rs1,rs2)




    # I-type(addi, sltiu)

    elif op=="0010011":

        imm_string=get_bits(ins,31,20)
        imm=signed(imm_string)


        if f3=="000":
            return("addi",rd,rs1,imm)
        

        elif f3 == "011":
            return("sltiu",rd,rs1,imm)


    #lw
    elif op=="0000011":

        imm_string=get_bits(ins,31,20)

        imm=signed(imm_string)



        if f3=="010":

            return("lw",rd,rs1,imm)
        

    #sw
    elif op=="0100011":

        part1=get_bits(ins,31,25)

        part2=get_bits(ins,11,7)

        imm_string=part1+part2

        imm=signed(imm_string)

        if f3=="010":
            return ("sw",rs2,rs1,imm)
        


    #b type
    elif op=="1100011":

        bit_12=get_bits(ins,31,31)

        bit_11=get_bits(ins,7,7)

        bits_10_5=get_bits(ins,30,25)
        bits_4_1=get_bits(ins,11,8)

        imm_string=bit_12 + bit_11+bits_10_5+bits_4_1 + "0"
        imm=signed(imm_string)
        
        if f3=="000":
            return("beq",rs1,rs2,imm)
        

        elif f3 =="001":
            return("bne",rs1,rs2,imm)
        
        elif f3 =="100":
            return("blt",rs1,rs2,imm)
        
        elif f3 =="101":
            return("bge",rs1,rs2,imm)
        
        elif f3 =="110":
            return("bltu",rs1,rs2,imm)
        
        elif f3 =="111":
            return("bgeu",rs1,rs2,imm)