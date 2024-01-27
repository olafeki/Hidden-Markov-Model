import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from welcome_window import WelcomeWindow

app = QApplication(sys.argv)
with open(r"Stochastic Project/hmm application/stylesheets/aqua_dark.css") as style:
    my_style = style.read()

app.setStyleSheet(my_style)
app.setWindowIcon(QIcon(r"Stochastic Project\hmm application\media\sunny.png"))
ex = WelcomeWindow()
ex.show()
sys.exit(app.exec_())


