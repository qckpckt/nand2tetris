// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// def mult(num1, num2):
//      if num1 > num2:
//          total = num2
//          val = num1
//       else:
//          total = num1
//          val = num2
//      product = 0
//      for {i = 1; i == total; i++}:
//          product = product + val
//      return product 

    @product
    M=0

    @i
    M=1
    
    @R0
    D=M

    @IS_ZERO
    D;JEQ

    @temp
    M=D

    @R1
    D=M

    @IS_ZERO
    D;JEQ

    @temp
    D=M-D
 
    @LESS_THAN_EQ_ZERO
    D;JLE

    D=M
    @val
    M=D

    @R0
    D=M
    @total
    M=D

(LESS_THAN_EQ_ZERO)
    @temp
    D=M
    @total
    M=D

    @R1
    D=M
    @val
    M=D

(LOOP)
    @i
    D=M
    @total
    D=D-M
    @STOP
    D;JGT

    @product
    D=M
    @val
    D=D+M
    @product
    M=D

    @i
    M=M+1
    @LOOP
    0;JMP

(STOP)
    @product
    D=M
    @R2
    M=D
    @END
    0;JMP

(IS_ZERO)
    @R2
    M=0

(END)
    @END
    0;JMP
