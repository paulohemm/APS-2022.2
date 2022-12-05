from telas.tela_lote import TelaLote
from datetime import datetime as datetime
from entidade.lote import Lote
from persistencia.loteDAO import LoteDAO


class ControladorLote():

    def __init__(self, controlador_sistema):
        self.__dao = LoteDAO()
        self.__tela_lote = TelaLote(self)
        self.__controlador_sistema = controlador_sistema
        self.__controlador_vacinas = self.__controlador_sistema.controlador_vacinas
        self.__controlador_agendamentos = None
        self.__mantem_tela_aberta = True

    def cadastrar_lote(self):
        while True:
            dados_lote = self.__tela_lote.pegar_dados_cadastrar()
            try:
                data_recebimento_str = dados_lote["data_recebimento"]
                data_recebimento_obj = datetime.strptime(data_recebimento_str, '%d/%m/%Y').date()
                data_vencimento_str = dados_lote["data_vencimento"]
                data_vencimento_obj = datetime.strptime(data_vencimento_str, '%d/%m/%Y').date()
            except:
                self.__tela_lote.mensagem('Data inválida, a data deve ser inserida neste formato: 11/11/2011')
                break
            if dados_lote is None:
                return None
            lista_de_vacinas = self.__controlador_vacinas.lista_de_vacinas()
            for vacina in lista_de_vacinas:
                if vacina is None:
                    self.__tela_lote.lote_nao_cadastrado()
                    return None
                else:
                    if vacina.fabricante == dados_lote["fabricante"]:
                        salvar_vacina = vacina
                        break
                    else:
                        self.__tela_lote.lote_nao_cadastrado()
                        return None
            if not self.__dao.get_all():
                lote = Lote(salvar_vacina, dados_lote["id_lote"], data_recebimento_obj, data_vencimento_obj,
                            dados_lote["quantidade"])
                self.__dao.add(lote)
                self.__tela_lote.lote_cadastrado()
                break
            else:
                if self.__dao.get(dados_lote["id_lote"]):
                    self.__tela_lote.lote_ja_cadastrado()
                    return None
                else:
                    lote = Lote(salvar_vacina, dados_lote["id_lote"], data_recebimento_obj, data_vencimento_obj, dados_lote["quantidade"])
                    self.__dao.add(lote)
                    self.__tela_lote.lote_cadastrado()
                    break


    def get_lote(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_lote.lista_vazia()
            return None
        else:
            lista_de_lotes = self.__dao.get_all()
            id_lote = self.__tela_lote.selecionar_lote(lista_de_lotes)
            if id_lote is None:
                return None
            if self.__dao.get(id_lote):
                return self.__dao.get(id_lote)
            else:
                self.__tela_lote.lote_nao_cadastrado()
                return None

    # def adicionar_dose(self):
    #     lote = self.get_lote()
    #     if lote is not None:
    #         quantidade = self.__tela_lote.pegar_quantidade()
    #         if quantidade is not None:
    #             lote.quantidade += quantidade
    #             self.__dao.add(lote)
    #
    # def subtrair_dose(self):
    #     lote = self.get_lote()
    #     if lote is not None:
    #         quantidade = self.__tela_lote.pegar_quantidade()
    #         if quantidade > lote.quantidade:
    #             self.__tela_lote.quantidade_insuficiente(lote.quantidade)
    #         else:
    #             lote.quantidade -= quantidade
    #             self.__dao.add(lote)

    def editar_lote(self):
        lote = self.get_lote()
        if lote is not None:
            dados_lote = self.__tela_lote.pegar_dados_editar()
            try:
                data_recebimento_str = dados_lote["data_recebimento"]
                lote.data_recebimento = datetime.strptime(data_recebimento_str, '%d/%m/%Y').date()
            except:
                self.__tela_lote.mensagem('Data recebimento inválida, o valor seguirá sendo o original')
            try:
                data_vencimento_str = dados_lote["data_vencimento"]
                lote.data_vencimento = datetime.strptime(data_vencimento_str, '%d/%m/%Y').date()
            except:
                self.__tela_lote.mensagem('Data validade inválida, o valor seguirá sendo o original')
            if dados_lote is None:
                return None
            try:
                lote.quantidade = int(dados_lote["quantidade"])
            except:
                self.__tela_lote.mensagem('Quantidade inválida, o valor seguirá sendo o original')
            self.__dao.add(lote)

    def remover_lote(self):
        lote = self.get_lote()
        if lote is not None:
            self.__dao.remove(lote.id_lote)

    def listar_doses_disponiveis(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_lote.lista_vazia()
        else:
            dados_lote = self.__dao.get_all()
            print(dados_lote)
            self.__tela_lote.mostrar_doses_disponiveis(dados_lote)


    def salvar_lote(self, lote):
        self.__dao.add(lote)

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
