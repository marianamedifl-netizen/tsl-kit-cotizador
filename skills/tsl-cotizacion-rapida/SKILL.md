---
name: "tsl-cotizacion-rapida"
description: "Crea la Cotización Rápida de The Suite Life (formato nuevo): viaje rápido en 2 hojas con tablas de vuelos, hoteles y servicios adicionales, costo agrupado y total. Úsala cuando Mariana pida una cotización rápida o sencilla de un viaje con vuelos, hotel y traslados o tours."
---

# TSL · Cotización Rápida (Formato Nuevo)

Cotización de un **viaje rápido**: vuelos, hoteles y servicios adicionales (traslados, tours) en **2 hojas**, solo con tablas. Es una **propuesta cerrada**: un solo viaje, sin opciones a comparar. Misma identidad que la Cotización Completa (`tsl-cotizacion-completa`). Aprobada por Mariana en noviembre de 2026; sustituye a la versión anterior de esta skill (hotel con hoja de fotos) y a la variante SENCILLA de `tsl-cotizaciones`.

Cuándo NO es esta:
- Solo opciones de vuelo (comparativa) → `tsl-cotizacion-vuelos`.
- Solo hoteles (varios hoteles, cuartos o ciudades) → `tsl-cotizacion-hoteles`.
- Viaje con itinerario día por día, mapa y hoja por hotel → `tsl-cotizacion-completa`.

## Dónde está la plantilla

En la computadora de Mariana, carpeta `Travel Agent Portal/TSL - Formato Nuevo/`:

- `tsl_base.py` y `tsl_formato.py`: tipografías, logos, estilos aprobados y piezas comunes (`flights_table`, `stars`, `notes`, `sign`, `furniture`, `measure`, `fit`, `print_pdf`). No se editan por cotización.
- `ejemplo_rapida/cotizacion_rapida_marrakech.py`: ejemplo canónico (Marrakech, marzo 2027) con su foto en `img/`.
- `fotos.py`: recortes y tratamiento de color.

Las fuentes están en `TSL - Brand Files/Fonts` (IvyOra y Karla). Si la computadora no está conectada o la carpeta no aparece, dilo de inmediato; no reconstruyas el formato a ojo.

## Antes de armar: dos preguntas

1. **Nombre del cliente** (va en la portada). Si Mariana no lo dio, pregúntalo.
2. **Precio agrupado o con desglose**. Pregúntalo **cada vez**; no lo des por hecho.
   - `agrupado`: tres cifras (Vuelos · Hospedaje · Servicios adicionales) y la franja del total.
   - `detalle`: cada tabla lleva su columna de costo en USD y abajo queda solo la franja del total.

## Flujo

1. Reúne los datos (Sabre, Expedia TAAP, sitio del hotel o de la aerolínea, conector Rolzo para traslados). Al buscar vuelos, la preferencia de Mariana es minimizar molestias (pocas escalas, buenos horarios) al precio razonable más bajo. **No inventes precios, horarios, políticas, categorías ni vigencias**; lo que falte se marca como pendiente de verificar y se le dice a Mariana. Un precio público de referencia (por ejemplo, un tour sin confirmar con el DMC) se dice como tal en la nota de precios.
2. En Sabre, los vuelos cargados al área de trabajo para cotizar se descartan siempre con `I`. Nunca se reserva, se guarda un PNR ni se emite sin que Mariana lo confirme en el chat.
3. Copia la carpeta `ejemplo_rapida/` y cambia **solo los bloques de datos** y la foto de `img/`.
4. Genera: `python3 cotizacion_rapida_<tema>.py salida.pdf agrupado` (o `detalle`).
5. Revisa: renderiza cada hoja a PNG y mírala; compara cifras, vuelos y fechas contra la fuente con `pdftotext -layout`; `pdffonts` debe listar solo IvyOra y Karla. El script ya valida que las cifras redondeadas sumen el total.
6. Entrega el PDF y guárdalo en `Cotizaciones/Formato Nuevo/` dentro de su carpeta. Nunca lo envíes a un cliente sin que Mariana lo confirme.

## Estructura

**Hoja 1**
- **Portada delgada**: franja de foto a todo el ancho (2.22 in de alto), en tonos apagados, y tarjeta beige `rgba(223,211,197,.9)` con el logo y lema, el **destino** como título y, **debajo, el nombre del cliente** en itálica; a la derecha de la tarjeta, los datos Fechas, Viajeros y Documento. Las fechas van del día en que sale el primer vuelo al día en que llega el último. El contenido empieza debajo de la franja, en la misma hoja.
- **Vuelos**: tabla TSL (Fecha, Aerolínea, No., Desde, Hacia, Clase, Salida, Llegada, Duración) con encabezado en banda beige y grupos Ida / Regreso. Fechas en negrita, la clase que no sea Business resaltada, «+1» como superíndice, duración a la derecha, horas en 24 h.
- **Hoteles**: Fechas · Nts · Hotel (nombre en IvyOra, estrellas solo si la categoría viene en la fuente, destino) · Habitación · Régimen.
- **Servicios adicionales**: Fecha · Servicio · Detalle · Horario. Una fila por traslado o tour, en orden de fecha.
- **Cotización**: en `agrupado`, tres cifras sin «US$» (Vuelos, Hospedaje, Servicios adicionales) con una línea de detalle cada una; después la franja beige «Total del viaje · N personas · USD» con el precio por persona y el total. Debajo, una línea que remite a la hoja de notas.
- Pie con logo y folio.

**Hoja 2 · Notas & Cancelación**
- Filete superior con sección y nombre del viaje; pie con logo y folio.
- Columna izquierda: El precio incluye, El precio excluye, Sobre los precios (monedas, tipos de cambio con su fuente y precios de referencia).
- Columna derecha: Sobre los vuelos (escalas, equipaje, reglas de tarifa), Para reservar (fecha de consulta, vigencia y forma de pago), Información general. Subtítulos en Karla negrita gris oscuro.
- Tabla de **Políticas de cancelación por concepto**: Vuelos, Hotel (por tramos), Traslados, Excursión. Si una política no se tiene, se escribe «Por confirmar al reservar» y se le avisa a Mariana.
- Firma al pie, en lugar de hoja de cierre: Mariana Medina · Luxury Travel Designer, teléfono, correo y `@thesuitelife.mx`, con enlaces.

**Si no cabe**: el script mide cada bloque (`F.measure`) y lo reparte (`F.fit`); lo que no entra bajo la portada pasa a la hoja siguiente y el documento crece solo. No se reduce la letra para forzar las 2 hojas.

## Bloques de datos del script

`N_PAX`, `PORTADA` (img, title, cliente, rows), `VUELOS` + `VUELOS_USD` + `VUELOS_NOTAS`, `HOTELES` (fechas, noches, hotel, estrellas, destino, habitación, régimen, USD), `SERVICIOS` (fecha, servicio, detalle, horario, USD), `GRUPOS` (se calcula de lo anterior), `NOTA_PRECIO`, `INCLUYE`, `EXCLUYE`, `RESERVAR`, `GENERAL`, `CANCELACION`, `CREDITOS`.

## Lo que nunca aparece en el PDF

Códigos de tarifa (NEM, API), nombres de programas de tarifa, comisiones, la plataforma de origen (Sabre, Expedia TAAP, Rolzo, SlickTrip) ni el nombre de un operador que aún no está confirmado.

## Fotos

- Solo lleva la franja de portada: del destino real, tratada con `fotos.ambiente()` como indica `fotos.py`. La tarjeta no debe tapar el punto focal de la foto: si hace falta, se vuelve a encuadrar para que el motivo quede a la derecha.
- Si es de Unsplash, regístrala con `download_asset` y pon el crédito del fotógrafo en `CREDITOS`.
- Esta cotización no lleva fotos de hotel ni de habitaciones; si Mariana las pide, corresponde la Cotización Completa o la de Hoteles.

## Marca

Las mismas reglas de `tsl-cotizacion-completa`: solo neutros, IvyOra Thin para títulos y Karla para texto, sin íconos, arcos, degradados ni sombras, y sin símbolos que caigan en fuente de respaldo. No reutilices los nombres de clase `.band` ni `.top` (ya existen en la base y causan errores); el script usa el prefijo `.rap.cq`.