#main.py
from learning import Parser, CodeWriter
import argparse, os

def main():
    argparser = argparse.ArgumentParser(description='VM translator')
    argparser.add_argument('--path',type=str,required=True,help='Path to .vm folder or file')
    args=argparser.parse_args()
    path=args.path

    if os.path.isdir(path):
        mode="dir"
    elif os.path.isfile(path):
        mode="file"
    else:
        raise ValueError(f"Path {path} is neither a file nor a directory")

    if mode == "file":
        vm_paths = [path]
        output_file = path.replace(".vm",".asm")
    else:
        folder= os.path.basename(os.path.normpath(path))
        output_file = os.path.join(path,f"{folder}.asm")
        vm_paths = [
            os.path.join(path,f)
            for f in sorted(os.listdir(path))
            if f.lower().endswith(".vm")
        ]
    
    codeWriter = CodeWriter(output_file)
    if mode=="dir":
        codeWriter._current_function="Bootstrap"
        codeWriter.writeInit()
    for vm_path in vm_paths:
        codeWriter.setFileName(vm_path)
        parser = Parser(vm_path)
        while parser.hasMoreLines():
            parser.advance()
            ctype=parser.commandType()
            arg1=parser.arg1()
            arg2=parser.arg2()
            match ctype:
                case "C_ARITHMETIC":
                    codeWriter.writeArithmetic(arg1)
                case "C_PUSH" | "C_POP":
                    codeWriter.writePushPop(ctype, arg1, arg2)
                case "C_LABEL":
                    codeWriter.writeLabel(arg1)
                case "C_GOTO":
                    codeWriter.writeGoto(arg1)
                case "C_IF":
                    codeWriter.writeIf(arg1)
                case "C_FUNCTION":
                    codeWriter.writeFunction(arg1, arg2)
                case "C_CALL":
                    codeWriter.writeCall(arg1, arg2)
                case "C_RETURN":
                    codeWriter.writeReturn()
                case "UNKNOWN":
                    print(f"Unknown command: {parser.current_command}")
    codeWriter.close()

if __name__=="__main__":
    main()
