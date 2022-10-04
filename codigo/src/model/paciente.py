from .pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, cpf, nome_completo, data_nascimento, telefone, dose_vacina, fabricante_vacina, lote_vacina):
        super().__init__(cpf, nome_completo, data_nascimento, telefone)
        self.__dose_vacina = 0
        self.__fabricante_vacina = ''
        self.__lote_vacina = ''

    @property
    def dose_vacina(self):
        return self.__dose_vacina

    @dose_vacina.setter
    def dose_vacina(self, dose_vacina):
        self.__dose_vacina = dose_vacina

    @property
    def fabricante_vacina(self):
        return self.__fabricante_vacina

    @fabricante_vacina.setter
    def fabricante_vacina(self, fabricante_vacina):
        self.__fabricante_vacina = fabricante_vacina

    @property
    def fabricante_vacina(self):
        return self.__fabricante_vacina

    @fabricante_vacina.setter
    def fabricante_vacina(self, fabricante_vacina):
        self.__fabricante_vacina = fabricante_vacina

    @property
    def lote_vacina(self):
        return self.__lote_vacina

    @lote_vacina.setter
    def lote_vacina(self, lote_vacina):
        self.__lote_vacina = lote_vacina


