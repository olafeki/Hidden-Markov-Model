import numpy as np
import string
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QScrollArea, QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QVBoxLayout, QPushButton, QMessageBox, QFileDialog

from output_window import OutputWindow
from graph_window import TransitionDiagram

import hmm_implementation as hmm


class HiddenWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # list ha7ot fiha el windows eli btefta7
        self.windows = []
        self.num_hidden = 3
        self.num_observation = 2

        self.edit_text3 = None
        self.edit_text4 = None
        self.submit_button = None  
        self.submit_button2 = None 

        self.initUI(parent)

    def initUI(self, parent=None):
        # # Create widgets
        # label1 = QLabel('Main Layout with Nested Layouts:')
        # dol tala3tohom fo2 34an el change_matrix w keda

        # Set up main layout
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(main_layout)

        scroll_area.setWidget(scroll_widget)

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll_area)

        # Set up window
        #self.setLayout(main_layout)
        # self.setGeometry(300, 300, 600, 300)
        # self.setWindowTitle('Hidden Markov Chain')

        # Text line to ask the user to choose
        choose_label = QLabel('Choose what you would like to do: ')

        # Nested layout in cell (0, 0)
        nested_layout_00 = QVBoxLayout()
        nested_layout_00.addStretch(1)  # Add stretch to center the labels and line edits
        self.combo_box = QComboBox(self)
        self.combo_box.addItem('Encoding - Forward Algorithm')
        self.combo_box.addItem('Encoding - Backward Algorithm')
        self.combo_box.addItem('Decoding - Viterbi Algorithm')
        self.combo_box.addItem('Learning - Baum Welch Algorithm')
        self.combo_box.addItem('Draw Transition Graph')
        nested_layout_00.addWidget(choose_label)
        nested_layout_00.addWidget(self.combo_box)
        nested_layout_00.addStretch(1)

        # Nested layout in cell (0, 1)
        nested_layout_01 = QHBoxLayout()
        self.edit_text1 = QLineEdit(self)
        edit_label1 = QLabel("Enter the number of possible hidden states:")
        self.edit_text2 = QLineEdit(self)
        edit_label2 = QLabel("Enter the number of possible observations:")

        # nafs fekret lw el button clicked.. bs ha5aliha lw el value bta3et el QLineEdit et8ayaraet
        self.edit_text1.textChanged.connect(self.change_matrix)
        self.edit_text2.textChanged.connect(self.change_matrix)

        nested_layout_01.addWidget(edit_label1)
        nested_layout_01.addWidget(self.edit_text1)
        nested_layout_00.addStretch(1)
        nested_layout_01.addWidget(edit_label2)
        nested_layout_01.addWidget(self.edit_text2)
        nested_layout_01.addStretch(1)


        # Nested layout in cell (1, 0)
        self.nested_layout_10 = QFormLayout()
        self.edit_text3 = QLineEdit(self)
        self.edit_text4 = QLineEdit(self)
        self.edit_text5 = QLineEdit(self)
        edit_label3 = QLabel("Enter values of hidden states separated by comma :")
        edit_label4 = QLabel("Enter values of observations separated by comma :")
        edit_label5 = QLabel("Enter values of observed sequence separated by comma :")
        
        enumerate_button = QPushButton('auto-enumerate')
        enumerate_button.setStyleSheet('QPushButton{margin-left:200px;margin-right:50px}')
        enumerate_button.clicked.connect(self.enumerate_values)

        self.nested_layout_10.addRow(edit_label3, self.edit_text3)
        self.nested_layout_10.addRow(edit_label4, self.edit_text4)
        self.nested_layout_10.addRow(QLabel(), enumerate_button)
        self.nested_layout_10.addRow(edit_label5, self.edit_text5)

        


        # # Submit button
        # self.submit_button = QPushButton("Submit", self)
        # self.submit_button.clicked.connect(self.on_submit)

        # main_layout.addWidget(label1)
        main_layout.addLayout(nested_layout_00)
        main_layout.addSpacing(25)
        main_layout.addLayout(nested_layout_01)
        main_layout.addLayout(self.nested_layout_10)
        # main_layout.addWidget(self.submit_button)
        # ha3mel button y-load data 34an 7asah manteki

        load_button = QPushButton('Read matrices from .npz file', self)
        load_button.clicked.connect(self.on_load)
        load_note = QLabel('Note: \tMatrices should be saved in order - transition matrix, emission matrix, initial distribution. \n\tMatrices should be the same dimension as below.')
        main_layout.addSpacing(25)
        main_layout.addWidget(load_button)
        main_layout.addWidget(load_note)
        main_layout.addSpacing(15)

        # di el 7eta eli kanet btet3emel on_submit

        self.matrices_layout = QVBoxLayout()
        self.transition_layout = QGridLayout()
        self.emission_layout = QGridLayout()
        self.initial_layout = QGridLayout()
        self.matrices_layout.addLayout(self.transition_layout)
        self.matrices_layout.addLayout(self.emission_layout)
        self.matrices_layout.addLayout(self.initial_layout)
        main_layout.addLayout(self.matrices_layout)

        # hena ha3mel el matrices bl default values eli ana 7ataha fl code
        self.create_and_add_grid_layout('t', "Transition Matrix", 3, 3)
        self.create_and_add_grid_layout('e', "Emission Matrix", 3, 2)
        self.create_and_add_grid_layout('i', "Initial Distribution", 1, 3)

        # set default values
        self.edit_text1.setText('3')  
        self.edit_text2.setText('2')
        self.edit_text3.setText('A, B, C')
        self.edit_text4.setText('0, 1')
        self.edit_text5.setText('0, 1, 0')
        # lw fi wa2t isa ne3mel button auto enumerate ll values of states di

        # Calculate button
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.clicked.connect(self.on_calculate)
        self.layout().addWidget(self.calculate_button)

        # self.adjustSize()
        #self.setMaximumSize(self.size())
        # self.setMinimumSize(1000,800)
        # # set window position
        # self.move(400,100)

    
    def change_matrix(self):
        # da eli kan bye7sal gowa el on_submit bardo
        try:
            self.num_hidden = int(self.edit_text1.text())
            self.num_observation = int(self.edit_text2.text())

            self.create_and_add_grid_layout('t', "Transition Matrix", self.num_hidden, self.num_hidden)
            self.create_and_add_grid_layout('e', "Emission Matrix", self.num_hidden, self.num_observation)
            self.create_and_add_grid_layout('i', "Initial State", 1, self.num_hidden)    
        except:
            return
        
    def on_calculate(self):
        # m7tagin n-check 3ala 100 7aga hena
        
        # check for null values
        if(self.edit_text1.text() and self.edit_text2.text() and self.edit_text3.text() and self.edit_text4.text() and self.edit_text5.text()):
            pass
        else:
            QMessageBox.warning(self, 'Invalid Input', 'Please fill in all inputs.')
            return
        
        # get num of possible obs/states as int.
        try:
            self.num_hidden = int(self.edit_text1.text())
            self.num_observation = int(self.edit_text2.text())
        except:
            QMessageBox.warning(self, 'Invalid Input', 'An error occured. Invalid input for number of possible observations/hidden states.')
            return
        
        hidden_states_values, observations_values, observed_sequence = [], [], []
        # get comma separated values
        hidden_states_values = self.edit_text3.text().replace(" ", "").split(",")
        
        try:
            # if values are int
            observations_values = self.string_to_list(self.edit_text4.text())
            observed_sequence = self.string_to_list(self.edit_text5.text())
        except:
            # if values are str
            observations_values = self.edit_text4.text().replace(" ", "").split(",")
            observed_sequence = self.edit_text5.text().replace(" ", "").split(",")
            # Create a dictionary mapping observations to indices
            observation_index = {obs: index for index, obs in enumerate(observations_values)}
            # Use list comprehension to map the sequence to indices
            observed_sequence = [observation_index[obs] for obs in observed_sequence]

        # check that length of values/observations equals the entered numbers
        if(len(hidden_states_values) != self.num_hidden):
            QMessageBox.warning(self, 'Invalid Input', f'Hidden State should be {self.num_hidden}. Please enter the values correctly.')
            return
        if(len(observations_values) != self.num_observation):
            QMessageBox.warning(self, 'Invalid Input', f'Observations should be {self.num_observation}. Please enter the values correctly.')
            return
        
        p_matrix = self.get_matrix(self.transition_layout,self.num_hidden,self.num_hidden, 'transition')
        if(not np.any(p_matrix)):
            return
        
        e_matrix = self.get_matrix(self.emission_layout,self.num_hidden,self.num_observation,'emission')
        if(not np.any(e_matrix)):
            return
        
        i_matrix = self.get_matrix(self.initial_layout,1,self.num_hidden, 'initial distribution')
        if(not np.any(i_matrix)):
            return
        
        print(p_matrix)
        print(e_matrix)
        print(i_matrix)
        print(observed_sequence)
        
        # show window
        index = self.combo_box.currentIndex()

        if index == 0:
            # Forward step
            alpha = hmm.forward_algorithm(obs=observed_sequence, P=p_matrix, E=e_matrix, pi=i_matrix)
            print(alpha)

            self.windows.append(OutputWindow('forward', a_matrix=alpha))
            self.windows[-1].show()
        elif index == 1:
            # Backward step
            beta = hmm.backward_algorithm(obs_seq=observed_sequence, start_prob=i_matrix, transition_prob=p_matrix, emission_prob=e_matrix)
            beta = beta
            print(beta)

            self.windows.append(OutputWindow('backward', b_matrix=beta, e_matrix=e_matrix, i_matrix=i_matrix, e_idx=observed_sequence[0]))
            self.windows[-1].show()
        elif index == 2:
            v = hmm.viterbi(p=p_matrix.tolist(), e=e_matrix.tolist(), pi=i_matrix.tolist()[0], o=observed_sequence,
                            number_steps=len(observed_sequence), number_states=len(p_matrix))
            v = np.array(v)
            self.windows.append(OutputWindow('viterbi', v_matrix=v, hidden_states=hidden_states_values))
            self.windows[-1].show()
        elif index == 3:
            p, e, pi=hmm.baum_welch(p=p_matrix.tolist(), e=e_matrix.tolist(), pi=i_matrix.tolist()[0], o=observed_sequence,
                                    number_steps=len(observed_sequence), number_states=len(p_matrix))
            p = np.array(p)
            e = np.array(e)
            pi = np.array([pi])
            # p, e, pi = p_matrix, e_matrix, i_matrix

            self.windows.append(OutputWindow('baum welch', p_matrix=p, e_matrix=e, i_matrix=pi))
            self.windows[-1].show()
        elif index == 4:
            if(isinstance(observations_values[0],int)):
                str_observations = [str(element) for element in observations_values]
            else:
                str_observations = observations_values
            self.windows.append(TransitionDiagram(transition_matrix=p_matrix.tolist(), emission_matrix=e_matrix.tolist(),
                                                state_names=hidden_states_values, observation_names=str_observations))
            self.windows[-1].show()
            return
            

    def create_and_add_grid_layout(self, type, label_text, num_rows, num_columns):

        default_value = 1 / num_columns  # Equal probabilities for each element in a row

        if type == 't':
            grid_layout = self.transition_layout
        elif type == 'e':
            grid_layout = self.emission_layout
        elif type == 'i':
            grid_layout = self.initial_layout
        
        self.clearLayout(grid_layout)
        
        # Add a label to the grid layout
        label = QLabel(label_text)
        grid_layout.addWidget(label, 0, 0, 1, num_columns)  # Span label across the entire row
        
        # Create and add QLineEdit widgets to the grid layout
        for i in range(num_rows):
            for j in range(num_columns):
                line_edit = QLineEdit(self)
                line_edit.setObjectName('MatElement') # 34an el css
                line_edit.setAlignment(Qt.AlignCenter)
                line_edit.setText(str(default_value)) # set default value
                grid_layout.addWidget(line_edit, i + 1, j)
        
        # self.adjustSize()

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clearLayout(item.layout())

    def get_matrix(self, grid_layout, nrow, ncol, type):
        
        # Get the number of rows and columns in the grid layout
        rows = grid_layout.rowCount()
        cols = grid_layout.columnCount()

        # Create an empty NumPy array to store the matrix
        matrix = np.zeros((nrow, ncol))

        # Iterate through each item in the grid layout
        for row in range(rows):
            for col in range(cols):
                # Get the widget at the specified row and column
                item = grid_layout.itemAtPosition(row, col)
                
                # Check if the item is a QLineEdit
                if item is not None and isinstance(item.widget(), QLineEdit):
                    try:
                        # Extract the text from the QLineEdit and store it in the matrix
                        # -1 34an awel row byeb2a el 3enwan
                        matrix[row-1, col] = float(item.widget().text())
                        # print(item.widget().text())
                    except Exception as e:
                        print(e)
                        QMessageBox.warning(self, 'Invalid Input', f'Invalid value {item.widget().text()} in {type} matrix cell ({row},{col})')
                        return 

        return matrix 

    def string_to_list(self, str):
        mylst = str.split(',')
        mylst= [int(n) for n in mylst]
        return mylst
    
    def enumerate_values(self):
        # Create a string of numbers separated by commas
        observation_string = ', '.join(str(i) for i in range(0, self.num_observation))
        # Create a string of the first n letters separated by commas
        states_string = ', '.join(string.ascii_uppercase[:self.num_hidden])
        # set text
        self.edit_text3.setText(states_string)
        self.edit_text4.setText(observation_string)

    
    def on_load(self):
        file_path = self.show_file_dialog()
        if(not file_path):
            return
        
        loaded_data = np.load(file_path)
        keys = list(loaded_data.keys())

        if(len(keys) != 3):
            QMessageBox.warning(self, 'Data Load Failed', f"Your file contains {len(keys)} matrices, instead of 3.")
            return

        # Access individual arrays using their keys
        loaded_p_matrix = loaded_data[keys[0]]
        loaded_e_matrix = loaded_data[keys[1]]
        loaded_i_matrix = loaded_data[keys[2]]

        v = self.load_matrix_into_layout(self.transition_layout, loaded_p_matrix, dims=(self.num_hidden,self.num_hidden))
        if(v == -1):
            return
        v = self.load_matrix_into_layout(self.emission_layout, loaded_e_matrix, dims=(self.num_hidden,self.num_observation))
        if(v == -1):
            return
        v = self.load_matrix_into_layout(self.initial_layout, loaded_i_matrix, dims=(1,self.num_hidden))
        if(v == -1):
            return


        return
    
    def show_file_dialog(self):
        # Open the file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # On some platforms, this flag avoids using the native file dialog
        file_dialog = QFileDialog(self, options=options)
        file_dialog.setFileMode(QFileDialog.ExistingFile)  # Set the dialog mode to select an existing file
        file_dialog.setNameFilter("NPZ Files (*.npz);;All Files (*)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            # Get the selected file(s)
            selected_file = file_dialog.selectedFiles()[0]
            print("Selected File(s):", selected_file)
            return selected_file
        
    def load_matrix_into_layout(self, grid_layout, matrix, dims):
        # Get the number of rows and columns in the grid layout
        rows = grid_layout.rowCount()
        cols = grid_layout.columnCount()

        # - 1 34an el label wa5da awel row
        if(dims != matrix.shape):
            print((rows,cols))
            print(matrix.shape)
            QMessageBox.warning(self, 'Data Load Failed', "Unable to load data from file. Matrix dimensions don't match.")
            return -1

        # Iterate through each item in the grid layout
        for row in range(rows):
            for col in range(cols):
                # Get the widget at the specified row and column
                item = grid_layout.itemAtPosition(row, col)
                # Check if the item is a QLineEdit
                if item is not None and isinstance(item.widget(), QLineEdit):
                    item.widget().setText(str(matrix[row-1,col]))

        return 0

