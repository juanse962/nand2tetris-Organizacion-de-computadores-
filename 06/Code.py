class Code(object):
    """
    Clase Code va contener los Token va a generar el codigo para cada
    instruccion en numeros binarios
    """

    _dest_codes = ['','M','D','MD','A','AM','AD','AMD',]
    _comp_codes = {'0': '0101010','1': '0111111','-1': '0111010','D': '0001100',
                   'A': '0110000','!D': '0001101','!A': '0110001','-D': '0001111',
                   '-A': '0110011','D+1': '0011111','A+1': '0110111','D-1': '0001110',
                   'A-1': '0110010','D+A': '0000010','D-A': '0010011','A-D': '0000111',
                   'D&A': '0000000','D|A': '0010101','': 'xxxxxxx','M': '1110000','!M': '1110001'
                   ,'-M': '1110011','M+1': '1110111','M-1': '1110010','D+M': '1000010',
                   'D-M': '1010011','M-D': '1000111','D&M': '1000000','D|M': '1010101',
        }
    _jump_codes = ['','JGT','JEQ','JGE','JLT','JNE','JLE','JMP',]

    def __init__(self):
        """Constructor"""
        pass

    def gen_a_code(self, address):
        """Genera el codigo binario para cada instruccion tipo a"""
        return '0' + self._bits(address).zfill(15)

    def gen_c_code(self,comp,dest,jump,):
        """Retorna el codigo para intrucciones tipo c"""
        return '111' + self.comp(comp) + self.dest(dest) \
            + self.jump(jump)

    def dest(self, mnemonic):
        """Retorna el dest en memoria"""
        return self._bits(self._dest_codes.index(mnemonic)).zfill(3)

    def comp(self, mnemonic):
        """Retorna el comp en memoria"""
        return self._comp_codes[mnemonic]

    def jump(self, mnemonic):
        """Retorna el jump en memoria"""
        return self._bits(self._jump_codes.index(mnemonic)).zfill(3)

    @staticmethod
    def _bits(num):
        """Convierte el numero en binario"""
        return bin(int(num))[2:]
