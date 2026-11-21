"""Clase abstracta Servicio y tres servicios especializados."""
from abc import abstractmethod
from functools import singledispatchmethod

from base import EntidadBase
from excepciones import CalculoCostoError, ServicioInvalidoError


class Servicio(EntidadBase):
    """Clase abstracta: define el contrato común de todos los servicios."""

    def __init__(self, nombre: str, tarifa_hora: float) -> None:
        super().__init__()
        # Solo se guardan los datos; cada subclase llama a validar_parametros()
        # cuando ya tiene todos sus atributos asignados.
        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self._disponible = True

    @abstractmethod
    def validar_parametros(self) -> None:
        """Valida los parámetros del servicio. Las subclases lo sobrescriben y
        reutilizan la validación común con super().validar_parametros()."""
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ServicioInvalidoError("El servicio requiere un nombre.")
        if (not isinstance(self._tarifa_hora, (int, float)) or isinstance(self._tarifa_hora, bool)
                or self._tarifa_hora <= 0):
            raise ServicioInvalidoError("La tarifa por hora debe ser un número positivo.")
        self._nombre = self._nombre.strip()
        self._tarifa_hora = float(self._tarifa_hora)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo antes de impuestos/descuentos; cada servicio lo define a su manera."""

    # ---- Sobrecarga 1: parámetros opcionales (impuesto y descuento) ----
    def calcular_costo(self, horas: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Variantes: calcular_costo(h) | calcular_costo(h, 0.19) | calcular_costo(h, 0.19, 0.10)."""
        if horas <= 0:
            raise CalculoCostoError("La duración debe ser mayor que cero.")
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoCostoError("Impuesto y descuento deben estar entre 0 y 1.")
        base = self.calcular_costo_base(horas)
        return round(base * (1 - descuento) * (1 + impuesto), 2)

    # ---- Sobrecarga 2: según el tipo del argumento (singledispatch) ----
    @singledispatchmethod
    def aplicar_descuento(self, descuento, horas: float = 1) -> float:
        raise CalculoCostoError(f"Tipo de descuento no soportado: {type(descuento).__name__}")

    @aplicar_descuento.register(int)
    @aplicar_descuento.register(float)
    def _(self, descuento, horas: float = 1) -> float:
        """Descuento como valor fijo en pesos."""
        return round(max(self.calcular_costo_base(horas) - descuento, 0), 2)

    @aplicar_descuento.register(str)
    def _(self, descuento, horas: float = 1) -> float:
        """Descuento como porcentaje en texto, p. ej. '15%'."""
        try:
            pct = float(descuento.strip().rstrip("%")) / 100
        except ValueError as exc:
            raise CalculoCostoError(f"Porcentaje inválido: '{descuento}'.") from exc
        return self.calcular_costo(horas, descuento=pct)


class SalaReunion(Servicio):
    """Reserva de salas: el costo depende de la capacidad."""

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int) -> None:
        super().__init__(nombre, tarifa_hora)
        self._capacidad = capacidad
        self.validar_parametros()

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if not isinstance(self._capacidad, int) or self._capacidad < 1:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero ≥ 1.")

    def calcular_costo_base(self, horas: float) -> float:
        recargo = 1.2 if self._capacidad > 10 else 1.0  # salas grandes cuestan 20% más
        return self._tarifa_hora * horas * recargo

    def describir(self) -> str:
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}, ${self._tarifa_hora:,.0f}/h)"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por unidades más un seguro fijo."""

    def __init__(self, nombre: str, tarifa_hora: float, unidades: int, seguro: float = 5000) -> None:
        super().__init__(nombre, tarifa_hora)
        self._unidades = unidades
        self._seguro = seguro
        self.validar_parametros()

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if not isinstance(self._unidades, int) or self._unidades < 1:
            raise ServicioInvalidoError("Las unidades deben ser un entero ≥ 1.")
        if not isinstance(self._seguro, (int, float)) or self._seguro < 0:
            raise ServicioInvalidoError("El seguro no puede ser negativo.")

    def calcular_costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self._unidades + self._seguro

    def describir(self) -> str:
        return f"Equipo '{self.nombre}' ({self._unidades} u., ${self._tarifa_hora:,.0f}/h c/u)"


class AsesoriaEspecializada(Servicio):
    """Asesorías: la tarifa sube según el nivel del asesor."""

    _FACTORES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre: str, tarifa_hora: float, nivel: str) -> None:
        super().__init__(nombre, tarifa_hora)
        self._nivel = nivel
        self.validar_parametros()

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if self._nivel not in self._FACTORES:
            raise ServicioInvalidoError(
                f"Nivel '{self._nivel}' no válido: {list(self._FACTORES)}.")

    def calcular_costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self._FACTORES[self._nivel]

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' (nivel {self._nivel}, ${self._tarifa_hora:,.0f}/h)"
