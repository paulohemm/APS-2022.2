from telas.tela_vacinas import TelaVacinas
from entidade.vacina import Vacina
from persistencia.vacinaDAO import VacinaDAO


class ControladorVacinas():

    def __init__(self, controlador_sistema):
        self.__dao = VacinaDAO()
        self.__tela_vacinas = TelaVacinas(self)
        self.__controlador_sistema = controlador_sistema
        self.__controlador_agendamentos = None
        self.__mantem_tela_aberta = True

    def cadastrar_vacina(self):
        dados_vacina = self.__tela_vacinas.pegar_dados_cadastrar()
        if dados_vacina is None:
            return None
        if not self.__dao.get_all():
            vacina = Vacina(dados_vacina["fabricante"], dados_vacina["quantidade"])
            self.__dao.add(vacina)
            self.__tela_vacinas.vacina_cadastrada()
        else:
            if self.__dao.get(dados_vacina["fabricante"]):
                self.__tela_vacinas.vacina_ja_cadastrada()
                return None
            else:
                vacina = Vacina(dados_vacina["fabricante"], dados_vacina["quantidade"])
                self.__dao.add(vacina)
                self.__tela_vacinas.vacina_cadastrada()

    def get_vacina(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_vacinas.lista_vazia()
            return None
        else:
            lista_de_vacinas = self.__dao.get_all()
            fabricante = self.__tela_vacinas.selecionar_vacina(lista_de_vacinas)
            if fabricante is None:
                return None
            if self.__dao.get(fabricante):
                return self.__dao.get(fabricante)
            else:
                self.__tela_vacinas.vacina_nao_cadastrada()
                return None

    def editar_vacina(self):
        vacina = self.get_vacina()
        if vacina is not None:
            quantidade = self.__tela_vacinas.pegar_quantidade()
            vacina.quantidade = quantidade
            self.__dao.add(vacina)

    def remover_vacina(self):
        vacina = self.get_vacina()
        if vacina is not None:
            self.__dao.remove(vacina.fabricante)

    def listar_doses_disponiveis(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_vacinas.lista_vazia()
        else:
            dados_vacinas = self.__dao.get_all()
            self.__tela_vacinas.mostrar_doses_disponiveis(dados_vacinas)


    def salvar_vacina(self, vacina):
        self.__dao.add(vacina)

    def retorna_tela_principal(self):
        self.__mantem_tela_aberta = False

    def abre_tela(self):
        self.__mantem_tela_aberta = True
        lista_opcoes = {
            1: self.cadastrar_vacina,
            2: self.editar_vacina,
            3: self.remover_vacina,
            4: self.listar_doses_disponiveis,
            0: self.retorna_tela_principal
        }

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_vacinas.tela_opcoes()]()
