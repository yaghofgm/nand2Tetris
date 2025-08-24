# VM Translator ((Nand2Tetris Project) Projects 7–8)

Translate Hack VM code to Hack assembly. One required flag controls everything:

- Required: --path <path>
	- If <path> is a folder: translate all .vm files inside it into a single <folder>.asm and include bootstrap.
	- If <path> is a single .vm file: translate it into <file>.asm without bootstrap.

Supported commands
- Arithmetic/logical: add, sub, neg, eq, gt, lt, and, or, not
- Memory access: push/pop for constant, local, argument, this, that, temp, pointer, static
- Program flow: label, goto, if-goto
- Functions: function, call, return

Requirements
- Python 3.10+

Usage (WSL/Linux shell)
- From the repo root:
	```bash
	cd vm_translator_p7_8
	```

Folder mode — includes bootstrap
- Use when your program has multiple .vm files or needs Sys.init (e.g., Project 8 function calls: SimpleFunction, NestedCall, FibonacciElement, StaticsTest).
- Behavior:
	- Writes <folder>.asm inside the folder.
	- Emits bootstrap: sets SP=256 and calls Sys.init.
	- Translates all .vm files in the folder (sorted by name).
- Example:
	```bash
	python3 ./main.py --path ./SomeProgramFolder
	# Produces: ./SomeProgramFolder/SomeProgramFolder.asm
	```

File mode — no bootstrap
- Use for simple, single-file tests that don’t require Sys.init (e.g., BasicTest.vm, StackTest.vm, PointerTest.vm, StaticTest.vm).
- Behavior:
	- Writes <file>.asm next to the .vm file.
	- Does not emit bootstrap.
- Examples:
	```bash
	python3 ./main.py --path ./BasicTest.vm
	python3 ./main.py --path ./StackTest.vm
	python3 ./main.py --path ./PointerTest.vm
	python3 ./main.py --path ./StaticTest.vm
	```

Notes and tips
- Running again overwrites the existing .asm.
- Static variables are file-scoped (Foo.vm -> symbols Foo.0, Foo.1, ...).
- Labels inside functions are scoped as FunctionName$LABEL.
- For multi-file programs that don’t define Sys.init, folder mode will still include bootstrap and then jump to Sys.init (ensure it exists in the inputs if required by the test).

Project structure
- main.py: CLI entry point (parses --path, decides folder vs file, runs translator).
- learning.py: Parser and CodeWriter (emits Hack assembly for all Project 7–8 commands; adds bootstrap in folder mode via writeInit).

Compare outputs (optional)
- Use the Nand2Tetris TextComparer (shell version) to diff against references if you have them:
	```bash
	../tools/TextComparer.sh ./out/YourOutput.asm ./reference/Expected.asm
	```

