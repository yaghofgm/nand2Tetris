#learning.py
import os
# vm translator passes vm commands in *.vm to assembly commands .asm

# lines after // are comments and should be ignored
# blank lines are permitted and are ignored
class Parser:  
    # class instance vars: raw_asm, index, current command
    def __init__(self, file:str)-> None:
        with open(file, "r") as f:
            self.raw_asm = self._clean_file(f.readlines())
            self.index = -1  # to track current line for .advance()
            self.current_command= None

    def hasMoreLines(self) -> bool:
        return self.index + 1 < len(self.raw_asm)
    
    def advance(self)-> None:
        self.index+=1
        self.current_command = self.raw_asm[self.index]
    
    def commandType(self)-> str:
        if self.current_command is None:
            return "UNKNOWN"
        
        parts = self.current_command.split()
        match parts[0]:
            case "push":
                return "C_PUSH"
            case "pop":
                return "C_POP"
            case "add" | "sub"| "neg"|"eq"|"gt"|"lt"|"and"|"or"|"not":
                return "C_ARITHMETIC"
            case "label":
                return "C_LABEL"
            case "goto":
                return "C_GOTO"
            case "if-goto":
                return "C_IF"
            case "function":
                return "C_FUNCTION"
            case "call":
                return "C_CALL"
            case "return":
                return "C_RETURN"
            case _:
                return "UNKNOWN"

    def arg1(self)->str:
        if self.current_command is None:
            return ""
        
        classify = self.commandType()
        parts = self.current_command.split()
        
        if classify == "C_ARITHMETIC":
            return parts[0]  
        elif classify in ["C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION", "C_CALL"]:
            return parts[1]
        else:
            return ""

    def arg2(self)->int:
        if self.current_command is None:
            return 0
        classify = self.commandType()
        parts = self.current_command.split()

        if classify in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return int(parts[2])
        else:
            return 0
    
    def _clean_line(self, line:str)->str: #the _makes it private
        line=line.strip()
        if "//" in line:
            line=line[:line.index("//")].strip()
        return line
    def _clean_file(self, file: list[str]) -> list[str]:
        parsed = []
        for line in file:
            cleaned = self._clean_line(line)
            if cleaned:  
                parsed.append(cleaned)
        return parsed
    
class CodeWriter:
    def __init__(self, file:str) -> None:
        self._f = open(file,"w") 
        # self._filename = file
        self._filename = os.path.splitext(os.path.basename(file))[0] #gets only Foo from C:/.../Foo.vm
        self._segment_pointers = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        self._binary_ops ={
            "add":"M=D+M",
            "sub":"M=M-D",
            "and":"M=D&M",
            "or":"M=D|M"
        }
        self._unary_ops={
            "neg":"M=-M",
            "not":"M=!M"
        }
        self._label_counter=0
        self._current_function=""
        self._ret_counter_by_func = {}
    
    def close(self)->None:
        self._f.close()

    def _write_block(self, asm: str) -> None:
        self._f.write(asm + "\n")

    def writeArithmetic(self,arg1:str)->None:
        if arg1 in self._binary_ops:
            asm_code = f"""@SP
AM=M-1
D=M
A=A-1
{self._binary_ops[arg1]}"""
            self._write_block(asm_code)
        elif arg1 in self._unary_ops:
            asm_code = f"""@SP
A=M-1
{self._unary_ops[arg1]}"""
            self._write_block(asm_code)
        elif arg1 in ["eq","lt","gt"]:
            jump= {
                "eq":"JEQ",
                "lt":"JLT",
                "gt":"JGT"
            }[arg1] #when i call jump, it will output what arg1 maps to

            true_label = f"{arg1.upper()}_TRUE{self._label_counter}"
            end_label = f"{arg1.upper()}_END{self._label_counter}"
            self._label_counter+=1
            #smart: x op y == x-y op 0
            asm_code = f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{true_label}
D;{jump}
@SP
A=M-1
M=0
@{end_label}
0;JMP
({true_label})
@SP
A=M-1
M=-1
({end_label})"""
            self._write_block(asm_code)

    def writePushPop(self,ctype:str,arg1:str,arg2:int)->None:
        if ctype == "C_PUSH":
            # Generate the value to push into D register
            if arg1 == "constant":
                asm_code = f"""@{arg2}
D=A"""
            elif arg1 in self._segment_pointers:
                asm_code = f"""@{self._segment_pointers[arg1]}
D=M
@{arg2}
D=D+A
A=D
D=M"""
            elif arg1 == "temp":
                asm_code = f"""@{5+arg2}
D=M"""
            elif arg1 == "pointer":
                if arg2==0:
                    pointer = "THIS"
                else:
                    pointer = "THAT"
                asm_code = f"""@{pointer}
D=M"""
            elif arg1 == "static":
                symbol=f"{self._filename}.{arg2}"
                asm_code = f"""@{symbol}
D=M"""
            else:
                self._f.write(f"// Unsupported segment for push {arg1}\n")
                return
            
            # Common push ending: *SP = D; SP++
            push_end = f"""@SP
A=M
M=D
@SP
M=M+1"""
            self._write_block(asm_code + "\n" + push_end)

        elif ctype=="C_POP":
            #there is no pop constant 5
            # Calculate target address and store in R13
            if arg1 in self._segment_pointers:
                asm_code = f"""@{self._segment_pointers[arg1]}
D=M
@{arg2}
D=D+A"""
            elif arg1 == "temp":
                assert 0 <= arg2 <= 7
                asm_code = f"""@{5+arg2}
D=A"""
            elif arg1 == "pointer":
                assert arg2 in [0,1]
                if arg2==0:
                    pointer = "THIS"
                else:
                    pointer = "THAT"
                asm_code = f"""@{pointer}
D=A"""
            elif arg1 == "static":
                symbol=f"{self._filename}.{arg2}"
                asm_code = f"""@{symbol}
D=A"""
            else:
                self._f.write(f"// Unsupported segment for pop {arg1}\n")
                return
            
            # Common pop ending: D = *(--SP); *R13 = D
            pop_end = f"""@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D"""
            self._write_block(asm_code + "\n" + pop_end)
        else:
            self._f.write(f"// ERROR, neither pop nor push : {ctype}\n")
        
    def writeLabel(self,arg1:str)->None:
        asm_code=f"({self._current_function}${arg1})" #the current function will already be compiled as filename.functionName 
        self._write_block(asm_code)
    
    def writeGoto(self,arg1:str)->None:
        asm_code=f"""@{self._current_function}${arg1}
0;JMP"""
        self._write_block(asm_code)
    
    def writeIf(self,arg1:str)->None:
        asm_code=f"""@SP
AM=M-1
D=M
@{self._current_function}${arg1}
D;JNE"""
        self._write_block(asm_code)
    
    def writeFunction(self,arg1:str,arg2:int)->None:
        self._current_function=arg1
        asm_code=f"({self._current_function})"
        self._write_block(asm_code)
        for _ in range(arg2):    
            self.writePushPop("C_PUSH","constant",0)
    
    def writeCall(self,arg1:str,arg2:int)->None:
        k=self._ret_counter_by_func.get(self._current_function,0) #get the number of returns of this function
        ret = f"{self._current_function}$ret.{k}"
        self._ret_counter_by_func[self._current_function] = k+1
        asm_code=f"@{ret}\nD=A\n"+self._pushTail()
        self._write_block(asm_code)
        for word in ("LCL","ARG","THIS","THAT"):
            asm_code=f"@{word}\nD=M\n"+self._pushTail()
            self._write_block(asm_code)
        asm_code=f"""@SP
D=M
@{arg2}
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@{arg1}
0;JMP
({ret})"""
        self._write_block(asm_code)
    def _pushTail(self)->str:
        asm_code="""@SP
A=M
M=D
@SP
M=M+1"""
        return asm_code

    def writeReturn(self)->None:
        return 
    