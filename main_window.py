from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QApplication

from hidden_window import HiddenWindow
from help_window import HelpWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.tab_widget = QTabWidget(self)
        self.window1 = HelpWindow(self)
        self.window2 = HiddenWindow(self)

        self.tab_widget.addTab(self.window1, 'Help Page')
        self.tab_widget.addTab(self.window2, 'Hidden Marcov Chain Model')

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)
        self.setWindowTitle('Stochastic App')
        self.setMinimumSize(1000,800)
        self.setGeometry(400, 100, 1000, 800)

    #  override l method fl QWidget 34an lama a2fel el app el windows kolaha te2fel
    def closeEvent(self, event):
        QApplication.quit() 

