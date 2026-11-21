"""Clase Reserva: integra cliente, servicio, duración y estado."""
from enum import Enum

from base import EntidadBase
from cliente import Cliente
from excepciones import ReservaInvalidaError, ServicioNoDisponibleError
from registro import log
from servicios import Servicio


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"


class Reserva(EntidadBase):
    IMPUESTO = 0.19  # IVA aplicado por defecto

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: float) -> None:
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        if not isinstance(horas, (int, float)) or not 0 < horas <= 12:
            raise ReservaInvalidaError("La duración debe estar entre 0 y 12 horas.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible.")
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = EstadoReserva.PENDIENTE

    def confirmar(self) -> float:
        """Confirma la reserva y devuelve el costo total con impuestos."""
        try:
            if self.estado is not EstadoReserva.PENDIENTE:
                raise ReservaInvalidaError(
                    f"Solo se confirman reservas pendientes (estado: {self.estado.value})."
                )
            costo = self.servicio.calcular_costo(self.horas, impuesto=self.IMPUESTO)
        except Exception as exc:
            log.error("Fallo al confirmar reserva #%s: %s", self.id, exc)
            raise
        else:  # solo si no hubo error
            self.estado = EstadoReserva.CONFIRMADA
            log.info("Reserva #%s confirmada. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            log.info("Intento de confirmación procesado para reserva #%s", self.id)

    def cancelar(self) -> None:
        """Cancela la reserva; no se permite si ya está cancelada o completada."""
        try:
            if self.estado in (EstadoReserva.CANCELADA, EstadoReserva.COMPLETADA):
                raise ReservaInvalidaError(
                    f"No se puede cancelar una reserva {self.estado.value}.")
        except ReservaInvalidaError as exc:
            log.error("Fallo al cancelar reserva #%s: %s", self.id, exc)
            raise
        self.estado = EstadoReserva.CANCELADA
        log.info("Reserva #%s cancelada.", self.id)

    def procesar(self) -> str:
        """Flujo completo: confirma (si está pendiente) y marca como completada.
        Los errores internos se encadenan en una ReservaInvalidaError con 'from'."""
        try:
            if self.estado is EstadoReserva.PENDIENTE:
                self.confirmar()
            if self.estado is not EstadoReserva.CONFIRMADA:
                raise ReservaInvalidaError(
                    f"No se puede procesar una reserva {self.estado.value}.")
            self.estado = EstadoReserva.COMPLETADA
        except ReservaInvalidaError:
            raise
        except Exception as exc:  # cualquier otro fallo se encadena con el original
            log.error("Fallo al procesar reserva #%s: %r", self.id, exc)
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}.") from exc
        else:
            log.info("Reserva #%s procesada y completada.", self.id)
            return f"Reserva #{self.id} completada."

    def describir(self) -> str:
        return (f"Reserva #{self.id} [{self.estado.value}] {self.cliente.nombre} -> "
                f"{self.servicio.nombre} x {self.horas}h")
