from kokoro import KPipeline
from abc import ABC, abstractmethod
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6 import QtWidgets
from app.ui import Ui_progressWindow
import tempfile
import soundfile as sf

global_text = ""
global_voice = ""
class TextToSpeachService(ABC):
    @abstractmethod
    def generate(self, text: str, voice: str, speed: int):
        pass


class KokoroTextToSpeachService(TextToSpeachService):
    def __init__(self, player_service):
        self.player_service = player_service
        self.pipeline = KPipeline(lang_code='a')
        self.file_paths = []
 

    def generate(self, main_window_controller, text: str, voice: str = 'af_heart', speed: int = 1):
        global global_text, global_voice
        global_voice = voice
        global_text = text
        progress_bar = QtWidgets.QMainWindow()
        progress_ui = Ui_progressWindow()

        self.worker = TTSThread(main_window_controller, progress_bar, progress_ui, self, text, voice, speed)
        self.merged_file_paths = []
        self.worker.progress.connect(lambda msg: progress_ui.progressBar.setProperty("value", ((int(msg.split('/')[0]) / int(msg.split('/')[1])) * 100 )))
        self.worker.finished.connect(lambda: (progress_bar.close()))
        # self.worker.run(text, voice, speed)
        self.worker.start()

class TTSThread(QThread):
        progress = pyqtSignal(str)
        finished = pyqtSignal(list)

        def __init__(self, main_window_controller, progress_bar, progress_ui, tts_service, text, voice, speed):
            super().__init__()
            progress_ui.setupUi(progress_bar)
            progress_bar.show()
            self.main_window_controller = main_window_controller
            self.tts_service = tts_service
            self.text = text
            self.voice = voice
            self.speed = speed

        def run(self, speed:int = 1):
            global global_text, global_voice
            text = global_text
            voice = global_voice
            lines = text.split("\n")
            length = len(lines)
            file_paths = []
            j = 1
            for line in lines:
                self.generator = self.tts_service.pipeline(
                    line, voice=voice, 
                    speed=speed,
                )

                for i, (gs, ps, audio) in enumerate(self.generator):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                        temp_file_path = temp_file.name
                        file_paths.append(temp_file_path)
                        with sf.SoundFile(temp_file_path, mode='w', samplerate=24000, channels=1, format='WAV') as f:
                            f.write(audio)
                self.progress.emit(f"{j}/{length}")
                print(f"converted line {j}/{length}")
                j+=1
            self.merged_file_path = self.tts_service.player_service.concatinate(file_paths)
            self.main_window_controller.merged_audio_path = self.merged_file_path
            self.finished.emit(file_paths)