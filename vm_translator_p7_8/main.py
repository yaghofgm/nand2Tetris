#main.py
from learning import Parser, CodeWriter
import argparse

def main():
    argparser = argparse.ArgumentParser(description='VM translator')
    argparser.add_argument('--file',type=str,required=True,help='Path to .vm file')
    args=argparser.parse_args()
    input_file=args.file
    output_file=input_file.replace(".vm",".asm")

    parser=Parser(input_file)
    codeWriter=CodeWriter(output_file)

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
