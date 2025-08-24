# Hack Assembler ((Nand2Tetris Project) Project 6)

A Python implementation of an assembler for the **Hack computer** architecture from the [Nand2Tetris](https://www.nand2tetris.org/) course. Converts Hack assembly language (`.asm`) files into binary machine code (`.hack`) files.

---
Hack Assembler (Project 6)

Python assembler for the Hack computer from Nand2Tetris. Converts .asm to .hack using a simple CLI with a few preset inputs.

Requirements
- Python 3.10+

Quick start (WSL/Linux)
```bash
cd assembler_python_p6

# Assemble one of the presets (outputs to output.hack)
python3 ./assembler.py --f input   # input.asm
python3 ./assembler.py --f mult    # Mult.asm
python3 ./assembler.py --f fill    # Fill.asm
python3 ./assembler.py --f pong    # PongL.asm

# If you omit --f, it defaults to input.asm
python3 ./assembler.py
```

Output
- The assembled machine code is written to output.hack in this folder.
- Running again overwrites output.hack.

What it does (brief)
- Two-pass assembler:
	- First pass: build symbol table (labels mapped to ROM addresses; predefined symbols like R0–R15, SCREEN, KBD).
	- Second pass: emit 16-bit binary for A- and C-instructions; variables start at RAM address 16.

Project files
- assembler.py: CLI entry point (selects which .asm to assemble).
- parser.py: trims comments/whitespace and returns cleaned lines.
- main_code.py: first and second pass logic and code generation.
- dcj_table.py: lookup tables for dest/comp/jump.
- input.asm, Mult.asm, Fill.asm, PongL.asm: sample programs.
- output.hack: generated output file.

Notes
- This CLI assembles only the included preset files. To assemble an arbitrary .asm, either add another choice in assembler.py or use the small script in main.py as a starting point.
- Map labels like `(LOOP)` to their ROM addresses
