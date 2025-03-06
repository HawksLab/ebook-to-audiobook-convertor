from tika import parser
from abc import ABC, abstractmethod

class ParserService(ABC):
    @abstractmethod
    def parse(self) -> str:
        pass

class TikaParserService:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def parse(self) -> str:
        parsed = parser.from_file(self.file_path)
        return parsed['content']
