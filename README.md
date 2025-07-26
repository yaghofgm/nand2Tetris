# 🧠 Hack Assembler (Nand2Tetris Project)

This is a Python implementation of an **assembler** for the **Hack computer**, part of the [Nand2Tetris](https://www.nand2tetris.org/) course.

---

## 🛠️ Assembler Workflow

The assembler performs the following steps:

---

### 1. Symbol Table Creation (First Pass)

- Parse each line to:
  - **Ignore** blank lines and comments (`// ...`)
  - **Handle labels** (e.g. `(LOOP)`) by mapping them to the ROM address of the following instruction
- Predefined symbols like `R0` to `R15`, `SCREEN`, `KBD`, and others are initialized

---

### 2. Instruction Parsing (Second Pass)

Each line is classified as:

- **A-instruction** (`@value`)
  - If `value` is numeric: directly convert to binary
  - If `value` is a symbol: resolve it via the symbol table (add to table if it's a new variable)
  
- **C-instruction** (`dest=comp;jump`)
  - Parse and translate using lookup tables for `dest`, `comp`, and `jump` fields

---

### 3. Line Classifier Logic

```python
if line == "" or line.startswith("//"):
    # Skip blank lines and comments
elif line.startswith("(") and line.endswith(")"):
    # Label (pseudo-instruction)
elif line.startswith("@"):
    # A-instruction: either direct number or symbol
else:
    # C-instruction
