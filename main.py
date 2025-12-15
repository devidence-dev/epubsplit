#!/usr/bin/env python3
"""
Script principal para ejecutar epubsplit de forma interactiva.
Lee EPUBs del directorio input, muestra sus capítulos y permite dividirlos.
"""

import os
import sys
import re
from pathlib import Path
import epubsplit


def get_input_files() -> list[str]:
    """Obtiene los archivos EPUB del directorio input."""
    input_dir = Path("input")
    if not input_dir.exists():
        input_dir.mkdir(exist_ok=True)
    
    epub_files = list(input_dir.glob("*.epub"))
    return sorted([f.name for f in epub_files])


def slug(s: str) -> str:
    """Convierte un título a un slug válido para nombres de archivo."""
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-") or "chapter"


def get_chapters(epub_path: str) -> list[dict]:
    """Obtiene la lista de capítulos de un EPUB."""
    with open(epub_path, "rb") as f:
        s = epubsplit.SplitEpub(f)
        lines = s.get_split_lines()
    
    chapters = []
    for i, line in enumerate(lines):
        toc_titles = line.get("toc") or []
        title = " > ".join(toc_titles) if toc_titles else "(sin TOC)"
        chapters.append({
            "index": i,
            "title": title,
            "href": line.get("href"),
            "anchor": line.get("anchor") or ""
        })
    
    return chapters


def display_chapters(chapters: list[dict]) -> None:
    """Muestra la lista de capítulos de forma legible."""
    print("\n" + "="*80)
    print("CAPÍTULOS DISPONIBLES:")
    print("="*80)
    for ch in chapters:
        print(f"  [{ch['index']:04d}] {ch['title']}")
    print("="*80 + "\n")


def parse_chapter_range(range_str: str, max_index: int) -> list[int]:
    """
    Parsea una entrada de rango de capítulos.
    Acepta: "5" o "1-5" o "1,3,5" o "1-3,5,7-9"
    """
    indices = []
    parts = range_str.replace(" ", "").split(",")
    
    for part in parts:
        if "-" in part:
            start, end = part.split("-")
            start, end = int(start.strip()), int(end.strip())
            indices.extend(range(start, min(end + 1, max_index + 1)))
        else:
            idx = int(part.strip())
            if idx <= max_index:
                indices.append(idx)
    
    return sorted(list(set(indices)))  # Remover duplicados y ordenar


def split_epub(input_path: str, output_dir: str, indices: list[int], filename: str) -> None:
    """Divide un EPUB en capítulos específicos."""
    with open(input_path, "rb") as f:
        s = epubsplit.SplitEpub(f)
        lines = s.get_split_lines()
        
        for idx in indices:
            if idx >= len(lines):
                print(f"⚠️  El índice {idx} no existe (máximo: {len(lines)-1})")
                continue
            
            line = lines[idx]
            toc_titles = line.get("toc") or []
            title = toc_titles[0] if toc_titles else f"part-{idx:04d}"
            
            os.makedirs(output_dir, exist_ok=True)
            out_path = os.path.join(output_dir, f"{idx:04d}-{slug(title)}.epub")
            
            with open(out_path, "wb") as out:
                s.write_split_epub(out, [idx], titleopt=title)
            
            print(f"  ✓ Creado: {out_path}")


def main():
    """Función principal con interfaz interactiva."""
    print("\n" + "="*80)
    print("EPUBSPLIT - Herramienta de división de EPUB")
    print("="*80 + "\n")
    
    # Obtener archivos disponibles
    epub_files = get_input_files()
    
    if not epub_files:
        print("❌ No hay archivos EPUB en el directorio 'input'")
        print("Por favor, coloca archivos .epub en ./input/\n")
        return
    
    # Mostrar archivos disponibles
    print("ARCHIVOS DISPONIBLES EN ./input/:")
    for i, filename in enumerate(epub_files, 1):
        print(f"  [{i}] {filename}")
    print()
    
    # Seleccionar archivo
    while True:
        try:
            choice = input("Selecciona el número del archivo a dividir (1-{}): ".format(len(epub_files)))
            file_idx = int(choice) - 1
            if 0 <= file_idx < len(epub_files):
                selected_file = epub_files[file_idx]
                break
            else:
                print("❌ Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
    
    input_path = os.path.join("input", selected_file)
    print(f"\n📖 Cargando: {selected_file}...")
    
    # Obtener capítulos
    try:
        chapters = get_chapters(input_path)
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return
    
    display_chapters(chapters)
    
    # Seleccionar opción de división
    print("OPCIONES DE DIVISIÓN:")
    print("  [1] Dividir TODO (todos los capítulos)")
    print("  [2] Dividir SELECCIÓN (especificar rango)\n")
    
    while True:
        option = input("Elige una opción (1 o 2): ").strip()
        if option in ["1", "2"]:
            break
        print("❌ Opción inválida. Ingresa 1 o 2.")
    
    # Procesar selección
    if option == "1":
        indices = [ch["index"] for ch in chapters]
        print(f"\n✓ Se dividirán todos los {len(indices)} capítulos.")
    else:
        print("\nEjemplos de entrada:")
        print("  '5'        → Solo el capítulo 5")
        print("  '1-5'      → Capítulos del 1 al 5")
        print("  '1,3,5'    → Capítulos 1, 3 y 5")
        print("  '1-3,5,7-9' → Capítulos 1-3, 5 y 7-9\n")
        
        while True:
            try:
                range_input = input("Ingresa el rango de capítulos: ").strip()
                indices = parse_chapter_range(range_input, len(chapters) - 1)
                
                if not indices:
                    print("❌ No se seleccionaron capítulos válidos. Intenta de nuevo.")
                    continue
                
                print(f"✓ Se dividirán {len(indices)} capítulo(s): {indices}")
                break
            except (ValueError, IndexError):
                print("❌ Formato inválido. Intenta de nuevo.")
    
    # Crear estructura de directorios
    output_dir = os.path.join("output", slug(Path(selected_file).stem))
    print(f"\n📁 Destino: {output_dir}/\n")
    
    # Confirmar antes de proceder
    confirm = input("¿Deseas continuar? (s/n): ").strip().lower()
    if confirm not in ["s", "sí", "si", "yes"]:
        print("Cancelado.")
        return
    
    print(f"\n🔄 Dividiendo {len(indices)} capítulo(s)...\n")
    
    try:
        split_epub(input_path, output_dir, indices, selected_file)
        print(f"\n✅ ¡Completado! Los archivos están en: {output_dir}/\n")
    except Exception as e:
        print(f"\n❌ Error durante la división: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
