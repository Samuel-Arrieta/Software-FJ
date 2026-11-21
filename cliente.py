"""Clase Cliente con encapsulación y validaciones."""
import re

from base import EntidadBase
from excepciones import ClienteInvalidoError

_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ. Atributos privados validados mediante setters."""

    def __init__(self, nombre: str, documento: str, correo: str, telefono: str) -> None:
        super().__init__()
        # Cada asignación pasa por el setter y por tanto por su validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if any(ch.isdigit() for ch in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self.__nombre = valor.strip().title()

    # ---- documento ----
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError("El documento debe ser numérico (6 a 12 dígitos).")
        self.__documento = valor

    # ---- correo ----
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not _PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self.__correo = valor.lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError("El teléfono debe ser numérico (7 a 10 dígitos).")
        self.__telefono = valor

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento}, {self.correo})"
