from ..model.paciente import Paciente
from ..view.paciente_view import PacienteView
from ..model.persistence.pacienteDAO import PacienteDAO


class PacienteController():
    def __init__(self):
        self.__pacienteDAO = PacienteDAO()
        self.__view = PacienteView()

    def option(self):
        escolha = self.__view.tela_paciente()
        while escolha != 'Sair' and escolha != None:
            options = {
                    'Cadastrar Paciente': self.incluir,
                    'Listar Pacientes': self.listagem,
                    'Atualizar Paciente': self.atualizar,
                    'Remover Paciente': self.excluir,
                    }
            function = options[escolha]
            function()
            escolha = self.__view.tela_paciente()

    def incluir(self) -> Paciente:
        dados = self.__view.incluir()
        if dados != None:
            nome = dados[0]
            try:
                print(dados)
                data_nascimento = int(dados[1])
                cpf = str(dados[2])
            except ValueError:
                self.__view.dado_invalido()
            else:
                novo_paciente = Paciente(nome, data_nascimento, cpf)
                lista_pacientes = list(self.__pacienteDAO.get_all())
                for paciente in lista_pacientes:
                    if paciente.cpf == cpf:
                        self.__view.paciente_duplicado()
                        return
                self.__pacienteDAO.add(novo_paciente)
                self.__view.cadastro_sucesso()
        else:
            return

    def listagem(self):
        self.__view.listagem(list(self.__pacienteDAO.get_all()))


    def get_paciente_att(self):
        lista_pacientes = list(self.__pacienteDAO.get_all())
        return self.__view.get_paciente_att(lista_pacientes)

    def atualizar(self):
        paciente_escolhido = self.get_paciente_att()
        if paciente_escolhido != None:
            try:
                paciente_escolhido = paciente_escolhido[0].split('---')
            except IndexError:
                #Erro ao clicar submit sem selecionar um paciente -> paciente_escolhido = [] - lista vazia
                self.__view.error("Nenhum Paciente Escolhido")
                return
        else:
            #Volta se clicar em Voltar -> paciente_escolhido = None
            return
        try:
            paciente_escolhido[1] = int(paciente_escolhido[1])
            cpf_int = int(paciente_escolhido[2])
        except ValueError:
            self.__view.dado_invalido()
        else:
            dados = self.__view.atualizar()
            lista_pacientes = list(self.__pacienteDAO.get_all())
            for paciente in lista_pacientes:
                if paciente.cpf == cpf_int:
                    paciente.nome_completo = dados[0]
                    paciente.idade = dados[1]
                    self.__pacienteDAO.add(paciente)


    def excluir(self):
        lista_pacientes = list(self.__pacienteDAO.get_all())
        paciente_a_excluir = self.__view.get_paciente_att(lista_pacientes)
        if lista_pacientes != None and paciente_a_excluir != None:
            for paciente in lista_pacientes:
                for exc in paciente_a_excluir:
                        if paciente.nome_completo in exc and str(paciente.cpf) in exc:
                            self.__pacienteDAO.remove(paciente.cpf)
                            self.__view.sucesso_excluir()
                            return
            self.__view.error("Nenhum paciente selecionado!")

    @property
    def pacientes(self):
        return list(self.__pacienteDAO.get_all())
