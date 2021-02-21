
from .parser import Parser


class Assembler():
    """Executor class for the hack_assembler.

    1. Read in filepath string & get file object as string
    2. Pass string to Parser
    3. Write out resulting binary to {filename}.hack
    """

    def __init__(self, filepath):
        """
        :param filepath: path (relative or absolute) to an asm file
        :type filepath: str
        :param parser: parser class to use with assembler. Defaults to parser.Parser.
        :type parser: Parser
        """
        self.filepath = filepath
        self.outfile = f"{self.filepath.split('.')[0]}.hack"

    def run(self):

        with open(self.filepath, "r") as infile, open(self.outfile, "w") as outfile:
            parser = Parser(infile)
            outfile.write(parser.parse())
