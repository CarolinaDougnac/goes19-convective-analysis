"""
Herramientas para descargar datos GOES (u otros satélites) para el proyecto
GOES-19 Ecuador.

La idea es separar la lógica de descarga del resto del análisis.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List
import logging

import requests

logger = logging.getLogger(__name__)


def ensure_dir(path: os.PathLike | str) -> Path:
    """Crea un directorio si no existe y devuelve el Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def download_file(url: str, out_dir: os.PathLike | str) -> Path:
    """
    Descarga un archivo desde `url` a la carpeta `out_dir`.
    Si el archivo ya existe, no lo descarga de nuevo.

    Parameters
    ----------
    url : str
        URL completa del archivo a descargar.
    out_dir : str or Path
        Carpeta destino.

    Returns
    -------
    Path
        Ruta local del archivo descargado.
    """
    out_dir = ensure_dir(out_dir)
    filename = url.split("/")[-1]
    out_path = out_dir / filename

    if out_path.exists():
        logger.info(f"Ya existe, no se descarga de nuevo: {out_path}")
        return out_path

    logger.info(f"Descargando {url} -> {out_path}")
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()

    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    logger.info(f"Descarga completa: {out_path}")
    return out_path


def download_many(urls: Iterable[str], out_dir: os.PathLike | str) -> List[Path]:
    """
    Descarga múltiples archivos desde una lista de URLs.

    Parameters
    ----------
    urls : iterable of str
        URLs a descargar.
    out_dir : str or Path
        Carpeta destino.

    Returns
    -------
    list of Path
        Lista de rutas locales de los archivos descargados.
    """
    results: List[Path] = []
    for url in urls:
        try:
            p = download_file(url, out_dir)
            results.append(p)
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Error descargando {url}: {exc}")
    return results


# --------------------------------------------------------------------------- #
# Nota: La estructura exacta de las URLs de GOES-19 depende de la fuente
# (por ejemplo, AWS, NOAA, etc.). Aquí dejamos una función "plantilla" para
# que puedas adaptarla a tu flujo real.
# --------------------------------------------------------------------------- #


def build_goes_example_url(base_url: str, filename: str) -> str:
    """
    Construye una URL simple a partir de un base_url y un nombre de archivo.

    Esta función es un ejemplo y debe adaptarse a la estructura real
    de tu proveedor de datos GOES (AWS, NOAA, etc.).

    Parameters
    ----------
    base_url : str
        URL base (por ejemplo, de un bucket público).
    filename : str
        Nombre del archivo.

    Returns
    -------
    str
        URL completa.
    """
    return f"{base_url.rstrip('/')}/{filename}"

