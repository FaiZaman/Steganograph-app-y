import sys
import PySimpleGUI as gui

class GraphicalUserInterface(object):

    def __init__(self):
        
        self.app_name = "Steganograph-App-y"


    def create_home_window(self):

        home_screen = [
            [gui.Text('Welcome to {0}!'.format(self.app_name), font=('Helvetica', 16), 
                justification='center')],
            [gui.Text('_'  * 100, size=(65, 1))],
            [gui.Text('Please select whether you would like to embed or extract a secret message.', 
                font=('Helvetica', 12))],
            [gui.Button('Embed'), gui.Button('Extract'), gui.Button('Exit')]
        ]

        home_window = gui.Window('{}'.format(self.app_name), home_screen)
        return home_window


    def create_embedding_window(self):

        embedding_screen = [
            [gui.Text('Embedding', font=('Helvetica', 15), justification='center')],
            [gui.Text('Choose File: ')],
            [gui.Text('Secret Key: ')],
            [gui.Button('Back to Main Menu')]
        ]

        embed_window = gui.Window('{0} - Embedding'.format(self.app_name), embedding_screen)
        return embed_window


    def create_extracting_window(self):
        
        extracting_screen = [
            [gui.Text('Extracting', font=('Helvetica', 15), justification='center')],
            [gui.Text('Choose File: ')],
            [gui.Text('Secret Key')],
            [gui.Button('Back to Main Menu')]
        ]

        extract_window = gui.Window('{0} - Extracting'.format(self.app_name), extracting_screen)
        return extract_window


    def display(self):

        selecting = True

        while selecting:

            window = self.create_home_window()
            embedding = extracting = False

            while True:
                event, values = window.read()
                if event in (None, 'Exit'):
                    sys.exit()
                    break
                if event == 'Embed':
                    embedding = True
                    break
                if event == 'Extract':
                    extracting = True
                    break

            window.close()

            if embedding:

                window = self.create_embedding_window()

                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    if event == 'Choose File':
                        pass
                    if event == 'Back to Main Menu':
                        break

                window.close()


            if extracting:

                window = self.create_extracting_window()

                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    if event == 'Choose File':
                        pass
                    if event == 'Back to Main Menu':
                        break

                window.close()


if __name__ == '__main__':

    GUI = GraphicalUserInterface()
    GUI.display()
