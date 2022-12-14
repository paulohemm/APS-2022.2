from datetime import datetime
import PySimpleGUI as sg

class TelaAgendamentos():

    def __init__(self, controlador_agendamento):
        self.__controlador_agendamento = controlador_agendamento
        self.lista_dia = ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
        self.lista_mes = ('01','02','03','04','05','06','07','08','09','10','11','12')
        self.lista_ano = ('2022','2023','2024')
        self.lista_hora = ('09','10','11','12','13','14','15')
        self.lista_minutos = ('00','10','20','30','40','50')
        self.lista_dose = ('1ª dose', '2ª dose')

    def tela_opcoes(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Registrar agendamento', size=(30, 2), key='1')],
            [sg.Button('Listar aplicações agendadas', size=(30, 2), key='2')],
            [sg.Button('Aplicar Vacina', size=(30, 2), key='3')],
            [sg.Button('Listar aplicações realizadas', size=(30, 2), key='4')],
            [sg.Button('Relatório agendamento por data', size=(30, 2), key='5')],
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
            [sg.Text('Registro de Agendamento')],
            [sg.Text('Data:')],
            [sg.Text('Dia:', size=(15,1)), sg.InputCombo(self.lista_dia, size=(15,1))],
            [sg.Text('Mês:', size=(15,1)), sg.InputCombo(self.lista_mes, size=(15,1))],
            [sg.Text('Ano:', size=(15,1)), sg.InputCombo(self.lista_ano, size=(15,1))],
            [sg.Text('Horário:')],
            [sg.Text('Hora:',size=(15, 1)), sg.InputCombo(self.lista_hora, size=(15,1))],
            [sg.Text('Minuto:',size=(15, 1)), sg.InputCombo(self.lista_minutos, size=(15,1))],
            [sg.Text('Dose:')],
            [sg.Text('Selecione:', size=(15,1)), sg.InputCombo(self.lista_dose, size=(15,1))],
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
                if values[0] not in self.lista_dia or values[1] not in self.lista_mes or values[2] not in self.lista_ano:
                    sg.popup('Data inválida.','Verifique a data desejada e tente novamente.')
                    window.close()
                    return None
                data_str = values[0]+'/'+values[1]+'/'+values[2]
                data = datetime.strptime(data_str, '%d/%m/%Y').date()
                if values[3] not in self.lista_hora or values[4] not in self.lista_minutos:
                    sg.popup('Horario inválido.','Verifique o horario desejado e tente novamente.')
                    window.close()
                    return None
                horario_str = values[3]+':'+values[4]
                horario = datetime.strptime(horario_str, '%H:%M').time()
                datetime.strptime('08:00', '%H:%M').time() <= horario <= datetime.strptime('18:00', '%H:%M').time()
                if values[5] not in self.lista_dose:
                    sg.popup('Lote inválido.','Verifique o lote desejado e tente novamente.')
                    window.close()
                    return None
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
                agendamento.enfermeiro.nome_completo,
                agendamento.paciente.nome_completo,
                agendamento.dose,
                agendamento.lote.vacina.fabricante,
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


    def mostrar_lista_agendamentos(self, lista_de_agendamentos):
        sg.theme('Default')
        dados = []
        dados.append(['Codigo','Data','Horário','Enfermeiro','Paciente','Dose','Lote','Aplicada'])
        for agendamento in lista_de_agendamentos:
            dados.append([
                agendamento.codigo,
                agendamento.data,
                agendamento.horario,
                agendamento.enfermeiro.nome_completo,
                agendamento.paciente.nome_completo,
                agendamento.dose,
                agendamento.lote.vacina.fabricante,
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

    def capturar_data_relatorio(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecione a data do Agendamento')],
            [sg.Text('Data:')],
            [sg.Text('Dia:', size=(15,1)), sg.InputCombo(self.lista_dia, size=(15,1))],
            [sg.Text('Mês:', size=(15,1)), sg.InputCombo(self.lista_mes, size=(15,1))],
            [sg.Text('Ano:', size=(15,1)), sg.InputCombo(self.lista_ano, size=(15,1))],
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
                if values[0] not in self.lista_dia or values[1] not in self.lista_mes or values[2] not in self.lista_ano:
                    sg.popup('Data inválida.','Verifique a data desejada e tente novamente.')
                    window.close()
                    return None
                data_str = values[0]+'/'+values[1]+'/'+values[2]
                data = datetime.strptime(data_str, '%d/%m/%Y').date()
                break
            except ValueError:
                sg.popup('Data inválida.','Verifique a data desejada e tente novamente.')
        window.close()
        return {'data': data}

    def agendamento_cadastrado(self):
        sg.theme('Default')
        sg.popup("Agendamento cadastrado com sucesso!")

    def ja_castrado_primeira_dose(self):
        sg.theme('Default')
        sg.popup('Já existe um agendamento da primeira dose cadastrado para este paciente.')
    
    def ja_cadastrado_segunda_dose(self):
        sg.theme('Default')
        sg.popup('Já existe um agendamento da segunda dose cadastrado para este paciente.')
    
    def data_recente_primeira_dose(self, dias):
        sg.theme('Default')
        sg.popup(f'Não agendado! Segunda dose deve ser agendada para {dias} dias após a aplicação da primeira dose.')
    
    def nao_cadastrado_primeira_dose(self):
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

    def lista_vazia_today(self):
        sg.theme('Default')
        sg.popup('Não existem agendamentos cadastrados para data atual no sistema.')
    
    def lista_vazia(self):
        sg.theme('Default')
        sg.popup('Não existem agendamentos cadastrados no sistema.')

    def enfermeiro_ja_possui_um_agendamento(self):
        sg.theme('Default')
        sg.popup('Não agendado! O Enfermeiro já possui um agendamento na data e horário selecionado')

    def lote_fora_de_validade(self):
        sg.theme('Default')
        sg.popup('Não é possivel registar o agendamento, a vacina esta fora do prazo de validade.')
    
    def doses_insuficientes(self):
        sg.theme('Default')
        sg.popup('Não é possivel registar o agendamento, não há doses disponíveis')

    def agendamento_com_data_anterior(self):
        sg.theme('Default')
        sg.popup('Não é possível realizar um agendamento em uma data anterior a data atual.')

    def sem_agendamento_para_a_data_seleciona(self):
        sg.theme('Default')
        sg.popup('Não existe agendamentos para a data selecionada, por favor tente novamente!')
