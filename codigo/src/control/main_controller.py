from .control_paciente import PacienteController
from ..view.main_view import TelaSistemaView


class MainController:

    def __init__(self):
        self.__view = TelaSistemaView()
        self.__controller_paciente = PacienteController()
        

    def run(self):
        escolha = 'x'
        while escolha != 'Sair' and escolha != None:
            opcoes = {
                    'Paciente': self.__controller_paciente.option,
                    }
            escolha = self.__view.menu_principal()
            try:
                opcoes[escolha]()
            except KeyError:
                return
    
   


