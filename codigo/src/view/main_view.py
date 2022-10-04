import PySimpleGUI as sg

sg.theme('DarkPurple1')

class TelaSistemaView:

    def __init__(self):
        pass

    def menu_principal(self):
        layout =[
                [sg.Text("---- Imuniza + Sistema de vacinação ----")],
                [sg.Button('Paciente')],
                [sg.Button('Sair')],
                ]
        window = sg.Window('Tela de Sistema', size=(300,300)).Layout(layout)
        button_str = window.read()
        window.close()
        return button_str[0]
