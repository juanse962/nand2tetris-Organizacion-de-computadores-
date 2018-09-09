import re

class Parser(object):

    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    _comment = re.compile(r'//.*$')

    def __init__(self, in_file):
        """Sé lee el archivo"""
        with open(in_file, 'r') as myf:
            self.lines = myf.readlines()
        self.command = ''
        self.cur_line = 0

    def has_more_commands(self):
        """Returna TRUE si hay mas de una linea"""
        if (self.cur_line + 1) < len(self.lines):
            return True
        else:
            return False

    def advance(self):
        """Va leyendo las lineas del archivo desde la linea actual"""
        self.cur_line += 1
        line = self.lines[self.cur_line]
        line = self._comment.sub('', line)
        if line == '\n':
            self.advance()
        else:
            self.command = line.strip()

    def command_type(self):
        """Returna el tipo de instrucción"""
        if re.match(r'^@.*', self.command):
            return Parser.A_COMMAND
        elif re.match(r'^\(.*', self.command):
            return Parser.L_COMMAND
        else:
            return Parser.C_COMMAND

    def symbol(self):
        """Retorna el simbolo actual por el que va leyendo el archivo"""
        matching = re.match(r'^[@\(](.*?)\)?$', self.command)
        symbol = matching.group(1)
        return symbol

    def dest(self):
        """Retorna el destino de la memoria"""
        matching = re.match(r'^(.*?)=.*$', self.command)
        if not matching:
            dest = ''
        else:
            dest = matching.group(1)
        return dest


    def comp(self):
        """Returna el comp en la instruccion si esta y si no imprime su error"""
        comp = re.sub(r'^.*?=', '', self.command)
        comp = re.sub(r';\w+$', '', comp)
        if not comp:
            print("UPS hay un error")
            print(self.command)
        return comp.strip()

    def jump(self):
        """Returna el JUMP en memoria si hay"""
        matching = re.match(r'^.*;(\w+)$', self.command)
        if not matching:
            jump = ''
        else:
            jump = matching.group(1)
        return jump
