

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from core.enums import SourceType
from core.models import Candidate


class BaseReader(ABC):

    def __init__(self, input_path: str | Path) -> None:
        self.input_path = Path(input_path)

    @property
    def reader_name(self) -> str:
       
        return self.__class__.__name__

    @property
    def exists(self) -> bool:
        return self.input_path.exists()

    def _validate_source(self) -> None:
        
        if not self.exists:
            raise FileNotFoundError(
                f"Input file not found: {self.input_path}"
            )

    @property
    @abstractmethod
    def source_type(self) -> SourceType:
       
        raise NotImplementedError

    @abstractmethod
    def extract_candidate(self) -> Candidate:
        
        raise NotImplementedError