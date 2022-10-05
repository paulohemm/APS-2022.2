from datetime import datetime as datetime
import PySimpleGUI as sg


class TelaPacientes():

    def __init__(self, controlador_pacientes):
        self.__controlador_pacientes = controlador_pacientes

    def tela_opcoes(self):
        sg.theme('DefaultNoMoreNagging')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Cadastrar paciente', size=(30, 2), key='1')],
            [sg.Button('Editar paciente', size=(30, 2), key='2')],
            [sg.Button('Listar pacientes cadastrados', size=(30, 2), key='3')],
            [sg.Button('Remover paciente', size=(30, 2), key='4')],
            [sg.Button('Retornar', size=(30, 2), key='5')]
            ]
        window = sg.Window('Pacientes',size=(800, 480), element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        botao, valores = window.read()
        try:
            opcao = int(botao)
            window.close()
            return opcao
        except TypeError:
            pass
        window.close()

    def pegar_dados_cadastrar(self):
        sg.theme('DefaultNoMoreNagging')
        layout = [
            [sg.Text('Dados do Paciente:')],
            [sg.Text('Nome *: ',size=(15, 1)), sg.InputText()],
            [sg.Text('CPF *: ',size=(15, 1)), sg.InputText()],
            [sg.Text('Telefone: ',size=(15, 1)), sg.InputText()],
            [sg.Text('Data de Nascimento (dd/mm/aaaa) *:', size=(25, 1)), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Pacientes', layout, size=(800, 480), element_justification="center").Finalize()
        window.Maximize()
        event, values = window.Read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            window.close()
            return None
        window.close()
        print(values[2])
        return {"nome": values[0], "cpf": values[1], "telefone": values[2], "data_nascimento": values[3]}

    def mensagem(self, mensagem=0):
        sg.theme('DefaultNoMoreNagging')
        sg.popup(f'{mensagem}', no_titlebar=True)

    def selecionar_paciente_tabela(self, dados_paciente, titulo):
        titulos = [dados_paciente[0][0], dados_paciente[0][1], dados_paciente[0][2], dados_paciente[0][3]]
        sg.theme('DefaultNoMoreNagging')
        layout = [[sg.Table(values=dados_paciente[1:][:], headings=titulos, max_col_width=50,
                             def_col_width=200,
                             auto_size_columns=True,
                             display_row_numbers=True,
                             justification='left',
                             alternating_row_color='lightgrey',
                             key='dado',
                             row_height=35,
                             tooltip='This is a table')],
                  [sg.Button('Selecionar', size=(20, 2)), sg.Button('sair', size=(20, 2))],
                  ]
        window = sg.Window(titulo, layout, size=(800, 480), element_justification="center").Finalize()
        window.Maximize()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'sair':
                break
            elif event == 'Selecionar':
                window.close()
                return values['dado']
        window.close()
        return None

    def listar_paciente_tabela(self, dados_paciente, titulo):
        titulos = [dados_paciente[0][0], dados_paciente[0][1], dados_paciente[0][2], dados_paciente[0][3]]
        print(titulos)
        sg.theme('DefaultNoMoreNagging')
        layout = [[sg.Table(values=dados_paciente[1:][:], headings=titulos, max_col_width=50,
                             def_col_width=200,
                             auto_size_columns=True,
                             display_row_numbers=True,
                             justification='left',
                             alternating_row_color='lightgrey',
                             key='dado',
                             row_height=35,
                             tooltip='This is a table')],
                            [sg.Button('ok')]
                            ]
        window = sg.Window(titulo, layout, size=(800, 480), element_justification="center").Finalize()
        window.Maximize()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'ok':
                break
        window.close()
        return None

    def cpf_ja_cadastrado(self, cpf):
        sg.theme('DefaultNoMoreNagging')
        sg.popup(f'O cpf {cpf} já foi cadastrado.', no_titlebar=True)

    def cpf_nao_cadastrado(self, cpf):
        sg.theme('DefaultNoMoreNagging')
        sg.popup(f'O cpf {cpf} ainda não foi cadastrado.', no_titlebar=True)

    def nenhum_paciente(self):
        sg.theme('DefaultNoMoreNagging')
        sg.popup('Ainda não há pacientes cadastrados.', no_titlebar=True)

    def sucesso(self, nome, cpf=0, telefone = str, data=datetime):
        sg.theme('DefaultNoMoreNagging')
        if cpf == 0:
            sg.popup(f'Paciente {nome}, nascido em {data}, telefone {telefone} editado!', no_titlebar=True)
        else:
            sg.popup(f'Paciente {nome}, com cpf {cpf}, nascido em {data} telefone {telefone} cadastrado!', no_titlebar=True)
