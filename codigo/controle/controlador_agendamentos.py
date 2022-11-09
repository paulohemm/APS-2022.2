from telas.tela_agendamentos import TelaAgendamentos
from entidade.agendamento import Agendamento
from datetime import datetime
from persistencia.agendamentoDAO import AgendamentoDAO


class ControladorAgendamentos():

    def __init__(self, controlador_sistema):
        self.__dao = AgendamentoDAO()
        self.__tela_agendamentos = TelaAgendamentos(self)
        self.__controlador_sistema = controlador_sistema
        self.__controlador_enfermeiros = self.__controlador_sistema.controlador_enfermeiros
        self.__controlador_pacientes = self.__controlador_sistema.controlador_pacientes
        self.__controlador_vacinas = self.__controlador_sistema.controlador_vacinas
        self.__controlador_lote = self.__controlador_sistema.controlador_lote
        self.__mantem_tela_aberta = True

    def cadastrar_agendamento(self):
        dados_agendamento = self.__tela_agendamentos.pegar_dados_cadastrar()
        if dados_agendamento is None:
            return None
        while True:
            paciente = self.__controlador_pacientes.get_paciente()
            if paciente is None:
                break
            codigo_primeiro_agendamento = str(1)+str(paciente.cpf)
            if dados_agendamento["dose"] == 1:
                codigo = str(dados_agendamento["dose"]) + str(paciente.cpf)
                if self.__dao.get(codigo):
                    self.__tela_agendamentos.ja_cadastrado_segunda_dose()
                    break
            if dados_agendamento["dose"] == 2:
                codigo = str(dados_agendamento["dose"])+str(paciente.cpf)
                if self.__dao.get(codigo):
                    self.__tela_agendamentos.ja_cadastrado_segunda_dose()
                    break
                primeiro_agendamento = self.__dao.get(codigo_primeiro_agendamento)
                if primeiro_agendamento is None:
                    self.__tela_agendamentos.nao_cadastrado_primeira_dose()
                    break
                diferenca_dias = dados_agendamento["data"] - primeiro_agendamento.data
                if diferenca_dias.days <= primeiro_agendamento.lote.vacina.periodo_dose_seguinte:
                    self.__tela_agendamentos.data_recente_primeira_dose(primeiro_agendamento.lote.vacina.periodo_dose_seguinte)
                    return None
            enfermeiro = self.__controlador_enfermeiros.get_enfermeiro()
            if enfermeiro is None:
                break
            if len(self.__dao.get_all()) > 0:
                agendamentos_abertos = []
                for agendamento in self.__dao.get_all():
                    if (agendamento.enfermeiro.nome == enfermeiro.nome and dados_agendamento["data"] == agendamento.data and dados_agendamento["horario"] == agendamento.horario):
                        self.__tela_agendamentos.enfermeiro_ja_possui_um_agendamento()
                        return None
            print(agendamentos_abertos)
            lote = self.__controlador_lote.get_lote()
            if dados_agendamento["dose"] == 2:
                vacina = lote.vacina
            else:
                if lote is None:
                    break
            if lote.quantidade < 1:
                self.__controlador_vacinas.chamar_doses_insuficiente()
                break
            lote.subtrai_quantidade(1)
            self.__controlador_lote.salvar_lote(lote)
            agendamento = Agendamento(enfermeiro, paciente, lote, dados_agendamento["data"], dados_agendamento["horario"], dados_agendamento["dose"])
            self.__dao.add(agendamento)
            self.__tela_agendamentos.agendamento_cadastrado()
            break

    @property
    def agendamentos(self):
        return self.__dao.get_all()

    def get_agendamento(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_agendamentos.lista_vazia()
            return None
        else:
            lista_de_agendamentos = self.__dao.get_all()
            codigo = self.__tela_agendamentos.selecionar_agendamento(lista_de_agendamentos)
            if codigo is None:
                return None
            if self.__dao.get(codigo):
                return self.__dao.get(codigo)
            else:
                self.__tela_agendamentos.agendamento_nao_cadastrado()
                return None

    def get_agendamento_today(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_agendamentos.lista_vazia()
            return None
        else:
            lista_de_agendamentos = self.__dao.get_all()
            nova_lista_agendamentos = []
            for agendamento in lista_de_agendamentos:
                if agendamento.data == datetime.today().date() and agendamento.aplicada == False:
                    nova_lista_agendamentos.append(agendamento)

            if len(nova_lista_agendamentos) == 0:
                self.__tela_agendamentos.lista_vazia_today()
                return None

            codigo = self.__tela_agendamentos.selecionar_agendamento(nova_lista_agendamentos)
            if codigo is None:
                return None
            if self.__dao.get(codigo):
                return self.__dao.get(codigo)
            else:
                self.__tela_agendamentos.agendamento_nao_cadastrado()
                return None

    def editar_agendamento(self):
        agendamento_editar = self.get_agendamento()
        if agendamento_editar is None:
            return None
        dados_agendamento = self.__tela_agendamentos.pegar_dados_editar()
        if dados_agendamento is None:
            return None
        while True:
            if agendamento_editar.dose == 2:
                codigo_primeiro_agendamento = str(1) + str(agendamento_editar.paciente.cpf)
                primeiro_agendamento = self.__dao.get(codigo_primeiro_agendamento)
                if primeiro_agendamento is None:
                    self.__tela_agendamentos.nao_cadastrado_primeira_dose()
                    break
                diferenca_dias = dados_agendamento["data"] - primeiro_agendamento.data
                if diferenca_dias.days <= primeiro_agendamento.lote.vacina.periodo_dose_seguinte:
                    self.__tela_agendamentos.data_recente_primeira_dose(primeiro_agendamento.lote.vacina.periodo_dose_seguinte)
                    return None
            enfermeiro = self.__controlador_enfermeiros.get_enfermeiro()
            if enfermeiro is None:
                break
            if enfermeiro.status == "Inativo":
                self.__controlador_enfermeiros.enfermeiro_inativo()
                break
            if agendamento_editar.dose == 2:
                vacina = primeiro_agendamento.vacina
            else:
                lote = self.__controlador_vacinas.get_lote()
                if lote is None:
                    break
            if lote.quantidade < 1:
                self.__controlador_vacinas.chamar_doses_insuficiente()
                break
            lote.subtrai_quantidade(1)
            agendamento_editar.vacina.adiciona_quantidade(1)
            self.__controlador_vacinas.salvar_vacina(vacina)
            self.__controlador_vacinas.salvar_vacina(agendamento_editar.vacina)
            agendamento_editar.enfermeiro = enfermeiro
            agendamento_editar.vacina = vacina
            agendamento_editar.data = dados_agendamento['data']
            agendamento_editar.horario = dados_agendamento['horario']
            agendamento_editar.aplicada = dados_agendamento['aplicada']
            self.__dao.add(agendamento_editar)
            self.__tela_agendamentos.agendamento_editado()
            break

    def aplicar_vacina(self):
        agendamento = self.get_agendamento_today()
        if agendamento is None:
            return None
        agendamento.aplicada = True
        self.__dao.add(agendamento)
        self.__tela_agendamentos.vacina_aplicada()
                

    def remover_agendamento(self):
        agendamento = self.get_agendamento()
        if agendamento is None:
            return None
        else:
            if not agendamento.aplicada:
                agendamento.vacina.adiciona_quantidade(1)
                self.__dao.remove(agendamento.codigo)
                self.__tela_agendamentos.agendamento_removido()
                self.__controlador_vacinas.salvar_vacina(agendamento.vacina)

    def listar_agendamentos_abertos(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_agendamentos.agendamento_aberto_nao_cadastrado()
            return None
        else:
            agendamentos_abertos = []
            for agendamento in self.__dao.get_all():
                if agendamento.aplicada == False:
                    agendamentos_abertos.append(agendamento)
            if len(agendamentos_abertos) == 0:
                self.__tela_agendamentos.agendamento_aberto_nao_cadastrado()
                return None
            else:
                self.__tela_agendamentos.mostrar_lista_agendamentos(agendamentos_abertos)

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
            1: self.cadastrar_agendamento,
            2: self.listar_agendamentos_abertos,
            3: self.aplicar_vacina,
            4: self.listar_aplicacoes_efetivadas,
            0: self.retorna_tela_principal
        }

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_agendamentos.tela_opcoes()]()
