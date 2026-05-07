# AutoDJ (LangGraph)

Proyecto que analiza el BPM de tus canciones, ordena los temas para que los cambios sean suaves y genera una mezcla con crossfade.

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
