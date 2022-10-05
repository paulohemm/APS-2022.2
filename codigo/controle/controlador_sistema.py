from telas.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_vacinas import ControladorVacinas



class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema(self)
        self.__controlador_vacinas = ControladorVacinas(self)
        self.__controlador_pacientes = ControladorPacientes(self)

    @property
    def controlador_pacientes(self):
        return self.__controlador_pacientes
    @property
    def controlador_vacinas(self):
        return self.__controlador_vacinas

    def inicializa_sistema(self):
        self.abre_tela()

    def opcoes_pacientes(self):
        self.__controlador_pacientes.abre_tela()

    def opcoes_vacinas(self):
        self.__controlador_vacinas.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.opcoes_pacientes,
            2: self.opcoes_vacinas,
            0: self.encerra_sistema
        }
        
        while True:
            lista_opcoes[self.__tela_sistema.tela_opcoes()]()
