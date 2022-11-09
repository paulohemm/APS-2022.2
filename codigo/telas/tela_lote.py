from datetime import datetime as datetime
#from controle.controlador_lote import ControladorLote:
import PySimpleGUI as sg


class TelaLote():

    def __init__(self, controlador_lote):
#self.__controlador_vacina = controlador_vacina
        self.__controlador_lote = controlador_lote

    def tela_opcoes(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Cadastrar Lote', size=(30, 2), key='1')],
            [sg.Button('Editar Lote', size=(30, 2), key='2')],
            [sg.Button('Remover Lote', size=(30, 2), key='3')],
            [sg.Button('Listar Lotes', size=(30, 2), key='4')],
            [sg.Button('Adicionar doses', size=(30, 2), key='5')],
            [sg.Button('Subtrair doses', size=(30, 2), key='6')],
            [sg.Button('Retornar', size=(30, 2), key='0')]
        ]
        window = sg.Window('Vacinas', size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        botao, _ = window.Read()
        opcao = int(botao)
        window.close()
        return opcao

    def pegar_dados_cadastrar(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Cadastrar Lote:')],
            [sg.Text('Fabricante*:',size=(15, 1)), sg.InputText()],
            [sg.Text('Lote*:',size=(15, 1)), sg.InputText()],
            [sg.Text('Data Recebimento*:', size=(15, 1)), sg.InputText()],
            [sg.Text('Data Vencimento*:', size=(15, 1)), sg.InputText()],
            [sg.Text('Quantidade*:', size=(15, 1)), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Lote',size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            try:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    return None
                if len(values[0]) == 0:
                    raise ValueError
                quantidade = int(values[4])
                break
            except ValueError:
                sg.popup('Campos marcados com * devem ser preenchidos obrigatoriamente', 'Tente novamente.')
        window.close()
        print(values[0],values[1], 'oi')
        return {'fabricante': values[0].upper(),'id_lote': values[1], 'data_recebimento': values[2], 'data_vencimento': values[3], 'quantidade': quantidade}

    def selecionar_lote(self, lista_de_lotes):
        sg.theme('Default')
        dados = []
        dados.append(['id_lote', 'Fabricante', 'Quantidade'])
        for lote in lista_de_lotes:
            dados.append([lote.id_lote, lote.vacina.fabricante, lote.quantidade])
        headings = ['  id Lote   ', '   Fabricante   ', 'Quantidade']
        layout = [
            [sg.Table(values=dados[1:][:], headings=headings, max_col_width=5,
                def_col_width=200,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                alternating_row_color='lightgrey',
                key='-LOTE-',
                row_height=35,
                tooltip='Lista de vacinas disponíveis')],
                [sg.Button('Selecionar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Vacinas', size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            try:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    return None
                elif event == 'Selecionar':
                    lote_selecionado = values['-LOTE-']
                    window.close()
                    return dados[lote_selecionado[0]+1][0]
            except IndexError:
                sg.popup('Vacina não selecionada.')
        window.close()

    def pegar_dados_editar(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Editar lote (preencha apenas os campos que deseja editar)')],
            [sg.Text('Data Recebimento*:', size=(15, 1)), sg.InputText()],
            [sg.Text('Data Vencimento*:', size=(15, 1)), sg.InputText()],
            [sg.Text('Quantidade:*',size=(15, 1)), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Vacinas',size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            try:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    return None
                window.close()
                return {'data_recebimento': values[0], 'data_vencimento': values[1], 'quantidade': values[2]}
            except:
                sg.popup('tente novamente')

    def mostrar_doses_disponiveis(self, dados_lote):
        sg.theme('Default')
        dados = []
        for lote in dados_lote:
            print(lote.vacina.fabricante)
            dados.append([lote.vacina.fabricante, lote.id_lote, lote.data_vencimento, lote.quantidade])
        headings = ['  Fabricante  ','  Id Lote  ','data vencimento', 'Quantidade']
        layout = [
            [sg.Table(values=dados, headings=headings, max_col_width=5,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='center',
                num_rows=5,
                alternating_row_color='lightgrey',
                key='-TABLE-',
                row_height=35,
                tooltip='Lista de vacinas disponíveis')],
                [sg.Button('Ok')]
        ]
        window = sg.Window('Vacinas',size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == 'Ok':
                break
        window.close()


    def lote_ja_cadastrado(self):
        sg.theme('Default')
        sg.popup('A vacina digitada já existe no sistema.')

    def lote_cadastrado(self):
        sg.theme('Default')
        sg.popup('Vacina cadastrada com sucesso!')

    def lista_vazia(self):
        sg.theme('Default')
        sg.popup('Não existem lotes cadastrados no sistema.')

    def lote_nao_cadastrado(self):
        sg.theme('Default')
        sg.popup('Vacina não existe no sistema, você deve cadastrar uma vacina antes de cadastrar um lote.')

    def mensagem(self, mensagem=0):
        sg.theme('Default')
        sg.popup(f'{mensagem}', no_titlebar=True)

    def quantidade_insuficiente(self, quantidade):
        sg.theme('Default')
        sg.popup('Quantidade disponível insuficiente. Seu estoque é de {} doses.'.format(quantidade))