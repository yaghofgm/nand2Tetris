# Nand2Tetris — course solutions and tools

This repo contains my solutions and small utilities for the Nand2Tetris course.

What’s here
- hardware_components_p1_2_3_4_5/01..05 — HDL-only versions of projects 1–5 (just the .hdl files I edited)
- assembler_python_p6 — Project 6 Hack assembler (Python)
- vm_translator_p7_8 — Projects 7–8 VM translator (Python)
- projects/ — Original course folders (kept for reference; may include extra files from the course zips)
- tools/ — Official Nand2Tetris tools (simulators, text comparer)

Prerequisites
- Python 3.10+
- Nand2Tetris tools (already included under tools/)

Run the assembler (Project 6)
```bash
cd assembler_python_p6
# Assemble one of the presets; output goes to output.hack
python3 ./assembler.py --f input   # input.asm
python3 ./assembler.py --f mult    # Mult.asm
python3 ./assembler.py --f fill    # Fill.asm
python3 ./assembler.py --f pong    # PongL.asm
```

Run the VM translator (Projects 7–8)
```bash
cd vm_translator_p7_8

# Folder mode (includes bootstrap; writes <folder>/<folder>.asm)
python3 ./main.py --path ./SomeProgramFolder

# File mode (no bootstrap; writes <file>.asm next to the input)
python3 ./main.py --path ./BasicTest.vm
```

Test HDL chips
- Use the Hardware Simulator from tools/ to load .hdl and run .tst scripts.
- On Linux/WSL:
  ```bash
  ./tools/HardwareSimulator.sh
  ```

Compare text outputs (optional)
- Use the course TextComparer to diff your .asm/.hack against references:
  ```bash
  ./tools/TextComparer.sh path/to/YourOutput.asm path/to/Expected.asm
  ```

Notes
- I keep only the .hdl files I changed under hardware_components_p1_2_3_4_5 to avoid extra .tst/.cmp noise.
- For multi-file VM programs, use folder mode so the bootstrap (Sys.init) runs.
