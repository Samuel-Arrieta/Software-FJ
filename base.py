"""Clase abstracta general del sistema."""
from abc import ABC, abstractmethod
from itertools import count


class EntidadBase(ABC):
    """Clase abstracta general: toda entidad tiene un id único y se describe."""

    _contador = count(1)  # generador compartido de identificadores

    def __init__(self) -> None:
        self._id = next(EntidadBase._contador)

    @property
    def id(self) -> int:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad concreta devuelve su descripción en texto."""
