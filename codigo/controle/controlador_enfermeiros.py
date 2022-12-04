from telas import TelaEnfermeiros
from entidade import Enfermeiro
from datetime import datetime
from persistencia import EnfermeiroDAO

class ControladorEnfermeiros():
    def __init__(self, controlador_sistema):
        self.__dao = EnfermeiroDAO()
        self.__tela_enfermeiros = TelaEnfermeiros(self)
        self.__controlador_sistema = controlador_sistema
        self.__mantem_tela_aberta = True

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    def enfermeiros(self):
        return self.__dao.get_all()

    def cadastrar_enfermeiro(self):
        while True:
            dados_enfermeiro = self.__tela_enfermeiros.dados_cadastro()
            if (len(dados_enfermeiro["nome"]) + len(dados_enfermeiro["cpf"]) + len(dados_enfermeiro["data_nascimento"]) + len(dados_enfermeiro["matricula_coren"])) == 0:
                self.__tela_enfermeiros.mensagem('Nenhum dado obrigatório foi digitado, por favor tente novamente')
            if dados_enfermeiro is None:
                break
            try:
                nome = dados_enfermeiro["nome"].upper()
                if not nome.replace(' ', '').isalpha():
                    break
            except (ValueError, TypeError):
                self.__tela_enfermeiros.mensagem('Houve problemas com o tipo de dado digitado')
            try:
                cpf = dados_enfermeiro["cpf"].replace(' ', '')
                if not (cpf.isnumeric() and len(cpf) == 11):
                    self.__tela_enfermeiros.mensagem(f'O cpf {cpf} é inválido!\nDigite um cpf com 11 dígitos')
                    break
            except (ValueError, TypeError):
                self.__tela_enfermeiros.mensagem('Houve problemas com o tipo de dado digitado')
            try:
                matricula_coren = dados_enfermeiro["matricula_coren"].replace(' ', '')
                if (matricula_coren is None or len(matricula_coren) == 0):
                    self.__tela_enfermeiros.mensagem(f'A matrícula COREN é obrigatória')
                    break
            except (ValueError, TypeError):
                self.__tela_enfermeiros.mensagem('Houve problemas com o tipo de dado digitado')
            try:
                telefone = dados_enfermeiro["telefone"]
                matricula_coren = dados_enfermeiro["matricula_coren"]
                data_nascimento_str = dados_enfermeiro["data_nascimento"]
                data_nascimento_obj = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
                idade_dias = datetime.today().date() - data_nascimento_obj
                idade = int(idade_dias.days // 365.24231481481481481481481481481481)
                if not 16 <= idade <= 130:
                    self.__tela_enfermeiros.mensagem('Não é possivel registar um profissinal menor de 16 anos ou com mais de 130 anos')
                    break                
            except:
                self.__tela_enfermeiros.mensagem('Data inválida, a data deve ser inserida neste formato: 11/11/2011')
                break
            if len(self.__dao.get_all()) == 0:
                self.__tela_enfermeiros.mensagem(f'Enfermeiro {nome} cadastrado')
                enfermeiro = Enfermeiro(nome, cpf, telefone, data_nascimento_obj, matricula_coren)
                self.__dao.add(enfermeiro)
                break
            else:
                for enfermeiro in self.__dao.get_all():
                    if not dados_enfermeiro:
                        self.__tela_enfermeiros.mensagem()
                        return None
                    if dados_enfermeiro["cpf"] == enfermeiro.cpf:
                        self.__tela_enfermeiros.mensagem(f'O cpf {dados_enfermeiro["cpf"]} já foi cadastrado')
                        return None
                enfermeiro = Enfermeiro(nome, cpf, telefone, data_nascimento_obj, matricula_coren)
                self.__dao.add(enfermeiro)
                self.__tela_enfermeiros.sucesso(nome, cpf, telefone, data_nascimento_obj, matricula_coren)
                break

    def editar_enfermeiro(self, nome=0, cpf=0, telefone='', data_nascimento=0):
        enfermeiro_editar = self.get_enfermeiro()
        if enfermeiro_editar is None:
            return None
        dados_editar = self.__tela_enfermeiros.dados_cadastro()
        if (len(dados_editar["nome"]) + len(dados_editar["cpf"]) + len(dados_editar["data_nascimento"]) + len(dados_editar["matricula_coren"])) == 0:
            self.__tela_enfermeiros.mensagem('Nenhum dado obrigatório foi digitado, por favor tente novamente')
            return None
        try:
            nome = dados_editar["nome"].upper()
            if nome.replace(' ', '').isalpha():
                nome_corrigido = nome
        except (ValueError, TypeError):
            self.__tela_enfermeiros.mensagem('Houve problemas com o tipo de dado digitado')
            return None
        try:
            data_nascimento_str = dados_editar["data_nascimento"]
            matricula_coren = dados_editar["matricula_coren"]
            data_nascimento_obj = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
            idade_dias = datetime.today().date() - data_nascimento_obj
            idade = int(idade_dias.days // 365.24231481481481481481481481481481)
            if not 16 <= idade <= 130:
                self.__tela_enfermeiros.mensagem('Não é possivel registar um profissinal menor de 16 anos ou com mais de 130 anos')
                return None
        except:
            self.__tela_enfermeiros.mensagem('Data inválida, a data deve ser inserida neste formato: 11/11/2011')
            return None
        enfermeiro_editar.nome = nome_corrigido
        enfermeiro_editar.telefone = dados_editar["telefone"]
        enfermeiro_editar.data_nascimento = data_nascimento_obj
        enfermeiro_editar.matricula_coren = matricula_coren
        self.__dao.add(enfermeiro_editar)
        self.__tela_enfermeiros.sucesso(enfermeiro_editar.nome, enfermeiro_editar.cpf, enfermeiro_editar.telefone, data_nascimento_obj, enfermeiro_editar.matricula_coren)

    def get_enfermeiro(self):
        if len(self.__dao.get_all()) == 0:
            self.__tela_enfermeiros.nenhum_enfermeiro()
            return None
        else:
            cpf = self.selecionar_lista_enfermeiros()
            if cpf is None:
                return None
            if self.__dao.get(cpf):
                return self.__dao.get(cpf)
            else:
                self.__tela_enfermeiros.cpf_nao_cadastrado(cpf)
        return None

    def selecionar_lista_enfermeiros(self):
        matriz = []
        linha = ['        Nome        ', '    CPF    ', '   Telefone    ','Matricula COREN', 'Idade']
        matriz.append(linha)
        if len(self.__dao.get_all()) == 0:
            self.__tela_enfermeiros.nenhum_enfermeiro()
            return None
        for enfermeiro in self.__dao.get_all():
            linha = [enfermeiro.nome_completo, enfermeiro.cpf, enfermeiro.telefone, enfermeiro.matricula_coren]
            idade_dias = datetime.today().date() - enfermeiro.data_nascimento
            idade = int(idade_dias.days // 365.24231481481481481481481481481481)
            linha.append(idade)
            matriz.append(linha)
        enfermeiro_selecionado = self.__tela_enfermeiros.selecionar_enfermeiro_tabela(matriz, 'Selecionar enfermeiros')
        if enfermeiro_selecionado:
            return matriz[enfermeiro_selecionado[0] + 1][1]

    def listar_enfermeiros(self):
        matriz = []
        linha = ['        Nome        ', '    CPF    ', '   Telefone    ','Matricula COREN', 'Idade']
        matriz.append(linha)
        if len(self.__dao.get_all()) == 0:
            self.__tela_enfermeiros.nenhum_enfermeiro()
            return None
        for enfermeiro in self.__dao.get_all():
            print(enfermeiro)
            linha = [enfermeiro.nome_completo, enfermeiro.cpf, enfermeiro.telefone, enfermeiro.matricula_coren]
            idade_dias = datetime.today().date() - enfermeiro.data_nascimento
            idade = int(idade_dias.days // 365.24231481481481481481481481481481)
            linha.append(idade)
            matriz.append(linha)
        self.__tela_enfermeiros.listar_enfermeiro_tabela(matriz, 'Lista de enfermeiros')

    def remover_enfermeiro(self):
        enfermeiro = self.get_enfermeiro()
        if enfermeiro is not None:
            self.__dao.remove(enfermeiro.cpf)

    def retorna_tela_principal(self):
        self.__mantem_tela_aberta = False

    def abre_tela(self):
        self.__mantem_tela_aberta = True
        lista_opcoes = {1: self.cadastrar_enfermeiro,
                        2: self.editar_enfermeiro,
                        3: self.listar_enfermeiros,
                        4: self.remover_enfermeiro,
                        5: self.retorna_tela_principal}

        while self.__mantem_tela_aberta:
            lista_opcoes[self.__tela_enfermeiros.tela_opcoes()]()
                        