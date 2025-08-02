from parser import parse_lines
from main_code import first_pass, second_pass

# with open("input.asm", "r") as f:
# with open("Mult.asm", "r") as f:
with open("Fill.asm", "r") as f:
    test_lines=f.readlines()
parsed = parse_lines(test_lines)
symbols = first_pass(parsed)
with open("output.hack", "w") as f:
    lines = second_pass(parsed, symbols)
    f.write("\n".join(lines)) 
     # Junta tudo com \n entre linhas, sem \n final extra

# print("Symbol Table:", symbol_table)