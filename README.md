# make an assembler for the Hack computer of Nand2Tetris
# first, make the list of symbols, mapping them to numbers
# second, map symbols to numbers for instructions 
# finally, decode all

# MAKING A CLASSIFIER
# if line == "" or line.startswith("//"):
#     # Ignore blank or comment lines
# elif line.startswith("(") and line.endswith(")"):
#     # It's a label declaration (pseudo-instruction)
# elif line.startswith("@"):
#     # It's an A-instruction
#         # It's a direct address (e.g., @10)
#     else:
#         # It's a variable or predefined symbol (e.g., @i)
# else:
#     # It's a C-instruction (e.g., D=M, D;JGT, M=D+1;JMP)

# MAKING A LINE CLEANER 
# we need line_cleaning to convert into stuff that matters first
# MAKE THE ASM PARSER 
# after knowing how to clean a line, 
# we make it able to clena the whole file 

# MAKING THE FIRST PASS ASSEMBLER
# we make the dictionary of symbols 
# rom-addresses start at 0
# dont forget the predefined ones

# with open("output.hack", "w") as f:
    # for line in binary_lines:
    #     f.write(line + "\n")
# with open("input.asm", "r") as f:
#     test_lines=f.readlines()
