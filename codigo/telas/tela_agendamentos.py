from datetime import datetime
import PySimpleGUI as sg

class TelaAgendamentos():

    def __init__(self, controlador_agendamento):
        self.__controlador_agendamento = controlador_agendamento

    def tela_opcoes(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Cadastrar agendamento', size=(30, 2), key='1')],
            [sg.Button('Editar agendamento', size=(30, 2), key='2')],
            [sg.Button('Remover agendamento', size=(30, 2), key='3')],
            [sg.Button('Listar aplicações agendadas', size=(30, 2), key='4')],
            [sg.Button('Aplicar Vacina', size=(30, 2), key='5')],
            [sg.Button('Listar aplicações realizadas', size=(30, 2), key='6')],
            [sg.Button('Retornar', size=(30, 2), key='0')]
        ]
        window = sg.Window('Agendamentos',size=(800, 480), element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        botao, _ = window.Read()
        opcao = int(botao)
        window.close()
        return opcao
    
    def pegar_dados_cadastrar(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Cadastro de Agendamento')],
            [sg.Text('Data:')],
            [sg.Text('Dia:', size=(15,1)), sg.InputCombo(('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'), size=(15,1))],
            [sg.Text('Mês:', size=(15,1)), sg.InputCombo(('01','02','03','04','05','06','07','08','09','10','11','12'), size=(15,1))],
            [sg.Text('Ano:', size=(15,1)), sg.InputCombo(('2020','2021','2022'), size=(15,1))],
            [sg.Text('Horário:')],
            [sg.Text('Hora:',size=(15, 1)), sg.InputCombo(('08','09','10','11','12','13','14','15','16','17'), size=(15,1))],
            [sg.Text('Minuto:',size=(15, 1)), sg.InputCombo(('00','10','20','30','40','50'), size=(15,1))],
            [sg.Text('Dose:')],
            [sg.Text('Selecione:', size=(15,1)), sg.InputCombo(('1ª dose', '2ª dose'), size=(15,1))],
            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Agendamentos',size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            try:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    return None
                data_str = values[0]+'/'+values[1]+'/'+values[2]
                data = datetime.strptime(data_str, '%d/%m/%Y').date()
                horario_str = values[3]+':'+values[4]
                horario = datetime.strptime(horario_str, '%H:%M').time()
                datetime.strptime('08:00', '%H:%M').time() <= horario <= datetime.strptime('18:00', '%H:%M').time()
                break
            except ValueError:
                sg.popup('Data inválida.','Verifique a data desejada e tente novamente.')
        if values[5] == '1ª dose':
            dose = 1
        if values[5] == '2ª dose':
            dose = 2
        window.close()
        return {'data': data, 'horario': horario, 'dose': dose}

    def selecionar_agendamento(self, lista_de_agendamentos):
        sg.theme('Default')
        dados = []
        dados.append(['Codigo','Data','Horário','Enfermeiro','Paciente','Dose','Vacina','Aplicada'])
        for agendamento in lista_de_agendamentos:
            dados.append([
                agendamento.codigo,
                agendamento.data,
                agendamento.horario,
                agendamento.enfermeiro.nome,
                agendamento.paciente.nome,
                agendamento.dose,
                # agendamento.vacina.fabricante,
                agendamento.aplicada])
        headings = ['   Codigo   ','   Data   ','Horário','   Enfermeiro   ','   Paciente   ','Dose','  Vacina  ','Aplicada']
        layout = [
            [sg.Table(values=dados[1:][:], headings=headings, max_col_width=5,
                def_col_width=200,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                alternating_row_color='lightgrey',
                key='-AGENDAMENTO-',
                row_height=35,
                tooltip='Lista de vacinas disponíveis')],
                [sg.Button('Selecionar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Agendamentos', size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            try:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    return None
                elif event == 'Selecionar':
                    window.close()
                    agendamento_selecionado = values['-AGENDAMENTO-']
                    return dados[agendamento_selecionado[0]+1][0]
            except IndexError:
                sg.popup('Agendamento não selecionada.', 'Tente novamente.')
        window.close()

    def pegar_dados_editar(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Editar Agendamento:')],
            [sg.Text('Data (dd/mm/aaaa):',size=(15, 1)), sg.InputText()],
            [sg.Text('Hora:',size=(15, 1)), sg.InputCombo(('08','09','10','11','13','14','15','16','17'), size=(15,1)),
            sg.Text('Minuto:',size=(6, 1)), sg.InputCombo(('00','10','20','30','40','50'), size=(15,1))],
            [sg.Text('Aplicada', size=(15,1)), sg.InputCombo(('Não', 'Sim'), size=(15,1))],
            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Agendamentos',size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            try:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    return None
                data_str = values[0]
                data = datetime.strptime(data_str, '%d/%m/%Y').date()
                horario_str = values[1]+':'+values[2]
                horario = datetime.strptime(horario_str, '%H:%M').time()
                datetime.strptime('08:00', '%H:%M').time() <= horario <= datetime.strptime('18:00', '%H:%M').time()
                break
            except ValueError:
                sg.popup('Valores digitados inválidos.', 'Tente novamente.')
        if values[3] == 'Não':
            aplicada = False
        if values[3] == 'Sim':
            aplicada = True
        window.close()
        return {'data': data, 'horario': horario, 'aplicada': aplicada}

    def mostrar_lista_agendamentos(self, lista_de_agendamentos):
        sg.theme('Default')
        dados = []
        dados.append(['Codigo','Data','Horário','Enfermeiro','Paciente','Dose','Lote','Aplicada'])
        for agendamento in lista_de_agendamentos:
            dados.append([
                agendamento.codigo,
                agendamento.data,
                agendamento.horario,
                agendamento.enfermeiro.nome,
                agendamento.paciente.nome,
                agendamento.dose,
                # agendamento.lote.fabricante,
                agendamento.aplicada])
        headings = ['   Codigo   ','   Data   ','Horário','   Enfermeiro   ','   Paciente   ','Dose','  Lote  ','Aplicada']
        layout = [
            [sg.Table(values=dados[1:][:], headings=headings, max_col_width=5,
                def_col_width=200,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                alternating_row_color='lightgrey',
                key='-AGENDAMENTO-',
                row_height=35,
                tooltip='Lista de vacinas disponíveis')],
                [sg.Button('Ok')]
        ]
        window = sg.Window('Agendamentos', size=(800, 480),element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == 'Ok':
                break
        window.close()

    def agendamento_cadastrado(self):
        sg.theme('Default')
        sg.popup("Agendamento cadastrado com sucesso!")
    
    def agendamento_editado(self):
        sg.theme('Default')
        sg.popup("Agendamento editado com sucesso!")
    
    def agendamento_removido(self):
        sg.theme('Default')
        sg.popup("O agendamento solicitado foi removido.")

    def ja_castrado_primeira_dose(self):
        sg.theme('Default')
        sg.popup('Já existe um agendamento da primeira dose cadastrado para este paciente.')
    
    def ja_castrado_segunda_dose(self):
        sg.theme('Default')
        sg.popup('Já existe um agendamento da segunda dose cadastrado para este paciente.')
    
    def data_recente_primeira_dose(self):
        sg.theme('Default')
        sg.popup('Não agendado! Segunda dose deve ser agendada para 20 dias após a aplicação da primeira dose.')
    
    def nao_castrado_primeira_dose(self):
        sg.theme('Default')
        sg.popup('Não agendado! Segunda dose só pode ser agendada após o agendamento da primeira dose.')

    def agendamento_nao_cadastrado(self):
        sg.theme('Default')
        sg.popup('Agendamento não cadastrado.')

    def vacina_aplicada(self):
        sg.theme('Default')
        sg.popup("Vacina aplicada com sucesso.")

    def agendamento_aberto_nao_cadastrado(self):
        sg.theme('Default')
        sg.popup('Nenhum agendamento aberto foi encontrado.')

    def agendamento_efetivado_nao_cadastrado(self):
        sg.theme('Default')
        sg.popup('Nenhum agendamento efetivado foi encontrado.')
    
    def lista_vazia(self):
        sg.theme('Default')
        sg.popup('Não existem agendamentos cadastradas no sistema.')
