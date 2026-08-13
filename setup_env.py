from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import venv
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"


# Algunos paquetes tienen un nombre al importar y otro
# diferente al instalarlos con pip.
PACKAGE_MAP = {
    "PIL": "pillow",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "skimage": "scikit-image",
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
}


# Módulos estándar de Python: NO deben instalarse con pip.
STDLIB = set(sys.stdlib_module_names)


# ============================================================
# UTILIDADES DEL ENTORNO VIRTUAL
# ============================================================

def get_venv_python() -> Path:
    """Devuelve la ruta al ejecutable de Python del entorno virtual."""
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"

    return VENV_DIR / "bin" / "python"


def create_virtual_environment() -> None:
    """Crea .venv si todavía no existe."""
    if VENV_DIR.exists():
        print(f"✅ Entorno virtual encontrado: {VENV_DIR}")
        return

    print("\n🔨 Creando entorno virtual...")
    venv.create(
        VENV_DIR,
        with_pip=True
    )

    print(f"✅ Entorno creado en: {VENV_DIR}")


def upgrade_pip() -> None:
    """Actualiza pip dentro del entorno virtual."""
    python = get_venv_python()

    print("\n📦 Actualizando pip...")

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        check=True,
    )


# ============================================================
# LECTURA DE IMPORTS
# ============================================================

def extract_imports_from_code(code: str) -> set[str]:
    """
    Analiza código Python y devuelve los módulos principales
    encontrados en import y from ... import ...
    """

    imports = set()

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return imports

    for node in ast.walk(tree):

        # import numpy
        # import matplotlib.pyplot
        if isinstance(node, ast.Import):
            for alias in node.names:
                package = alias.name.split(".")[0]
                imports.add(package)

        # from PIL import Image
        # from matplotlib import pyplot
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                package = node.module.split(".")[0]
                imports.add(package)

    return imports


def extract_imports_from_python(file_path: Path) -> set[str]:
    """Extrae imports de un archivo .py."""

    try:
        code = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except OSError:
        return set()

    return extract_imports_from_code(code)


def extract_imports_from_notebook(file_path: Path) -> set[str]:
    """Extrae imports de las celdas de código de un .ipynb."""

    imports = set()

    try:
        with file_path.open(
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            notebook = json.load(file)

    except (OSError, json.JSONDecodeError):
        print(f"⚠️ No se pudo leer: {file_path.name}")
        return imports

    for cell in notebook.get("cells", []):

        if cell.get("cell_type") != "code":
            continue

        source = cell.get("source", [])

        if isinstance(source, list):
            code = "".join(source)
        else:
            code = source

        imports.update(
            extract_imports_from_code(code)
        )

    return imports


# ============================================================
# ESCANEO DE LA CARPETA
# ============================================================

def find_local_modules(folder: Path) -> set[str]:
    """
    Detecta módulos propios del proyecto para evitar intentar
    instalarlos desde PyPI.
    """

    modules = set()

    for file in folder.rglob("*.py"):
        modules.add(file.stem)

    return modules


def scan_folder(folder: Path) -> set[str]:
    """
    Busca archivos .py e .ipynb y obtiene todas las librerías
    importadas.
    """

    imports = set()

    python_files = list(folder.rglob("*.py"))
    notebooks = list(folder.rglob("*.ipynb"))

    print("\n🔎 Archivos encontrados:")
    print(f"   Python:   {len(python_files)}")
    print(f"   Notebook: {len(notebooks)}")

    for file in python_files:
        print(f"   📄 {file.relative_to(ROOT)}")
        imports.update(
            extract_imports_from_python(file)
        )

    for file in notebooks:
        print(f"   📓 {file.relative_to(ROOT)}")
        imports.update(
            extract_imports_from_notebook(file)
        )

    return imports


# ============================================================
# FILTRADO DE PAQUETES
# ============================================================

def filter_external_packages(
    imports: set[str],
    folder: Path
) -> set[str]:

    local_modules = find_local_modules(folder)

    external = set()

    for module in imports:

        # Ignorar librerías estándar
        if module in STDLIB:
            continue

        # Ignorar archivos/módulos creados por nosotros
        if module in local_modules:
            continue

        # Traducir nombre del import -> nombre de pip
        package = PACKAGE_MAP.get(
            module,
            module
        )

        external.add(package)

    return external


# ============================================================
# VERIFICAR SI YA ESTÁ INSTALADO
# ============================================================

def installed_packages() -> set[str]:
    """Obtiene los paquetes instalados actualmente en .venv."""

    python = get_venv_python()

    result = subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "list",
            "--format=json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    packages = json.loads(result.stdout)

    return {
        item["name"].lower().replace("_", "-")
        for item in packages
    }


def normalize_package_name(name: str) -> str:
    return name.lower().replace("_", "-")


# ============================================================
# INSTALACIÓN
# ============================================================

def install_packages(packages: set[str]) -> None:

    if not packages:
        print("\n✅ No hay nuevas librerías que instalar.")
        return

    python = get_venv_python()

    print("\n📦 Instalando:")

    for package in sorted(packages):
        print(f"   → {package}")

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            *sorted(packages),
        ],
        check=True,
    )


# ============================================================
# REQUIREMENTS
# ============================================================

def create_requirements(
    folder: Path,
    packages: set[str]
) -> None:

    requirements = folder / "requirements.txt"

    content = "\n".join(
        sorted(packages)
    )

    if content:
        content += "\n"

    requirements.write_text(
        content,
        encoding="utf-8"
    )

    print(
        f"\n📝 requirements.txt creado en:\n"
        f"   {requirements}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("       VISIÓN - GESTOR DE ENTORNO VIRTUAL")
    print("=" * 60)

    print("\n📁 Carpetas disponibles:\n")

    folders = [
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and path.name != "__pycache__"
    ]

    for folder in sorted(folders):
        print(f"   • {folder.name}")

    print()

    folder_name = input(
        "👉 Escribe la carpeta que deseas analizar: "
    ).strip()

    folder = ROOT / folder_name

    if not folder.exists():
        print(
            f"\n❌ La carpeta '{folder_name}' no existe."
        )
        return

    if not folder.is_dir():
        print(
            f"\n❌ '{folder_name}' no es una carpeta."
        )
        return

    print(
        f"\n🔍 Analizando: {folder.name}"
    )

    imports = scan_folder(folder)

    print("\n🐍 Imports encontrados:")

    if imports:
        for module in sorted(imports):
            print(f"   • {module}")
    else:
        print("   Ninguno")

    packages = filter_external_packages(
        imports,
        folder
    )

    print("\n📦 Librerías externas necesarias:")

    if packages:
        for package in sorted(packages):
            print(f"   • {package}")
    else:
        print("   Ninguna")

    # Crear entorno virtual
    create_virtual_environment()

    # Actualizar pip
    upgrade_pip()

    # Necesario para utilizar .venv como kernel de Jupyter
    packages.add("ipykernel")

    installed = installed_packages()

    missing = {
        package
        for package in packages
        if normalize_package_name(package)
        not in installed
    }

    print("\n🔍 Librerías que faltan:")

    if missing:
        for package in sorted(missing):
            print(f"   • {package}")
    else:
        print("   Ninguna 🎉")

    install_packages(missing)

    # requirements.txt contiene únicamente las dependencias
    # detectadas para ESTA semana/carpeta.
    create_requirements(
        folder,
        packages
    )

    print("\n" + "=" * 60)
    print("✅ TODO LISTO")
    print("=" * 60)

    print(
        f"\nEntorno virtual general:\n"
        f"   {VENV_DIR}"
    )

    print(
        "\nEn VS Code selecciona como Kernel el Python de:"
    )

    print(
        f"   {get_venv_python()}"
    )

    print(
        "\nPuedes ejecutar este mismo script cada vez que "
        "agregues una nueva semana."
    )


if __name__ == "__main__":
    main()