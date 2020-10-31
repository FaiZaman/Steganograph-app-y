import PySimpleGUI as gui

class GraphicalUserInterface(object):

    def __init__(self):

        self.home_screen = [
            [gui.Text('Welcome to Steganograph-app-y!', font=('Helvetica', 16), justification='center')],
            [gui.Text('_'  * 100, size=(65, 1))],
            [gui.Text('Please select whether you would like to embed or extract a secret message.', 
                font=('Helvetica', 12))],
            [gui.Button('Embed'), gui.Button('Extract'), gui.Cancel()]
        ]

        self.embed_screen = [
            [gui.Text('Embedding', font=('Helvetica', 15), justification='center')],
            [gui.Text('Choose File: ')],
            [gui.Text('Secret Key: ')]
        ]

        self.extract_screen = [
            [gui.Text('Extracting', font=('Helvetica', 15), justification='center')],
            [gui.Text('Choose File: ')],
            [gui.Text('Secret Key')]
        ]
    
    def display(self):

        window = gui.Window('App', self.home_screen)
        embedding = extracting = False

        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                break
            if event == 'Embed':
                embedding = True
            if event == 'Extract':
                extracting = True


if __name__ == '__main__':

    GUI = GraphicalUserInterface()
    GUI.display()

