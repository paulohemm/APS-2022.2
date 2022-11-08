from entidade.vacina import Vacina
from datetime import date as Date


class Lote:
    def __init__(self, fabricante: str, id_lote: str, data_recebimento: Date, data_vencimento: Date, quantidade: int = 0):
        if isinstance(fabricante, str):
            self.__fabricante = fabricante
        if isinstance(id_lote, str):
            self.__id_lote = id_lote
        if isinstance(data_recebimento, Date):
            self.__data_recebimento = data_recebimento
        if isinstance(data_vencimento, Date):
            self.__data_vencimento = data_vencimento
        if isinstance(quantidade, int):
            self.__quantidade = quantidade

    @property
    def fabricante(self) -> str:
        return self.__fabricante

    @fabricante.setter
    def fabricante(self, fabricante):
        if isinstance(fabricante, str):
            self.__fabricante = fabricante

    @property
    def id_lote(self) -> str:
        return self.__id_lote

    @id_lote.setter
    def id_lote(self, id_lote):
        if isinstance(id_lote, str):
            self.__id_lote = id_lote

    @property
    def data_recebimento(self) -> Date:
        return self.__data_recebimento

    @data_recebimento.setter
    def data_recebimento(self, data_recebimento):
        if isinstance(data_recebimento, Date):
            self.__data_recebimento = data_recebimento

    @property
    def data_vencimento(self) -> Date:
        return self.__data_vencimento

    @data_vencimento.setter
    def data_vencimento(self, data_vencimento):
        if isinstance(data_vencimento, Date):
            self.__data_vencimento = data_vencimento

    @property
    def quantidade(self) -> int:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        if isinstance(quantidade, int):
            self.__quantidade = quantidade

    def adiciona_quantidade(self, quantidade):
        self.__quantidade += quantidade

    def subtrai_quantidade(self, quantidade):
        self.__quantidade -= quantidade
