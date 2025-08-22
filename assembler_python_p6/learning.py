from dcj_table import DEST, COMP, JUMP

# #this is a type hint, it is optional and not inforced 
# def classify_line(line: str) -> str: 
#     if line=="" or line.startswith("//"):
#         out="comment"
#     elif line.startswith("(") and line.endswith(")"):
#         out="label_instruction"
#     elif line.startswith("@"):
#         symbol=line[1:]
#         if symbol.isdigit():
#             out="address"
#         else:
#             out="variable or predefined symbol"
#     else:
#         out="C_instruction"
#     print(f"This line is a {out}")
def classify_line(line: str) -> str:
    line = line.strip()  # In case there's whitespace

    if line == "" or line.startswith("//"):
        return "comment"
    elif line.startswith("(") and line.endswith(")"):
        return "label_instruction"
    elif line.startswith("@"):
        symbol = line[1:]
        if symbol.isdigit():
            return "address"
        else:
            return "variable or predefined symbol"
    else:
        return "C_instruction"

test_lines = [
    "// this is a comment",
    "",
    "(LOOP)",
    "@100",
    "@i",
    "D=M",
    "0;JMP"
]
print(f"Test 1: \n")
for l in test_lines:
    print(f"{l} --> {classify_line(l)}")


def clean_line(line: str) -> str:
    # Remove comments
    if '//' in line:
        line = line[:line.index('//')]
    
    # Remove surrounding whitespace
    return line.strip()
# lines = [
#     "   @i    // load i",
#     "D=M     // compute",
#     "// this is a full comment",
#     "    ",
#     "(LOOP)  // label"
# ]
print(f"\nTest 2: \n")
for raw in test_lines:
    cleaned = clean_line(raw)
    if cleaned:  # ignore empty cleaned lines
        print(f"{cleaned} --> {classify_line(cleaned)}")

def parse_lines(raw_lines:list[str])->list[str]:
    cleaned_lines=[]
    for line in raw_lines:
        cleaned = clean_line(line)
        if cleaned:
            cleaned_lines.append(cleaned)
    return cleaned_lines
raw_lines = [
    "   @2    // load 2",
    "",
    "D=A     // store in D",
    "    ",
    "(LOOP)  // jump label",
    "@LOOP",
    "0;JMP",
    "// a comment"
]
print(f"\n Test 3:\n")
parsed = parse_lines(raw_lines)

for line in parsed:
    print(f"{line} --> {classify_line(line)}")

def first_pass(cleaned_lines:list[str])->dict[str,int]:
    symbol_table={}
    rom_address=0

    for line in cleaned_lines:
        if classify_line(line)=="label_instruction":
            label=line[1:-1] #remove the parenthesis
            symbol_table[label]=rom_address
        else:
            rom_address+=1
    return symbol_table
lines = [
    "@2",
    "D=A",
    "(LOOP)",
    "@LOOP",
    "0;JMP",
    "(END)",
    "@END",
    "0;JMP"
]
print(f"\nTest 4:\n")
parsed = parse_lines(lines)
symbols = first_pass(parsed)
print(symbols)  # Expected: {'LOOP': 2}

def create_symbol_table()->dict[str,int]:
    table = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }

    # Add R0 to R15
    for i in range(16):
        table[f"R{i}"] = i

    return table

def first_pass(cleaned_lines:list[str])->dict[str,int]:
    symbol_table=create_symbol_table()
    rom_address=0

    for line in cleaned_lines:
        if classify_line(line)=="label_instruction":
            label=line[1:-1] #remove the parenthesis
            symbol_table[label]=rom_address
        else:
            rom_address+=1
    return symbol_table

print(f"\nTest 5:\n")
parsed = parse_lines(lines)
symbols = first_pass(parsed)
print(symbols)  # Expected: {'LOOP': 2} and the predefineds

def first_pass(cleaned_lines:list[str])->dict[str,int]:
    symbol_table=create_symbol_table()
    rom_address=0
    next_var_address=16

    for line in cleaned_lines:
        if classify_line(line)=="label_instruction":
            label=line[1:-1] #remove the parenthesis
            symbol_table[label]=rom_address
        else:
            rom_address+=1

    for line in cleaned_lines:
        if classify_line(line)=="variable or predefined symbol":
            symbol=line[1:]
            if symbol not in symbol_table:
                while next_var_address in symbol_table.values():
                    next_var_address+=1
                symbol_table[symbol]=next_var_address
                next_var_address+=1

    return symbol_table

test_lines = [
    "@i",
    "M=1",
    "@sum",
    "M=0",
    "(LOOP)",
    "@i",
    "D=M",
    "@R0",
    "D=D-M",
    "@STOP",
    "D;JGT",
    "@i",
    "D=M",
    "@sum",
    "M=D+M",
    "@i",
    "M=M+1",
    "@LOOP",
    "0;JMP",
    "(STOP)",
    "@sum",
    "D=M"
]
print(f"\nTest 5:\n")
parsed = parse_lines(test_lines)
symbols = first_pass(parsed)
print(symbols)  # Expected: {'LOOP': 2} and the predefineds

print(f"\nTest 6:\n")
with open("input.asm", "r") as f:
    test_lines=f.readlines()
parsed = parse_lines(test_lines)
symbols = first_pass(parsed)
print(symbols)  # Expected: {'LOOP': 2} and the predefineds

def second_pass(cleaned_lines:list[str], symbol_table:dict[str,int])->list[str]:
    output=[]
    for line in cleaned_lines:
        classification=classify_line(line)

        if classification=="label_instruction":
            continue 
        elif classification in ("address", "variable or predefined symbol"): #A-instruction
            symbol=line[1:]
            if symbol.isdigit():
                address=int(symbol) #was previously a string
            else:
                address=symbol_table[symbol]
            binary=f"{address:016b}" #16 bit binary string  padded with zeros
            output.append(binary)
        elif classification=="C_instruction":
            dest,comp,jump = parse_c_instruction(line)
            binary="111"+comp_to_bin(comp)+dest_to_bin(dest)+jump_to_bin(jump)
            output.append(binary)
    
    return output
def parse_c_instruction(c_instr:str)->tuple[str,str,str]:
    """
    Retorna as partes da instruction dest xor jump podem ser nulos
    """
    dest="null"
    jump="null"
    code=c_instr.strip()

    if "=" in code:
        dest,code=code.split("=",1) #maxsplit tells to divide only once from the left 
        dest = dest.strip()
    if ";" in code:
        comp,jump=code.split(";",1)
        comp=comp.strip()
        jump=jump.strip()
    else:
        comp=code.strip()

    return dest,comp,jump

def dest_to_bin(dest: str) -> str:
    try:
        return DEST[dest]
    except KeyError:
        raise ValueError(f"dest inválido: '{dest}'")

def comp_to_bin(comp: str) -> str:
    try:
        return COMP[comp]
    except KeyError:
        raise ValueError(f"comp inválido: '{comp}'")

def jump_to_bin(jump: str) -> str:
    try:
        return JUMP[jump]
    except KeyError:
        raise ValueError(f"jump inválido: '{jump}'")

print(f"\nTest 7:\n")
with open("input.asm", "r") as f:
    test_lines=f.readlines()
parsed = parse_lines(test_lines)
symbols = first_pass(parsed)
with open("output.hack","w") as f:
    for line in second_pass(parsed,symbols):
        f.write(line+"\n")