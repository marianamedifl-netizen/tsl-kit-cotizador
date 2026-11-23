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

1. Reúne las opciones (Sabre, sitio de la aerolínea). La preferencia de Mariana al buscar: minimizar molestias (pocas escalas, buenos horarios) al precio razonable más bajo. Cuando dos o más vuelos sean de la misma aerolínea, cotízalos siempre primero juntos, como un solo boleto, y compara contra los tramos sueltos (detalle en `tsl-cotizar-hoteles-sabre`, sección 4 bis). **No inventes precios, horarios, reglas de tarifa ni vigencias**; lo que falte se marca como pendiente de verificar y se le dice a Mariana.
2. En Sabre, los vuelos que se carguen al área de trabajo para cotizar se descartan siempre con `I`. Nunca se reserva, se guarda un PNR ni se emite sin que Mariana lo confirme en el chat.
3. Copia `ejemplo_vuelos/` y cambia **solo los bloques de datos** (portada, `OPCIONES`, notas) y la foto de `img/`.
4. Genera: `python3 cotizacion_vuelos.py salida.pdf`.
5. Revisa: renderiza cada hoja a PNG y mírala; compara cifras, vuelos, horarios y fechas contra la fuente con `pdftotext -layout`; `pdffonts` debe listar solo IvyOra y Karla.
6. Entrega el PDF y guárdalo en la carpeta del cliente: `Claude/CLIENTES/<Cliente>/<Año del viaje>/<Viaje>/`, con el nombre `OpcionesVuelo_<Cliente>_<Fecha>.pdf` (ejemplo: `CLIENTES/Francisco Medina/2027/Europa y Sudáfrica/OpcionesVuelo_FranciscoMedina_17Nov2026.pdf`). La fecha es la del día en que se cotizó, para distinguir versiones. Si no se sabe quién es el cliente o cómo se llama el viaje, preguntarle a Mariana antes de guardar. Nunca lo envíes a un cliente sin que Mariana lo confirme.

## Tarifas promocionales y netas de la agencia

Antes de armar el documento, revisar si alguna opción aplica a una tarifa promocional o neta de la agencia (tabla y entradas de Sabre en `tsl-cotizar-hoteles-sabre`, sección 4b).

- Si una opción se cotiza con una de esas tarifas, avisarle a Mariana en el chat **en negritas, en mayúsculas y al inicio de la respuesta**, con el programa y si es comisionable.
- Si es neta, la cifra es el costo de la agencia: preguntarle el precio de venta antes de ponerla en el PDF.
- **Tarifa promocional: el cliente sí debe verla** (decisión de Mariana, noviembre de 2026). En el script, la opción lleva `True` como último dato de su tupla, y con eso salen dos cosas:
  - En la comparativa, la etiqueta dorada **Promocional** junto al nombre de la aerolínea (mayúsculas chicas, color `#927F68`, igual que «Recomendada» en la Cotización de Hoteles).
  - En la nota de la opción, **«Tarifa promocional.»** en negritas al inicio.
- Lo que no aparece en el PDF: el código o nombre del programa (BUPQ, TO1), la palabra «neta» y la comisión. Una tarifa neta no lleva etiqueta: se muestra al precio de venta que diga Mariana.

## Hoja 1

**Portada compacta**
- Franja de foto del destino a todo el ancho, de 3.25 in de alto, en tonos apagados.
- Tarjeta beige `rgba(223,211,197,.9)` a la izquierda con logo y lema, título ("Opciones de Vuelo"), ruta en itálica y los datos: Fechas, Viajeros, Documento.
- La tarjeta no debe tapar el punto focal de la foto: si hace falta, se vuelve a encuadrar para que el motivo quede a la derecha.

**Orden de las opciones: de la más barata a la más cara** (decisión de Mariana, noviembre de 2026)
- La comparativa y los bloques de opciones van en ese orden, y la letra sigue al precio: la opción A es siempre la más barata.
- El script lo hace solo: ordena `OPCIONES` por el total y asigna las letras. No importa en qué orden se escriban los datos.
- La nota final se escribe con las letras ya ordenadas (por ejemplo, la vigencia por opción). Revisarlo en el PDF.
- En el chat, las tablas de opciones también se presentan de barata a cara y con las mismas letras del PDF.

**Comparativa**
- Tabla con Opción (punto con letra), Aerolínea (con ruta y si es uno o dos boletos), Cabina, Escalas ida · regreso y Total con su equivalente.
- Si la opción es tarifa promocional, lleva la etiqueta dorada **Promocional** junto al nombre de la aerolínea.

**Primera opción**
- Cabe bajo la comparativa en la hoja 1; las demás van dos por hoja (`POR_HOJA`).
- Con cuatro opciones se usa `POR_HOJA = [1, 3]` y el documento queda en dos hojas: las opciones B, C y D van juntas en la hoja 2 con la nota final y la firma. Mariana lo pidió así en noviembre de 2026; no mandar una opción sola a una tercera hoja.
- Una hoja con tres opciones se compacta sola (clase `dense`: menos aire entre opciones y renglones un poco más juntos). Para que quepa, las notas tienen que ser cortas. Revisar siempre en el PNG que la nota final no se encime con la firma.

## Un bloque por opción

- Etiqueta "Opción A", aerolínea y ruta, total a la derecha.
- Tabla de vuelos corrida, con encabezado en banda beige y **sin renglones de grupo** (Ida, Regreso, etc.). Mariana los quitó en noviembre de 2026 porque cargaban el documento. Los vuelos van en orden de fecha, uno por renglón.
- En el script los datos siguen escritos en grupos, y `opcion()` los aplana: `F.flights_table([(None, [r for _, rows in groups for r in rows])])`. El ejemplo canónico ya lo hace así. Esta regla es solo de la Cotización Vuelos; la Rápida, la Completa y la Entrega Final no cambian.
- Reglas de la tabla: fechas en negrita, la clase que no sea Business resaltada, "+1" como superíndice, duración a la derecha, horas en 24 h.
- **Nota corta, en texto corrido** (decisión de Mariana, noviembre de 2026). No va en párrafo largo ni en columnas con rótulos: probó las columnas y prefirió el texto. Lleva siempre este orden, en frases cortas:
  1. Boleto: «Un solo boleto.» o «Dos boletos separados.». Si los dos boletos conectan el mismo día, se dice que la conexión no queda protegida.
  2. «Ida: vuelos directos.» o «Ida: escala de 2 h 50 m en Londres.»
  3. «Regreso: escala de 7 h 55 m en Fráncfort.»
  4. Cambios y reembolso: «Cambios: MXN 5,121; reembolso según la tarifa.» o «Cambios y reembolso sin cargo.»
  5. Equipaje: «Equipaje: 2 × 32 kg por persona.» o «Equipaje por confirmar.»
- La nota no repite lo que ya dice la tabla (cabina, horarios, hora de llegada) ni el desglose de precio por boleto. Debe caber en una o dos líneas; si una palabra queda sola en la segunda línea, unir la última frase con ` `.
- Ejemplo completo: «Un solo boleto. Ida: vuelos directos. Regreso: escala de 7 h 55 m en Fráncfort. Cambios y reembolso sin cargo. Equipaje: 2 × 32 kg por persona.»

## Cierre

- Nota final con vigencia por opción, tipo de cambio, equipaje y crédito de la foto.
- En lugar de hoja de cierre, la firma de contacto al pie de la última hoja (`F.sign()`): Mariana Medina · Luxury Travel Designer, teléfono, correo y `@thesuitelife.mx`, con enlaces.

## Fotos

- Franja de portada: Unsplash, del destino real; regístrala con `download_asset` y acredita al fotógrafo en la nota final. Se captura desde Chrome y se trata con `fotos.ambiente()`.

## Marca

Las mismas reglas de `tsl-cotizacion-completa`: solo neutros, IvyOra Thin para títulos y Karla para texto, sin íconos, arcos, degradados ni sombras, y sin símbolos que caigan en fuente de respaldo.