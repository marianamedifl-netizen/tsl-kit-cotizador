# TSL · Formato Nuevo

Plantillas del formato nuevo de The Suite Life, aprobado en noviembre de 2026.

- `tsl_base.py`: tipografías, logos, mapa, CSS base y ayudantes. No se edita por documento.
- `tsl_formato.py`: estilos aprobados y piezas comunes (tabla de vuelos, portada compacta, firma, impresión a PDF) y las piezas de documento largo: portada, índice, apertura, mapa, itinerario diario, hoja de hotel, cierre, y reparto en hojas con alturas medidas (`measure`, `fit`).
- `fotos.py`: recortes y tratamiento de color de las fotos.
- `logo/`: logos vectoriales. `geo/countries-50m.json`: países para el mapa (Natural Earth, world-atlas).

Ejemplos canónicos (se copia la carpeta y se cambian solo los datos y las fotos):

- `ejemplo_laponia/`: Cotización Completa.
- `ejemplo_vuelos/`: Cotización Vuelos, comparativa de opciones de vuelo (antes `ejemplo_rapida_vuelos/`).
- `ejemplo_rapida/`: Cotización Rápida, viaje rápido en 2 hojas con vuelos, hoteles y servicios adicionales (traslados, tours). Propuesta cerrada, solo tablas; bajo el destino de la portada va el nombre del cliente; precio `agrupado` o `detalle` (segundo argumento del script; preguntar cada vez). Crece sola si no cabe.
- `ejemplo_entrega_final/`: Entrega Final (datos del viaje en `datos_garza.py`; confirmaciones de vuelos, hoteles y restaurantes).
- `ejemplo_guia_viaje/`: Guía de Viaje (clima diario, qué empacar por destino, maletas, propinas, esenciales). Sin íconos.
- `ejemplo_hoteles/`: Cotización de Hoteles (puros hoteles: una o varias ciudades, varias opciones de hotel y tipos de cuarto, una o varias habitaciones). Hoja 1 con un precio «desde» por hotel; una hoja por hotel con foto y precio de cada cuarto; notas y cancelación.

Nombres de clase reservados por la base, no reutilizar: `.band`, `.top`.

Requiere las fuentes de `TSL - Brand Files/Fonts` (IvyOra y Karla), Google Chrome, y Python con playwright, shapely, numpy y Pillow.
