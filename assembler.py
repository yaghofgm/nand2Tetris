import argparse
from parser import parse_lines
from main_code import first_pass, second_pass

def main():
    parser = argparse.ArgumentParser(description='Hack Assembler')
    # Add "input" to choices and keep strings
    parser.add_argument('--f', type=str, choices=["input", "mult", "fill"])
    args = parser.parse_args()
    # Map flags to files - use args.f (not args.flag)
    if args.f == "input":
        input_file = "input.asm"
    elif args.f == "mult":
        input_file = "Mult.asm"
    elif args.f == "fill":
        input_file = "Fill.asm"
    else:
        # Default to input.asm if no flag provided
        input_file = "input.asm"
    

    with open(input_file, "r") as f:
        test_lines = f.readlines()
    parsed = parse_lines(test_lines)
    symbols = first_pass(parsed)
    with open("output.hack", "w") as f:
        lines = second_pass(parsed, symbols)
        f.write("\n".join(lines))
    
    print(f"Successfully assembled {input_file} to output.hack")

if __name__ == "__main__":
    main()
