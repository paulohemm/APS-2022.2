from ..persistence.abstractDAO import AbstractDAO
from ..paciente import Paciente


class PacienteDAO(AbstractDAO):
    def __init__(self):
        super().__init__('pacientes.pkl')
    
    def add(self, paciente: Paciente):
        if isinstance(paciente.cpf, int) and (paciente is not None) and isinstance(paciente, Paciente):
            super().add(paciente, paciente.cpf)
    
    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            super().remove(key)
