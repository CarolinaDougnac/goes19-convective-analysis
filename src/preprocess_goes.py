"""
Funciones de preprocesamiento para escenas GOES:
- apertura del archivo
- selección de variable
- recorte a dominio geográfico
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import xarray as xr


def open_goes_scene(path: str | Path) -> xr.Dataset:
    """
    Abre una escena GOES usando xarray.

    Parameters
    ----------
    path : str or Path
        Ruta del archivo GOES (por ejemplo, NetCDF).

    Returns
    -------
    xarray.Dataset
    """
    path = Path(path)
    ds = xr.open_dataset(path)
    return ds


def select_variable(ds: xr.Dataset, var_name: str) -> xr.DataArray:
    """
    Selecciona la variable principal de interés (por ejemplo, temperatura de brillo).

    Parameters
    ----------
    ds : xr.Dataset
        Dataset con la escena GOES.
    var_name : str
        Nombre de la variable (depende del producto, por ejemplo: 'CMI', 'tbb', etc.).

    Returns
    -------
    xr.DataArray
    """
    if var_name not in ds:
        raise KeyError(f"La variable '{var_name}' no existe en el Dataset.")
    return ds[var_name]


def subset_domain(
    da: xr.DataArray,
    lat_bounds: Tuple[float, float],
    lon_bounds: Tuple[float, float],
    lat_name: str = "y",
    lon_name: str = "x",
) -> xr.DataArray:
    """
    Recorta la escena a un dominio geográfico aproximado.

    Parameters
    ----------
    da : xr.DataArray
        Campo a recortar.
    lat_bounds : (min_lat, max_lat)
        Límites de latitud.
    lon_bounds : (min_lon, max_lon)
        Límites de longitud.
    lat_name : str, default "y"
        Nombre de la coordenada de latitud en el archivo.
    lon_name : str, default "x"
        Nombre de la coordenada de longitud en el archivo.

    Returns
    -------
    xr.DataArray
        DataArray recortado.
    """
    # Nota: esto asume que las coordenadas ya están en lat/lon.
    # Si están en proyección satelital, el recorte se haría distinto.
    lat_min, lat_max = lat_bounds
    lon_min, lon_max = lon_bounds

    da_sub = da.sel(
        {lat_name: slice(lat_min, lat_max), lon_name: slice(lon_min, lon_max)}
    )
    return da_sub


def prepare_scene(
    path: str | Path,
    var_name: str,
    lat_bounds: Tuple[float, float],
    lon_bounds: Tuple[float, float],
    lat_name: str = "y",
    lon_name: str = "x",
) -> xr.DataArray:
    """
    Flujo rápido: abre, selecciona variable y recorta dominio.

    Parameters
    ----------
    path : str or Path
        Ruta de la escena GOES.
    var_name : str
        Nombre de la variable a analizar.
    lat_bounds, lon_bounds : tuple
        Límites de latitud y longitud.
    lat_name, lon_name : str
        Nombres de las coordenadas.

    Returns
    -------
    xr.DataArray
    """
    ds = open_goes_scene(path)
    da = select_variable(ds, var_name)
    da_sub = subset_domain(
        da,
        lat_bounds=lat_bounds,
        lon_bounds=lon_bounds,
        lat_name=lat_name,
        lon_name=lon_name,
    )
    return da_sub

