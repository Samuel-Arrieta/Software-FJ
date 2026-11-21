"""Simulación de 12 operaciones del Sistema Integral de Gestión de Software FJ.
Sin bases de datos: todo vive en listas de objetos. Solo se escribe el archivo de logs."""
from cliente import Cliente
from excepciones import ClienteInvalidoError, ErrorSoftwareFJ
from registro import ARCHIVO_LOG, log
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, SalaReunion


class GestorFJ:
    """Administra clientes, servicios y reservas en listas en memoria."""

    def __init__(self) -> None:
        self.clientes: list[Cliente] = []
        self.servicios: list = []
        self.reservas: list[Reserva] = []

    def ejecutar(self, numero: int, titulo: str, operacion):
        """Corre una operación; captura cualquier error del sistema y sigue operando."""
        print(f"\n[{numero:02d}] {titulo}")
        try:
            resultado = operacion()
        except ErrorSoftwareFJ as exc:
            print(f"     ✗ Error controlado: {exc}")
            log.error("Operación %02d (%s) falló: %s", numero, titulo, exc)
        except Exception as exc:  # error inesperado: se registra y el programa continúa
            print(f"     ✗ Error inesperado: {exc!r}")
            log.critical("Operación %02d (%s) error inesperado: %r", numero, titulo, exc)
        else:
            # Si el resultado es una entidad, se muestra su descripción legible
            texto = resultado.describir() if hasattr(resultado, "describir") else resultado
            print(f"     ✓ {texto}")
            log.info("Operación %02d (%s) exitosa.", numero, titulo)
            return resultado
        finally:
            pass  # aquí podrían liberarse recursos si fuera necesario

    # ---- operaciones de negocio ----
    def registrar_cliente(self, *datos) -> Cliente:
        try:
            cliente = Cliente(*datos)
        except TypeError as exc:  # parámetros faltantes o sobrantes
            raise ClienteInvalidoError("Faltan parámetros para registrar el cliente.") from exc
        self.clientes.append(cliente)
        return cliente

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        return servicio

    def reservar(self, cliente, servicio, horas) -> Reserva:
        reserva = Reserva(cliente, servicio, horas)
        self.reservas.append(reserva)
        return reserva


def main() -> None:
    g = GestorFJ()
    log.info("=== Inicio de simulación Software FJ ===")

    # --- Clientes ---
    ana = g.ejecutar(1, "Registrar cliente válido (Ana)", lambda: g.registrar_cliente(
        "ana gómez", "1043123456", "ana@correo.com", "3001234567"))
    g.ejecutar(2, "Registrar cliente con correo inválido", lambda: g.registrar_cliente(
        "Luis Pérez", "1043999888", "luis-correo", "3109876543"))
    luis = g.ejecutar(3, "Registrar cliente válido (Luis)", lambda: g.registrar_cliente(
        "Luis Pérez", "1043999888", "luis@correo.com", "3109876543"))
    g.ejecutar(4, "Registrar cliente con documento no numérico", lambda: g.registrar_cliente(
        "Marta Ruiz", "ABC123", "marta@correo.com", "3201112233"))

    # --- Servicios ---
    sala = g.ejecutar(5, "Crear sala de reuniones válida", lambda: g.agregar_servicio(
        SalaReunion("Sala Bolívar", 50000, 12)))
    g.ejecutar(6, "Crear servicio con tarifa negativa", lambda: g.agregar_servicio(
        AlquilerEquipo("Proyector", -100, 2)))
    equipo = g.ejecutar(7, "Crear alquiler de equipo válido", lambda: g.agregar_servicio(
        AlquilerEquipo("Portátiles", 8000, 5)))
    asesoria = g.ejecutar(8, "Crear asesoría válida", lambda: g.agregar_servicio(
        AsesoriaEspecializada("Ciberseguridad", 120000, "senior")))

    # --- Reservas ---
    r1 = g.ejecutar(9, "Reserva exitosa (Ana - Sala, 3 h)", lambda: g.reservar(ana, sala, 3))
    g.ejecutar(10, "Reserva con duración inválida (30 h)", lambda: g.reservar(luis, equipo, 30))
    equipo.disponible = False
    g.ejecutar(11, "Reserva de servicio no disponible", lambda: g.reservar(luis, equipo, 2))
    r2 = g.ejecutar(12, "Reserva exitosa (Luis - Asesoría, 2 h)",
                    lambda: g.reservar(luis, asesoria, 2))

    # --- Confirmaciones y sobrecarga de costos ---
    g.ejecutar(13, "Confirmar reserva de Ana", lambda: f"Total con IVA: ${r1.confirmar():,.2f}")
    g.ejecutar(14, "Confirmar de nuevo (estado inválido)", lambda: r1.confirmar())
    g.ejecutar(15, "Costo asesoría: solo horas", lambda: asesoria.calcular_costo(2))
    g.ejecutar(16, "Costo asesoría: IVA 19% + descuento 10%",
               lambda: asesoria.calcular_costo(2, 0.19, 0.10))
    g.ejecutar(17, "Descuento fijo ($20.000) con singledispatch",
               lambda: asesoria.aplicar_descuento(20000, 2))
    g.ejecutar(18, "Descuento por texto ('15%')", lambda: asesoria.aplicar_descuento("15%", 2))
    g.ejecutar(19, "Descuento de tipo no soportado", lambda: asesoria.aplicar_descuento([1], 2))
    g.ejecutar(20, "Cancelar reserva de Luis", lambda: r2.cancelar() or r2.describir())
    g.ejecutar(21, "Cancelar de nuevo (operación no permitida)", lambda: r2.cancelar())
    g.ejecutar(22, "Registrar cliente con parámetros faltantes",
               lambda: g.registrar_cliente("Marta Ruiz"))
    g.ejecutar(23, "Cálculo inconsistente (impuesto 150%)",
               lambda: asesoria.calcular_costo(2, impuesto=1.5))
    g.ejecutar(24, "Crear asesoría con nivel inexistente", lambda: g.agregar_servicio(
        AsesoriaEspecializada("Cloud", 90000, "maestro")))
    r3 = g.ejecutar(25, "Reserva exitosa (Ana - Sala, 1 h)", lambda: g.reservar(ana, sala, 1))
    g.ejecutar(26, "Procesar reserva completa (confirmar + completar)", lambda: r3.procesar())
    g.ejecutar(27, "Procesar reserva ya completada", lambda: r3.procesar())
    g.ejecutar(28, "Reserva con cliente inexistente (None)", lambda: g.reservar(None, sala, 2))

    print("\n=== Resumen final ===")
    for lista in (g.clientes, g.servicios, g.reservas):
        for item in lista:
            print(" -", item.describir())
    log.info("=== Fin de simulación: sistema estable ===")
    print(f"\nLog generado en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
