from dcj_table import DEST,COMP,JUMP

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
                # while next_var_address in symbol_table.values():
                #     next_var_address+=1
                symbol_table[symbol]=next_var_address
                next_var_address+=1

    return symbol_table
def second_pass(cleaned_lines:list[str], symbol_table:dict[str,int])->list[str]:
    output=[]
    next_var_address=16
    # print("Symbol Table:", symbol_table)
    for line in cleaned_lines:
        classification=classify_line(line)

        if classification=="label_instruction":
            continue 
        elif classification in ("address", "variable or predefined symbol"): #A-instruction
            symbol=line[1:]
            if symbol.isdigit():
                address=int(symbol) #was previously a string
            else:
                # if symbol not in symbol_table:
                #     # Allocate next available RAM address
                #     # while next_var_address in symbol_table.values():
                #     #     next_var_address += 1
                #     symbol_table[symbol] = next_var_address
                #     next_var_address += 1
                address=symbol_table[symbol]
            binary=f"{address:016b}" #16 bit binary string  padded with zeros
            output.append(binary)
        elif classification=="C_instruction":
            dest,comp,jump = parse_c_instruction(line)
            binary="111"+comp_to_bin(comp)+dest_to_bin(dest)+jump_to_bin(jump)
            output.append(binary)
    print("Symbol Table:", symbol_table)
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

