"""
Funciones de visualización para escenas GOES en mapas con Cartopy.

Incluye soporte para:
- ploteo del campo (por ejemplo, temperatura de brillo)
- sobreposición de track de vuelo
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr


def plot_goes_scene(
    da: xr.DataArray,
    extent: Optional[Tuple[float, float, float, float]] = None,
    cmap: str = "turbo",
    title: Optional[str] = None,
    flight_track: Optional[Tuple[Sequence[float], Sequence[float]]] = None,
    save_path: Optional[str | Path] = None,
    show: bool = False,
) -> None:
    """
    Dibuja una escena GOES sobre un mapa simple.

    Parameters
    ----------
    da : xr.DataArray
        Campo a mostrar (ya recortado a la región de interés).
    extent : (lon_min, lon_max, lat_min, lat_max), optional
        Extensión del mapa en coordenadas geográficas.
    cmap : str, default 'turbo'
        Colormap de Matplotlib.
    title : str, optional
        Título de la figura.
    flight_track : (lons, lats), optional
        Tupla con listas/arrays de longitudes y latitudes del vuelo.
    save_path : str or Path, optional
        Ruta donde guardar la figura (PNG, etc.). Si es None, no se guarda.
    show : bool, default False
        Si True, muestra la figura en pantalla.
    """
    # Proyección del dato (asumimos lat/lon en PlateCarree)
    data_crs = ccrs.PlateCarree()

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=data_crs)

    if extent is not None:
        ax.set_extent(extent, crs=data_crs)

    # Coastlines y gridlines simples
    ax.coastlines(resolution="50m", linewidth=0.7)
    gl = ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.3)
    gl.top_labels = False
    gl.right_labels = False

    # Ploteo del campo
    im = da.plot(
        ax=ax,
        transform=data_crs,
        cmap=cmap,
        add_colorbar=True,
        cbar_kwargs={"label": str(da.name) if da.name else "Valor"},
    )

    # Track de vuelo si está disponible
    if flight_track is not None:
        lons, lats = flight_track
        ax.plot(
            lons,
            lats,
            transform=data_crs,
            linewidth=1.5,
            linestyle="-",
        )

    if title is not None:
        ax.set_title(title, fontsize=12)

    fig.tight_layout()

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
        print(f"Figura guardada en: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

