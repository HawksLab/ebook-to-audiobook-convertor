from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from app.service.player import QTMusicPlayerService
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
        from app.service.tts import KokoroTextToSpeachService
        from app.service.parser import TikaParserService

        self.progress.emit("Loading TTS...")
        tts_service = KokoroTextToSpeachService(music_player_service)
        self.progress.emit("Loading parser...")
        parser = TikaParserService()
        self.progress.emit("Starting Application...")
        time.sleep(2)

def on_loading_complete(splash):
    from app.ui import Ui_MainWindow
    global music_player_service, tts_service, parser, main_window
    main_window = Ui_MainWindow(music_player_service, tts_service, parser)
    splash.close()
    main_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/logo.ico"))  

    splash = QtWidgets.QMainWindow()
    splash_ui = Ui_SplashScreen()
    main_window = None
    music_player_service = QTMusicPlayerService() # Intializing this in main thread
    
    worker = LoadingThread(splash,splash_ui)
    worker.progress.connect(lambda msg: splash_ui.loadingStatus.setText(msg))
    worker.finished.connect(lambda: on_loading_complete(splash))
    worker.start()
    
    sys.exit(app.exec())