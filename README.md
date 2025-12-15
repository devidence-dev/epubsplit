# EPUBSPLIT - EPUB Splitting Tool

An interactive tool to split EPUB files into individual chapters. Allows selecting which chapters to extract and save them as separate EPUB files.

## Requirements

- Python 3.13 or higher
- Dependencies specified in `pyproject.toml`

## Installation

### Option 1: With Dev Container (Recommended)

1. **Requirements:**
   - Docker Desktop installed
   - VS Code with "Dev Containers" extension

2. **Open in Dev Container:**
   - Open the project folder in VS Code
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Linux/Windows)
   - Type and select: **"Dev Containers: Reopen in Container"**
   - Wait for the image to build and the container to start

3. **Run inside the container:**
   ```bash
   python3 main.py
   ```

### Option 2: Local Installation

1. **Clone or download the project**
   ```bash
   cd epubsplit
   ```

2. **Install dependencies**
   ```bash
   # With uv (recommended)
   uv sync
   
   # Or with traditional pip
   pip install beautifulsoup4 html5lib six
   ```

## Usage

### Interactive execution (recommended)

```bash
python main.py
```

The program will guide you through:
1. Select an EPUB file from the `input/` directory
2. View the list of available chapters
3. Choose between splitting all or a selection
4. Specify the range of chapters to extract (if applicable)
5. Files will be created in `output/{file-name}/`

### Range examples

- `5` → Only chapter 5
- `1-5` → Chapters 1 to 5
- `1,3,5` → Chapters 1, 3, and 5
- `1-3,5,7-9` → Chapters 1-3, 5, and 7-9

### Command line scripts

If you prefer to use individual scripts:

#### View chapters of an EPUB
```bash
python list_split_lines.py input/my_book.epub
```

Shows all chapters with their index, title, and location in the file.

#### Split specific chapters
```bash
python split_by_indices.py input/my_book.epub output/result 1 2 3
```

Splits chapters 1, 2, and 3 from the specified EPUB.

## Directory structure

```
epubsplit/
├── .devcontainer/              # Dev Containers configuration
│   └── devcontainer.json       # VS Code configuration
├── input/                       # Place your EPUB files here
│   └── .gitkeep
├── output/                      # Automatically created with results
│   └── .gitkeep
├── main.py                      # Main interactive script
├── epubsplit.py                 # Main library
├── pyproject.toml               # Project configuration
├── README.md                    # This file
└── .gitignore                   # Git ignore file
```

**Notes about Git:**
- The `input/` and `output/` folders are versioned (`.gitkeep` files)
- The content of `input/` and `output/` is NOT versioned
- Only locally generated EPUBs are automatically ignored

## Project files

- **main.py** - Main interactive script (recommended entry point)
- **epubsplit.py** - Main library for manipulating EPUB
- **pyproject.toml** - Project configuration and dependencies
- **.devcontainer/** - Configuration to run in Docker container
  - `devcontainer.json` - VS Code Dev Containers configuration

## License

GPL v3

## Credits

- **epubsplit.py**: Based on [JimmXinu's EpubSplit](https://github.com/JimmXinu/EpubSplit/blob/main/epubsplit.py)
