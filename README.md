# Monitor de estabilidad de APP-04

Programa de menú que analiza las descargas y las caídas semanales de una aplicación móvil.

**Módulo:** IC44 — Fundamentos de programación en Python

**Unidad:** 2 — Estructuras de control, depuración y excepciones

**Autores:** ricardo.palomares.viseras · pablo.morales.gabarron

**Equipo asignado:** APP-04

**Repositorio:** https://github.com/Rykyp/monitor-app-04

## Datos y funcionamiento

La aplicación asignada tiene 12 semanas de datos. La tasa de caídas se calcula por cada mil
descargas (‰). Las semanas sin descargas se consideran de mantenimiento.

El programa ofrece estas opciones:

1. Listado semanal.
2. Resumen.
3. Estabilidad por semana.
4. Primera semana que alcanza un umbral.
5. Mejor racha sin problemas.
6. Previsión de crecimiento.
7. Consultar una semana.
8. Comprobar los datos.
9. Salir, con confirmación.

Al arrancar, se comprueban los datos. Los errores impiden continuar y las semanas de
mantenimiento generan avisos. Ctrl+C permite interrumpir el programa.

## Ejecución en local

Requiere Python 3.10 o superior. Solo utiliza la biblioteca estándar; no necesita instalar
paquetes externos. Ejecuta los comandos desde la raíz del repositorio.

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python monitor_app.py
```

En Windows, con PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python monitor_app.py
```

## Ejecución desde Docker Hub

Repositorio previsto de la imagen: https://hub.docker.com/r/4132853/monitor-app-04

Después de que Ricardo publique la versión, se podrá ejecutar con Docker, sin instalar
Python ni descargar este repositorio:

```bash
docker run --rm -it --pull always 4132853/monitor-app-04:1.0.0
```

`-i` mantiene abierta la entrada para responder a las preguntas y `-t` asigna un terminal.
`--rm` elimina el contenedor al terminar y `--pull always` comprueba la imagen publicada.

La entrega requiere las arquitecturas `linux/amd64` y `linux/arm64`, las etiquetas `1.0.0`
y `latest`, y que la imagen `1.0.0` corresponda al código de la etiqueta Git `v1.0.0`.
La publicación y su comprobación están pendientes.

## Construcción local de la imagen

Desde la raíz del repositorio, con Docker disponible:

```bash
docker build -t monitor-app-04:1.0.0 .
docker run --rm -it monitor-app-04:1.0.0
```

El Dockerfile utiliza Python 3.14 y ejecuta `monitor_app.py`.

## Estructura del proyecto

```text
.
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── monitor_app.py
```

`.gitignore` excluye el entorno virtual y los archivos generados por Python.
`.dockerignore` excluye del contexto de construcción Git, el entorno virtual y otros
archivos innecesarios. `requirements.txt` se conserva aunque no haya dependencias externas.
