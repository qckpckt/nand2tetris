import unittest

from hack_assembler import parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.test_file_no_sym = open("max/MaxL.asm", "r")
        self.test_file_no_sym_comments = open("max/MaxLComments.asm", "r")
        self.comp_file_no_sym = open("max/MaxL.hack", "r")
        self.files = [self.comp_file_no_sym, self.test_file_no_sym, self.test_file_no_sym_comments]

    def tearDown(self):
        [file.close() for file in self.files]

    def test_no_symbols(self):
        ps = parser.Parser()
        output = ps.parse(self.test_file_no_sym)
        self.assertEqual(output, self.comp_file_no_sym.read())

    def test_no_symbols_inline_comments(self):
        ps = parser.Parser()
        output = ps.parse(self.test_file_no_sym_comments)
        self.assertEqual(output, self.comp_file_no_sym.read())
