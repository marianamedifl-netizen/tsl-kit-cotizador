---
name: "tsl-cotizar-hoteles-sabre"
description: "Cotiza y compara hoteles y vuelos para The Suite Life en Sabre (tarifas NEM/API), Expedia y el sitio del hotel o la aerolínea, y entrega el comparativo en el chat antes de cualquier documento; incluye comandos Sabre y traslados Rolzo."
---

# TSL · Cotizar y comparar hoteles (Sabre · Expedia TAAP · página del hotel)

Úsala siempre que Mariana pida cotizar un hotel, comparar plataformas, buscar en Sabre, Expedia TAAP o el sitio del hotel, o usar cualquier comando de Sabre. También aplica a los vuelos de una cotización. **Siempre que Mariana pida una cotización, este comparativo va primero y en el chat**; los documentos se arman después, cuando ella elija (ver la regla 5).

**Guía completa de comandos Sabre** (hoteles, aéreo, PNR, utilidades, con fuentes): documento del proyecto `claude/Guia_Sabre_TSL.md` y copia en la carpeta `Travel Agent Portal/Sabre/Guia_Sabre_TSL.md`. Aquí va lo esencial y lo **comprobado en vivo** en la cuenta de TSL.

## Reglas que no se rompen

1. **No inventar** precios, disponibilidad, políticas ni comisiones. Lo que no se vea en pantalla se marca **"pendiente de verificar"**.
2. **Nunca reservar, emitir, enviar ni cobrar** sin confirmación explícita de Mariana en el chat. En Sabre: botón **Book**, `0H…`, `01…`, `E`, `ER`, `EM…`, `W‡…`, `X…`. En TAAP: **Reserve**. En el sitio del hotel: no pasar de la selección de tarifa.
3. **Contraseñas:** nunca escribirlas. Si una página pide iniciar sesión, decirle a Mariana que entre ella y esperar.
4. Rechazar las cookies no esenciales.
5. **Primero el comparativo, después los documentos.** Cuando Mariana pida una cotización, antes de armar cualquier PDF se le entrega en el chat la comparación de tarifas entre **Sabre, Expedia y directo** (sitio de la aerolínea para vuelos, página del hotel para hoteles). No se genera ningún documento hasta que ella vea el comparativo y escoja. Si una de las tres fuentes no se pudo consultar, se dice cuál y por qué; no se omite en silencio.
6. **Avisar siempre de la reembolsable más barata.** Aunque se prefieran las tarifas NEM reembolsables, si existe otra tarifa reembolsable más barata (promoción, API, pública, paquete, en cualquiera de las tres fuentes), se le avisa a Mariana con el nombre de la tarifa, el precio, la diferencia contra la NEM y lo que se gana o se pierde (beneficios, fecha límite de cancelación, forma de pago).

## Navegador

- Usar el **navegador integrado del panel lateral** (Mariana lo pide así). Abrir cada plataforma en su propia pestaña y dejarlas abiertas para comparar.
- Antes de pedirle a Mariana que haga algo en el navegador, revisar con `tabs_context` si el panel está visible. Si está oculto, pedirle que lo muestre con Cmd+Shift+B o con el ícono del globo.
- Permisos de sitio que se necesitan (scope "site"): `srw.sabre.com`, `accounts.havail.sabre.com`, `expediataap.com`, el dominio del hotel y el de su motor de reservas (por ejemplo `app.namastay.io` en La Mamounia).
- Leer con `get_page_text` / `find`. Usar capturas solo cuando el contenido viene en un iframe.

---

## 1. Sabre (Agency Workspace, srw.sabre.com · PCC 6FK2)

### Búsqueda: formato de Mariana

```
HOT<ciudad>¥NEM¥API/<entrada>-<salida><adultos>/C-<moneda>/N-<hotel>
Ej.: HOTRAK¥NEM¥API/15MAR-18MAR2/C-USD/N-MAMOUNIA
```

- **`<ciudad>`:** el código de la ciudad del hotel (RAK = Marrakech). Si el ejemplo de Mariana trae otro código, usar el de la ciudad correcta.
- **La `/` antes de las fechas es obligatoria.** `HOTRAK15MAR-18MAR2` responde "command not supported".
- **`¥`:** se escribe tal cual en la línea de comandos. Separa los Client ID.
- **`NEM` y `API`:** son los códigos de tarifas preferenciales de la agencia.
- **Adultos:** el número va pegado a la fecha de salida (1–9, una habitación).
- **`/C-USD`:** Sabre convierte solo a esa moneda. **`/N-`:** filtra por nombre.
- Si hay que separar el origen de cada tarifa, buscar `¥NEM` solo, luego `¥API` solo y luego sin código. También se puede usar el filtro **Client ID** de la lista de tarifas.

### Ruta para ver las tarifas (comprobada)

1. **Escribir el comando:** clic en la línea de comandos (`TYPE COMMAND HERE`), escribir el comando y Enter. Esperar unos 8 segundos.
2. **Desplegar el hotel:** `find` el nombre del hotel, usar la referencia **más reciente** (la de número más alto) y dar clic. Si el clic falla por estar fuera de pantalla, usar la otra referencia del par.
3. **Abrir las tarifas:** `find "View Rates"` → `scroll_to` → clic. Esperar unos 8 segundos y confirmar con `find "Room Rates"`, que muestra el número de tarifas.
4. **Leer:** `get_page_text`. La pantalla **acumula** todas las búsquedas anteriores, así que se lee solo el último bloque `Room Rates (n)`.
5. **Detalle de una tarifa:** `find` el código de la tarifa (por ejemplo `A1QAVI`) → clic para desplegarla → `find "Rate Details"` → clic. Ahí vienen los impuestos, la garantía, la cancelación con fechas exactas, la **comisión** y las **amenidades** (desayuno, upgrade, crédito, early/late). Cerrar con **Close**. **Nunca dar clic en Book.**
6. **Si el panel Trip Summary tapa la lista:** cerrarlo con el ícono "Trip Summary" de la barra derecha.

### Orden para cotizar

1. Tarifas **NEM**.
2. Tarifas **API**.
3. Tarifas normales.

Dentro de cada grupo, **reembolsables primero, de la más barata a la más cara**. Siempre abrir el Rate Details de la tarifa preferencial: en La Mamounia, la *Tarif Virtuoso* (API) costaba **igual** que la Best Available Rate e incluía desayuno diario, upgrade, early/late y un crédito de 100. Si una preferencial cuesta lo mismo y trae más, esa es la recomendada.

Al terminar, revisar la lista completa de reembolsables de la misma habitación: si alguna cuesta menos que la NEM reembolsable, se reporta aparte como «reembolsable más barata» (regla 6), aunque la recomendación siga siendo la NEM.

### Comprobado en la cuenta (nov 2026)

| Formato | Resultado |
|---|---|
| `HOTRAK/15MAR-18MAR2` | ✅ disponibilidad en la ciudad |
| `HOTRAK¥NEM¥API/…/C-USD/N-…` | ✅ sale la etiqueta API y 69 tarifas (38 Virtuoso + 31 normales) |
| `DC¥MAD27297/USD` | ✅ conversión con BSR de Sabre (1 MAD ≈ 0.1025 USD) |
| `DCMAD27297/USD` (sin `¥`) | ❌ "RESTRICTED": era el formato, no un permiso |
| `HOD1` | ⚠️ toma el 1 como **Sabre ID**, no como línea (abrió el Hyatt Regency Tulsa) |
| Moneda en la lista de tarifas | El selector solo ofrece Supplier/MXN. Para dólares usar `/C-USD` en el `HOT` |

### Si NEM o API no salen

- Correr `HIC*ALL` para ver si el código existe y su categoría (N/X).
- Correr `W/HV*` para revisar la visibilidad.
- Probar `HOT…/RC-X¥NEM`.
- Si sigue sin salir, preguntarle al hotel si tiene la tarifa cargada.

### Comandos Sabre más usados (detalle en la guía completa)

| Formato | Qué hace | ¿Modifica? |
|---|---|---|
| `HOD<id>/<fechas><ad>/¥NEM/C-USD` | Una propiedad por Sabre ID | No |
| `HRD*<línea>` / `HOD*<línea>` | Detalle de tarifa / descripción (sin confirmar en esta cuenta) | No |
| `DC¥<mon><monto>/<mon>` | Convierte moneda (BSR) | No |
| `W/*<código>` · `W/-CC<ciudad>` | Decodifica / codifica ciudad o aerolínea | No |
| `T*<ciudad>` · `T¤ETMEX/RAK` | Hora local / diferencia horaria | No |
| `1<fecha><orig><dest>/D` · `…‡AM//BB` | Disponibilidad aérea: solo directos / aerolínea + Business | No |
| `JR.` · `FQ` · `RD1*M` · `WPNC` · `WPNI` · `WPAE` | Shopping aéreo sin reservar, tarifas, reglas, más barato, alternativas, equipaje | No |
| `WPNCB` | Más barato **y re-reserva** las clases | **Sí** |
| `HELP/<palabra>` | Format Finder dentro de Sabre | No |
| `0H1¥<línea>` · `01…` · `E`/`ER` · `EM` · `W‡…` | Vender hotel o aéreo · guardar PNR · enviar al cliente · emitir | **Sí: solo con OK de Mariana** |

---

## 2. Expedia TAAP (expediataap.com)

1. **Entrar:** abrir `https://www.expediataap.com`. Si pide sesión, Mariana entra ella.
2. **Buscar:** ir directo a la búsqueda por URL:
   `https://www.expediataap.com/Hotel-Search?destination=<Hotel>%2C%20<Ciudad>%2C%20<País>&startDate=AAAA-MM-DD&endDate=AAAA-MM-DD&adults=2&rooms=1`
3. **Abrir el hotel:** `find` el nombre del hotel y tomar el **href completo** de su liga `…Hotel-Information?…` en los resultados.
   - Ahí también está el ID del hotel (`h438418` en La Mamounia).
   - **No usar una URL corta:** la sección de habitaciones no carga.
4. **Leer las habitaciones:** confirmar con `find "Reserve"` y luego `get_page_text`. De cada habitación sale:
   - **Datos de la habitación:** m², vista y camas.
   - **"The current price is $X":** precio **por noche**, de la opción seleccionada.
   - **"$Y total includes taxes & fees":** el total de la estancia.
   - **Opción reembolsable:** aparece como "Fully refundable before <fecha>, + $Z", donde **$Z es por noche**. Para ver el total real, dar clic en ese radio (`find "Fully refundable before"`) y volver a leer `find "total"` y `find "The current price is"`. Dar clic en el radio **no reserva**.
5. **Revisar la sección Fees / Policies:**
   - Impuestos que **se pagan en el hotel** (en Marrakech, la tasa municipal de MAD 49.50 por persona por noche), que no van en el total.
   - Precio del desayuno, del traslado del hotel y de la cama extra.
   - Horarios de check-in y check-out, y código de vestimenta.
6. **Comisión:** TAAP solo muestra "TAAP information · Premium" y no el porcentaje. Queda **pendiente de verificar**.
7. **Nunca dar clic en "Reserve" ni en "Generate quote"** sin permiso.

## 3. Página oficial del hotel

1. **Abrir el sitio:** abrir el sitio oficial, rechazar las cookies y buscar el botón "Réserver" / "Book" → estancia.
2. **Motor de reservas:** muchos hoteles de lujo usan un motor en **iframe** (La Mamounia usa Namastay). Si `find`/`get_page_text` no ven precios:
   - Pedir permiso para el dominio del motor.
   - Navegar con clics por coordenadas sobre una captura reciente: flecha de mes → fecha de llegada → fecha de salida → adultos → **Suivant/Continue**.
   - Leer bajando la página con `scroll` y `zoom` sobre la región del recuadro.
3. **Precios de la lista:** son "À partir de / desde", por noche y normalmente con IVA e impuestos. Ese "desde" casi siempre es la tarifa **no reembolsable** de compra anticipada.
4. **Planes de tarifa:** abrir la habitación → "Choisissez votre tarif". Suelen venir dos: "Réservez en avance" (no reembolsable, prepago) y "Meilleur tarif disponible" (flexible). El ícono ⓘ muestra las condiciones de pago y cancelación.
5. **Moneda:** el selector de moneda del motor (MAD/EUR/USD) sirve como referencia para comparar.
6. Comparar contra Sabre: en La Mamounia el precio del sitio era **idéntico** a Sabre más el impuesto de MAD 99 por noche.

---

## 4. Comparar y recomendar

Comparar **la misma habitación y el mismo tipo de tarifa** (por defecto: la reembolsable más barata). Todo en **una sola moneda**, diciendo de dónde salió el tipo de cambio: `/C-USD` de Sabre, `DC¥` (BSR), el convertidor del sitio del hotel, o el que indique Mariana.

Tabla en formato TSL, con una columna por plataforma (Sabre · Sitio oficial · Expedia TAAP):

| Fila | Qué poner |
|---|---|
| Habitación / Tarifa | Nombre exacto y código de tarifa |
| Promedio por noche | Indicar si incluye impuestos |
| **Total de la estancia** | |
| Impuesto municipal | Incluido o se paga en el hotel |
| **Total real para el cliente** | Sumando lo que se paga en el hotel |
| Cancelación gratuita hasta | Fecha y hora del hotel |
| Penalidad | Por tramos |
| Pago | Garantía con pago en el hotel, prepago o pago a Expedia |
| Desayuno / amenidades | |
| Comisión | % o "pendiente" |

Cómo decidir:
- **Mismo precio:** recomendar **Sabre** (comisión del 10% y reserva bajo el PCC). Si además hay preferencial NEM/API con amenidades al mismo precio, recomendar esa tarifa.
- **TAAP:** conviene cuando da cancelación gratuita más larga (en La Mamounia, hasta 7 días antes contra 21 en Sabre) o un precio claramente menor **después** de sumar los impuestos que se pagan en el hotel.
- **Sitio directo:** solo si tiene una oferta que no aparece en Sabre (y Sabre/TAAP no la igualan), o si el cliente es miembro de un programa como Leaders Club o similar.
- **Reembolsable más barata:** además de la tarifa recomendada, una línea aparte con la reembolsable más barata encontrada en cualquiera de las tres fuentes, si es distinta de la recomendada (regla 6). Si no hay ninguna más barata, decirlo.
- **Cierre de la respuesta:** decir siempre qué quedó pendiente de verificar y preguntar qué habitación, tarifa y plataforma usar. **No armar el PDF hasta que Mariana escoja.**

## 4 bis. Vuelos: comparar Sabre, Expedia y la aerolínea

Cuando la cotización lleva vuelos, se compara **el mismo itinerario** (mismos vuelos, cabina y familia tarifaria) en las tres fuentes y se entrega en el chat, en la tabla de vuelos de Mariana:

- **Sabre:** disponibilidad y tarifa con los comandos de la guía. Los vuelos que se carguen al área de trabajo para cotizar se descartan siempre con `I`; nunca se guarda un PNR ni se emite sin su confirmación.
- **Expedia:** el mismo itinerario en Expedia (TAAP o el conector de Expedia).
- **Directo:** el sitio de la aerolínea.

Por cada fuente: total por persona y para todos, moneda, equipaje incluido, cambios, reembolso y selección de asiento. Si una fuente no ofrece el mismo itinerario o la misma tarifa, se dice y se muestra la más cercana, marcada como distinta. La preferencia de Mariana al buscar: minimizar molestias (pocas escalas, buenos horarios) al precio razonable más bajo.

### Vuelos en Sabre: procedimiento comprobado (nov 2026)

1. **Área de trabajo vacía:** `*A` debe responder `NO DATA` antes de empezar.
2. **Revisar desde qué países se puede emitir cada aerolínea:** `WETP*<aerolínea>` (ej. `WETP*MS`). Muestra la lista POINT OF SALE COUNTRY.
   - **Si aparece MX:** se cotiza normal desde México (PCC 6FK2).
   - **Si no aparece MX:** se cotiza con punto de venta US, que es la oficina de **Brickell Travel (PCC V60H)** en Miami. En nov 2026 EgyptAir (MS) no tenía MX.
3. **Cargar cada segmento con venta larga**, con la misma clase del itinerario de Mariana: `0<aerolínea><vuelo><clase><fecha><origen><destino>NN<pax>`. Ej.: `0AM107D14JANTRCMEXNN2`, `0AF179I14JANMEXCDGNN2`. No hace falta poner los ARNK.
4. **Si un segmento sale `UC`**, la clase ya no tiene lugar. Revisar disponibilidad con `1<fecha><origen><destino><hora>¥<aerolínea>` (ej. `114JANMEXCDG1955¥AF`). Descartar todo con `I` y volver a cargar el segmento en la siguiente clase disponible de la misma cabina. Avisarle a Mariana qué clase se cerró, porque si ya la tiene confirmada en su PNR no debe soltarla.
5. **Cotizar un boleto por aerolínea**, seleccionando sus segmentos y la validadora, en USD:
   - Con MX en la lista: `WPS1/8¥AAM¥MUSD`, `WPS2/6-7¥AAF¥MUSD`, `WPS4-5¥ATK¥MUSD`.
   - Sin MX (se emite por Brickell): agregar venta y emisión en Miami, `WPSMIA¥TMIA`. Ej.: con un solo boleto en pantalla, `WPSMIA¥TMIA¥AMS¥MUSD`.
   - `WPNC¥S1/8¥AAM¥MUSD` busca la más barata **sin re-reservar** (nunca usar `WPNCB` sin permiso).
6. **Cargo de Brickell Travel:** $3.75 USD por pasajero por emisión de boleto. Va como renglón aparte ("FEE BRICKELL") y se suma al total por pasajero, junto con los asientos.
7. **De cada cotización, leer y reportar:** total por pasajero y para todos, familia de marca (BRANDED FARE), si es tarifa privada, la validadora, la fecha límite de compra (LAST DAY TO PURCHASE) y las maletas.
8. **Al terminar:** `I` para descartar y `*A` para confirmar `NO DATA`. Nunca `E`/`ER`.
9. **Formato del total de Mariana:** TTL TKTS (suma de boletos) + TTL SEATS + FEE BRICKELL = TTL P/PAX.

### Misma aerolínea: cotizar siempre como un solo boleto

Cuando dos o más vuelos del itinerario son de la misma aerolínea, **siempre se intenta primero cotizarlos juntos, como un solo boleto**, aunque no sean consecutivos ni formen un viaje redondo (por ejemplo Seúl–Tokio y, semanas después, Okinawa–Seúl con Korean Air). Suele salir más barato que la suma de los tramos sueltos.

- **En Sabre:** cargar juntos todos los segmentos de esa aerolínea y cotizarlos en una sola entrada.
  - Misma cabina en todos: `WPNC¥S<n>/<m>¥TC-BB¥MUSD` (o `TC-YB` para Economy).
  - Cabinas mezcladas (un tramo sin Business a la venta, por ejemplo): revisar la disponibilidad, vender cada segmento en la clase más baja disponible de su cabina y cotizar tal como está reservado con `WPMUSD`. `WP¥MUSD` da error de formato.
  - Descartar siempre con `I` y confirmar con `*A` que diga NO DATA.
- **En Expedia y en el sitio de la aerolínea:** buscar la misma combinación como multidestino. Si no la arman (pasa con cabinas mezcladas), decirlo y mostrar los tramos por separado.
- **En el comparativo:** mostrar las dos cifras, juntos y por separado, con la diferencia, y usar la más barata en el total. Avisar de las condiciones del boleto único (cambios, reembolso, fecha límite de compra y cualquier restricción de venta que marque la regla).
- Si la aerolínea no permite combinarlos o juntos sale más caro, decirlo y dejar los tramos sueltos.

## 5. Traslados (conector Rolzo)

- **Herramientas:** `estado_rolzo` (confirma que diga "produccion"), `buscar_lugar` y `cotizar_traslado`.
- **Lugares:** pasar el objeto `rolzo` de `buscar_lugar` como `origen_lugar` / `destino_lugar`, con un `fullAddress` limpio. Para aeropuertos, escribir el nombre ("Marrakech Menara airport"), no el código IATA.
- **Horarios:** cotizar llegada y salida con los horarios reales de los vuelos. Si no hay, usar horas de referencia y avisarlo.
- **Qué reportar:** vehículo, capacidad (pax y maletas), precio por trayecto y redondo, conversión a USD (`aUSD`), cancelación, espera incluida y su costo extra, y comisión (`comisionPct`).
- **El campo `tarifaConMarkup`** no cuadra con el markup y no se usa.
- El conector solo cotiza. Las reservas de Rolzo las hace Mariana.

## 6. Después

Solo cuando Mariana haya visto los comparativos y escogido, armar el PDF con la skill que corresponda (`tsl-cotizacion-rapida`, `tsl-cotizacion-hoteles`, `tsl-cotizacion-vuelos` o `tsl-cotizacion-completa`), usando la tarifa elegida, sus condiciones reales y el tipo de cambio aplicado.