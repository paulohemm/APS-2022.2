from datetime import datetime
import PySimpleGUI as sg

class TelaAplicacao():

    def __init__(self, controlador_aplicacao):
        self.__controlador_aplicacao = controlador_aplicacao

    def tela_opcoes(self):
        sg.theme('Default')
        layout = [
            [sg.Text('Selecione a opção desejada', size=(30, 1))],
            [sg.Button('Aplicar Vacina', size=(30, 2), key='3')],
            [sg.Button('Listar histórico de vacinações', size=(30, 2), key='6')],
            [sg.Button('Retornar', size=(30, 2), key='0')]
        ]
        window = sg.Window('Aplicação de vacina',size=(800, 480), element_justification="center").Layout(layout).Finalize()
        window.Maximize()
        botao, _ = window.Read()
        opcao = int(botao)
        window.close()
        return opcao

    def vacina_aplicada(self):
        sg.theme('Default')
        sg.popup("Vacina aplicada com sucesso!.")
    
