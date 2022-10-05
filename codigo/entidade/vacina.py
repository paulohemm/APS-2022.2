class Vacina:
    def __init__(self, fabricante: str, quantidade: int=0):
        if isinstance(fabricante, str):
            self.__fabricante = fabricante
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
    def quantidade(self) -> str:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        if isinstance(quantidade, int):
            self.__quantidade = quantidade

    def adiciona_quantidade(self, quantidade):
        self.__quantidade += quantidade
