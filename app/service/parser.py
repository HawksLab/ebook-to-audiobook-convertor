from tika import parser
from abc import ABC, abstractmethod

class ParserService(ABC):
    @abstractmethod
    def parse(self) -> str:
        pass

class TikaParserService:
    def __init__(self):
        self.file_path = None
    
    def parse(self, file_path) -> str:
        parsed = parser.from_file(file_path)
        return parsed['content']
