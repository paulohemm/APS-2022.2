from telas.tela_aplicacao import TelaAplicacao
from persistencia.aplicacaoDao import AplicacaoDAO

class ControladorAplicacao():
    def __init__(self, controlador_sistema):
        self.__dao = AplicacaoDAO()
        self.__tela_aplicacao = TelaAplicacao(self)
        self.__controlador_sistema = controlador_sistema
        self.__mantem_tela_aberta = True

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    def aplicar_vacina(self):
        agendamento = self.get_agendamento()
        if agendamento is None:
            return None
        agendamento.aplicada = True
        self.__dao.add(agendamento)
        self.__tela_agendamentos.vacina_aplicada()

    def listar_aplicacoes_efetivadas(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_agendamentos.agendamento_aberto_nao_cadastrado()
            return None
        else:
            aplicacoes_efetivadas = []
            for agendamento in self.__dao.get_all():
                if agendamento.aplicada == True:
                    aplicacoes_efetivadas.append(agendamento)
            if len(aplicacoes_efetivadas) == 0:
                self.__tela_agendamentos.agendamento_aberto_nao_cadastrado()
                return None
            else:
                self.__tela_agendamentos.mostrar_lista_agendamentos(aplicacoes_efetivadas)

    def retorna_tela_principal(self):
        self.__mantem_tela_aberta = False

    def abre_tela(self):
        self.__mantem_tela_aberta = True
        lista_opcoes = {
            1: self.aplicar_vacina,
            2: self.listar_aplicacoes_efetivadas,
            0: self.retorna_tela_principal
        }

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_aplicacao.tela_opcoes()]()
