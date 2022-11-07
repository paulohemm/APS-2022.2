from telas.tela_lote import TelaLote
from entidade.lote import Lote
from persistencia.loteDAO import LoteDAO


class ControladorLote():

    def __init__(self, controlador_sistema):
        self.__dao = LoteDAO()
        self.__tela_lote = TelaLote(self)
        self.__controlador_sistema = controlador_sistema
        self.__controlador_agendamentos = None
        self.__mantem_tela_aberta = True

    def cadastrar_lote(self):
        dados_lote = self.__tela_lote.pegar_dados_cadastrar()
        if dados_lote is None:
            return None
        if not self.__dao.get_all():
            lote = Lote(dados_lote["fabricante"], dados_lote["numero_de_doses"], dados_lote["periodo_dose_seguinte"])
            self.__dao.add(lote)
            self.__tela_lote.lote_cadastrado()
        else:
            if self.__dao.get(dados_lote["id_lote"]):
                self.__tela_lote.lote_ja_cadastrado()
                return None
            else:
                lote = Lote(dados_lote["fabricante"], dados_lote["numero_de_doses"],dados_lote["periodo_dose_seguinte"])
                self.__dao.add(lote)
                self.__tela_lote.lote_cadastrado()

    def get_lote(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_lote.lista_vazia()
            return None
        else:
            lista_de_vacinas = self.__dao.get_all()
            fabricante = self.__tela_lote.selecionar_vacina(lista_de_vacinas)
            if fabricante is None:
                return None
            if self.__dao.get(fabricante):
                return self.__dao.get(fabricante)
            else:
                self.__tela_lote.vacina_nao_cadastrada()
                return None

    def editar_lote(self):
        vacina = self.get_lote()
        if vacina is not None:
            quantidade = self.__tela_lote.pegar_quantidade()
            vacina.quantidade = quantidade
            self.__dao.add(vacina)

    def remover_lote(self):
        vacina = self.__tela_lote()
        if vacina is not None:
            self.__dao.remove(vacina.fabricante)

    def listar_doses_disponiveis(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_lote.lista_vazia()
        else:
            dados_vacinas = self.__dao.get_all()
            self.__tela_lote.mostrar_doses_disponiveis(dados_vacinas)


    def salvar_lote(self, vacina):
        self.__dao.add(vacina)

    def retorna_tela_principal(self):
        self.__mantem_tela_aberta = False

    def abre_tela(self):
        self.__mantem_tela_aberta = True
        lista_opcoes = {
            1: self.cadastrar_lote,
            2: self.editar_lote,
            3: self.remover_lote,
            4: self.listar_doses_disponiveis,
            0: self.retorna_tela_principal
        }

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_lote.tela_opcoes()]()
