# Análisis GOES-19 para campañas de estimulación de nubes en Ecuador (2025)

Este repositorio reúne el código, notebooks y ejemplos de productos gráficos utilizados para el **monitoreo y la evaluación de campañas de estimulación de nubes (cloud seeding)** en Ecuador durante 2025, a partir de imágenes satelitales **GOES-19 (banda 13)**.

El objetivo principal es mostrar mi forma de trabajo integrando:
- análisis meteorológico operativo,
- procesamiento de datos satelitales en Python,
- y generación de productos visuales para la toma de decisiones.

---

## ✨ Objetivos del proyecto

- Identificar y seguir sistemas convectivos relevantes para las operaciones de siembra.
- Generar secuencias **antes–durante–después** asociadas a vuelos específicos.
- Superponer trayectorias de vuelo y áreas de interés sobre campos satelitales.
- Dejar un flujo de trabajo reproducible que pueda adaptarse a otras campañas o regiones.

---

## 📂 Estructura del repositorio

```text
.
├── data/
│   ├── raw/          # Datos crudos GOES-19 (no incluidos por tamaño)
│   └── processed/    # Datos recortados/preprocesados
├── figures/          # Figuras de ejemplo del análisis
├── notebooks/        # Notebooks del flujo de trabajo
├── src/              # Funciones reutilizables en Python
├── LICENSE
├── README.md
└── requirements.txt

