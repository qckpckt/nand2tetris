import argparse
import logging

from . import code

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(
    description=(
        "Argument parser for the hack assembler program. Accepts one argument - "
        "a path to a .asm file to convert to a .hack file.")
)

parser.add_argument("asm_file", type=str, help="path to a .asm file")

args = parser.parse_args()

assembler = code.Assembler(args.asm_file)

assembler.run()
