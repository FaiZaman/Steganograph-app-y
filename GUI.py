import sys
import PySimpleGUI as gui
from algorithms.LSB import LSB
from algorithms.LSBM import LSBM

class GraphicalUserInterface(object):

    def __init__(self):

        self.app_name = "Steganograph-App-y"
        self.algorithm_list = ["LSB", "LSBM", "LSBMR", "PVD"]
        self.instantiators = {
            "LSB": LSB,
            "LSBM": LSBM
        }


    def create_home_window(self):

        home_screen = [
            [gui.Text('Welcome to {0}!'.format(self.app_name), font=('Helvetica', 16), 
                justification='center')],
            [gui.Text('Please select whether you would like to embed or extract a secret message.', 
                font=('Helvetica', 11))],
            [gui.Button('Embed'), gui.Button('Extract'), gui.Button('Exit')]
        ]

        home_window = gui.Window('{}'.format(self.app_name), home_screen)
        return home_window


    def create_embedding_window(self):

        embedding_screen = [
            [gui.Text('Embedding', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Embedding algorithm', size=(16, 1)), 
                gui.Combo(self.algorithm_list, size=(10, 1), key="input_algorithm"),
                gui.Button('Algorithm Information')],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="cover_image"), 
                gui.FileBrowse(file_types=(("Image Files", "*.png"),))],
            [gui.Text('Text file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="message"),
                gui.FileBrowse(file_types=(("Text Files", "*.txt"),))],
            [gui.Text('Secret key', size=(16, 1)), gui.Input(size=(40, 1), key="input_key")],
            [gui.Text('Save Folder', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="save_folder"),
                gui.FolderBrowse()],
            [gui.Text('')],
            [gui.Button('Embed'), gui.Button('Back to Main Menu')]
        ]

        embed_window = gui.Window('{0} - Embedding'.format(self.app_name), embedding_screen)
        return embed_window


    def create_extracting_window(self):

        extracting_screen = [
            [gui.Text('Extracting', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Extracting algorithm', size=(16, 1)),
                gui.Combo(self.algorithm_list, size=(10, 1), key="output_algorithm"),
                gui.Button('Algorithm Information')],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="stego_image"),
                gui.FileBrowse(file_types=(("Image Files", "*.png"),))],
            [gui.Text('Secret key', size=(16, 1)), gui.Input(size=(40, 1), key="output_key")],
            [gui.Text('Save Folder', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="save_folder"),
                gui.FolderBrowse()],
            [gui.Text('')],
            [gui.Button('Extract'), gui.Button('Back to Main Menu')]
        ]

        extract_window = gui.Window('{0} - Extracting'.format(self.app_name), extracting_screen)
        return extract_window
    

    def create_info_window(self, algorithm):

        info_screen = [
            [gui.Text('Information', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Description of ' + algorithm)],
            [gui.Text('')],
            [gui.Button('Close')]
        ]

        info_window = gui.Window('{0} - Information'.format(self.app_name), info_screen)
        return info_window
    

    def check_algorithm_information(self, event, values, embedding):

        if event == 'Algorithm Information':
            algorithm = values['input_algorithm'] if embedding else values['output_algorithm']
            info_window = self.create_info_window(algorithm)
            while True:
                event, values = info_window.read()
                if event in (None, 'Close'):
                    info_window.close()
                    break


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
                    self.check_algorithm_information(event, values, embedding=True)
                    if event == 'Embed':
                        algorithm_name, cover_file, message_file, key, save_path =\
                            values['input_algorithm'], values['cover_image'],\
                                values['message'], values['input_key'], values['save_folder']

                        window.close()
                        return [self.instantiators[algorithm_name],\
                            cover_file, message_file, key, save_path, embedding]

                    if event == 'Back to Main Menu':
                        break

                window.close()


            if extracting:

                window = self.create_extracting_window()

                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    self.check_algorithm_information(event, values, embedding=False)
                    if event == 'Extract':
                        algorithm_name, stego_file, key, save_path =\
                            values['output_algorithm'], values['stego_image'],\
                                values['output_key'], values['save_folder']
                        
                        window.close()
                        return [self.instantiators[algorithm_name],\
                            stego_file, key, save_path, embedding]

                    if event == 'Back to Main Menu':
                        break

                window.close()
