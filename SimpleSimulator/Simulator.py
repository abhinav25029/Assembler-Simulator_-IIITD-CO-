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
        




    #jal

    elif op=="1101111":   

        bit_20=get_bits(ins,    31,31)

        bits_19_12=get_bits(ins,19,12)

        bit_11= get_bits(ins,20,                          20)
        bits_10_1 =get_bits(ins, 30,  21)

        imm_string=  bit_20+bits_19_12+bit_11+bits_10_1+"0"
        imm=signed(imm_string)


        return("jal",rd,imm)


    #jalr


    elif op== "1100111":

        imm_string  =get_bits(ins,31, 20)

        imm =signed(imm_string)

        if f3=="000":
            return("jalr",rd,rs1,imm)


    #lui

    elif op =="0110111":

        imm_string= get_bits(ins,31, 12) + "000000000000"

        imm= signed(imm_string)
        return("lui",rd,imm)


    #auipc


    elif op== "0010111":

        imm_string= get_bits(ins,31,12) + "000000000000"

        imm =signed(imm_string)

        return("auipc",rd,imm)
        
    return None



#memory read 


def mem_read(addr):

    if addr>=0x00010000 and addr<0x00010080:

        if addr in data:

            return data[addr]
        
        else:

            return 0
            
    elif addr >=0x00000100 and addr< 0x00000180:

        if addr in stack:

            return stack[addr]
        
        else:
            return 0
            
    return 0



#writing to memory


def mem_write(addr, val):


    if addr>=0x00010000 and addr<0x00010080:

        data[addr] =val & 0xFFFFFFFF

        

    elif addr>=0x00000100 and addr<0x00000180:

        stack[addr]=val & 0xFFFFFFFF



# some safe arguments to prevent crashes

if len(sys.argv)<3:

    print("Usage: python Simulator.py <input> <output>")

    sys.exit(1)



# loading instructions


instructions = []

try:

    with open(sys.argv[1],'r') as f:

        for line in f:

            clean_line = line.strip()

            if clean_line != "":

                instructions.append(clean_line)



except Exception as e:

    print("Error reading file:"+str(e))

    sys.exit(1)



HALT = "00000000000000000000000001100011"
pc = 0



with open(sys.argv[2], 'w', newline='\n') as out:

    while True:


       
        no_ins =len(instructions)
        idx_fetch =pc // 4
        
        if pc%4 !=0 or pc <0 or idx_fetch>=no_ins:


            print("Error: Invalid memory access or PC out of bounds at line " + str(idx_fetch))
            sys.exit(0)  



        ins=instructions[idx_fetch]
        t =decode(ins)


        if t is None:

            print("Error: Invalid instruction at line "+str(idx_fetch))

            sys.exit(0)


        # check for HALT 

        if ins==HALT:

            trace_str ="0b" + format(pc, '032b')
            for r in reg:
                trace_str=trace_str +" 0b"+format(r & 0xFFFFFFFF, '032b')
            
            out.write(trace_str +"\n")

            break

        
        operation=t[0]



        if operation=="add":

            rd =t[1]
            rs1=t[2]
            rs2=t[3]

            if rd!= 0:
                result =reg[rs1]+reg[rs2]
                reg[rd] =result & 0xFFFFFFFF


            pc=pc + 4

        elif operation=="sub":

            rd =t[1]
            rs1=t[2]
            rs2=t[3]

            if rd!=0:

                result=reg[rs1]-reg[rs2]
                reg[rd]=result & 0xFFFFFFFF

            pc=pc +4



        elif operation=="sll":

            rd=t[1]
            rs1=t[2]
            rs2=t[3]


            if rd!=0:

                shift_amt=reg[rs2] & 0x1F
                result =reg[rs1] <<shift_amt
                reg[rd] =result & 0xFFFFFFFF

            pc =pc+4



        elif operation=="slt":

            rd=t[1]
            rs1=t[2]
            rs2= t[3]

            if rd!=0:

                signed_rs1=sign32(reg[rs1])
                signed_rs2=sign32(reg[rs2])


                if signed_rs1<signed_rs2:
                    reg[rd] = 1


                else:
                    reg[rd] = 0


            pc = pc + 4



        elif operation=="sltu":

            rd=t[1]
            rs1=t[2]
            rs2=t[3]


            if rd!=0:


                unsigned_rs1=reg[rs1] & 0xFFFFFFFF
                unsigned_rs2=reg[rs2] & 0xFFFFFFFF

                if unsigned_rs1<unsigned_rs2:
                    reg[rd]=1

                else:
                    reg[rd]=0

            pc = pc + 4



        elif operation=="xor":
            rd=t[1]
            rs1=t[2]
            rs2=t[3]

            if rd!=0:
                result= reg[rs1] ^reg[rs2]
                reg[rd]=result & 0xFFFFFFFF

            pc = pc + 4

        elif operation =="srl":

            rd=t[1]
            rs1=t[2]
            rs2=t[3]


            if rd!=0:

                unsigned_rs1=reg[rs1] & 0xFFFFFFFF
                shift_amt=reg[rs2] & 0x1F

                result =unsigned_rs1>> shift_amt

                reg[rd]=result


            pc = pc + 4



        elif operation=="or":
            rd=t[1]
            rs1=t[2]

            rs2=t[3]

            if rd!= 0:

                result = reg[rs1] | reg[rs2]

                reg[rd] = result & 0xFFFFFFFF
            pc =pc+4

        elif operation=="and":
            rd = t[1]

            rs1 = t[2]
            rs2 = t[3]
            if rd!= 0:

                result=reg[rs1] & reg[rs2]

                reg[rd] =result & 0xFFFFFFFF

            pc =pc+4

        elif operation=="addi":
            rd =t[1]

            rs1 = t[2]
            imm= t[3]

            if rd!= 0:
                result =reg[rs1]+imm

                reg[rd]=result & 0xFFFFFFFF
            pc =pc+4

        elif operation=="sltiu":
            rd =t[1]
            rs1 =t[2]

            imm =t[3]

            if rd != 0:
                unsigned_rs1 =reg[rs1] & 0xFFFFFFFF

                unsigned_imm =imm & 0xFFFFFFFF

                if unsigned_rs1<unsigned_imm:
                    reg[rd] =1
                else:

                    reg[rd] =0
            pc =pc+4

        elif operation =="lw":
            rd = t[1]

            rs1 = t[2]
            imm = t[3]
            
            addr = reg[rs1]+imm
            masked_addr = addr&0xFFFFFFFF
            
            if data_mem (masked_addr)==False:
                ln =pc//4

                print("Error: Invalid memory access at line "+str(ln))

                sys.exit(0)
                
            if rd!=0:

                lv= mem_read(masked_addr)
                reg[rd]=lv

            pc = pc + 4

        elif operation=="sw":
            rs2 =t[1]

            rs1= t[2]
            imm = t[3]
            
            addr =reg[rs1]+imm

            masked_addr= addr & 0xFFFFFFFF
            
            if data_mem(masked_addr)==False:
                ln =pc//4
                print("Error: Invalid memory access at line "+str(ln))


                sys.exit(0)
                
            value_to_store =reg[rs2]

            mem_write(masked_addr,value_to_store)
            pc =pc+4

        elif operation=="beq":
            rs1= t[1]

            rs2= t[2]

            imm =t[3]
            if reg[rs1]==reg[rs2]:
                jump_addr =pc+imm

                pc = jump_addr & 0xFFFFFFFF
            else:
                pc =pc+4

        elif operation=="bne":
            rs1= t[1]
            rs2 =t[2]

            imm =t[3]

            if reg[rs1]!= reg[rs2]:
                jump_addr= pc +imm
                pc =jump_addr & 0xFFFFFFFF


            else:
                pc= pc+4

        elif operation=="blt":
            rs1= t[1]
            rs2= t[2]

            imm= t[3]

            signed_rs1=sign32(reg[rs1])
            signed_rs2= sign32(reg[rs2])

            if signed_rs1<signed_rs2:
                jump_addr =pc+imm

                pc=jump_addr & 0xFFFFFFFF
            else:
                pc =pc+4

        elif operation =="bge":
            rs1 =t[1]
            rs2 =t[2]

            imm =t[3]

            signed_rs1=sign32(reg[rs1])
            signed_rs2=sign32(reg[rs2])
            if signed_rs1>=signed_rs2:

                jump_addr = pc + imm

                pc = jump_addr & 0xFFFFFFFF

            else:

                pc = pc+4

        elif operation=="bltu":
            rs1 = t[1]

            rs2 = t[2]

            imm = t[3]

            unsigned_rs1=reg[rs1] & 0xFFFFFFFF
            unsigned_rs2=reg[rs2] & 0xFFFFFFFF

            if unsigned_rs1<unsigned_rs2:
                jump_addr=pc+imm

                pc =jump_addr & 0xFFFFFFFF
            else:

                pc = pc + 4

        elif operation== "bgeu":
            rs1 =t[1]

            rs2= t[2]
            imm =t[3]

            unsigned_rs1 =reg[rs1] & 0xFFFFFFFF

            unsigned_rs2= reg[rs2] & 0xFFFFFFFF
            if unsigned_rs1>=unsigned_rs2:

                jump_addr =pc+imm

                pc =jump_addr & 0xFFFFFFFF
            else:


                pc=pc+ 4

        elif operation=="lui":
            rd= t[1]

            imm =t[2]
            if rd!=0:

                reg[rd]=imm & 0xFFFFFFFF

            pc =pc+4

        elif operation=="auipc":


            rd =t[1]

            imm =t[2]
            if rd != 0:

                result=pc +imm
                reg[rd]=result & 0xFFFFFFFF

            pc =pc+4

        elif operation=="jal":
            rd= t[1]

            imm =t[2]

            if rd!=0:
                return_addr =pc+4
                reg[rd] =return_addr

            jump_addr =pc+imm

            pc =jump_addr & 0xFFFFFFFF

        elif operation=="jalr":
            rd = t[1]
            rs1 =t[2]
            imm =t[3]
            
            target_addr =reg[rs1]+imm
            

            next_pc=target_addr & ~1   
            
            if rd!= 0:

                return_addr =pc + 4

                reg[rd]=return_addr
                
            pc =next_pc & 0xFFFFFFFF

        
        reg[0]=0

        
        trace_str="0b"+format(pc,'032b')

        for r in reg:


            trace_str=trace_str+" 0b"+format(r & 0xFFFFFFFF,'032b')
            

        out.write(trace_str+"\n")

    
    crt_adr=0x00010000

    end_address=0x00010080
    
    while crt_adr<end_address:

        if crt_adr in data:

            value=data[crt_adr]

        else:

            value=0
            
        hex_string=format(crt_adr,'08X')
        binary_string=format(value, '032b')

        out.write("0x"+hex_string+":0b"+binary_string+"\n")
        crt_adr=crt_adr+4