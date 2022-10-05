import PySimpleGUI as sg


class TelaVacinas():

    def __init__(self, controlador_vacina):
        self.__controlador_vacina = controlador_vacina

    def tela_opcoes(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Cadastrar vacina', size=(30, 2), key='1')],
            [sg.Button('Editar vacina', size=(30, 2), key='2')],
            [sg.Button('Remover vacina', size=(30, 2), key='3')],
            [sg.Button('Listar doses por fabricante', size=(30, 2), key='4')],
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
            [sg.Text('Cadastrar Vacina:')],
            [sg.Text('Fabricante*:',size=(15, 1)), sg.InputText()],
            [sg.Text('Quantidade*:',size=(15, 1)), sg.InputText()],
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
                if len(values[0]) == 0:
                    raise ValueError
                quantidade = int(values[1])
                break
            except ValueError:
                sg.popup('Valor inválido para fabricante ou quantidade.', 'Tente novamente.')
        window.close()
        return {'fabricante': values[0].upper(), 'quantidade': quantidade}

    def selecionar_vacina(self, lista_de_vacinas):
        sg.theme('Default')
        dados = []
        dados.append(['Fabricante', 'Quantidade'])
        for vacina in lista_de_vacinas:
            dados.append([vacina.fabricante, vacina.quantidade])
        headings = ['   Fabricante   ', 'Quantidade']
        layout = [
            [sg.Table(values=dados[1:][:], headings=headings, max_col_width=5,
                def_col_width=200,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                alternating_row_color='lightgrey',
                key='-VACINA-',
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
                    vacina_selecionada = values['-VACINA-']
                    window.close()
                    return dados[vacina_selecionada[0]+1][0]
            except IndexError:
                sg.popup('Vacina não selecionada.')
        window.close()

    def pegar_quantidade(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecionar Quantidade:*')],
            [sg.Text('Quantidade',size=(15, 1)), sg.InputText()],
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
                if int(values[0]) < 0:
                    raise ValueError
                quantidade = int(values[0])
                window.close()
                return quantidade
            except ValueError:
                sg.popup('Valor inválido para a quantidade.', 'Digite um valor válido.')

    def mostrar_doses_disponiveis(self, dados_vacina):
        sg.theme('Default')
        dados = []
        for vacina in dados_vacina:
            dados.append([vacina.fabricante, vacina.quantidade])
        headings = ['   Fabricante   ', 'Quantidade']
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


    def vacina_ja_cadastrada(self):
        sg.theme('Default')
        sg.popup('A vacina digitada já existe no sistema.')

    def vacina_cadastrada(self):
        sg.theme('Default')
        sg.popup('Vacina cadastrada com sucesso!')

    def lista_vazia(self):
        sg.theme('Default')
        sg.popup('Não existem vacinas cadastradas no sistema.')

