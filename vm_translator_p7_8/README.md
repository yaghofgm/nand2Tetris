VM Translator (Project 7)

Small, single-file VM-to-Hack translator for the Nand2Tetris course. It reads a .vm file and writes the corresponding Hack assembly .asm next to it.

Supported (Project 7 scope)
- Arithmetic/logical: add, sub, neg, eq, gt, lt, and, or, not
- Memory access: push/pop for segments constant, local, argument, this, that, temp, pointer, static
- Single input file only (no directories)

Not yet supported (Project 8 features)
- Program flow: label, goto, if-goto
- Function calling: function, call, return

Requirements
- Python 3.10+ (tested with 3.10)

Quick start
1) From the repo root, change into this folder.
	 - Windows PowerShell:
		 ```powershell
		 cd vm_translator
		 ```
2) Run the translator on a .vm file. Output .asm will be created beside the input and will overwrite any existing file with the same name.
	 - Windows PowerShell examples:
		 ```powershell
		 # Basic arithmetic test
		 python .\main.py --file .\BasicTest.vm

		 # Stack operations
		 python .\main.py --file .\StackTest.vm

		 # Pointer and static segment tests
		 python .\main.py --file .\PointerTest.vm
		 python .\main.py --file .\StaticTest.vm
		 ```

Expected outputs
- This folder includes reference .asm files (e.g., BasicTest.asm, StackTest.asm, PointerTest.asm, StaticTest.asm).
- Running the translator with the same .vm name will overwrite those files. If you want to compare your output to the references, either:
	- Copy the .vm to a different filename before running (e.g., copy BasicTest.vm to BasicOut.vm), or
	- Run the translator in another directory.

Verifying your output (optional)
- You can visually diff your generated .asm with the provided reference .asm.
- The Nand2Tetris tools include TextComparer.bat you can use, e.g.:
	```powershell
	# Example if you generated .\out\BasicTest.asm and want to compare to the reference
	..\tools\TextComparer.bat .\out\BasicTest.asm .\BasicTest.asm
	```

How it’s structured
- main.py: CLI entry point. Usage: python main.py --file path/to/File.vm
- learning.py:
	- Parser: cleans input and classifies commands (C_ARITHMETIC, C_PUSH, C_POP)
	- CodeWriter: emits Hack assembly for arithmetic and push/pop

Notes
- Output file name matches the input .vm name, with .asm extension.
- The translator currently handles only one .vm file at a time.
- No bootstrap code (Sys.init) is emitted.

