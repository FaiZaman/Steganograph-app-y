import sys
import json
import PySimpleGUI as gui
from algorithms.LSB import LSB
from algorithms.LSBM import LSBM
from algorithms.LSBMR import LSBMR
from algorithms.PVD import PVD
from algorithms.EA_LSBMR import EA_LSBMR

class GraphicalUserInterface(object):

    def __init__(self):

        self.app_name = "Steganograph-App-y"

        with open('data/algorithms.json') as f:
            a_data = json.load(f)
        with open('data/combinators.json') as g:
            c_data = json.load(g)

        self.algorithm_data = {}
        self.combinator_data = {}

        for datum in a_data['algorithms']:
            self.algorithm_data[datum['name']] = datum['description']
        for datum in c_data['combinators']:
            self.combinator_data[datum['name']] = datum['description']

        self.edge_detector_list = ["Canny", "Sobel", "LoG"]
        self.instantiators = {
            "LSB": LSB,
            "LSBM": LSBM,
            "LSBMR": LSBMR,
            "PVD": PVD,
            "EA-LSBMR": EA_LSBMR
        }


    def create_home_window(self):

        home_screen = [
            [gui.Text('Welcome to {0}!'.format(self.app_name), font=('Helvetica', 16), 
                justification='center')],
            [gui.Text('Please select whether you want to embed or extract a secret message.', 
                font=('Helvetica', 11))],
            [gui.Button('Embed', size=(16, 1)), gui.Button('Extract', size=(16, 1))],
            [gui.Button('Hybrid Embed', size=(16, 1)),\
                gui.Button('Hybrid Extract', size=(16, 1))],
            [gui.Button('Exit', font=('Helvetica', 10, 'bold'))]
        ]

        home_window = gui.Window('{}'.format(self.app_name),\
                                    home_screen, element_justification='c')
        return home_window


    def create_embedding_window(self):

        embedding_screen = [
            [gui.Text('Embedding', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Embedding algorithm', size=(16, 1)), 
                gui.Combo(list(self.algorithm_data.keys()), size=(10, 1), key="input_algorithm"),
                gui.Button('Algorithm Information')],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="cover_image"), 
                gui.FileBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover', 
                file_types=(("Image Files", "*.png")))],
            [gui.Text('Text file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="message"),
                gui.FileBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Messages/Embedding', 
                file_types=(("Text Files", "*.txt"),))],
            [gui.Text('Secret key', size=(16, 1)), gui.Input(size=(40, 1), key="input_key")],
            [gui.Text('Save Folder', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="save_folder"),
                gui.FolderBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego')],
            [gui.Text('')],
            [gui.Button('Embed'), gui.Button('Back to Main Menu')]
        ]

        embed_window = gui.Window('{0} - Embedding'.format(self.app_name), embedding_screen)
        return embed_window
    

    def create_hybrid_embedding_window(self):

        hybrid_embedding_screen = [
            [gui.Text('Hybrid Embedding', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Edge Detector 1', size=(16, 1)),
                gui.Combo(self.edge_detector_list, size=(10, 1), key="input_detector_1"),
                gui.Button('Detector Information')],
            [gui.Text('Edge Detector 2', size=(16, 1)),
                gui.Combo(self.edge_detector_list, size=(10, 1), key="input_detector_2"),
                gui.Button('Detector Information')],
            [gui.Text('Hybrid Technique', size=(16, 1)),
                gui.Combo(list(self.combinator_data.keys()), size=(10, 1), key="comb_technique"),
                gui.Button('Hybrid Information')],
            [gui.Text('_' * 55)],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="cover_image"), 
                gui.FileBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover', 
                file_types=(("Image Files", "*.png")))],
            [gui.Text('Text file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="message"),
                gui.FileBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Messages/Embedding', 
                file_types=(("Text Files", "*.txt")))],
            [gui.Text('Secret key', size=(16, 1)), gui.Input(size=(40, 1), key="input_key")],
            [gui.Text('Save Folder', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="save_folder"),
                gui.FolderBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego')],
            [gui.Text('')],
            [gui.Button('Hybrid Embed'), gui.Button('Back to Main Menu')]
        ]

        hybrid_embed_window = gui.Window('{0} - Hybrid Embedding'.format(self.app_name),\
                                            hybrid_embedding_screen)
        return hybrid_embed_window


    def create_extracting_window(self):

        extracting_screen = [
            [gui.Text('Extracting', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Extracting algorithm', size=(16, 1)),
               gui.Combo(list(self.algorithm_data.keys()), size=(10, 1), key="output_algorithm"),
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


    def create_hybrid_extracting_window(self):

        hybrid_extracting_screen = [
            [gui.Text('Hybrid Extracting', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text('Edge Detector 1', size=(16, 1)),
                gui.Combo(self.edge_detector_list, size=(10, 1), key="input_detector_1"),
                gui.Button('Detector Information')],
            [gui.Text('Edge Detector 2', size=(16, 1)),
                gui.Combo(self.edge_detector_list, size=(10, 1), key="input_detector_2"),
                gui.Button('Detector Information')],
            [gui.Text('Hybrid Technique', size=(16, 1)),
                gui.Combo(list(self.combinator_data.keys()), size=(10, 1), key="comb_technique"),
                gui.Button('Hybrid Information')],
            [gui.Text('_' * 55)],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="cover_image"), 
                gui.FileBrowse(file_types=(("Image Files", "*.png")))],
            [gui.Text('Secret key', size=(16, 1)), gui.Input(size=(40, 1), key="input_key")],
            [gui.Text('Save Folder', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="save_folder"),
                gui.FolderBrowse()],
            [gui.Text('')],
            [gui.Button('Hybrid Extract'), gui.Button('Back to Main Menu')]
        ]

        hybrid_extract_window = gui.Window('{0} - Hybrid Extracting'.format(self.app_name),\
                                            hybrid_extracting_screen)
        return hybrid_extract_window


    def create_info_window(self, algorithm):

        info_screen = [
            [gui.Text('Information', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text(self.algorithm_data[algorithm], size=(60, 4))],
            [gui.Text('')],
            [gui.Button('Close')]
        ]

        info_window = gui.Window('{0} - Information'.format(self.app_name), info_screen)
        return info_window


    def display_information(self, event, values, operation):

        if operation == "embedding":
            algorithm = values['input_algorithm']
        else:
            algorithm = values['output_algorithm']

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
            operation = ""

            while True:
                event, values = window.read()
                if event in (None, 'Exit'):
                    sys.exit()
                    break
                if event == 'Embed':
                    operation = "embedding"
                    break
                if event == 'Hybrid Embed':
                    operation = "hybrid_embedding"
                    break
                if event == 'Extract':
                    operation = "extracting"
                    break
                if event == 'Hybrid Extract':
                    operation = "hybrid_extracting"
                    break

            window.close()

            if operation == "embedding":

                window = self.create_embedding_window()

                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    if event == 'Algorithm Information':
                        self.display_information(event, values, operation)
                    if event == 'Embed':
                        algorithm_name, cover_file, message_file, key, save_path =\
                            values['input_algorithm'], values['cover_image'],\
                                values['message'], values['input_key'], values['save_folder']

                        window.close()
                        return [self.instantiators[algorithm_name],\
                            cover_file, message_file, key, save_path, operation]

                    if event == 'Back to Main Menu':
                        break

                window.close()


            if operation == "hybrid_embedding":

                window = self.create_hybrid_embedding_window()
                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    if event == 'Back to Main Menu':
                        break

                window.close()


            if operation == "extracting":

                window = self.create_extracting_window()

                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    if event == 'Algorithm Information':
                        self.check_algorithm_information(event, values, operation)
                    if event == 'Extract':
                        algorithm_name, stego_file, key, save_path =\
                            values['output_algorithm'], values['stego_image'],\
                                values['output_key'], values['save_folder']

                        window.close()
                        return [self.instantiators[algorithm_name],\
                            stego_file, key, save_path, operation]

                    if event == 'Back to Main Menu':
                        break

                window.close()


            if operation == "hybrid_extracting":

                window = self.create_hybrid_extracting_window()
                while True:
                    event, values = window.read()
                    if event is None:
                        sys.exit()
                    if event == 'Back to Main Menu':
                        break

                window.close()
