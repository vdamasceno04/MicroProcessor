def insert_bin(rom_file, bin):
    with open(rom_file, 'r') as file:
        lines = file.readlines()
    
    while True:
        if lines[14] != '        -- abaixo: casos omissos => (zero em todos os bits)\n':
            lines.pop(14)
        else:
            break
    count = 0
    for line in bin:
        lines.insert(14+count, f'      {count} => "{line}",\n')
        count += 1
    with open(rom_file, 'w') as file:
        for line in lines:
            file.write(line)

def read_asm(asm_file):
    with open(asm_file, 'r') as file:
        lines = file.readlines()
    return lines

def int_to_bin(num):
    try:
        num = int(num)
        if (num < 0):
            num =  num + 0xFF + 1
        return format(num, '08b')
    except:
        return '00000000'

def asm_to_bin(asm):
    asm = asm.upper()
    asm = asm.replace(',', ' ')
    asm = asm.split()
    bin = ''
    if asm[0] in op_map:
        bin += op_map[asm[0]]
        if asm[0] in reg_ops:
            if not (asm[1] in reg_map):
                return '0000000000000000'
            bin = reg_map[asm[1]] + bin
            asm.pop(1)
        else:
            bin = '000' + bin
        if asm[0] in imm_ops:
            bin = int_to_bin(asm[1]) + bin
        else:
            bin = '00000000' + bin
        return bin
    return '0000000000000000'

bin = [
"0000000011111111",
"0000000011111111",
"0000000011111111",
"0000000011111111",
"0000000011111111",
"0000000011111111",
"0000000011111111",
"0000000011111111",
"0000000011111111",
"1111111111111111"
]

op_map = {
    'MOVFA' : '11100',
    'MOVTA' : '11000',
    'LD' :  '00100',
    'JMP' : '01110',
    'NOP' : '00000',
    'AND' : '00001',
    'ANDI' : '00011',
    'OR' : '00101',
    'ORI' : '00111',
    'XOR' : '01001',
    'XORI' : '01011',
    'ADD' : '01101',
    'ADDI' : '01111',
    'SUB' : '10001',
    'SUBI' : '10011',
    'BNEQ' : '00010',
    'BGTR' : '00110',
    'JC' : '10010',
    'JN' : '10110',
    'JO' : '11010',
    'LW': '10100',
    'SW': '10000',
    'LU': '01100',
    'DJNZ': '11110'
}

imm_ops = ['LD', 'JMP', 'ANDI', 'ORI', 'XORI', 'ADDI', 'SUBI', 'BNEQ', 
           'BGTR', 'JC', 'JN', 'JO', 'LW', 'SW', 'LU', 'DJNZ']

reg_ops = ['MOVFA', 'MOVTA', 'LD', 'AND', 'OR', 'XOR', 'ADD', 'SUB', 
           'BNEQ', 'BGTR', 'LW', 'SW', 'LU', 'DJNZ']

reg_map = {
    'R0' : '000',
    'R1' : '001',
    'R2' : '010',
    'R3' : '011',
    'R4' : '100',
    'R5' : '101',
    'R6' : '110',
    'R7' : '111'
}

rom_file = 'uc/rom.vhd'
asm_file = 'assembly.txt'

asm = read_asm(asm_file)
bin = []
for line in asm:
    bin.append(asm_to_bin(line))

insert_bin(rom_file, bin)
