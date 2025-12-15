# EPUBSPLIT - Herramienta de División de EPUB

Una herramienta interactiva para dividir archivos EPUB en capítulos individuales. Permite seleccionar qué capítulos extraer y guardarlos como archivos EPUB separados.

## Requisitos

- Python 3.13 o superior
- Dependencias especificadas en `pyproject.toml`

## Instalación

### Opción 1: Con Dev Container (Recomendado)

1. **Requisitos:**
   - Docker Desktop instalado
   - VS Code con extensión "Dev Containers"

2. **Abrir en Dev Container:**
   - Abre la carpeta del proyecto en VS Code
   - Presiona `Cmd+Shift+P` (macOS) o `Ctrl+Shift+P` (Linux/Windows)
   - Escribe y selecciona: **"Dev Containers: Reopen in Container"**
   - Espera a que se construya la imagen y se inicie el contenedor

3. **Ejecutar dentro del contenedor:**
   ```bash
   python3 main.py
   ```

### Opción 2: Instalación local

1. **Clonar o descargar el proyecto**
   ```bash
   cd epubsplit
   ```

2. **Instalar dependencias**
   ```bash
   # Con uv (recomendado)
   uv sync
   
   # O con pip tradicional
   pip install beautifulsoup4 html5lib six
   ```

## Uso

### Ejecución interactiva (recomendado)

```bash
python main.py
```

El programa te guiará a través de:
1. Seleccionar un archivo EPUB del directorio `input/`
2. Ver la lista de capítulos disponibles
3. Elegir entre dividir todo o una selección
4. Especificar el rango de capítulos a extraer (si aplica)
5. Los archivos se crearán en `output/{nombre-del-archivo}/`

### Ejemplos de rangos

- `5` → Solo el capítulo 5
- `1-5` → Capítulos del 1 al 5
- `1,3,5` → Capítulos 1, 3 y 5
- `1-3,5,7-9` → Capítulos 1-3, 5 y 7-9

### Scripts de línea de comandos

Si prefieres usar los scripts individuales:

#### Ver capítulos de un EPUB
```bash
python list_split_lines.py input/mi_libro.epub
```

Muestra todos los capítulos con su índice, título y ubicación en el archivo.

#### Dividir capítulos específicos
```bash
python split_by_indices.py input/mi_libro.epub output/resultado 1 2 3
```

Divide los capítulos 1, 2 y 3 del EPUB especificado.

## Estructura de directorios

```
epubsplit/
├── .devcontainer/              # Configuración para Dev Containers
│   └── devcontainer.json       # Configuración de VS Code
├── input/                       # Coloca aquí tus archivos EPUB
│   └── .gitkeep
├── output/                      # Se crea automáticamente con resultados
│   └── .gitkeep
├── main.py                      # Script principal interactivo
├── epubsplit.py                 # Librería principal
├── pyproject.toml               # Configuración del proyecto
├── README.md                    # Este archivo
└── .gitignore                   # Archivo de ignorados de Git
```

**Notas sobre Git:**
- Las carpetas `input/` y `output/` están versionadas (archivos `.gitkeep`)
- El contenido de `input/` y `output/` NO se versiona
- Solo los EPUBs que generes localmente se ignoran automáticamente

## Archivos del proyecto

- **main.py** - Script interactivo principal (punto de entrada recomendado)
- **epubsplit.py** - Librería principal para manipular EPUB
- **pyproject.toml** - Configuración del proyecto y dependencias
- **.devcontainer/** - Configuración para ejecutar en contenedor Docker
  - `devcontainer.json` - Configuración de VS Code Dev Containers

## Licencia

GPL v3

## Autor original

Jim Miller (epubsplit base)
