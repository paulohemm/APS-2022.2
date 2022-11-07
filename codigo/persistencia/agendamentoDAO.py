from persistencia.dao import DAO
from entidade.agendamento import Agendamento


class AgendamentoDAO(DAO):
    def __init__(self):
        super().__init__('agendamentos.pkl')

    def add(self, agendamento: Agendamento):
        if (isinstance(agendamento.codigo, str)) and (agendamento is not None) \
                and isinstance(agendamento, Agendamento):
            super().add(agendamento.codigo, agendamento)
    
    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
