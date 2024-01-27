from datetime import datetime
import numpy as np
from itertools import product
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QScrollArea, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox


class OutputWindow(QWidget):

    def __init__(self, text, **kwargs):
        super().__init__()

        # build window layout depending on analysis method
        if text == "forward":
            main_layout = self.get_alpha_layout(a_matrix=kwargs['a_matrix'])
        elif text == "backward":
            main_layout = self.get_beta_layout(b_matrix=kwargs['b_matrix'], e_matrix=kwargs['e_matrix'], i_matrix=kwargs['i_matrix'], e_idx=kwargs['e_idx'])
        elif text == "viterbi":
            main_layout = self.get_decoding_layout(v_matrix=kwargs['v_matrix'], hidden_states=kwargs['hidden_states'])
        elif text == "baum welch":
            main_layout = self.get_learning_layout(p_matrix=kwargs['p_matrix'], e_matrix=kwargs['e_matrix'], i_matrix=kwargs['i_matrix'])

        # Set the layout for the new window
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(main_layout)

        scroll_area.setWidget(scroll_widget)

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll_area)

        self.setWindowTitle(text.capitalize())
        self.adjustSize()
        self.setMinimumSize(400,300)
    
    
    def get_alpha_layout(self, a_matrix):
        print('alpha layout')

        # Create main layout
        main_layout = QVBoxLayout()

        matrix_layout = QGridLayout()
        self.print_matrix(matrix_layout, a_matrix, 'Alpha: ')
        main_layout.addLayout(matrix_layout)
        main_layout.setAlignment(matrix_layout, Qt.AlignTop)

        sequence_probability = np.sum(a_matrix[-1,:])
        label = QLabel(f'Probability of sequence = {sequence_probability}', self)
        
        main_layout.addWidget(label)
        main_layout.setAlignment(label, Qt.AlignTop)

        return main_layout
    
    def get_beta_layout(self, b_matrix, e_matrix, i_matrix, e_idx):
        print('beta layout')

        # Create main layout
        main_layout = QVBoxLayout()

        matrix_layout = QGridLayout()
        self.print_matrix(matrix_layout, b_matrix, 'Beta: ')
        main_layout.addLayout(matrix_layout)
        main_layout.setAlignment(matrix_layout, Qt.AlignTop)

        sequence_probability = 0
        text = ''
        for i in range(len(b_matrix[0])):
            if(text == ''):
                text = text + f'    {b_matrix[0,i]} * {i_matrix[0,i]} * {e_matrix[i,e_idx]}\n'
            else:
                text = text + f'+ {b_matrix[0,i]} * {i_matrix[0,i]} * {e_matrix[i,e_idx]}\n'
            
            sequence_probability = sequence_probability + (b_matrix[0,i]*i_matrix[0,i]*e_matrix[i,e_idx])

        
        label = QLabel(f'Probability of sequence =\n{text}\n= {sequence_probability}', self)

        main_layout.addWidget(label)
        main_layout.setAlignment(label, Qt.AlignTop)

        return main_layout

    def get_decoding_layout(self, v_matrix, hidden_states):
        print('viterbi layout')
        # Create main layout
        main_layout = QVBoxLayout()

        matrix_layout = QGridLayout()
        self.print_matrix(matrix_layout, v_matrix, 'Viterbi: ')
        main_layout.addLayout(matrix_layout)
        main_layout.setAlignment(matrix_layout, Qt.AlignTop)

        sequence = {}
        for row_idx, row in enumerate(v_matrix):
            indices = np.where(row == row.max())[0].tolist() # get list of indices of highest viterbi value in each row
            sequence[row_idx]=[hidden_states[i] for i in indices]  # get equivalent list of states and store in dictionary

        all_combinations = list(product(*(sequence[key] for key in sequence.keys()))) # get allcombinations of these paths

        text = [', '.join(c) for c in all_combinations]
        text = '\n'.join(text)
        text = f"Most Likely Sequence of Hidden States:\n{text}"
            
        label = QLabel(text, self)
        main_layout.addWidget(label)
        main_layout.setAlignment(label, Qt.AlignTop)
        


        return main_layout
    
    def get_learning_layout(self, p_matrix, e_matrix, i_matrix):
        print('learning layout')
        # Create main layout
        main_layout = QVBoxLayout()
        transition_layout = QGridLayout()
        emission_layout = QGridLayout()
        initial_layout = QGridLayout()
        self.print_matrix(transition_layout, p_matrix, 'Updated Transition Matrix: ')
        self.print_matrix(emission_layout, e_matrix, 'Updated Emission Matrix: ')
        self.print_matrix(initial_layout, i_matrix, 'Updated Initial Distribution: ')
        main_layout.addLayout(transition_layout)
        main_layout.addLayout(emission_layout)
        main_layout.addLayout(initial_layout)

        save_button = QPushButton('Save as .npz file', self)
        save_button.clicked.connect(lambda: self.on_save(p_matrix, e_matrix, i_matrix))
        main_layout.addWidget(save_button)

        return main_layout

    def print_matrix(self, grid_layout, matrix, label_text):
# Add a label to the grid layout
        num_rows, num_columns = matrix.shape

        label = QLabel(label_text)
        grid_layout.addWidget(label, 0, 0, 1, num_columns)  # Span label across the entire row
        
        # Create and add QLineEdit widgets to the grid layout
        # kont hatba3 f QLabel bs di 4aklaha a7la
        for i in range(num_rows):
            for j in range(num_columns):
                element = QLineEdit(str(matrix[i, j]))
                
                element.setObjectName('MatElement') # 34an el css
                element.setAlignment(Qt.AlignCenter)
                element.setReadOnly(True)
                grid_layout.addWidget(element, i + 1, j)
    
    def on_save(self, p_matrix, e_matrix, i_matrix):
        # Create a dictionary with keys for each array
        data = {'p_matrix': p_matrix, 'e_matrix': e_matrix, 'i_matrix': i_matrix}
        # Generate a unique filename based on the current time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f'Stochastic Project\\hmm application\\saved_data\\updated_model_{current_time}.npz'
        # Save the arrays to an npz file
        np.savez(output_filename, **data)
        QMessageBox.information(self, 'Saved Successfully', f'File saved as {output_filename}')