from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from main_window import MainWindow

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create an instance of the MainWindow
        self.main_window = MainWindow()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Welcome message label
        welcome_label = QLabel('Welcome to our Application!', self)
        welcome_label.setStyleSheet("font-size: 30pt;")

        # HMM Picture
        pixmap = QPixmap(r"Stochastic Project\hmm application\media\full.png") # load image as pixmap
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)

        # Button to go to the main window
        button = QPushButton('Start', self)
        button.clicked.connect(self.show_main_window)  # Connect to the method

        # Center the widgets in the layout
        layout.addWidget(welcome_label, alignment=Qt.AlignCenter)
        layout.addWidget(image_label, alignment=Qt.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('HMM App')
        self.setMinimumSize(1000,800)
        # set window position
        self.move(400,100)

    def show_main_window(self):
        # Hide the welcome window and show the main window
        self.hide()
        self.main_window.show()

