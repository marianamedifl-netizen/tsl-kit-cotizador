---
name: "tsl-cotizacion-hoteles"
description: "Crea la Cotización de Hoteles de The Suite Life (formato nuevo): puros hoteles, con una o varias ciudades, opciones de hotel, tipos de cuarto y habitaciones. Úsala cuando Mariana pida cotizar solo hoteles en PDF."
---

# TSL · Cotización de Hoteles (Formato Nuevo)

Cotización de **puros hoteles**: una o varias ciudades, una o varias opciones de hotel por ciudad, varios tipos de cuarto por hotel y una o varias habitaciones. Misma identidad que la Cotización Completa (`tsl-cotizacion-completa`). Aprobada por Mariana en noviembre de 2026 (comparativa «Maqueta A»).

Cuándo NO es esta:
- Viaje rápido con vuelos, hotel y traslados o tours → `tsl-cotizacion-rapida`.
- Solo opciones de vuelo → `tsl-cotizacion-vuelos`.
- Viaje con itinerario día por día → `tsl-cotizacion-completa`.

## Antes del documento

Primero se entrega en el chat el comparativo de tarifas (Sabre, Expedia y página del hotel) con `tsl-cotizar-hoteles-sabre`, avisando si hay una reembolsable más barata que la NEM. **El PDF se arma solo cuando Mariana ya escogió** hoteles, cuartos y tarifas.

## Dónde está la plantilla

En la computadora de Mariana, carpeta `Travel Agent Portal/TSL - Formato Nuevo/`:

- `tsl_base.py` y `tsl_formato.py`: tipografías, logos, estilos aprobados y piezas comunes. No se editan por cotización.
- `ejemplo_hoteles/cotizacion_hoteles_japon.py`: ejemplo canónico (Tokio, Kioto y Osaka; familia en 2 habitaciones) con sus fotos en `img/`.
- `fotos.py`: recortes y tratamiento de color.

Las fuentes están en `TSL - Brand Files/Fonts` (IvyOra y Karla). Si la computadora no está conectada o la carpeta no aparece, dilo de inmediato; no reconstruyas el formato a ojo.

## Flujo

1. Con las tarifas que Mariana eligió, copia la carpeta `ejemplo_hoteles/` y cambia **solo los bloques de datos** y las fotos de `img/`. **No inventes precios, políticas, categorías ni vigencias**; lo que falte se marca como pendiente de verificar y se le dice a Mariana.
2. Genera: `python3 cotizacion_hoteles_<tema>.py salida.pdf`.
3. Revisa: renderiza cada hoja a PNG y mírala; compara cifras y fechas contra la fuente con `pdftotext -layout`; `pdffonts` debe listar solo IvyOra y Karla.
4. Entrega el PDF y guárdalo en `Cotizaciones/Formato Nuevo/` dentro de su carpeta. Nunca lo envíes a un cliente sin que Mariana lo confirme.

## Estructura

**Hoja 1 · Comparativa (pocas cifras)**
- Portada compacta de franja de foto con tarjeta beige: destino, ciudades, Fechas, Viajeros (personas y habitaciones) y Documento.
- Por ciudad: rótulo con la ciudad a la izquierda y «fechas · noches» a la derecha.
- Por hotel: punto con letra, nombre con las estrellas al lado, zona y régimen; en una línea, los tipos de cuarto cotizados, del más barato al más caro (el primero en tinta, los demás en gris); a la derecha **un solo precio «Desde»** por hotel, sin «US$».
- Franja beige «Viaje completo desde · N habitaciones · N noches · USD»: suma siempre la **opción más barata de cada ciudad**.
- No lleva etiqueta de «Recomendado» ni políticas de cancelación; esas van en las hojas de hotel y en Notas.

**Una hoja por hotel**
- Nombre, ubicación, estrellas y datos: Fechas, Noches, Habitaciones, Régimen.
- Dos fotos del hotel.
- Tabla de cuartos: foto del cuarto, nombre con sus datos y camas, precio por habitación con su promedio por noche y total para las N habitaciones.
- «Beneficios The Suite Life» (lo que da la tarifa preferencial) y una línea con la cancelación de ese hotel.

**Notas & Cancelación**
- El precio incluye, El precio excluye (con los impuestos locales que se pagan en el hotel), Para reservar, Información general.
- Tabla de cancelación por hotel (fecha límite y penalidad).
- Firma al pie: Mariana Medina · Luxury Travel Designer, teléfono, correo y `@thesuitelife.mx`.

## Bloques de datos del script

`N_HAB`, `PORTADA`, `CIUDADES` (por ciudad: ciudad, fechas, noches, hoteles; por hotel: letra, nombre, zona, estrellas, régimen, fotos, cuartos, beneficios, cancelación; por cuarto: nombre, datos, total por habitación, nota de camas, imagen), `NOTA_PRECIO`, `INCLUYE`, `EXCLUYE`, `RESERVAR`, `GENERAL`, `CREDITOS`.

## Lo que nunca aparece en el PDF

Códigos de tarifa (NEM, API), nombres de programas de tarifa, comisiones ni la plataforma de origen. Los beneficios de la tarifa preferencial se presentan como «Beneficios The Suite Life».

## Fotos

- Hotel y cuartos: del sitio oficial del hotel o de la biblioteca de Mariana (`Documents/Claude/Fotos/<hotel>`), tratadas con `fotos.hotel()`. **No pongas la foto de un cuarto de otra categoría** que la cotizada.
- Si falta una foto, la hoja deja el hueco marcado; no se rellena con otra. Avísale a Mariana cuáles faltan o salieron en baja resolución.
- Franja de portada: del destino real, tratada con `fotos.ambiente()`. Si es de Unsplash, regístrala con `download_asset` y acredita al fotógrafo en `CREDITOS`.

## Marca

Las mismas reglas de `tsl-cotizacion-completa`: solo neutros, IvyOra Thin para títulos y Karla para texto, sin íconos, arcos, degradados ni sombras, y sin símbolos que caigan en fuente de respaldo. No reutilices los nombres de clase `.band` ni `.top` (ya existen en la base y causan errores).