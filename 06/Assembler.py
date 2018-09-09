import sys
import Parser
import Code
import SymbolTable

class Assembler(object):
    #Para ejecutar el programa $python Assembler.py MiArchivo.asm

    def __init__(self, in_file):
        """Constructor"""
        self.in_file = in_file
        self.out_file = self._get_out_file(in_file)
        self.symbol_table = SymbolTable.SymbolTable()
        self.symbol_address = 16

    def assemble(self):
        """Pasos en Assembler"""
        self.first_pass()
        self.second_pass()


    def first_pass(self):
        """Primer paso contruir la tabla de simbolos"""
        parser = Parser.Parser(self.in_file)
        cur_address = 0
        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == parser.A_COMMAND \
                    or parser.command_type() == parser.C_COMMAND:
                cur_address += 1
            elif parser.command_type() == parser.L_COMMAND:
                self.symbol_table.add_entry(parser.symbol(), cur_address)

    def second_pass(self):
        """Segundo paso empezar con el codigo en Assembler"""
        parser = Parser.Parser(self.in_file)
        outf = open( self.out_file, 'w')
        code = Code.Code()
        while(parser.has_more_commands()):
            parser.advance()
            if parser.command_type() == parser.A_COMMAND:
                outf.write(code.gen_a_code(self._get_address(parser.symbol()))
                        + '\n')
            elif parser.command_type() == parser.C_COMMAND:
                outf.write(code.gen_c_code(parser.comp(), parser.dest(),
                    parser.jump()) + '\n')
            elif parser.command_type == parser.L_COMMAND:
                pass
        outf.close()


    def _get_address(self, symbol):
        """Retorna la direccion del simbolo"""
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbol_table.get_address(symbol)

    @staticmethod
    def _get_out_file(in_file):
        """traduce el archivo de .asm a .hack"""
        if in_file.endswith('.asm'):
            return in_file.replace('.asm', '.hack')
        else:
            return in_file + '.hack'


def main():
    """Metodo principal"""
    in_file = ""
    if len(sys.argv) !=2:
        print("Usage: $python Assembler.py MiArchivo.asm")
    else:
        in_file = sys.argv[1]

    asm = Assembler(in_file)
    asm.assemble()

main()