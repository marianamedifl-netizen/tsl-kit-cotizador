---
name: "tsl-cotizacion-completa"
description: "Crea la Cotización Completa de The Suite Life en el formato nuevo (nov 2026): portada con foto, índice, resumen con mapa, vuelos, hoteles, itinerario diario, hoja por hotel, cotización, notas y cierre. Úsala cuando Mariana pida una cotización completa o pasar una cotización al formato nuevo; sustituye a la variante COMPLETA de tsl-cotizaciones."
---

# TSL · Cotización Completa (Formato Nuevo)

Formato aprobado por Mariana Medina en noviembre de 2026, hoja por hoja. Sustituye a la variante COMPLETA de `tsl-cotizaciones` (la SENCILLA sigue en esa skill). El objetivo es que el documento sea un diferenciador frente al mercado y que **no parezca hecho por IA**.

## Dónde está la plantilla

En la computadora de Mariana, carpeta `Travel Agent Portal/TSL - Formato Nuevo/`:

- `tsl_base.py`: tipografías, logos, mapa, CSS base y ayudantes. No se edita por cotización.
- `tsl_formato.py`: estilos aprobados y piezas comunes a todas las plantillas del formato nuevo. No se edita por cotización.
- `ejemplo_laponia/cotizacion_completa_laponia.py`: ejemplo canónico (Laponia · Opción 2), con sus fotos en `img/` y `himg_g/`.
- `fotos.py`: recortes y tratamiento de color de las fotos.
- `logo/` (logos vectoriales) y `geo/countries-50m.json` (países para el mapa).

Las fuentes están en `Travel Agent Portal/TSL - Brand Files/Fonts` (IvyOra y Karla). Si la ruta de marca cambia, se indica con la variable de entorno `TSL_BRAND`.

Si la computadora no está conectada o la carpeta no aparece, dilo de inmediato y pide que la conecte o que adjunte `TSL_Formato_Nuevo_plantilla.zip`. No reconstruyas el formato a ojo.

## Flujo

1. Reúne los datos del cliente (capturas de Sabre, Expedia TAAP, hoteles, aerolíneas, cotización previa). **No inventes precios, disponibilidad, horarios, políticas, categorías de hotel ni vigencias**; lo que falte se marca como pendiente de verificar y se le dice a Mariana.
2. Trae la plantilla y las fuentes al espacio de trabajo. Copia `ejemplo_laponia/` a una carpeta nueva del cliente y cambia **solo los bloques de datos**: mapa (`STOPS`, límites y países), `DAYS`, `HOTELS`, y los textos de portada, vuelos, hoteles, cotización y notas. No cambies el CSS ni los ayudantes.
3. Consigue y trata las fotos (ver Fotos).
4. Genera: `python3 cotizacion_completa_<cliente>.py salida.pdf`. El script mide la altura de cada día con Playwright, pagina el itinerario y imprime con Chrome headless.
5. Revisa antes de entregar:
   - Renderiza todas las páginas a PNG y míralas: sin encimados, sin texto cortado (incluido el lema bajo el logo de portada), sin palabras solas en un renglón.
   - Compara cifras, vuelos y fechas contra la fuente con `pdftotext -layout`.
   - `pdffonts` debe listar solo IvyOra y Karla (nada de fuentes de respaldo).
   - `pdfinfo` debe mostrar el título del viaje, no el nombre del archivo HTML.
6. Entrega el PDF y guárdalo en `Cotizaciones/` dentro de su carpeta. **Nunca lo envíes a un cliente sin que Mariana lo confirme.** Los datos del cliente se usan solo dentro de su subproyecto.

## Orden de las hojas

1. Portada
2. Índice
3. Resumen (mapa y etapas)
4. Vuelos
5. Hoteles (tabla)
6. Apertura del itinerario (foto a página completa)
7. Itinerario Diario (las hojas que hagan falta)
8. Una hoja por hotel
9. Cotización
10. Notas & Políticas de Cancelación
11. Cierre

Las hojas interiores llevan arriba un filete con `.0N SECCIÓN` a la izquierda y el nombre del viaje a la derecha; abajo, filete con el logo de una línea (enlaza al índice) y el folio.

## Reglas por hoja

**Portada**
- Foto vertical a página completa, en tonos apagados y arenosos.
- Tarjeta beige `rgba(223,211,197,.9)` abajo a la izquierda, con margen de 0.7 in, sobre una zona tranquila de la foto: no debe tapar el punto focal.
- Dentro: logo con lema completo, título en IvyOra Thin, subtítulo, y el nombre del cliente tal cual («Familia X», sin «Para la»).
- Datos: Fechas en una sola línea («26 dic 2026 – 9 ene 2027»), Viajeros y Documento («Cotización · Opción N»).
- **El viaje empieza el día que sale el primer vuelo**, no el día de llegada.
- Sin texto vertical.

**Índice**
- Panel beige a la izquierda con «Índice». Lista `.01, .02…` con nombre y página; cada renglón es un enlace interno.
- Abajo: «Propuesta para» y «Diseñado por».

**Resumen**
- Solo título, mapa grande y tabla de etapas. Sin columna lateral, sin contacto de emergencia y **sin precio**.
- Mapa con fondo transparente: solo los países. Países del viaje en Oatmeal, países de contexto en Soft Almond.
- Puntos numerados en las paradas, **sin líneas entre ubicaciones**.
- Tabla toda en Karla chica y uniforme, fechas en negrita, punto numerado en la columna #, encabezado en banda beige.

**Vuelos**
- Solo el título, sin subtítulo.
- «Pasajeros · N» y debajo los nombres en **una sola fila**, chicos (7 pt), separados por un círculo pequeño.
- Tabla: Fecha, Aerolínea, No., Desde, Hacia, Clase, Salida, Llegada, Duración. Encabezado en banda beige.
- Renglones agrupados en Ida, Vuelos internos y Regreso. Fechas en negrita; clase en negro y la que no sea Business resaltada; «+1» como superíndice; duración alineada a la derecha.
- Horas de la tabla en 24 h.
- Al pie, una nota bajo la otra y muy chicas (6.4 pt): «Equipaje» en una sola fila por aerolínea, y «Políticas de cancelación» como párrafo. La tarifa va en la hoja de Cotización.

**Hoteles (tabla)**
- Columnas: # (punto numerado), Fechas (desde y hasta fusionadas: «27 – 28 dic»), Nts, Destino, Hotel, Habitación / Régimen.
- Encabezado en banda beige, fechas en negrita, nombre del hotel en una sola línea.
- Sin foto en esta hoja.

**Apertura del itinerario**
- Foto a página completa, hermana de la portada, con tarjeta beige que dice «Itinerario Diario».

**Itinerario Diario**
- Rótulo de día «DÍA n · FECHA» en Karla negrita, versalitas, 7.8 pt, arena `#927F68`.
- El título del día es la ubicación; si hay cambio de ciudad, «Helsinki – Rovaniemi».
- Horas en negrita y en **AM/PM**. Sin subtítulos, sin íconos, sin renglones con borde; un filete fino entre días.
- Si ningún día de la hoja trae hora, no se reserva la columna de hora: el texto alinea con el título.
- Fotos rectangulares de 2.35 × 3.1 in, alineadas con el día que ilustran, alternando de lado en cada hoja.
- **Regla: cada hoja del itinerario lleva al menos 2 fotos.** El generador falla si no se cumple.
- La noche o momento que da nombre al viaje siempre lleva foto.

**Hoja por hotel** (después del itinerario)
- Nombre grande; debajo, punto numerado, ubicación en itálica y estrellas.
- Las estrellas se dibujan en SVG y solo se ponen si la categoría viene en la fuente.
- Franja de datos: Fechas, Noches, Habitación, Régimen. Descripción a dos columnas.
- **Cuatro fotos grandes en retícula 2 × 2**, todas con el mismo tratamiento de color. No usar retícula asimétrica.

**Cotización**
- Título «Cotización» con «Opción N» en itálica.
- Tabla Concepto / Costo total, agrupada por concepto.
- Banda beige con el total. Sin subtotales repetidos y sin suma debajo del total.
- Nota con moneda, tipo de cambio y aviso de disponibilidad.
- Aquí no van incluye, excluye ni forma de pago.

**Notas & Políticas de Cancelación**
- Subtítulos en Karla normal, negritas y gris oscuro (no itálica).
- Columna izquierda: El precio incluye, El precio excluye, Para reservar.
- Columna derecha: Información general y Políticas de cancelación (tabla con encabezado en banda).

**Cierre**
- Hoja beige completa, minimalista, tono sobre tono: logo, una línea corta, «Síguenos en Instagram», `@thesuitelife.mx` en grande y `thesuitelife.com.mx` en itálica.
- Abajo: Mariana Medina · Luxury Travel Designer, teléfono 55 1850 0549 y mariana.medina@nuba.com, con enlaces para llamar y escribir.
- Créditos de foto muy pequeños. Sin recuadros ni código QR.

**PDF como archivo**
- Título del documento con el nombre del viaje, índice enlazado, marcadores por sección y logo del pie enlazado al índice.

## Marca y estilo

- Paleta, solo neutros: Stone Grey `#7D766C`, Oatmeal `#DFD3C5`, Soft Almond `#F0EDE8`, Antique White `#FCF9F5`, Eerie Black `#232323`, gris oscuro de texto `#55504A`.
- Tipos: IvyOra Display Thin (títulos), IvyOra Thin Italic (subtítulos y pies de foto), Karla (texto).
- Tamaños mínimos: etiquetas en versalitas 6.8 pt, texto de tablas 9 pt.
- Para no parecer de IA: nada de arcos, íconos, líneas punteadas, degradados, sombras ni esquinas redondeadas. Fotos como impresiones rectangulares con margen. Texto sobrio y factual.
- No usar símbolos que caigan en fuente de respaldo (★, ✈, ⇄). Guion «–», nunca «→».

## Fotos

- **Ambiente** (portada, apertura, itinerario): Unsplash. Deben parecer el destino y la temporada reales del viaje; revisa paisaje, vegetación y estación antes de usarlas. Registra cada foto usada con `download_asset` y acredita a los fotógrafos en el cierre. Avisa a Mariana que son de ambiente y no de los proveedores.
- **Hoteles**: del sitio oficial del hotel, de la biblioteca de Mariana (`Documents/Claude/Fotos/<hotel>`) o las que ya traiga. Nada de fotos de otra temporada (por ejemplo, terrazas de verano en un viaje de invierno).
- El proxy bloquea descargar las imágenes directamente. Se capturan desde Chrome: se pinta la imagen en un `<img>` fijo con `object-fit: cover` y se toma captura a escala 1. Medidas y recortes en `fotos.py`.
- Tratamiento: `fotos.ambiente()` para ambiente y `fotos.hotel()` para todas las fotos de hotel, de modo que el documento tenga una sola paleta apagada.
- No descargues ni insertes fotos de personas públicas.

## Reglas de precio

- Tabla agrupada por concepto o región, no línea por línea.
- Markup de alrededor de 15 % sobre servicios terrestres y vuelos regionales (tarifas NETT del operador). Vuelos internacionales al costo que dé Mariana, salvo indicación.
- La moneda es la de la cotización. Si hay dos monedas, el total aproximado indica el tipo de cambio aplicado y su fecha; confírmalo con el del día.

## Copy estándar de Notas

- **Información general**: precios y disponibilidad sujetos a cambio; variación por tipo de cambio; documentos de viaje vigentes a cargo del cliente; seguro de viaje recomendado; más las advertencias propias del destino.
- **Para reservar**: depósito no reembolsable del 30 % al reservar; saldo 60 días antes de la salida; los pagos tardíos pueden cancelar la reserva.
- **Políticas de cancelación**: 61 días o más, 30 % del valor total; 60 días o menos, 100 %; No Show, 100 %.
- Si la cotización se emite a menos de 60 días de la salida, avísale a Mariana: el esquema de depósito y saldo ya no cuadra con las fechas.