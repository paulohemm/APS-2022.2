from persistencia import DAO
from entidade import Enfermeiro


class EnfermeiroDAO(DAO):
    def __init__(self):
        super().__init__('enfermeiro.pkl')

    def add(self, enfermeiro: Enfermeiro):
        if (isinstance(enfermeiro.cpf, str)) and (enfermeiro is not None) \
                and isinstance(enfermeiro, Enfermeiro):
            super().add(enfermeiro.cpf, enfermeiro)
    
    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
