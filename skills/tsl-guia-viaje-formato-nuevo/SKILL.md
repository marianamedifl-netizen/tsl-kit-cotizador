---
name: "tsl-guia-viaje-formato-nuevo"
description: "Crea la Guía de Viaje de The Suite Life en el formato nuevo (nov 2026): clima diario con íconos, qué empacar por destino, inspiración de outfits (mujer y hombre), maletas, propinas y esenciales. Úsala cuando Mariana pida una guía de viaje, qué empacar, clima o propinas; sustituye a tsl-guia-viaje."
---

# TSL · Guía de Viaje (Formato Nuevo)

Documento complementario que acompaña a la Entrega Final (`tsl-entrega-final-formato-nuevo`) y se entrega aparte. Misma identidad que la Cotización Completa (`tsl-cotizacion-completa`): lee sus reglas de marca y de fotos antes de armarlo. Aprobado por Mariana en noviembre de 2026. Sustituye a `tsl-guia-viaje` (el formato anterior de emblemas e íconos grandes).

## Dónde está la plantilla

En la computadora de Mariana, carpeta `Travel Agent Portal/TSL - Formato Nuevo/`:

- `tsl_base.py` y `tsl_formato.py`: tipografías, logos, estilos aprobados y piezas comunes (`cover_page`, `index_page`, `furniture`, `closing_page`, `print_pdf`). No se editan por documento.
- `ejemplo_guia_viaje/guia_viaje_garza.py`: ejemplo canónico (Europa & África, 12 hojas). Los datos, los íconos de clima y el CSS propio de la guía (`GUIA_CSS`) van en ese archivo; las fotos, en `img/` y las prendas de inspiración en `img/ins/`.
- `fotos.py`: recortes y tratamiento de color.

Las fuentes están en `TSL - Brand Files/Fonts` (IvyOra y Karla). Si la computadora no está conectada o la carpeta no aparece, dilo de inmediato; no reconstruyas el formato a ojo.

## Flujo

1. Parte del itinerario confirmado (fechas, destinos, hoteles, restaurantes, actividades). El clima se busca por destino y mes (promedios históricos) y se dice de dónde sale. Propinas, reglas de equipaje de chárter, visas, vacunas y enchufes se toman del DMC, de los lodges o de fuentes oficiales. **No inventes montos, reglas ni requisitos**; lo que no esté confirmado se marca como pendiente de verificar y se le dice a Mariana. Los temas de salud remiten siempre al médico del viajero.
2. Copia `ejemplo_guia_viaje/` a una carpeta del cliente y cambia solo los bloques de datos: `PORTADA`, `CLIMA`, `EMPACAR`, `INSPIRACION`, `MALETAS`, `PROPINAS`, `ESENCIALES` y `CREDITOS`. Las hojas de Maletas y Propinas solo van si el viaje las necesita (safari, chárter, expedición).
3. Consigue las fotos (ver Fotos) y genera: `python3 guia_viaje_<cliente>.py salida.pdf`.
4. Revisa: renderiza todas las páginas a PNG y míralas (nada encimado ni tapando el pie); compara cifras y fechas contra la fuente con `pdftotext`; `pdffonts` solo IvyOra y Karla; `pdfinfo` con el título; índice y marcadores enlazados; la referencia de Esenciales a la hoja de propinas con el número de página correcto.
5. Entrega el PDF y guárdalo en su carpeta. **Nunca lo envíes a un cliente sin que Mariana lo confirme.**

## Orden de las hojas

1. Portada
2. Índice (abajo «Preparado para»)
3. Clima Diario
4. Qué Empacar, una hoja por destino
5. Inspiración · Mujer
6. Inspiración · Hombre
7. Guía de Maletas
8. Guía de Propinas
9. Esenciales
10. Cierre

## Reglas por hoja

**Portada**
- Misma foto y tarjeta que la Entrega Final del viaje, pero **el título es «Guía de Viaje»** en una sola línea (`h1_pt=41`) y debajo va el destino («Europa & África»), para distinguirla de un vistazo de la Entrega Final.
- Luego el cliente y los datos: Ruta, Fechas, Viajeros. Sin renglón «Documento».

**Clima Diario**
- Tabla con encabezado en banda beige: Fecha (negrita), Día, Destino, Clima esperado, Mín, Máx.
- **Ícono de clima de línea fina** antes de la descripción: sol, parcial, nublado o llovizna, en arena `#927F68`, dibujados en SVG (nunca emoji ni símbolos de fuente). Los días de vuelo van sin ícono y con raya en las temperaturas.
- Debajo, leyenda de los íconos y una nota chica con la unidad y la fuente de las temperaturas.
- Son los únicos íconos del documento.

**Qué Empacar** (una hoja por destino)
- Título «Qué Empacar» con el destino en itálica al lado.
- Franja de datos: Fechas y Clima.
- Foto vertical del destino (3 × 3.97 in) con pie en itálica, alternando de lado en cada hoja.
- Junto a la foto: «Imprescindibles», ocho prendas en dos columnas en IvyOra con filete; y «Recomendaciones», lista en Karla con guion.
- Al final, franja Soft Almond «Tip TSL».

**Inspiración** (una hoja Mujer y otra Hombre)
- Título «Inspiración» con «Mujer» u «Hombre» en itálica; franja con Para (destino) y Paleta.
- **Doce prendas en retícula de 4 × 3**, cada foto con su nombre debajo en versalitas. Primero ropa, luego calzado y accesorios.
- Fotos de prendas sueltas, de preferencia sin rostros, en la paleta del viaje y todas con el mismo tratamiento de color. Si Mariana da fotos de producto de marcas que recomienda, se usan esas.
- Nota al pie: son fotos de inspiración, no prendas específicas.
- No se copia la composición de un collage de terceros; la referencia solo marca el tipo de hoja.

**Guía de Maletas**
- Título con el destino en itálica y filete debajo.
- Foto vertical y, al lado: tres renglones Sí / No / Sí con el tipo de equipaje en IvyOra y su descripción; luego «Reglas del chárter» y «Qué evitar» con subtítulos en Karla negrita.
- Franja «Tip TSL».

**Guía de Propinas**
- Párrafo de introducción; tabla con banda beige (Posición, Sugerido por pareja / día, Grupo / día, Total) y renglón de total en banda beige.
- Dos bloques por lodge con fechas, cálculo y total en IvyOra grande.
- Franja «Tip TSL» y una foto apaisada angosta al pie.

**Esenciales**
- Renglones con título en IvyOra a la izquierda (Moneda & Efectivo, Enchufes & Electricidad, Documentos & Salud, Propinas, Husos & Contacto) y texto en Karla a la derecha, separados por filetes.
- Teléfonos enlazados; la referencia a la hoja de propinas enlaza y lleva su número de página.

**Cierre**
- Igual que en los demás documentos. Con muchas fotos, los créditos se ensanchan para no acercarse al contacto.

## Fotos

- Destino: las mismas de ambiente de la Entrega Final del viaje (Unsplash), con `fotos.ambiente()`.
- Inspiración: Unsplash, 24 prendas. Se buscan por prenda, se revisan en hoja de contactos y se capturan desde Chrome en mosaicos de 330 × 408 px (cinco por fila); se recortan y se tratan con `fotos.ambiente()`. Evitar logotipos de marca visibles, fondos chillones y fotos de retrato.
- Registra cada foto usada con `download_asset` y acredita a los fotógrafos en el cierre.
- No descargues ni insertes fotos de personas públicas.

## Notas técnicas

- Clases reservadas por la base, no reutilizarlas en CSS nuevo: `.band`, `.top`.
- Las tablas con encabezado en banda usan la clase `bnd`.