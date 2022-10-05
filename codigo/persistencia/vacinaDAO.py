from persistencia.dao import DAO
from entidade.vacina import Vacina


class VacinaDAO(DAO):
    def __init__(self):
        super().__init__('vacinas.pkl')

    def add(self, vacina: Vacina):
        if (isinstance(vacina.fabricante, str)) and (vacina is not None) \
                and isinstance(vacina, Vacina):
            super().add(vacina.fabricante, vacina)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)
