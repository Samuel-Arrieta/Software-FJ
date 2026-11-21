# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Proyecto del curso **Programación (213023)**, UNAD — Fase 4: Prácticas simuladas.

Aplicación orientada a objetos en Python que gestiona clientes, servicios y reservas de la empresa ficticia **Software FJ** (reserva de salas, alquiler de equipos y asesorías especializadas). **No usa bases de datos**: toda la información vive en objetos y listas en memoria; los archivos se emplean únicamente para el registro de eventos y errores (`logs/software_fj.log`).

## Requisitos

- Python 3.10 o superior (no requiere librerías externas).

## Ejecución

```bash
python main.py
```

Al ejecutarse, el programa simula 28 operaciones (válidas e inválidas), muestra el resultado de cada una en consola, imprime un resumen final y genera el archivo `logs/software_fj.log`. La aplicación continúa funcionando después de cada error.

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSoftwareFJ` y derivadas). |
| `registro.py` | Configuración del archivo de logs. |
| `base.py` | Clase abstracta general `EntidadBase`. |
| `cliente.py` | Clase `Cliente` con encapsulación (`@property`) y validaciones. |
| `servicios.py` | Clase abstracta `Servicio` y servicios `SalaReunion`, `AlquilerEquipo`, `AsesoriaEspecializada`. |
| `reserva.py` | Clase `Reserva` (cliente, servicio, duración y estado) con confirmar, cancelar y procesar. |
| `main.py` | `GestorFJ` (listas en memoria) y simulación de operaciones. |

## Conceptos de POO aplicados

- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `EntidadBase`; los tres servicios especializados heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `calcular_costo_base`, `describir` y `validar_parametros`.
- **Encapsulación:** atributos privados de `Cliente` expuestos mediante propiedades con validación.
- **Sobrecarga de métodos:** `calcular_costo(horas, impuesto=0, descuento=0)` con parámetros opcionales y `aplicar_descuento()` con `singledispatchmethod` (según el tipo del argumento).

## Manejo de excepciones

- Excepciones personalizadas para clientes, servicios, disponibilidad, reservas y cálculo de costos.
- Uso de `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones (`raise ... from`).
- Todos los errores y eventos relevantes se registran en `logs/software_fj.log`.

## Autor

Grupo:213023_47 
Samuel David Arrieta Rios