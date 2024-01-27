from datetime import datetime
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from graphviz import Digraph

class TransitionDiagram(QWidget):
    def __init__(self, transition_matrix, emission_matrix, state_names, observation_names):
        super().__init__()

        self.transition_matrix = transition_matrix
        self.emission_matrix = emission_matrix
        self.state_names = state_names
        self.observation_names = observation_names

        self.image_data = None
        
        self.init_ui()

    # def __init__(self):
    #     super().__init__()

    #     self.image_data = None

    #     self.transition_matrix = [
    #         [0.99,0.01],
    #         [0.01,0.99]
    #     ]

    #     self.emission_matrix = [
    #         [0.8, 0.2],
    #         [0.1, 0.9]
    #     ]

    #     self.state_names = [f'S_{i}' for i in range(len(self.transition_matrix))]
    #     self.observation_names = [f'Ob_{i}' for i in range(len(self.emission_matrix[0]))]

    #     self.init_ui()

    def init_ui(self):

        # self.setStyleSheet('background-color: #1E1E1E; color: #FFFFFF;')  # Dark mode style

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.create_diagram()

        save_button = QPushButton('Save as .png', self)
        save_button.clicked.connect(self.savePng)
        self.main_layout.addWidget(save_button)

        self.setMinimumSize(800,600)
        self.adjustSize()
        self.setWindowTitle('Transition Diagram')
        self.show()

    def create_diagram(self):
        graph = Digraph('TransitionDiagram', format='png', graph_attr={'bgcolor': 'transparent', 'fontcolor': 'white','dpi': '140'})

        # Add states to the graph with light blue color
        for i, state in enumerate(self.state_names):
            graph.node(state, color='lightblue', fontcolor='white')

        # Add observations to the graph with light blue color
        for i, observation in enumerate(self.observation_names):
            graph.node(observation, color='lightblue', fontcolor='white')

        # Add transitions to the graph with light blue color
        for i, from_state in enumerate(self.state_names):
            for j, to_state in enumerate(self.state_names):
                prob = self.transition_matrix[i][j]
                if prob > 0:
                    graph.edge(from_state, to_state, label=f'{prob:.2f}', color='lightblue', fontcolor='white', penwidth='1.5')

        # Add emission connections to the graph with light blue color
        for i, state in enumerate(self.state_names):
            for j, observation in enumerate(self.observation_names):
                prob = self.emission_matrix[i][j]
                if prob > 0:
                    graph.edge(state, observation, label=f'{prob:.2f}', color='lightblue', fontcolor='white', penwidth='1.5')

        # Save the graph as a PNG file
        self.image_data = graph.pipe(format='png')

        # Display the graph
        self.display_graph()

    def display_graph(self):
        # Load the PNG file generated by Graphviz
        pixmap = QPixmap()
        if(self.image_data):
            pixmap.loadFromData(self.image_data)

        # Create a QGraphicsScene and add the image to it
        scene = QGraphicsScene(self)
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)

        # Create a QGraphicsView and set the scene
        view = QGraphicsView(self)
        view.setScene(scene)

        # Set up some basic animations
        view.setRenderHint(QPainter.Antialiasing, True)
        view.setRenderHint(QPainter.SmoothPixmapTransform, True)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # add graph to the layout
        self.main_layout.addWidget(view)

    def savePng(self):
        
        if self.image_data:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f'Stochastic Project\\hmm application\\saved_png\\transition_graph_{current_time}.png'
            
            with open(output_filename, 'wb') as file:
                file.write(self.image_data)
            
            QMessageBox.information(self, 'Saved Successfully', f'File saved as {output_filename}')


# def main():
#     app = QApplication(sys.argv)
#     ex = TransitionDiagram()
#     sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()
