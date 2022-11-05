from datetime import datetime
import PySimpleGUI as sg


class TelaEnfermeiros():

    def __init__(self, controlador_enfermeiros):
        self.__controlador_enfermeiros = controlador_enfermeiros

    def tela_opcoes(self):
        sg.theme('DefaultNoMoreNagging')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Cadastrar enfermeiro', size=(30, 2), key='1')],
            [sg.Button('Editar enfermeiro', size=(30, 2), key='2')],
            [sg.Button('Listar enfermeiros cadastrados', size=(30, 2), key='3')],
            [sg.Button('Remover enfermeiro', size=(30, 2), key='4')],
            [sg.Button('Retornar', size=(30, 2), key='5')]
            ]
        window = sg.Window('Enfermeiros',size=(800, 480), element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        botao, valores = window.read()
        try:
            opcao = int(botao)
            window.close()
            return opcao
        except TypeError:
            pass
        window.close()

    def dados_cadastro(self):
        sg.theme('DefaultNoMoreNagging')
        layout = [
            [sg.Text('Dados do enfermeiro:')],
            [sg.Text('Nome completo*: ',size=(24, 1)), sg.InputText()],
            [sg.Text('CPF*: ',size=(24, 1)), sg.InputText()],
            [sg.Text('Telefone: ', size=(24, 1)), sg.InputText()],
            [sg.Text('Data nascimento(dd/mm/aaaa)*:', size=(24, 1)), sg.InputText()],
            [sg.Text('Matrícula COREN*:', size=(24, 1)), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Enfermeiro', layout, size=(800, 480), element_justification="center").Finalize()
        window.Maximize()
        event, values = window.Read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            window.close()
            return None
        window.close()
        return {"nome": values[0], "cpf": values[1], "telefone": values[2], "data_nascimento": values[3], "matricula_coren": values[4]}

    def mensagem(self, mensagem=0):
        sg.theme('DefaultNoMoreNagging')
        sg.popup(f'{mensagem}', no_titlebar=True)

    def selecionar_enfermeiro_tabela(self, dados_enfermeiro, titulo):
        titulos = [dados_enfermeiro[0][0], dados_enfermeiro[0][1], dados_enfermeiro[0][2], dados_enfermeiro[0][3], dados_enfermeiro[0][4]]
        sg.theme('DefaultNoMoreNagging')
        layout = [[sg.Table(values=dados_enfermeiro[1:][:], headings=titulos, max_col_width=50,
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

    def listar_enfermeiro_tabela(self, dados_enfermeiro, titulo):
        titulos = [dados_enfermeiro[0][0], dados_enfermeiro[0][1], dados_enfermeiro[0][2], dados_enfermeiro[0][3], dados_enfermeiro[0][4]]
        print(titulos)
        sg.theme('DefaultNoMoreNagging')
        layout = [[sg.Table(values=dados_enfermeiro[1:][:], headings=titulos, max_col_width=50,
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

    def nenhum_enfermeiro(self):
        sg.theme('DefaultNoMoreNagging')
        sg.popup('Ainda não há enfermeiros cadastrados.', no_titlebar=True)

    def sucesso(self, nome, cpf=0, telefone = str, data=datetime, matricula_coren = str):
        sg.theme('DefaultNoMoreNagging')
        if cpf == 0:
            sg.popup(f'Enfermeiro {nome}, nascido em {data}, telefone {telefone}, matricula {matricula_coren} editado!', no_titlebar=True)
        else:
            sg.popup(f'Enfermeiro {nome}, com cpf {cpf}, nascido em {data} telefone {telefone}, matricula {matricula_coren} cadastrado!', no_titlebar=True)
