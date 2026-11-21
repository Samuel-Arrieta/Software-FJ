"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio se crea con parámetros incorrectos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva es inconsistente o su estado no permite la acción."""


class CalculoCostoError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros del cálculo de costos son inválidos."""
