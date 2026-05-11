# AutoDJ (LangGraph)

AutoDJ es un pipeline de agentes en LangGraph que toma una carpeta de canciones, estima su BPM, ordena la secuencia para transiciones suaves y exporta una mezcla con crossfade junto con un reporte JSON.

## Qué hace

- Ingesta archivos de audio desde una carpeta.
- Analiza BPM y duracion por tema.
- Planifica el orden para minimizar saltos de BPM.
- Mezcla segmentos con crossfade y exporta el resultado.
- Genera un reporte JSON con metadatos de cada pista.

## Agentes (LangGraph)

El flujo se modela con `StateGraph` y cuatro agentes, cada uno responsable de un paso del estado:

- `ingest_agent`: lista archivos y prepara rutas de entrada.
- `bpm_agent`: estima BPM y duración por archivo.
- `plan_agent`: ordena pistas para cambios suaves de BPM.
- `mix_agent`: construye la mezcla, exporta el audio y el reporte.

## Requisitos

- Python 3.10+
- ffmpeg disponible en el PATH (necesario para exportar MP3 con pydub)

Instala dependencias de Python:

```
pip install -r requirements.txt
```

## Uso

Mezclar canciones desde la carpeta local:

```
python main.py --songs-dir Canciones --seconds-per-track 40 --crossfade-sec 8
```

Elegir formato y salida (el formato se deduce por la extension):

```
python main.py --songs-dir Canciones --seconds-per-track 40 --crossfade-sec 8 --output output/mix.wav
```

## Salidas

- output/mix.mp3 (por defecto)
- output/mix_report.json

## Datos incluidos

- En la rama `main`, la carpeta `Canciones` se distribuye comprimida para descargar.
- En `output/` se incluye un `mix.wav` de ejemplo: en `main` es la version sin beat sync y en `feature/beat-sync` es la version con beat sync.

## Informe JSON

El reporte se guarda en UTF-8 con tildes correctas y contiene:

- `title`: nombre del archivo sin extension
- `bpm`: BPM estimado
- `duration_sec`: duracion total en segundos
- `path`: ruta completa al archivo

## Opciones CLI

- `--songs-dir`: carpeta con audio (mp3, wav, flac, m4a, aac, ogg)
- `--seconds-per-track`: segundos usados por cancion
- `--crossfade-sec`: segundos de crossfade
- `--analysis-seconds`: segundos analizados para BPM
- `--output`: ruta y extension del archivo de mezcla
- `--report`: ruta del JSON de reporte

## Notas

- El analisis de BPM usa solo los primeros N segundos (por defecto 90) para acelerar.
- El crossfade se limita para evitar errores en segmentos cortos.
