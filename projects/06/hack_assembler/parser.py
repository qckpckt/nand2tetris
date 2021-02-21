import re

from . import symbol_table

CODE_PATTERN = re.compile(r"^\s*?([\w\d\-+=|&\!\.@_$;]+)")
C_INSTR_PATTERN = re.compile(r"([AMD]{1,3})?=?([AMD01]?[\!+\-&|]?[AMD01]?);?(J[\w]{2})?")
LABEL_PATTERN = re.compile(r"\(([\w\d_\.$]+)\)")
INTEGER_PATTERN = re.compile(r"\d+")


class Parser():
    """Core logic of the assembler.

    Accepts a string representation of file

    VERSION 1:

    1. Strip whitespace and comments from string
    2. Convert the A and C instructions into binary forms using symbol_table
    3. return binary string file to be written out

    VERSION 2:

    1. Strip whitespace and comments from string
    2. Loop over string and find all labels - eg (SOME_LABEL). Record the line number of the following line into the
       symbol_table
    3. Loop over the string again:
        a. every variable declaration (eg @i), on first encounter add to symbol table, on every subsequent encounter,
           map to whatever the memory register was associated on first encounter
        b. every label invocation (eg @SOME_LABEL), map to the line number recorded in first pass
    4. Convert the A and C instructions into binary forms using symbol_table
    5. return binary string file to be written out
    """
    c_base_string = "111{a}{comp}{dest}{jmp}"  # c instructions always start with 111

    def __init__(self, asm_file, symbols=symbol_table.SymbolTable):

        self.asm_file = asm_file
        self.symbols = symbols()

    def a_to_binary(self, instruction):
        """Convert instruction to 15 bit binary number with 0 added as the MSB"""
        return f"0{int(instruction):015b}"

    def c_to_binary(self, instruction):
        """Parse and assemble C instruction.
        """
        a = "1" if "M" in instruction.comp else "0"  # if comp contains reference to M, a must be 1.
        return self.c_base_string.format(
            a=a,
            comp=self.symbols.comp_map.get(instruction.comp),
            dest=self.symbols.dest_map.get(instruction.dest, "000"),
            jmp=self.symbols.jmp_map.get(instruction.jmp, "000")
            )

    def _store_labels(self):
        """Iterate over self.asm_file and store labels in self.symbols."""
        labels = line = 0
        for instr in self.asm_file:
            if not CODE_PATTERN.match(instr) and not LABEL_PATTERN.match(instr):
                continue
            label = LABEL_PATTERN.match(instr)
            if label:
                labels += 1
                # A label refers to the following line, but the label lines will be ignored during parsing.
                # Therefore, the line to which a label refers will be the label line plus 1,
                # minus the number of label lines so far.
                self.symbols.add(label.group(1), ((line + 1) - labels))
            line += 1
        self.asm_file.seek(0)  # return to beginning of file for next loop.

    def parse(self):
        """Public method of parser class.
        """
        self._store_labels()
        output = []
        for line in self.asm_file:
            cleaned = CODE_PATTERN.match(line)
            if not cleaned:
                continue
            code = cleaned.group(1)
            if "@" in code:
                instruction = AInstruction(code)
                if INTEGER_PATTERN.match(instruction.register):
                    output.append(self.a_to_binary(instruction.register))
                else:
                    value = self.symbols.get(instruction.register)
                    output.append(self.a_to_binary(value))
            else:
                output.append(self.c_to_binary(CInstruction(code)))
        return "\n".join(output)


class Instruction:

    kind = None

    def __init__(self, raw):
        self.raw = raw
        self.register = self.dest = self.comp = self.jmp = None


class AInstruction(Instruction):

    kind = "A"

    def __init__(self, raw):
        super().__init__(raw)
        self.register = self.raw.split("@")[1]


class CInstruction(Instruction):
    """C instructions in hack assembly language follow this pattern:

            dest=comp;jmp

        Both the dest and jmp fields are optional.
        If dest is missing, there will be no "=".
        If jmp is missing, there will be no ";".
    """

    kind = "C"

    def __init__(self, raw, pattern=C_INSTR_PATTERN):
        super().__init__(raw)
        self.pattern = pattern
        self.dest, self.comp, self.jmp = self.pattern.match(self.raw).groups()
        if self.comp == '':  # "D;JNE" will lead to comp being None with the above regex. TODO - fix this
            self.comp = self.dest
            self.dest = ''
