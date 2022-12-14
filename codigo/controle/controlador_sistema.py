from telas.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_vacinas import ControladorVacinas
from controle.controlador_enfermeiros import ControladorEnfermeiros
from controle.controlador_agendamentos import ControladorAgendamentos
from controle.controlador_lote import ControladorLote


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema(self)
        self.__controlador_vacinas = ControladorVacinas(self)
        self.__controlador_lote = ControladorLote(self)
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_enfermeiros = ControladorEnfermeiros(self)
        self.__controlador_agendamentos = ControladorAgendamentos(self)
        


    @property
    def controlador_pacientes(self):
        return self.__controlador_pacientes
    @property
    def controlador_vacinas(self):
        return self.__controlador_vacinas
    @property
    def controlador_lote(self):
        return self.__controlador_lote    
    @property
    def controlador_enfermeiros(self):
        return self.__controlador_enfermeiros

    def inicializa_sistema(self):
        self.abre_tela()

    def opcoes_pacientes(self):
        self.__controlador_pacientes.abre_tela()

    def opcoes_vacinas(self):
        self.__controlador_vacinas.abre_tela()

    def opcoes_lote(self):
        self.__controlador_lote.abre_tela()

    def opcoes_enfermeiros(self):
        self.__controlador_enfermeiros.abre_tela()

    def opcoes_agendamentos(self):
        self.__controlador_agendamentos.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.opcoes_pacientes,
            2: self.opcoes_vacinas,
            3: self.opcoes_lote,
            4: self.opcoes_enfermeiros,
            5: self.opcoes_agendamentos,
            0: self.encerra_sistema
        }
        
        while True:
            lista_opcoes[self.__tela_sistema.tela_opcoes()]()
