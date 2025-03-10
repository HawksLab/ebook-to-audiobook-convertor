from abc import ABC, abstractmethod
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl
import io

class PlayerService(ABC):
    @abstractmethod
    def play(self, file_path: str):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

class QTMusicPlayerService(PlayerService):
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

    def play(self, file_path: bytes):
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def resume(self):
        self.player.resume()