from persistencia.dao import DAO
from entidade.vacina import Vacina


class AplicacaoDAO(DAO):
    def __init__(self):
        super().__init__('aplicacao.pkl')

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)
