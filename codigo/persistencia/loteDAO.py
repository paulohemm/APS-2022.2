from persistencia.dao import DAO
from entidade.lote import Lote


class LoteDAO(DAO):
    def __init__(self):
        super().__init__('lote.pkl')

    def add(self, lote: Lote):
        if (isinstance(lote.fabricante, str)) and (lote is not None) \
                and isinstance(lote, Lote):
            super().add(lote.fabricante, lote)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)