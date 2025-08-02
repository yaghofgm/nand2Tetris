# 🧠 Hack Assembler (Nand2Tetris Project)

A Python implementation of an assembler for the **Hack computer** architecture from the [Nand2Tetris](https://www.nand2tetris.org/) course. Converts Hack assembly language (`.asm`) files into binary machine code (`.hack`) files.

---

## � Quick Start

```bash
# Assemble one of the preset files
python assembler.py --f input    # Assembles input.asm
python assembler.py --f mult     # Assembles Mult.asm  
python assembler.py --f fill     # Assembles Fill.asm

# Get help
python assembler.py -h
```

**Output:** All commands generate `output.hack` with the assembled machine code.

---

## 📁 Project Structure

```
assembler_python/
├── assembler.py        # Main CLI interface
├── parser.py          # Assembly line parser
├── main_code.py       # Two-pass assembler logic
├── dcj_table.py       # Lookup tables for C-instructions
├── input.asm          # Sample assembly file
├── Mult.asm           # Multiplication program
├── Fill.asm           # Screen fill program
└── output.hack        # Generated machine code
```

---

## 🛠️ How It Works

### Two-Pass Assembly Process

**First Pass:** Build symbol table
- Scan all lines and record label positions
- Initialize predefined symbols (`R0`-`R15`, `SCREEN`, `KBD`, etc.)
- Map labels like `(LOOP)` to their ROM addresses

**Second Pass:** Generate machine code
- Translate each instruction to 16-bit binary
- Resolve symbols using the symbol table
- Output final machine code

### Instruction Types

| Type | Format | Example | Description |
|------|--------|---------|-------------|
| **A-instruction** | `@value` | `@100`, `@sum` | Load address/value into A register |
| **C-instruction** | `dest=comp;jump` | `D=M+1;JGT` | Compute and conditionally jump |
| **Label** | `(LABEL)` | `(LOOP)` | Mark position for jumps |

### Symbol Resolution

```python
# Numbers: direct conversion
@17        → 0000000000010001

# Variables: allocated in RAM starting at address 16
@sum       → 0000000000010000  (if first variable)

# Labels: resolved to instruction addresses
(LOOP)     → Maps to ROM address of next instruction
@LOOP      → 0000000000000101  (if LOOP is at instruction 5)
```

---

## 🧩 Architecture Details

**Parser (`parser.py`):** Cleans and categorizes assembly lines
**Symbol Table:** Tracks labels, variables, and predefined symbols  
**Code Generator:** Uses lookup tables to convert instructions to binary
**CLI Interface:** Provides easy file selection and assembly

---

## 📝 Example Assembly

**Input (`input.asm`):**
```assembly
@i
M=1
@sum  
M=0
(LOOP)
@i
D=M
@R0
D=D-M
@STOP
D;JGT
@i
D=M
@sum
M=D+M
@i
M=M+1
@LOOP
0;JMP
(STOP)
@sum
D=M
```

**Output (`output.hack`):**
```
0000000000010000
1110111111001000
0000000000010001
1110101010001000
0000000000010000
1111110000010000
...
```

---

## 🔧 Usage Options

| Command | File | Description |
|---------|------|-------------|
| `python assembler.py --f input` | `input.asm` | Basic arithmetic loop |
| `python assembler.py --f mult` | `Mult.asm` | Multiplication algorithm |
| `python assembler.py --f fill` | `Fill.asm` | Screen manipulation |

All commands output to `output.hack` and display success message.
