import sys
import json
import PySimpleGUI as gui
from algorithms.LSB import LSB
from algorithms.LSBM import LSBM
from algorithms.LSBMR import LSBMR
from algorithms.PVD import PVD
from algorithms.EA_LSBMR import EA_LSBMR
from edge_detectors.Sobel import Sobel

class GraphicalUserInterface(object):

    def __init__(self):

        self.app_name = "Steganograph-App-y"

        with open('data/algorithms.json') as f:
            a_data = json.load(f)
        with open('data/combinators.json') as g:
            c_data = json.load(g)
        with open('data/detectors.json') as h:
            d_data = json.load(h)

        self.algorithm_data = {}
        self.combinator_data = {}
        self.detector_data = {}

        for a_datum in a_data['algorithms']:
            self.algorithm_data[a_datum['name']] = a_datum['description']
        for c_datum in c_data['combinators']:
            self.combinator_data[c_datum['name']] = c_datum['description']
        for d_datum in d_data['detectors']:
            self.detector_data[d_datum['name']] = d_datum['description']

        self.algorithm_instantiators = {
            "LSB": LSB,
            "LSBM": LSBM,
            "LSBMR": LSBMR,
            "PVD": PVD,
            "EA-LSBMR": EA_LSBMR
        }

        self.detector_instantiators = {
            "Sobel": Sobel
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
                file_types=(("Image Files", "*.png"),))],
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
                gui.Combo(list(self.detector_data.keys()), size=(10, 1),
                key="First_input_detector"),
                gui.Button('First Detector Information')],
            [gui.Text('Edge Detector 2', size=(16, 1)),
                gui.Combo(list(self.detector_data.keys()), size=(10, 1),
                key="Second_input_detector"),
                gui.Button('Second Detector Information')],
            [gui.Text('Hybrid Technique', size=(16, 1)),
                gui.Combo(list(self.combinator_data.keys()), size=(10, 1), key="input_hybrid"),
                gui.Button('Hybrid Information')],
            [gui.Text('_' * 55)],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="hybrid_cover_image"), 
                gui.FileBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover', 
                file_types=(("Image Files", "*.png"),))],
            [gui.Text('Text file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="hybrid_message"),
                gui.FileBrowse(initial_folder=
                'C:/Users/faizz/University Work/Year 4/Advanced Project/Messages/Embedding', 
                file_types=(("Text Files", "*.txt"),))],
            [gui.Text('Secret key', size=(16, 1)), gui.Input(size=(40, 1), key="hybrid_in_key")],
            [gui.Text('Save Folder', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="hybrid_save_folder"),
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
                gui.Combo(list(self.detector_data.keys()), size=(10, 1),
                key="First_output_detector"),
                gui.Button('First Detector Information')],
            [gui.Text('Edge Detector 2', size=(16, 1)),
                gui.Combo(list(self.detector_data.keys()), size=(10, 1),
                key="Second_output_detector"),
                gui.Button('Second Detector Information')],
            [gui.Text('Hybrid Technique', size=(16, 1)),
                gui.Combo(list(self.combinator_data.keys()), size=(10, 1), key="output_hybrid"),
                gui.Button('Hybrid Information')],
            [gui.Text('_' * 55)],
            [gui.Text('Image file', size=(16, 1)),
                gui.In(size=(40, 1), enable_events=True, key="cover_image"), 
                gui.FileBrowse(file_types=(("Image Files", "*.png"),))],
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


    def create_info_window(self, data, name):

        info_screen = [
            [gui.Text('Information', font=('Helvetica', 15), justification='center')],
            [gui.Text('_'  * 70)],
            [gui.Text('')],
            [gui.Text(data[name], size=(60, 4))],
            [gui.Text('')],
            [gui.Button('Close')]
        ]

        info_window = gui.Window('{0} - Information'.format(self.app_name), info_screen)
        return info_window


    def display_algorithm_information(self, values, operation):

        if operation == "embedding":
            algorithm = values['input_algorithm']
        else:
            algorithm = values['output_algorithm']

        if algorithm:

            info_window = self.create_info_window(self.algorithm_data, algorithm)

            while True:
                event, values = info_window.read()
                if event in (None, 'Close'):
                    info_window.close()
                    break


    def display_detector_information(self, values, operation, position):

        if operation == "hybrid_embedding":
            detector = values[position + "_input_detector"]
        else:
            detector = values[position + '_output_detector']
        
        if detector:

            info_window = self.create_info_window(self.detector_data, detector)

            while True:
                event, values = info_window.read()
                if event in (None, 'Close'):
                    info_window.close()
                    break


    def display_combinator_information(self, values, operation):

        if operation == "hybrid_embedding":
            combinator = values['input_hybrid']
        else:
            combinator = values['output_hybrid']

        if combinator:

            info_window = self.create_info_window(self.combinator_data, combinator)

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
                        self.display_algorithm_information(values, operation)
                    if event == 'Embed':
                        algorithm_name, cover_file, message_file, key, save_path =\
                            values['input_algorithm'], values['cover_image'],\
                                values['message'], values['input_key'], values['save_folder']

                        window.close()
                        return [self.algorithm_instantiators[algorithm_name],\
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
                    if event == 'First Detector Information':
                        self.display_detector_information(values, operation, 'First')
                    if event == 'Second Detector Information':
                        self.display_detector_information(values, operation, 'Second')
                    if event == 'Hybrid Information':
                        self.display_combinator_information(values, operation)
                    if event == 'Hybrid Embed':
                        detector_1, detector_2, combinator, cover_file, message_file, key,\
                            save_path = values['First_input_detector'],\
                                values['Second_input_detector'], values['input_hybrid'],\
                                values['hybrid_cover_image'], values['hybrid_message'],\
                                values['hybrid_in_key'], values['hybrid_save_folder']
                        
                        window.close()
                        return [self.detector_instantiators[detector_1],\
                            self.detector_instantiators[detector_2], combinator, cover_file,\
                            message_file, key, save_path, operation]

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
                        return [self.algorithm_instantiators[algorithm_name],\
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
                    if event == 'First Detector Information':
                        self.display_detector_information(values, operation, 'First')
                    if event == 'Second Detector Information':
                        self.display_detector_information(values, operation, 'Second')
                    if event == 'Hybrid Information':
                        self.display_combinator_information(values, operation)
                    if event == 'Back to Main Menu':
                        break

                window.close()
