# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Dict


class RawEmail(ABC):
    @abstractmethod
    def source(self) -> str:
        pass

    @abstractmethod
    def destinations(self) -> List[str]:
        pass

    @abstractmethod
    def raw_message(self) -> Dict[str, str]:
        pass
