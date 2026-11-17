---
name: "tsl-ads-instagram"
description: "Crea anuncios de Instagram de The Suite Life (carrusel, anuncio individual, Story y series de stories de ofertas) con la marca TSL, a partir de una promoción o viaje. Úsala cuando Mariana pida ads, anuncios, posts o stories de una oferta."
---

# TSL · Anuncios de Instagram

Anuncios con la identidad de The Suite Life que no parezcan hechos con IA: fotografía real, tipografía de marca, mucho aire y texto sobrio. Formatos aprobados por Mariana en noviembre de 2026.

Ejemplo canónico: el lienzo de diseño «Ads Instagram · Safari alrededor del mundo en jet privado» (https://claude.ai/artifact/9CyXWRPNDEseicVmNR3jEo). Ábrelo y úsalo como base antes de diseñar algo nuevo.

## De dónde sale la promoción

Correos, PDFs que Mariana adjunta, o páginas a las que ella entra con su cuenta (Virtuoso, Four Seasons Preferred Partner, Abercrombie & Kent; ver `tsl-buscar-ofertas-hoteles`). Si una página pide iniciar sesión, entra ella; nunca escribas contraseñas.

## Antes de diseñar

1. Saca los datos de la fuente: nombre, fechas de viaje, fecha límite para reservar, precio y a qué aplica, condiciones. **No inventes cifras, fechas ni beneficios**; lo que falte se pregunta o se deja fuera.
2. Pregunta el **idioma** (español o inglés) si Mariana no lo dijo. El ejemplo canónico quedó en inglés.
3. No nombres al proveedor (A&K, Virtuoso, Four Seasons Preferred Partner) en el arte salvo que ella lo pida.

## Formatos (1080 × 1350; Story 1080 × 1920)

- **Cover**: foto a sangre con velo oscuro, logo arriba, rótulo en mayúsculas, titular en dos líneas con la segunda en itálica, una frase y la llamada a la acción subrayada.
- **Encounter**: fondo Soft Almond, foto enmarcada de 612 × 810 centrada, numeración y país arriba, pie de dos líneas con una palabra en itálica, fecha y lugar abajo. Una lámina por destino o experiencia.
- **Fact**: fondo Oatmeal, una cifra enorme en IvyOra y una frase. Solo con cifras de la fuente.
- **Route**: fondo Stone Grey, lista numerada de destinos con lo que se vive en cada uno.
- **Close**: fondo Antique White, logo con lema, fechas, precio, llamada a la acción y contacto (Mariana Medina, +52 55 1850 0549, @thesuitelife.mx).
- **Journey card**: anuncio individual con logo, foto apaisada, titular, tres cifras (días, destinos, viajeros), fechas y precio.
- **Story**: como el Cover, dejando libres 290 px arriba y 340 px abajo para la interfaz de Instagram.

Un carrusel se arma con Cover + varias Encounter + Fact + Route + Close.

### Serie de stories de ofertas (aprobada con «Black Friday Deals»)

Ejemplo: lienzo «Black Friday Deals · Stories» (https://claude.ai/artifact/2dKpYci6pdnuyecy9bXWhP). Las ofertas salen de `tsl-buscar-ofertas-hoteles`, y Mariana escoge antes las cadenas.

- **Portada de la serie**: foto a sangre con velo de 42%, logo, rótulo, titular en dos líneas (la segunda en itálica), una frase con las cadenas y la llamada a la acción. A Mariana le gustan fotos de ambiente con actitud, como una cama destendida con luz de la mañana; sin personas ni logotipos de otros hoteles.
- **Lista por cadena**: fondo de la paleta (alternar Stone Grey, Antique White, Oatmeal y Soft Almond), logo, rótulo, nombre de la cadena en grande y una fila por hotel: nombre a la izquierda, oferta en itálica a la derecha. Dos cadenas pueden compartir una story con un subtítulo cada una.
- **Foto después de cada lista**: foto oficial enmarcada (900 × 675) del primer hotel de la lista, con nombre, oferta en itálica y destino.
- **Legibilidad**: máximo 8 hoteles por story para que el nombre quede en 48 px o más; con más de 10, dividir en dos stories. Nunca bajar de 33 px. Los nombres van en una sola línea: acortar el nombre antes que reducir la letra.
- Antes de armar, releer cada oferta en la fuente y sacar las que no sean lo que dice el titular (por ejemplo, un descuento en vez de una noche gratis). Si no se confirmaron fechas y condiciones, el pie dice «Conditions vary by hotel» y no se ponen fechas.

## Marca

- Colores: Stone Grey #7D766C, Oatmeal #DFD3C5, Soft Almond #F0EDE8, Antique White #FCF9F5, Eerie Black #232323; texto chico sobre fondos claros en #55504A.
- Tipografía: IvyOra Display Thin y Thin Italic para titulares; Karla para rótulos (mayúsculas, espaciado 0.28em) y texto.
- Sin emojis, íconos, degradados, sombras ni esquinas redondeadas. Un solo acento en itálica por titular.
- Legibilidad: sobre foto con velo o sobre Stone Grey, todo el texto de 24 px o más. En fotos muy claras el velo sube a 50% (la guía de marca dice 20–30%, pero el texto blanco no se lee).
- Texto: frases cortas, sin superlativos ni signos de exclamación; datos concretos.

## Cómo se construye

1. Se hace en el lienzo de diseño de Claude (tipo Design), un tablero por lámina, siguiendo las instrucciones del tipo.
2. Fuentes: subir `IvyOraDisplay-Thin.ttf`, `-ThinItalic.ttf` y `-Light.ttf` desde `TSL - Brand Files/Fonts`; Karla desde Google Fonts.
3. Logos: `TSL - Formato Nuevo/logo/l1.svg` (con lema) y `l2.svg`; quitar el bloque `<style>` y poner el color como atributo (blanco #FCF9F5 sobre foto, tinta #232323 sobre claro).
4. Fotos: recortarlas al tamaño exacto antes de subirlas y mirarlas para saber dónde queda el motivo; el texto va en la zona vacía.

## Fotos

- Lo ideal son las fotos oficiales del proveedor para agentes o fotos de Mariana; son lo que hace único el anuncio. Mariana confirmó que puede usar las fotos oficiales en redes.
- Fotos oficiales de un hotel: en Virtuoso, `/travel/api/hotel/<id>` trae `imageLibraryItems` (url y caption). Elegir por el caption (exterior, vista aérea, alberca, lobby) y evitar las que tengan huéspedes en primer plano.
- Nunca poner una foto genérica junto al nombre de un hotel real.
- Si se usa Unsplash: foto del animal o lugar correcto, registrar cada una con `download_asset`, y avisar si no es del sitio exacto.
- Se capturan desde Chrome; ni la nube ni la computadora pueden descargar de Unsplash directamente. Si Chrome no está conectado, dilo y pide a Mariana que lo abra o que adjunte las fotos.
- Tratarlas con `fotos.ambiente()` para que queden en tonos apagados.
- Nunca fotos de personas públicas.

## Entrega

Avisa a Mariana qué fotos son provisionales, qué datos tomaste de la fuente y qué decidiste por tu cuenta. No publiques ni envíes nada: ella publica.

**Revisar antes de entregar.** El lienzo no se puede ver desde aquí, así que cada pieza se dibuja aparte: tomar el contenido de cada tablero, cambiar las direcciones `/_blob/…` por los archivos locales (fuentes IvyOra y Karla de `TSL - Brand Files/Fonts`, logos y fotos), abrirlo con Playwright y Chrome a 1080 × 1920 (o 1080 × 1350) y guardar un JPG. Mirar todas en una hoja de contacto y corregir lo que se vea chico, cortado o encimado antes de avisarle.

**Imágenes para publicar.** Cuando pida los archivos, entregar esos JPG numerados en orden de publicación (`00_Cover.jpg`, `01_…`) en una carpeta con el nombre de la campaña dentro de Descargas (`~/Downloads`); hay que pedirle acceso a esa carpeta.

**Publicar.** No hay conector directo de Instagram. Si conecta una herramienta de programación (Metricool, Windsor.ai), se programa solo con su confirmación de cada pieza, texto, fecha y hora.