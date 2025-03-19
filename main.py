from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from app.ui import Ui_SplashScreen
import sys
import time

class LoadingThread(QThread):
    progress = pyqtSignal(str)

    def __init__(self, splash, splash_ui):
        super().__init__()
        splash_ui.setupUi(splash)
        splash.show()


    def run(self):
        global music_player_service, tts_service, parser, controller
        from app.service.player import QTMusicPlayerService
        from app.service.tts import KokoroTextToSpeachService
        from app.service.parser import TikaParserService

        self.progress.emit("Loading player...")
        music_player_service = QTMusicPlayerService()
        self.progress.emit("Loading TTS...")
        tts_service = KokoroTextToSpeachService()
        self.progress.emit("Loading parser...")
        parser = TikaParserService()
        self.progress.emit("Starting Application...")
        time.sleep(2)

def on_loading_complete(splash, MainWindow):
    from app.ui import Ui_MainWindow
    global music_player_service, tts_service, parser 
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, music_player_service, tts_service, parser)
    splash.close()
    MainWindow.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/logo.ico"))  

    splash = QtWidgets.QMainWindow()
    splash_ui = Ui_SplashScreen()
    MainWindow = QtWidgets.QMainWindow()
    
    worker = LoadingThread(splash,splash_ui)
    worker.progress.connect(lambda msg: splash_ui.loadingStatus.setText(msg))
    worker.finished.connect(lambda: on_loading_complete(splash, MainWindow))
    worker.start()
    
    sys.exit(app.exec())