# Fast TCP Port Scanner

Escáner de puertos TCP en Python con ejecución concurrente. Incluye control de señales para salir de forma segura y prueba simple de cabeceras HTTP cuando el puerto parece un servicio web.

## Características
- Concurrencia con `ThreadPoolExecutor` (por defecto 50 hilos).
- Soporte de puertos en rango (`1-1000`), lista (`22,80,443`) o único (`443`).
- Timeout por socket (1s por defecto) y cierre ordenado ante `Ctrl+C`.

## Requisitos
- Python 3.8+
- Sin dependencias externas (librerías estándar).

## Uso

```bash
python3 port_scanner.py -t <IP|HOST> -p <PUERTOS> [-w <WORKERS>] [--timeout <SEGUNDOS>]
```

Ejemplos breves:
- `python3 port_scanner.py -t 192.168.1.1 -p 1-1024`
- `python3 port_scanner.py -t 192.168.1.1 -p 22,80,443`
- `python3 port_scanner.py -t 192.168.1.1 -p 443`

## Salida esperada
- Imprime `[OPEN] <puerto>/tcp` cuando el puerto está abierto.
- Si responde como HTTP/HTTPS, muestra algunas cabeceras con una solicitud `HEAD`.

## Consideraciones
- El intento de cabeceras HTTP no aplica a todos los servicios ni sustituye un escaneo de versiones completo.
- Use esta herramienta únicamente en entornos donde tenga autorización.
