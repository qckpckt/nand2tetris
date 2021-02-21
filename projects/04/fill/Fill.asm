// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// def fill_screen():
//      addr = SCREEN
//      end = addr + 8191
//      i = 0
//      if KEYBOARD > 0:  
//          for {i=0; i==end, i++}:
//              addr[i] =-1
//      else:
//          for {i=0; i==end; i++}:
//              addr[i] = 0

(MAIN_LOOP)

    @SCREEN
    D=A
    @addr
    M=D
    @8191
    D=A
    @end
    M=D

    @i
    M=0

    @KBD
    D=M

    @KEYPRESS
    D;JNE

(OFF_LOOP)

    @i
    D=M
    @end
    D=D-M

    @MAIN_LOOP
    D;JGT

    @addr
    A=M
    M=0

    @addr
    M=M+1

    @i
    M=M+1
    @OFF_LOOP
    0;JMP

(KEYPRESS)
(ON_LOOP)

    @i
    D=M
    @end
    D=D-M

    @MAIN_LOOP
    D;JGT

    @addr
    A=M
    M=-1
    @addr
    M=M+1

    @i
    M=M+1
    @ON_LOOP
    0;JMP