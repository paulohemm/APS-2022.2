from entidade.vacina import Vacina
from entidade.enfermeiro import Enfermeiro
from entidade.paciente import Paciente
from entidade.lote import Lote
from datetime import date
from datetime import time


class Agendamento:
    def __init__(
        self,
        enfermeiro: Enfermeiro,
        paciente: Paciente,
        lote: Lote,
        data: date,
        horario: time,
        dose: int
    ):
        self.__enfermeiro = enfermeiro
        self.__paciente = paciente
        self.__lote = lote
        self.__data = data
        self.__horario = horario
        self.__dose = dose
        self.__aplicada = False
        self.__codigo = str(str(self.__dose)+str(self.__paciente.cpf))

    @property
    def enfermeiro(self) -> Enfermeiro:
        return self.__enfermeiro

    @enfermeiro.setter
    def enfermeiro(self, enfermeiro):
        if isinstance(enfermeiro, Enfermeiro):
            self.__enfermeiro = enfermeiro

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente):
        if isinstance(paciente, Paciente):
            self.__paciente = paciente

    @property
    def lote(self) -> Lote:
        return self.__lote

    @lote.setter
    def lote(self, lote):
        if isinstance(lote, Lote):
            self.__lote = lote

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data):
        if isinstance(data, date):
            self.__data = data

    @property
    def horario(self) -> time:
        return self.__horario

    @horario.setter
    def horario(self, horario):
        if isinstance(horario, time):
            self.__horario = horario

    @property
    def dose(self) -> int:
        return self.__dose

    @dose.setter
    def dose(self, dose):
        if isinstance(dose, int):
            self.__dose = dose

    @property
    def aplicada(self) -> bool:
        return self.__aplicada

    @aplicada.setter
    def aplicada(self, aplicada):
        if isinstance(aplicada, bool):
            self.__aplicada = aplicada
    
    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if isinstance(codigo, str):
            self.__codigo = codigo
