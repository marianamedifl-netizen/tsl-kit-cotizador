---
name: "tsl-entrega-final-formato-nuevo"
description: "Crea la Entrega Final de The Suite Life en el formato nuevo (nov 2026): portada, índice, resumen con mapa, vuelos por pasajero, hoteles, itinerario diario, hoja por hotel, confirmaciones y cierre. Úsala cuando Mariana pida una Entrega Final o Documento Final; sustituye a tsl-entrega-final."
---

# TSL · Entrega Final (Formato Nuevo)

Documento final del viaje, con todo reservado y confirmado. Usa la misma identidad y las mismas hojas que la Cotización Completa (`tsl-cotizacion-completa`), pero en lugar de Cotización y Notas lleva las hojas de **Confirmaciones**. Aprobado por Mariana en noviembre de 2026. Sustituye a `tsl-entrega-final` (el formato anterior de emblemas e íconos).

Las reglas de marca, de fotos y de cada hoja compartida (portada, índice, vuelos, hoteles, apertura, itinerario diario, hoja por hotel, cierre, PDF como archivo) son las de `tsl-cotizacion-completa`: léela antes de armar el documento. Aquí solo va lo que cambia.

Se acompaña de la Guía de Viaje (`tsl-guia-viaje-formato-nuevo`), que se entrega aparte.

## Dónde está la plantilla

En la computadora de Mariana, carpeta `Travel Agent Portal/TSL - Formato Nuevo/`:

- `tsl_base.py` y `tsl_formato.py`: tipografías, logos, estilos aprobados y piezas comunes. No se editan por documento. Las piezas de documento largo están en `tsl_formato.py`: `cover_page`, `index_page`, `map_svg`, `flights_table`, `opener_page`, `paginate_days`, `itin_pages`, `hotel_sheet`, `closing_page`, `measure`, `fit`, `print_pdf`.
- `ejemplo_entrega_final/entrega_final_garza.py`: ejemplo canónico (Europa & África, 23 hojas), con los datos del viaje en `datos_garza.py` y las fotos en `img/` (ambiente) y `himg/` (hoteles).
- `fotos.py`: recortes y tratamiento de color.

Las fuentes están en `TSL - Brand Files/Fonts` (IvyOra y Karla). Si la computadora no está conectada o la carpeta no aparece, dilo de inmediato; no reconstruyas el formato a ojo.

## Flujo

1. Reúne las reservas: boletos y localizadores, confirmaciones de hotel, roadbook del DMC, traslados y restaurantes. **No inventes horarios, códigos, asientos, equipaje, categorías ni políticas**; lo que falte se marca como pendiente de verificar y se le dice a Mariana.
2. Copia `ejemplo_entrega_final/` a una carpeta del cliente. Cambia el módulo de datos (`VUELOS`, `ETAPAS`, `HOTELES`, `DIAS`, `HOJAS_HOTEL`, `CONF_VUELOS`, `CONF_HOTELES`, `RESTAURANTES`) y, en el script, solo los bloques de portada, mapa, pies de foto, fotos por hotel, contacto de emergencia y créditos. No cambies el CSS ni los ayudantes.
3. Consigue y trata las fotos como en la Cotización Completa. Para hoteles, primero la biblioteca de Mariana (`Documents/Claude/Fotos/<hotel>`), luego el sitio oficial.
4. Genera: `python3 entrega_final_<cliente>.py salida.pdf`. El script mide con Chrome la altura de cada día y de cada bloque de vuelos y confirmaciones, y los reparte en hojas.
5. Revisa antes de entregar:
   - Renderiza todas las páginas a PNG y míralas: nada encimado ni tapando el pie, mapa con todos los puntos legibles.
   - Compara contra la fuente, con `pdftotext -layout`, todos los localizadores, números de vuelo, horarios, asientos y números de confirmación.
   - `pdffonts` solo IvyOra y Karla; `pdfinfo` con el título del viaje; índice y marcadores enlazados.
6. Entrega el PDF y guárdalo en su carpeta. **Nunca lo envíes a un cliente sin que Mariana lo confirme.** Los datos del cliente (nombres, localizadores, confirmaciones) se usan solo dentro de su subproyecto y el documento se entrega como archivo, no como página publicada.

## Orden de las hojas

1. Portada (Documento: «Entrega Final»)
2. Índice (abajo dice «Preparado para», no «Propuesta para»)
3. Resumen
4. Vuelos, por grupo de pasajeros
5. Hoteles (tabla)
6. Apertura del itinerario
7. Itinerario Diario
8. Una hoja por hotel
9. Confirmaciones · Vuelos
10. Confirmaciones · Hoteles
11. Confirmaciones · Restaurantes
12. Cierre

## Lo que cambia frente a la Cotización Completa

**Portada**
- El título es el destino («Europa & África»). Debajo, la ruta en una línea chica («Madrid · Londres · Nairobi · Serengeti») y el nombre del cliente. Viajeros con personas y noches.

**Resumen**
- Mapa y tabla de etapas iguales, más una franja discreta en Soft Almond con el **contacto de emergencia 24 h** y sus teléfonos enlazados. Sin precio.
- Cuando dos etapas caen en el mismo punto del mapa, los números van juntos en una fila; si la etiqueta va a la izquierda, los números crecen hacia la izquierda para no encimarse con la parada vecina.

**Vuelos**
- Un bloque por grupo de pasajeros que vuela igual: etiqueta «Pasajeros», nombres en una sola fila chica separados por un círculo pequeño, y su tabla de vuelos (mismas columnas y reglas que la cotización, renglones compactos, sin grupos Ida/Regreso).
- Sin notas de equipaje ni tarifa: el equipaje y los localizadores van en Confirmaciones.

**Itinerario Diario**
- Igual que en la cotización (rótulo de día, ubicación como título, horas en AM/PM, mínimo 2 fotos por hoja). Varios días iguales pueden agruparse: «Días 11 – 13 · Miércoles 15 – viernes 17 de julio».
- Las entradas de cada día van en orden cronológico.

**Hoja por hotel**
- Cuatro fotos en retícula 2 × 2. Si solo hay tres fotos buenas del hotel: una ancha arriba y dos abajo; si solo hay dos: una sobre otra a todo el ancho. No se rellena con fotos de otro hotel ni de otra categoría de habitación; se le avisa a Mariana qué hotel necesita más fotos.

**Confirmaciones · Vuelos**
- Un bloque por grupo de pasajeros. Tabla: Fecha, Ruta, Vuelo, Clase, Asientos, Equipaje, Código. Encabezado en banda beige, fecha y código en negrita. Asientos sin asignar: «Por asignar».

**Confirmaciones · Hoteles**
- Un bloque por hotel: nombre en IvyOra con estrellas, y una línea con dirección, fechas, noches y régimen.
- Tabla Huéspedes y habitación / Confirmación (número en negrita) y, debajo, una línea chica con lo que incluye.

**Confirmaciones · Restaurantes**
- Tabla: Fecha, Hora (AM/PM), Pax, Restaurante (nombre en IvyOra y dirección chica debajo), Titular de la reserva.

**Cierre**
- Igual que en la cotización, con los créditos de las fotos.

## Notas técnicas

- Clases reservadas por la base, no reutilizarlas en CSS nuevo: `.band`, `.top`.
- El reparto de vuelos y confirmaciones usa `F.measure` y `F.fit` con tope de 8.3 in en la primera hoja (lleva título) y 9.1 in en las siguientes.
- El mapa se arma con `F.map_svg(bbox, trip, stops, labels, width)`; `trip` son los códigos ISO numéricos de los países del viaje.