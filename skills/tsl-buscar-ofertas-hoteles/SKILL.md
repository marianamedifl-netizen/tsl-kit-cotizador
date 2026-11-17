---
name: "tsl-buscar-ofertas-hoteles"
description: "Busca ofertas de noches gratis y promociones en Virtuoso y Four Seasons Preferred Partner con la sesión de Mariana, y las entrega en el chat. Úsala cuando pida ofertas, noches gratis o material para una serie de deals."
---

# TSL · Buscar ofertas de hoteles (Virtuoso y Four Seasons Preferred Partner)

Sirve para armar series como «Black Friday Deals»: encontrar ofertas de noches gratis en hoteles muy conocidos y entregárselas a Mariana **en el chat** para que escoja. Los anuncios se hacen después, con `tsl-ads-instagram`.

## Reglas

- Se usa Chrome con la sesión de Mariana. Si un sitio pide iniciar sesión, entra ella; nunca escribas contraseñas.
- Solo se lee. No se reserva, no se envían formularios ni correos.
- **No inventes** ofertas, fechas ni condiciones. La lista sale de lo que muestra el sitio ese día; di la fecha de consulta.
- Deja el aviso de cookies sin aceptar.
- Pocas consultas y espaciadas (una cada 250 ms o más); no recorras los miles de hoteles del catálogo.

## Virtuoso (comprobado, nov 2026)

1. Abre `https://www.virtuoso.com/travel/luxury-hotels/search?virtuosoExclusives=Virtuoso+Exclusive+Hotel+Offer&sort=HotelNameAsc`. Si arriba aparece el nombre de Mariana, la sesión está activa.
2. La lista carga 24 hoteles; pulsa «Show More» hasta tener todos (eran 77). De cada tarjeta, toma el enlace «More Details and Photos»: `/travel/luxury-hotels/<id>/<nombre>`.
3. Por cada hotel, lee `/travel/api/hotel/<id>` desde la misma página. Los campos útiles: `companyName`, `virtuosoExclusivePromotions` y `promotions` (cada una con `promotionName`, `formattedTravelDates`, `description`), y `virtuosoAmenitiesHtml`.
4. Filtra las de noches gratis buscando en nombre y descripción: «night free», «complimentary night», «Stay X Pay Y», «night on us», «3rd/4th/5th night».
5. El resultado de un script se corta a unos mil caracteres: para leer la lista completa, escríbela en la página y léela con la lectura de texto de la página.

Límite: el filtro solo trae los hoteles marcados con oferta exclusiva Virtuoso. Otros hoteles pueden tener promociones normales que no aparecen ahí; para cubrirlos, usa la búsqueda por cadena.

### Búsqueda por cadena (la que Mariana prefiere)

Cadenas que le interesan: Four Seasons, Aman, Mandarin Oriental, Peninsula, Rosewood, Accor solo lo más alto (Raffles, Fairmont, Sofitel Legend, Orient Express), Auberge, Belmond, Hyatt premium (Park Hyatt, Alila, Andaz), IHG premium (Six Senses, Regent, InterContinental), Marriott premium (Ritz-Carlton, St. Regis, EDITION, Bulgari, Luxury Collection), Oetker, Rocco Forte, y propiedades muy top de otras cadenas.

1. Desde la página de búsqueda de hoteles, consulta `POST /travel/api/search/hotels` con `{query:"<cadena>", sortBy:"HotelRelevance", currentPage:1, highestPageShown:1, nextPage:2, prependScrollPosition:0, previousPage:0, rowsPerPage:300, startRow:0}`. Devuelve `results` con `id`, `name`, `city` y `country` (máximo 100 por consulta).
2. La búsqueda también coincide con descripciones: filtra por nombre del hotel (por ejemplo, que contenga «Rosewood»). Oetker y Rocco Forte traen la marca en el nombre.
3. Lee `/travel/api/hotel/<id>` de cada hotel, tres a la vez con 300 ms de pausa (590 hoteles tardan unos 3 minutos), y filtra las de noches gratis.
4. Preferred Hotels y Leading Hotels of the World son afiliaciones, no nombres: Virtuoso no permite filtrarlas. Dilo al entregar.
5. Descarta las que cierran reserva antes de la fecha de la campaña y agrupa por cadena: hotel, tipo de oferta (3ª, 4ª, 5ª noche), viaje hasta y reservar antes de.

## Four Seasons Preferred Partner

1. Abre `https://preferredpartners.fourseasons.com/offers/`. Si dice «Welcome Mariana Medina», la sesión está activa.
2. En este sitio no se pueden ejecutar scripts: se lee el texto de la página. La página de ofertas muestra solo cuatro por región; para la lista completa entra a «View all exclusive offers» y, si hace falta, filtra por país.
3. Busca «Fourth Night Free», «Third Night Free» y «Stay Longer». Anota también las de mucho valor (upgrade garantizado, créditos altos, media pensión).
4. Las ofertas «Travel Advisor Rate» y las de comisión son para agentes: nunca van a clientes ni a anuncios.

## Qué entregar en el chat

Una tabla por fuente con: hotel, destino, oferta, fechas de viaje, fecha límite para reservar. Después:

- Marca las que vencen antes de la fecha de la campaña (para Black Friday, las que cierran reserva ese día o antes).
- Di qué no se revisó (categorías de habitación, fechas bloqueadas, condiciones completas) y que hay que confirmarlo antes de publicar.
- Pregunta cuáles quiere para la serie. No hagas anuncios hasta que escoja.