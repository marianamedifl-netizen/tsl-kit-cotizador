---
name: "tsl-cotizacion-vuelos"
description: "Crea la Cotización Vuelos de The Suite Life en el formato nuevo: comparativa de opciones de vuelo para un mismo viaje (2 hojas). Úsala cuando Mariana pida cotizar solo vuelos u opciones de vuelo en PDF; antes era la versión de vuelos de tsl-cotizacion-rapida."
---

# TSL · Cotización Vuelos (Formato Nuevo)

Documento corto, normalmente de 2 hojas, que compara varias opciones de vuelo para un mismo viaje. Misma identidad que la Cotización Completa (`tsl-cotizacion-completa`). Aprobado por Mariana en noviembre de 2026. Antes era la versión "Vuelos · comparativa" de `tsl-cotizacion-rapida`; para solo vuelos se usa esta.

Si la cotización lleva además hotel o servicios, usa `tsl-cotizacion-rapida`. Para puros hoteles, `tsl-cotizacion-hoteles`.

## Dónde está la plantilla

En la computadora de Mariana, carpeta `Travel Agent Portal/TSL - Formato Nuevo/`:

- `tsl_base.py` y `tsl_formato.py`: tipografías, logos, estilos aprobados y piezas comunes (`band_cover`, `flights_table`, `sign`, `print_pdf`). No se editan por cotización.
- `ejemplo_vuelos/cotizacion_vuelos.py`: ejemplo canónico (Ciudad de México – El Cairo, tres opciones).
- `fotos.py`: recortes y tratamiento de color.

Las fuentes están en `TSL - Brand Files/Fonts` (IvyOra y Karla). Si la computadora no está conectada o la carpeta no aparece, dilo de inmediato; no reconstruyas el formato a ojo.

## Flujo

1. Reúne las opciones (Sabre, sitio de la aerolínea). La preferencia de Mariana al buscar: minimizar molestias (pocas escalas, buenos horarios) al precio razonable más bajo. **No inventes precios, horarios, reglas de tarifa ni vigencias**; lo que falte se marca como pendiente de verificar y se le dice a Mariana.
2. En Sabre, los vuelos que se carguen al área de trabajo para cotizar se descartan siempre con `I`. Nunca se reserva, se guarda un PNR ni se emite sin que Mariana lo confirme en el chat.
3. Copia `ejemplo_vuelos/` y cambia **solo los bloques de datos** (portada, `OPCIONES`, notas) y la foto de `img/`.
4. Genera: `python3 cotizacion_vuelos.py salida.pdf`.
5. Revisa: renderiza cada hoja a PNG y mírala; compara cifras, vuelos, horarios y fechas contra la fuente con `pdftotext -layout`; `pdffonts` debe listar solo IvyOra y Karla.
6. Entrega el PDF y guárdalo en `Cotizaciones/` dentro de su carpeta. Nunca lo envíes a un cliente sin que Mariana lo confirme.

## Hoja 1

**Portada compacta**
- Franja de foto del destino a todo el ancho, de 3.25 in de alto, en tonos apagados.
- Tarjeta beige `rgba(223,211,197,.9)` a la izquierda con logo y lema, título ("Opciones de Vuelo"), ruta en itálica y los datos: Fechas, Viajeros, Documento.
- La tarjeta no debe tapar el punto focal de la foto: si hace falta, se vuelve a encuadrar para que el motivo quede a la derecha.

**Comparativa**
- Tabla con Opción (punto con letra), Aerolínea (con ruta y si es uno o dos boletos), Cabina, Escalas ida · regreso y Total con su equivalente.

**Primera opción**
- Cabe bajo la comparativa en la hoja 1; las demás van dos por hoja (`POR_HOJA`).

## Un bloque por opción

- Etiqueta "Opción A", aerolínea y ruta, total a la derecha.
- Tabla de vuelos con encabezado en banda beige y grupos Ida / Regreso.
- Reglas de la tabla: fechas en negrita, la clase que no sea Business resaltada, "+1" como superíndice, duración a la derecha, horas en 24 h.
- Nota chica con cabinas, boletos, escalas, cambios y reembolsos. Si son boletos separados, se dice que la conexión no queda protegida.

## Cierre

- Nota final con vigencia por opción, tipo de cambio, equipaje y crédito de la foto.
- En lugar de hoja de cierre, la firma de contacto al pie de la última hoja (`F.sign()`): Mariana Medina · Luxury Travel Designer, teléfono, correo y `@thesuitelife.mx`, con enlaces.

## Fotos

- Franja de portada: Unsplash, del destino real; regístrala con `download_asset` y acredita al fotógrafo en la nota final. Se captura desde Chrome y se trata con `fotos.ambiente()`.

## Marca

Las mismas reglas de `tsl-cotizacion-completa`: solo neutros, IvyOra Thin para títulos y Karla para texto, sin íconos, arcos, degradados ni sombras, y sin símbolos que caigan en fuente de respaldo.