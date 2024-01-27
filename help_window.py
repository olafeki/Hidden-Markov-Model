from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QSizePolicy
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt

class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        file_path = r'Stochastic Project\hmm application\media\vid.mp4'

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)

        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.play)

        self.seekSlider = QSlider(Qt.Horizontal)
        self.seekSlider.setRange(0, 0)  # The range will be set dynamically based on the video duration
        self.seekSlider.sliderMoved.connect(self.setMediaPosition)

        layout.addWidget(self.seekSlider)
        layout.addWidget(self.playButton)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

        self.mediaPlayer.durationChanged.connect(self.setDuration)
        self.mediaPlayer.positionChanged.connect(self.setPosition)
        self.mediaPlayer.stateChanged.connect(self.updateButtons)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def setMediaPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def setDuration(self, duration):
        self.seekSlider.setRange(0, duration)

    def setPosition(self, position):
        self.seekSlider.setValue(position)

    def updateButtons(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")
