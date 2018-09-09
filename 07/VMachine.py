!/usr/bin/env python
import os# https://docs.python.org/2/library/os.html documentación del modulo

COMMENT = '//'
#Lellendo el archivo
class Parser(object):
    def __init__(self, vm_filename):
        self.vm_filename = vm_filename
        self.vm = open(vm_filename, 'r')
        self.commands = self.commands_dict()
        self.curr_instruction = None
        self.initialize_file()
    """Utilizo el modulo os de python"""
    def advance(self):
        self.curr_instruction = self.next_instruction
        self.load_next_instruction()

    @property
    def has_more_commands(self):
        return bool(self.next_instruction)

    @property
    def command_type(self):
        return self.commands.get(self.curr_instruction[0].lower())

    @property
    def arg1(self):
        if self.command_type == 'C_ARITMETICA':
            return self.argn(0)
        return self.argn(1)

    @property
    def arg2(self):
        return self.argn(2)
    """Fin de la utilizacion de el modulo"""

    def initialize_file(self):
        self.vm.seek(0)
        line = self.vm.readline().strip()
        while not self.is_instruction(line):
            line = self.vm.readline().strip()
        self.load_next_instruction(line)

    def load_next_instruction(self, line=None):
        line = line if line is not None else self.vm.readline().strip()
        self.next_instruction = line.split(COMMENT)[0].strip().split()

    def is_instruction(self, line):
        return line and line[:2] != COMMENT

    def argn(self, n):
        if len(self.curr_instruction) >= n+1:
            return self.curr_instruction[n]
        return None

    def commands_dict(self):
        return {'add': 'C_ARITMETICA',
                'sub': 'C_ARITMETICA',
                'neg': 'C_ARITMETICA',
                'eq': 'C_ARITMETICA',
                'gt': 'C_ARITMETICA',
                'lt': 'C_ARITMETICA',
                'and': 'C_ARITMETICA',
                'or': 'C_ARITMETICA',
                'not': 'C_ARITMETICA',
                'push': 'C_PUSH',
                'pop': 'C_POP',
                'label': 'C_LABEL',
                'goto': 'C_GOTO',
                'if-goto': 'C_IF',
                'function': 'C_FUNCTION',
                'return': 'C_RETURN',
                'call': 'C_CALL'}

class CodeWriter(object):
    """Escribiendo archivo .asm """
    def __init__(self, asm_filename):
        self.asm = open(asm_filename, 'w')
        self.curr_file = None
        self.bool_count = 0
        self.addresses = self.address_dict()

    def set_file_name(self, vm_filename):
        """Restableciendo SP"""
        self.curr_file = vm_filename.replace('.vm', '').split('/')[-1]

    def write_arithmetic(self, operation):
        """Aplicando operaciones al Stack"""
        if operation not in ['neg', 'not']:
            self.pop_stack_to_D()
        self.decrement_SP()
        self.set_A_to_stack()

        #Operaciones Pila
        if operation == 'add':
            self.write('M=M+D')
        elif operation == 'sub':
            self.write('M=M-D')
        elif operation == 'and':
            self.write('M=M&D')
        elif operation == 'or':
            self.write('M=M|D')
        elif operation == 'neg':
            self.write('M=-M')
        elif operation == 'not':
            self.write('M=!M')
        elif operation in ['eq', 'gt', 'lt']:
            self.write('D=M-D')
            self.write('@BOOL{}'.format(self.bool_count))

            if operation == 'eq':
                self.write('D;JEQ')
            elif operation == 'gt':
                self.write('D;JGT')
            elif operation == 'lt':
                self.write('D;JLT')

            self.set_A_to_stack()
            self.write('M=0')
            self.write('@ENDBOOL{}'.format(self.bool_count))
            self.write('0;JMP')

            self.write('(BOOL{})'.format(self.bool_count))
            self.set_A_to_stack()
            self.write('M=-1')

            self.write('(ENDBOOL{})'.format(self.bool_count))
            self.bool_count += 1
        else:
            self.raise_unknown(operation)
        self.increment_SP()

    def write_push_pop(self, command, segment, index):
        self.resolve_address(segment, index)
        if command == 'C_PUSH': # carga M[address] a D
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')
            self.push_D_to_stack()
        elif command == 'C_POP': # carga D a M[address]
            self.write('D=A')
            self.write('@R13')
            self.write('M=D')
            self.pop_stack_to_D()
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        else:
            self.raise_unknown(command)

    def close(self):
        self.asm.close()

    def write(self, command):
        self.asm.write(command + '\n')

    def raise_unknown(self, argument):
        raise ValueError('{} is an invalid argument'.format(argument))

    def resolve_address(self, segment, index):
        """Direcciones de A register"""
        address = self.addresses.get(segment)
        if segment == 'constant':
            self.write('@' + str(index))
        elif segment == 'static':
            self.write('@' + self.curr_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.write('@R' + str(address + int(index)))
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write('@' + address)
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A')
        else:
            self.raise_unknown(segment)

    def address_dict(self):
        return {'local': 'LCL',
                'argument': 'ARG',
                'this': 'THIS',
                'that': 'THAT',
                'pointer': 3,
                'temp': 5,
                'static': 16,}

    def push_D_to_stack(self):
        """Push y incremento de @SP"""
        self.write('@SP') # obtener direccion stack pointer
        self.write('A=M') # direccion actual del stack pointer
        self.write('M=D') # Escribe dato hasta arriba del stack
        self.write('@SP')
        self.write('M=M+1') #incremento de SP

    def pop_stack_to_D(self):
        """Decremento @SP, pop de arriba del Stack"""
        self.write('@SP')
        self.write('M=M-1') # Decremento SP
        self.write('A=M') # Establecer direccion del SP
        self.write('D=M') # llevar dato hasta arriba de la pila

    def decrement_SP(self):
        self.write('@SP')
        self.write('M=M-1')

    def increment_SP(self):
        self.write('@SP')
        self.write('M=M+1')

    def set_A_to_stack(self):
        self.write('@SP')
        self.write('A=M')


class Main(object):
    def __init__(self, file_path):
        self.parse_files(file_path)
        self.cw = CodeWriter(self.asm_file)
        for vm_file in self.vm_files:
            self.translate(vm_file)

    def parse_files(self, file_path):
        if '.vm' in file_path:
            self.asm_file = file_path.replace('.vm', '.asm')
            self.vm_files = [file_path]
        else:
            file_path = file_path[:-1] if file_path[-1] == '/' else file_path
            path_elements = file_path.split('/')
            path = '/'.join(path_elements)
            self.asm_file = path + '/' + path_elements[-1] + '.asm'
            dirpath, dirnames, filenames = next(os.walk(file_path), [[],[],[]])
            vm_files = filter(lambda x: '.vm' in x, filenames)
            self.vm_files = [path + '/' +  vm_file for vm_file in vm_files]

    def translate(self, vm_file):
        parser = Parser(vm_file)
        self.cw.set_file_name(vm_file)
        while parser.has_more_commands:
            parser.advance()
            self.cw.write('// ' + ' '.join(parser.curr_instruction))
            if parser.command_type == 'C_PUSH':
                self.cw.write_push_pop('C_PUSH', parser.arg1, parser.arg2)
            elif parser.command_type == 'C_POP':
                self.cw.write_push_pop('C_POP', parser.arg1, parser.arg2)
            elif parser.command_type == 'C_ARITMETICA':
                self.cw.write_arithmetic(parser.arg1)


if __name__ == '__main__':
    import sys

    file_path = sys.argv[1]
    Main(file_path)
