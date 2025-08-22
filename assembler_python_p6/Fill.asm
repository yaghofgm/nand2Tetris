// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//pseudocode, go forward blackening or backward whitening
//pseudocode, new approach: 
//blacken/whiten all in every loop from start to finish

//min_addr = @SCREEN
@SCREEN
D=A
@min
M=D
//max_addr = @KBD-1
@KBD
D=A-1
@max
M=D
(LOOP)
    //start the loop from the min
    @min
    D=M
    @addr
    M=D
    //if ((*KBD)!=0) 
    @KBD
    D=M
    @NOKEY
    D;JEQ
        //addr->black for every pixel
        (BLACK_LOOP)
        @addr
        A=M
        M=-1
        //if on max, end black loop
        D=A
        @max
        D=D-M
        @LOOP
        D;JEQ
        //else, addr+=1
        @addr
        M=M+1
        @BLACK_LOOP
        0;JMP
    //else 
    (NOKEY)
        //addr->white for every pixel
        (WHITE_LOOP)
        @addr
        A=M
        M=0
        //if on max, end white loop
        D=A
        @max
        D=D-M
        @LOOP
        D;JEQ
        //else, addr+=1
        @addr
        M=M+1
        @WHITE_LOOP
        0;JMP