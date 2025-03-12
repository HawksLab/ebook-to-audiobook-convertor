from kokoro import KPipeline
from abc import ABC, abstractmethod
import tempfile
import soundfile as sf

class TextToSpeachService(ABC):
    @abstractmethod
    def generate(self, text: str, voice: str, speed: int):
        pass


class KokoroTextToSpeachService(TextToSpeachService):
    def __init__(self):
        self.pipeline = KPipeline(lang_code='a')

    def generate(self, text: str, voice: str = 'af_heart', speed: int = 1):
        lines = text.split("\n")
        length = len(lines)
        file_paths = []
        j = 1
        for line in lines:
            self.generator = self.pipeline(
                line, voice=voice, 
                speed=speed,
            )

            for i, (gs, ps, audio) in enumerate(self.generator):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file_path = temp_file.name
                    file_paths.append(temp_file_path)
                    with sf.SoundFile(temp_file_path, mode='w', samplerate=24000, channels=1, format='WAV') as f:
                        f.write(audio)
            print(f"converted line {j}/{length}")
            j+=1

        return file_paths
