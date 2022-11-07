from entidade.lote import Lote

class Vacina:
    def __init__(self, fabricante: str, lote: Lote ,numero_de_doses: int=1, periodo_dose_seguinte: int=0):
        if isinstance(fabricante, str):
            self.__fabricante = fabricante
        # if isinstance(quantidade, int):
        #     self.__quantidade = quantidade
        if isinstance(numero_de_doses, int):
            self.__numero_de_doses = numero_de_doses
        if isinstance(periodo_dose_seguinte, int):
            self.__periodo_dose_seguinte = periodo_dose_seguinte

    @property
    def fabricante(self) -> str:
        return self.__fabricante

    @fabricante.setter
    def fabricante(self, fabricante):
        if isinstance(fabricante, str):
            self.__fabricante = fabricante

    # @property
    # def quantidade(self) -> str:
    #     return self.__quantidade
    #
    # @quantidade.setter
    # def quantidade(self, quantidade):
    #     if isinstance(quantidade, int):
    #         self.__quantidade = quantidade

    def adiciona_quantidade(self, quantidade):
        self.__quantidade += quantidade

    @property
    def numero_de_doses(self) -> int:
        return self.__numero_de_doses

    @numero_de_doses.setter
    def numero_de_doses(self, numero_de_doses):
        if isinstance(numero_de_doses, int):
            self.__numero_de_doses = numero_de_doses

    @property
    def periodo_dose_seguinte(self) -> int:
        return self.__periodo_dose_seguinte

    @numero_de_doses.setter
    def periodo_dose_seguinte(self, periodo_dose_seguinte):
        if isinstance(periodo_dose_seguinte, int):
            self.__periodo_dose_seguinte = periodo_dose_seguinte