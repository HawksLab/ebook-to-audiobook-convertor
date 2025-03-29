from abc import ABC, abstractmethod
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import tempfile
import soundfile as sf
import numpy as np

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

class QTMusicPlayerService(PlayerService):
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(1.0)
        self.player.setAudioOutput(self.audio_output)
    
    def concatinate(self, audio_temp_paths):
        audio_data = []
        samplerate = None
        for temp_path in audio_temp_paths:
            data, sr = sf.read(temp_path)
            audio_data.append(data)
            if samplerate is None:
                samplerate = sr

        # Concatenate all audio data
        concatenated_audio = np.concatenate(audio_data)

        # Write the concatenated audio data to a new temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file_path = temp_file.name
            sf.write(temp_file_path, concatenated_audio, samplerate)

        return temp_file_path

    def play(self, audio_temp_path):
        self.player.setSource(QUrl.fromLocalFile(audio_temp_path))
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()
    
    def resume(self):
        self.player.play()