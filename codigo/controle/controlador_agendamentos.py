from telas.tela_agendamentos import TelaAgendamentos
from entidade.agendamento import Agendamento
from datetime import datetime
from persistencia.agendamentoDAO import AgendamentoDAO
from persistencia.pacienteDAO import PacienteDAO

class ControladorAgendamentos():

    def __init__(self, controlador_sistema):
        self.__dao = AgendamentoDAO()
        self.__paciente_dao = PacienteDAO()
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
        if dados_agendamento["data"] < datetime.date(datetime.now()):
            self.__tela_agendamentos.agendamento_com_data_anterior()
            return None
        # if [(dados_agendamento["data"] == datetime.date(datetime.now())) and (dados_agendamento["horario"]) < datetime.time(datetime.now())]:
        #     self.__tela_agendamentos.agendamento_com_data_anterior()
        #     return None
        while True:
            paciente = self.__controlador_pacientes.get_paciente()
            if paciente is None:
                break
            codigo_primeiro_agendamento = str(1)+str(paciente.cpf)
            if dados_agendamento["dose"] == 1:
                codigo = str(dados_agendamento["dose"]) + str(paciente.cpf)
                if self.__dao.get(codigo):
                    self.__tela_agendamentos.ja_castrado_primeira_dose()
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
                for agendamento in self.__dao.get_all():
                    if (agendamento.enfermeiro.nome_completo == enfermeiro.nome_completo and dados_agendamento["data"] == agendamento.data and dados_agendamento["horario"] == agendamento.horario):
                        self.__tela_agendamentos.enfermeiro_ja_possui_um_agendamento()
                        return None
            lote = self.__controlador_lote.get_lote()
            if lote is None:
                return None
            if dados_agendamento["data"] > lote.data_vencimento:
                self.__tela_agendamentos.lote_fora_de_validade()
                break
            if dados_agendamento["dose"] == 2:
                vacina = lote.vacina
            else:
                if lote is None:
                    break
            if lote.quantidade < 1:
                self.__tela_agendamentos.doses_insuficientes()
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
    
    @property
    def paciente_dao(self):
        return self.__paciente_dao.get_all()

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

    def aplicar_vacina(self):
        agendamento = self.get_agendamento_today()
        if agendamento is None:
            return None
        agendamento.aplicada = True
        lista_pacientes = self.__paciente_dao.get_all()
        for paciente in lista_pacientes:
            if paciente.cpf == agendamento.paciente.cpf:
                paciente.dose_vacina = agendamento.dose
        self.__controlador_pacientes.teste_pacientes(paciente)
        self.__dao.add(agendamento)
        self.__tela_agendamentos.vacina_aplicada()

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

    def relatorio_agendamentos_por_data(self):
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
            agendamento_por_data = []
            data_selecionada = self.__tela_agendamentos.capturar_data_relatorio()
            try:
                for agendamento in agendamentos_abertos:
                    if agendamento.data == data_selecionada["data"]:
                        agendamento_por_data.append(agendamento)
                if agendamento_por_data != []:
                    self.__tela_agendamentos.mostrar_lista_agendamentos(agendamento_por_data)
                else:
                    self.__tela_agendamentos.sem_agendamento_para_a_data_seleciona()
                    return None
            except:
                return None

    def retorna_tela_principal(self):
        self.__mantem_tela_aberta = False

    def abre_tela(self):
        self.__mantem_tela_aberta = True
        lista_opcoes = {
            1: self.cadastrar_agendamento,
            2: self.listar_agendamentos_abertos,
            3: self.aplicar_vacina,
            4: self.listar_aplicacoes_efetivadas,
            5: self.relatorio_agendamentos_por_data,
            0: self.retorna_tela_principal
        }

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_agendamentos.tela_opcoes()]()
