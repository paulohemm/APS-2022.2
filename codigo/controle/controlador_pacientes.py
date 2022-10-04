from limite.tela_pacientes import TelaPacientes
from entidade.paciente import Paciente
from datetime import datetime as datetime
from math import trunc
from persistencia.pacienteDAO import PacienteDAO


class ControladorPacientes():

    def __init__(self, controlador_sistema):
        self.__dao = PacienteDAO()
        self.__tela_pacientes = TelaPacientes(self)
        self.__controlador_sistema = controlador_sistema
        self.__mantem_tela_aberta = True

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    def pacientes(self):
        return self.__dao.get_all()

    def cadastrar_paciente(self):
        while True:
            dados_paciente = self.__tela_pacientes.pegar_dados_cadastrar()
            if dados_paciente is None:
                break
            try:
                nome = dados_paciente["nome"].upper()
                if not nome.replace(' ', '').isalpha():
                    break
            except (ValueError, TypeError):
                self.__tela_pacientes.mensagem('Houve problemas com o tipo de dado digitado')
            try:
                cpf = dados_paciente["cpf"].replace(' ', '')
                if not (cpf.isnumeric() and len(cpf) == 11):
                    self.__tela_pacientes.mensagem(f'O cpf {cpf} é inválido!\nDigite um cpf com 11 dígitos')
                    break
            except (ValueError, TypeError):
                self.__tela_pacientes.mensagem('Houve problemas com o tipo de dado digitado')
            try:
                data_nascimento_str = dados_paciente["data_nascimento"]
                data_nascimento_obj = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
                idade_dias = datetime.today().date() - data_nascimento_obj
                idade = int(idade_dias.days // 365.24231481481481481481481481481481)
                if not 0 < idade < 150:
                    self.__tela_pacientes.mensagem('Idade inválida, a idade deve ser entre 0 e 150 anos')
                    break
            except:
                self.__tela_pacientes.mensagem('Data inválida, a data deve ser inserida neste formato: 11/11/2011')
                break
            if len(self.__dao.get_all()) == 0:
                self.__tela_pacientes.mensagem(f'Paciente {nome} cadastrado')

                paciente = Paciente(nome, cpf, data_nascimento_obj)
                self.__dao.add(paciente)
                break
            else:
                for paciente in self.__dao.get_all():
                    if not dados_paciente:
                        self.__tela_pacientes.mensagem()
                        return None
                    if dados_paciente["cpf"] == paciente.cpf:
                        self.__tela_pacientes.mensagem(f'O cpf {dados_paciente["cpf"]} já foi cadastrado')
                        return None
                paciente = Paciente(nome, cpf, data_nascimento_obj)
                self.__dao.add(paciente)
                self.__tela_pacientes.sucesso(nome, cpf, data_nascimento_obj)
                break

    def editar_paciente(self, nome=0, cpf=0, data_nascimento=0):
        paciente_editar = self.get_paciente()
        # rever
        if paciente_editar is None:
            return None
        dados_editar = self.__tela_pacientes.pegar_dados_cadastrar()
        try:
            nome = dados_editar["nome"].upper()
            if nome.replace(' ', '').isalpha():
                nome_ok = nome
        except (ValueError, TypeError):
            self.__tela_pacientes.mensagem('Houve problemas com o tipo de dado digitado')
            return None
        try:
            data_nascimento_str = dados_editar["data_nascimento"]
            data_nascimento_obj = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
            idade_dias = datetime.today().date() - data_nascimento_obj
            idade = int(idade_dias.days // 365.24231481481481481481481481481481)
            if not 0 < idade < 150:
                self.__tela_pacientes.mensagem('Idade inválida, a idade deve ser entre 0 e 150 anos')
                return None
        except:
            self.__tela_pacientes.mensagem('Data inválida, a data deve ser inserida neste formato: 11/11/2011')
        paciente_editar.nome = nome_ok
        paciente_editar.data_nascimento = data_nascimento_obj
        self.__dao.add(paciente_editar)
        self.__tela_pacientes.sucesso(paciente_editar.nome, paciente_editar.cpf, data_nascimento_obj)

    def get_paciente(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_pacientes.nenhum_paciente()
            return None
        else:
            cpf = self.selecionar_lista_pacientes()
            if cpf is None:
                return None
            if self.__dao.get(cpf):
                return self.__dao.get(cpf)
            else:
                self.__tela_pacientes.cpf_nao_cadastrado(cpf)
        return None

    def selecionar_lista_pacientes(self):
        matriz = []
        linha = ['        Nome        ', '    CPF    ', 'Idade']
        matriz.append(linha)
        if len(self.__dao.get_all()) == 0:
            self.__tela_pacientes.nenhum_paciente()
            return None
        for paciente in self.__dao.get_all():
            linha = [paciente.nome, paciente.cpf]
            idade_dias = datetime.today().date() - paciente.data_nascimento
            idade = int(idade_dias.days // 365.24231481481481481481481481481481)
            linha.append(idade)
            matriz.append(linha)
        paciente_selecionado = self.__tela_pacientes.selecionar_paciente_tabela(matriz, 'Selecionar Pacientes')
        if paciente_selecionado:
            return matriz[paciente_selecionado[0] + 1][1]

    def listar_pacientes(self):
        matriz = []
        linha = ['        Nome        ', '    CPF    ', 'Idade']
        matriz.append(linha)
        if len(self.__dao.get_all()) == 0:
            self.__tela_pacientes.nenhum_paciente()
            return None
        for paciente in self.__dao.get_all():
            linha = [paciente.nome, paciente.cpf]
            idade_dias = datetime.today().date() - paciente.data_nascimento
            idade = int(idade_dias.days // 365.24231481481481481481481481481481)
            linha.append(idade)
            matriz.append(linha)
        self.__tela_pacientes.listar_paciente_tabela(matriz, 'Lista de pacientes')

   

    def remover_paciente(self):
        paciente = self.get_paciente()
        # for agendamento in self.__controlador_agendamentos.agendamentos:
        #     if agendamento.paciente == paciente:
        #         return None
        if paciente is not None:
            self.__dao.remove(paciente.cpf)

    def retorna_tela_principal(self):
        self.__mantem_tela_aberta = False

    def abre_tela(self):
        self.__mantem_tela_aberta = True
        lista_opcoes = {1: self.cadastrar_paciente,
                        2: self.editar_paciente,
                        3: self.listar_pacientes,
                        4: self.remover_paciente,
                        5: self.retorna_tela_principal}

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_pacientes.tela_opcoes()]()
