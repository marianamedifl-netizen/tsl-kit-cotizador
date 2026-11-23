# Guía Sabre · Cotización de vuelos avanzada (The Suite Life)

Armada el 23 nov 2026 con cinco investigaciones en fuentes públicas (guías de Sabre publicadas, clue cards de aerolíneas, manuales de capacitación). Complementa `Guia_Sabre_TSL.md`; no la sustituye.

**Cómo leer el estado de cada formato**
- ✅ **Comprobado** en vivo en la cuenta de TSL (PCC 6FK2).
- 📄 **Documentado** en una guía pública, todavía sin probar en la cuenta. Varias guías son de 2008-2017: probar una vez antes de confiar.
- ❓ **Sin confirmar**: no aparece textual en ninguna fuente.

El separador cruz de Lorena se escribe `¥`. La tecla de cambio se escribe `¤`.

> **Regla de oro.** Solo se cotiza. Estas entradas venden, re-reservan o guardan y **no se usan sin el OK de Mariana**: `0…` (salvo la venta larga para cotizar, que siempre se descarta con `I`), `JR01` y `WC¥<n>` (venden la opción elegida), `WPNCB` (re-reserva), `WPRQ` y `WPA*<n>¥RQ` (guardan PQ), `E`/`ER`, `W¥…`.

---

## 0. Confirmado el 23 nov 2026 (prevalece sobre las marcas 📄 de las tablas)

**En vivo en 6FK2, solo consulta**
- `FQMEXMAD15MARBB-IB¥SA`: funciona. Devolvió 126 tarifas business de Iberia ordenadas de menor a mayor, con las privadas marcadas con `¤` y su designador (`/CNTN`, `/MXTO`) junto a las públicas.
- `RD1*5/15/16`: funciona. Muestra juntas compra anticipada, restricciones de venta y penalidades de la línea 1.
- `115MARMEXMAD¥/*S`: funciona. Filtra por SkyTeam. En el ejemplo la clase `I` salió en `I0`: la tarifa más baja del tarifario existía, pero no había lugar en su clase.
- `WQMEX15MAR/AIB/CIMAD29MAR/AIB/CIMEX-VIB/MUSD`: funciona. Cotiza ida y vuelta sin PNR ni segmentos y lista las tarifas con impuestos y total. `*A` siguió en `NO DATA`.

**Oficial, leído en Finder (Sabre Hub), artículos «Pricing/Fares Optional Qualifiers», «Price using Low Fare Search (WPNI)», «Display a Fare Quote (FQ)», «Price an itinerary using auto price (WP)» y «How to use Shop Fares in Agency Workspace air module»**
- **Pasajeros:** `¥P2ADT/C08` y `¥P2ADT/2C08` (cantidad + tipo, separados por `/`). También `WPP1ADT/1CNN/1INS`. Sin selección de nombres, el orden debe coincidir con el de los nombres del PNR.
- **Cabina en pricing:** `¥TC-` con `PB` premium first, `FB` first, `JB` premium business, `BB` business, `SB` premium economy, `YB` económica, `AB` todas.
- **Cabina en tarifario:** el código va pegado a la fecha y se pueden poner varios: `FQBCNSIN01OCTJB-AF`, `…JBSBYB-AF`.
- **Reembolso y cambios:** `¥MP-I` (muestra si es cambiable y reembolsable y con qué penalidad), `¥MPR-ANY` (solo reembolsables), `¥MPC-ANY` (solo cambiables), `¥MPC-ANY¥MPR-ANY` (ambas), `¥MP-0` (sin ninguna penalidad), `¥MPC-100¥MPR-ANY` (tope de penalidad). En `WPNI` también `¥MPC-100/BEFDEP` y `/AFTDEP`.
- **Multi-ticket:** `¥MT` en pricing y `WPNI¥MT-Y`. Devuelve como máximo dos boletos sencillos (ida y regreso) cuando salen más baratos que uno solo, y muestra también el precio de un solo boleto. Requisitos: estar activo en el TJR de la agencia y que el itinerario tenga un solo stopover. Admite varios tipos de pasajero.
- **Sin restricciones:** `¥XP` sin penalidad (depende de cómo cargó la aerolínea la categoría 16), `¥XA` sin compra anticipada, `¥XS` sin estancia, `¥XR` ninguna. `¥XM` muestra tarifas que no corresponden a la clase reservada.
- **Privadas y corporativas:** `¥PV`, `¥PL`; `¥AC*<código>` (hasta 4, separados por `¥`); `¥I<corporate ID>` (hasta 4); `¥XC` para forzarlas.
- **Punto de venta y de emisión:** `¥S<ciudad>` y `¥T<ciudad>`, juntos para boletos SOTO (`WPSMAD¥TMAD`). Solo valen con `WP`.
- **Marcas:** `¥BR<marca>` y por segmento `¥S1*BRMAIN¥S2*BRMAINFL`. No funciona con `WPA` ni `WQ`. El código de marca sale en el `FQ` de una sola aerolínea.
- **Base tarifaria con validación:** `¥ZZ<fare basis>` cotiza una base concreta respetando las reglas. `¥Q<fare basis>` es command pricing y las ignora.
- **Otros:** `¥RW` vuelta al mundo; `¥X<seg>` conexión forzada; `¥O<seg>` stopover forzado; `¥BF<seg>` y `¥NB<seg>` quiebre de tarifa; `¥ST3-6` side trip; `¥C-<aer>` aerolínea que gobierna; `¥B<fecha>` fecha de compra; `¥FFS-<aer><nivel>` estatus de viajero frecuente.
- **Con riesgo de nota de débito, no usar:** `¥TE` (exentar impuestos; Finder lo marca como override sujeto a débito) y `¥TX` (forzar impuestos).
- **`WPNI` (oficial):** `/D` directos, `/K0` a `/K3` conexiones máximas, `/A<aer>…` y `/X<aer>…` (hasta 20), `/O` misma aerolínea, `/MIX` interlínea, `/THRU` tarifas directas, `/T<1-9>` ± horas, `/P<n>` y `/M<n>` días (máx. 9), `/*AC-MEX*100` aeropuertos alternos por radio, `/CTM840-1200` tiempo de conexión en minutos, `/EO-T2200-0500` excluye conexiones de madrugada, `/XJ` no cambia de cabina, `¥Z19` hasta 19 opciones, `WPNIN` mismos aeropuertos, `WPNIX` mismas conexiones, `WPNIS` sin validar disponibilidad. Valida married segments y busca la mejor combinación de punta a punta. `WC¥<n>` **vende** la opción: no usar.
- **`FQ` (oficial):** `¥R<fecha>` regreso; `/<moneda>`; `<f1>*<f2>` rango (sin la segunda fecha toma 30 días); `¥SA`/`¥SD` orden; `¥FL` base e impuestos; `FT<línea>` impuestos de una línea; `¥B<clase>-<aer>`; `¥Q<fare basis>`; tipos `PM` promocionales, `SP` especiales, `NET` netas, `IT` tour, `RW` vuelta al mundo, `ALL` todas; `FQL2/3¥R24JUN` tarifas de una línea de disponibilidad; histórico hasta dos años; hasta 364 días a futuro. Por omisión muestra públicas y privadas que no requieren código.
- **Tras cotizar con `WP`, `WPNC` o `WPNCS`**, Agency Workspace muestra «More Fares Available» con las ofertas NDC del mismo itinerario. `WPNI` y `WPA` no lo hacen.

**Shop Fares gráfico (Air Module de Agency Workspace): la mejor forma de buscar sin tocar inventario**
- Cabina con cuatro modos: cualquiera, incluir, solo, o «al menos» en todos los vuelos o solo en el vuelo principal (deja la conexión corta en cabina menor).
- Escalas, **tipo de asiento**, tiempo total de viaje, tiempo de conexión, excluir conexiones nocturnas, alianza, aerolínea (incluir, excluir, solo, solo sin códigos compartidos).
- Calendario flexible de ±3 días o fin de semana; multi-ticket; fuente del contenido (NDC, Sabre, LCC); solo reembolsables o cambiables; equipaje documentado gratis; públicas o privadas; account code y corporate ID.
- Hasta 200 opciones, de la más barata a la más cara. Barra de apoyo con tendencia de la tarifa en 14 días, fechas flexibles, aeropuertos alternos a 100 km, y las aerolíneas más baratas y más rápidas.
- **No dar clic en «SELL & SAVE PRICE» ni en «CREATE ORDER»**: venden y guardan.

**Sigue sin confirmar:** `WPA` y `WPA¥OC-BC`, `JR.`, Direct Access (`1…¤<aer>`), y si 6FK2 tiene multi-ticket activo en su TJR. La Academia de Sabre Hub no abrió desde el navegador integrado.

---

## 1. Orden sugerido para cotizar un vuelo

1. **Conocer la ruta.** Quién la vuela, si hay directos, qué alianzas: `S<fecha><par>` sin aerolínea, `1<fecha><par>/D`, `¥/*A`.
2. **Mirar el tarifario antes de buscar vuelos.** `FQ` en business, ordenado de menor a mayor, para saber cuál es la tarifa más baja publicada, en qué clase y con qué condiciones (sección 2).
3. **Buscar disponibilidad en esa clase**, pidiendo siempre el origen-destino completo, no tramo por tramo (sección 3).
4. **Cotizar.** Sin tocar inventario cuando se pueda (`WQ`, `JR.`); con venta larga + `WPNC…` cuando haga falta el precio exacto (sección 4).
5. **Leer las condiciones** desde el pricing: penalidades, equipaje, fecha límite de compra (sección 4.3).
6. **Descartar** con `I` y confirmar `*A` = `NO DATA`.
7. **Comparar** contra Expedia y la aerolínea directa, sumando los recargos de canal (sección 7).

---

## 2. Tarifario (`FQ`) y reglas (`RD`): encontrar la tarifa más baja y las promociones

| Formato | Qué hace | Ejemplo | Estado |
|---|---|---|---|
| `FQ<par><fecha>BB-<aer>` | Solo tarifas business (`BB` va pegado a la fecha) | `FQMEXMAD10MARBB-IB` | 📄 |
| `¥SA` / `¥SD` | Ordena de menor a mayor / de mayor a menor | `FQMEXMAD10MAR¥SA` | 📄 |
| `RT` / `OW` / `HR` (tras la fecha) | Redondo / sencillo / medio redondo. Finder los lista como códigos de tipo de tarifa, pegados a la fecha y separados por coma; guías antiguas los escriben con `¥` | `FQMEXMAD10MARRT-IB` | 📄 |
| `¥R<fecha>` | Fecha de regreso: valida estancia y temporada | `FQMEXMAD10MAR¥R20MAR-IB` | 📄 |
| `<f1>*<f2>` | Rango de fechas de viaje (una semana de una vez) | `FQMEXMAD6JUN*12JUN-IB` | 📄 |
| `¥VN` | Muestra tarifas aunque no cumplan temporada, anticipación o estancia: sirve para descubrir promociones de otras fechas | `FQMEXMAD10MAR-IB¥VN` | 📄 |
| `PM`, `SP`, `ALL` (tras la fecha) | Solo promocionales / especiales / todas | `FQMEXMAD10MARPM-IB` | 📄 (guías antiguas) |
| `¥PL` / `¥PV` / `¥PNEG` | Solo públicas / solo privadas / negociadas | `FQMEXMAD10MAR¥PV` | 📄 |
| `/USD` | Moneda en el `FQ` (en el pricing es `¥MUSD`) | `FQMEXMAD10MAR-IB/USD` | 📄 |
| `,ACI` | Adulto, niño e infante en la misma pantalla | `FQMEXMAD10MAR-IB,ACI` | 📄 |
| `FQ*-**` | Pasa la misma consulta a todas las aerolíneas | — | 📄 |
| `FT<línea>` | Impuestos de una línea del `FQ` | `FT1` | 📄 |
| `RB<línea>` | Clase de reserva que exige la tarifa | `RB2` | 📄 |
| `RD<línea>*<c>/<c>…` | Varias categorías de regla juntas | `RD2*2/3/5/6/7/11/14/15/16` | 📄 |
| `RD<línea>*PN` / `*RE` | Penalidades / reembolso por palabra clave | `RD6*RE/PN` | 📄 |
| `RD<línea>*RTG` | Ruteo permitido por la tarifa | `RD3*RTG` | 📄 |
| `WN<ciudades>` | Millas del recorrido (TPM, MPM, recargo) | `WNMEXMADROMMEX` | 📄 |
| `FQ<par><fecha>RW-<aer>` | Tarifas de vuelta al mundo (mismo origen y destino) | `FQMEXMEX10MARRW-IB` | 📄 |

**Cómo leer la pantalla del `FQ`**
- `BK`: clase y tipo de viaje (X ida, R redondo, H medio redondo).
- `AP`: días de compra anticipada. `MINMAX`: estancia mínima y máxima (`SU` = regla del domingo).
- `TRAVEL-TICKET`: aquí se reconoce una promoción. `T` es la última fecha de emisión y `C` la fecha en que el viaje debe estar completado.
- Marcas de tarifa privada: `*` (corporate ID), `/` (con markup), `X` (neta no emitible).
- El `FQ` no incluye impuestos ni cargo de combustible: el total real sale al cotizar el itinerario.

**Categorías de regla más útiles:** 2 día y hora, 3 temporada, 5 compra anticipada, 6 y 7 estancia, 8 stopovers, 9 transfers, 10 combinaciones, 11 blackout, 14 fechas de viaje, 15 restricciones de venta, 16 penalidades, 19 niños, 31 cambios voluntarios, 35 negociadas.

---

## 3. Disponibilidad y rutas

| Formato | Qué hace | Ejemplo | Estado |
|---|---|---|---|
| `1<fecha><par>¥<aer>` | Filtra por aerolínea | `119JULMEXICN¥AM` | ✅ |
| `¥<aer><aer><aer>` | Varias aerolíneas, códigos pegados | `110MARMEXMAD¥IBAMAF` | 📄 |
| `¥*<aer><aer>` | Excluye aerolíneas | `110MARMEXMAD¥*UAAA` | 📄 |
| `¥/*A` · `¥/*S` · `¥/*O` | Star Alliance · SkyTeam · oneworld | `110MARMEXMAD¥/*S` | 📄 (una fuente escribe oneworld como `OW`) |
| `/D` | Directos y sin escalas | `110MARMEXMAD/D` | 📄 |
| `<hora>-<hora>` | Rango de hora de salida | `110MARMEXMAD1P-9P` | 📄 |
| `/<hora>` | Por hora de llegada | `110MARMEXMAD/9A` | 📄 |
| `//BB` · `//FB` · `//SB` · `//JB` | Solo business · first · premium economy · premium business | `110MARMEXMAD//BB¥IB` | 📄 |
| `.` tras el par | Oculta códigos compartidos: queda quien opera | `110MARMEXMAD.¥IB` | 📄 |
| `1*C` | Todas las clases de los vuelos mostrados | `1*C` | 📄 |
| `1<fecha><par>-<clase>` | Solo vuelos con esa clase abierta | `110MARMEXMAD-I` | 📄 |
| `1<fecha><par>¤<aer>` | **Disponibilidad real del sistema de la aerolínea** (Direct Access). `¥<aer>` solo filtra | `110MARMEXMAD¤IB` | 📄 |
| `1¤<aer>` | Convierte la pantalla actual a Direct Access | `1¤IB` | 📄 |
| `S<fecha><par>/ES¥<aer>` | Dos semanas de frecuencias de una aerolínea | `S10MARMEXMAD/ES¥IB` | 📄 |
| `T*CT-<apto>/<aer><aer>` | Tiempo mínimo de conexión entre dos aerolíneas | `T*CT-MAD/IBIB` | 📄 |
| `T*CT-<ciudad>///<apto><apto>` | Tiempo mínimo con cambio de aeropuerto | `T*CT-LON///LHRLGW` | 📄 |
| `VA*<n>` | Detalle de una línea: equipo, escalas ocultas, terminales, tiempo de vuelo | `VA*1` | 📄 |
| `4G*<aer><vuelo><clase><fecha><par>` | Mapa de asientos sin vender nada | `4G*IB6400J10MARMEXMAD` | 📄 |
| `W/-CY<ciudad>` · `W/-AT<apto>` | Aeropuertos alternos cercanos | `W/-ATMEX` | 📄 |

**Cómo leer la pantalla**
- El número junto a la clase (`J9`, `I4`) es el máximo de asientos vendibles en una entrada, no el total que queda.
- Clase cerrada: `L` lista de espera, `R` solo a petición, `C` cerrada, `0` sin lugar. Un segmento vendido que contesta `LL` o `UC` no tiene lugar en esa clase ✅.
- Columna de escalas: `0` sin escalas; `1` es un «directo» con parada.
- Etiqueta al final: `DCA` significa que el dato viene en tiempo real de la aerolínea.

**Por qué un tramo suelto cuesta distinto que dentro de una conexión.** Las aerolíneas abren y cierran clases según el origen-destino completo y el país de venta (married segments). Por eso se pide la disponibilidad de MEX al destino final con su conexión, y no tramo por tramo. Vender con disponibilidad de tramo suelto para armar una conexión es una infracción (sección 6).

---

## 4. Cotizar

### 4.1 Con el itinerario cargado (venta larga, siempre se descarta con `I`)

| Formato | Qué hace | Ejemplo | Estado |
|---|---|---|---|
| `0<aer><vuelo><clase><fecha><par>NN<pax>` | Venta larga para cotizar | `0AM90D19JULMEXICNNN5` | ✅ |
| `WPNC¥S<segs>¥TC-BB¥MUSD` | Tarifa más baja disponible en business, en dólares, sin re-reservar | `WPNC¥S1/5¥TC-BB¥MUSD` | ✅ |
| `WPNC¥TC-FB¥MUSD` | Lo mismo en first | — | ✅ |
| `WPMUSD` | Cotiza tal como está reservado (cabinas mezcladas) | — | ✅ (`WP¥MUSD` da error de formato) |
| `WPS<segs>¥A<aer>¥MUSD` | Un boleto por aerolínea, con validadora | `WPS1/8¥AAM¥MUSD` | ✅ (Luis) |
| `WPS<ciudad>¥T<ciudad>` | Punto de venta y de emisión (Brickell, Miami) | `WPSMIA¥TMIA¥AMS¥MUSD` | ✅ (Luis) |
| `WPNC¥P2ADT/C09/C08/C06` | **Familia en una sola entrada**: adultos y niños con edad a dos dígitos. El total de pasajeros debe igualar los asientos vendidos | `WPNC¥P2ADT/C09/C08/C06¥TC-BB¥MUSD` | 📄 (el patrón `WPP2ADT/C07/C09` es textual; la combinación con cabina y moneda, por probar) |
| `WPA` | Lista hasta 12 tarifas alternativas del mismo itinerario, sin re-reservar | `WPA¥MUSD` | 📄 |
| `WPA¥OC-BC` / `-BF` / `-BY` | Alternativas en business / first / económica | `WPA¥OC-BC` | 📄 |
| `WP<n>` | Detalle de la opción n de `WPA` | `WP2` | 📄 |
| `WPNC¥XP` / `¥XR` | Excluye tarifas con penalidad / con cualquier restricción | `WPNC¥XP¥TC-BB` | 📄 |
| `WPMPR-ANY` / `WPMPC-ANY` | Pide tarifa reembolsable / cambiable | — | 📄 |
| `WPMP-I` | Muestra las penalidades de cambio y reembolso | — | 📄 |
| `WPNC¥MT` / `WPMT` | **Compara el itinerario como un boleto contra boletos separados** (multi-ticket). La agencia debe tenerlo activado | `WPNC¥MT` | 📄 (guía de Sabre Taiwán; otra investigación no lo encontró) |
| `WPNC¥PV` / `¥PL` | Solo privadas / solo públicas: dice de dónde sale el ahorro | — | 📄 |
| `WPAC*<código>¥XC` | Fuerza la tarifa del account code aunque haya una pública más barata | — | 📄 |
| `WPB<fecha con año>` | Recotiza como si se comprara en otra fecha | `WPB19JUN27` | 📄 |
| `WPX<seg>` / `WPO<seg>` | Trata un punto como conexión / como escala (stopover) | `WPX2` | 📄 |
| `WPNI` + calificadores | Alternativas más baratas al itinerario cargado: `¥TC-BB` cabina, `/XJ` no saltar de cabina, `/D` directos, `/K1` máximo una conexión, `/A*S` alianza, `/X<aer>` excluir, `/T3` ±3 horas, `/P2` y `/M2` días después o antes, `/*AC-MEX*100` aeropuertos a 100 millas, `¥Z19` hasta 19 opciones, `¥BRALL` todas las marcas, `¥MT-Y` boletos separados | `WPNI/D/A*S¥TC-BB¥MUSD` | 📄 (los calificadores con `/` van antes que los de `¥`) |

### 4.2 Sin tocar inventario

| Formato | Qué hace | Ejemplo | Estado |
|---|---|---|---|
| `WQ<ciudad><fecha>/A<aer>/C<clase>…-V<validadora>` | Cotiza un recorrido sin PNR ni segmentos, con fecha, aerolínea y clase por tramo | `WQMEX19JUL/AAM/CDICN11AUG/AAM/CDMEX-VAM/MUSD` | 📄 (ejemplo armado con el patrón de la guía; límite de 125 caracteres) |
| `/X<ciudad>` · `/-<ciudad>` | Conexión · tramo terrestre dentro del `WQ` | — | 📄 |
| `/P<tipo>` · `/L` · `/M<moneda>` | Tipo de pasajero · tarifa más baja · moneda | `…/PC09/MUSD` | 📄 |
| `WQ¥<n>` · `WQRD*L<n>` | Detalle y reglas de una opción | — | 📄 |
| `JR.<orig>/S-OY<dest><fecha><aer>/S-OY<orig><fecha>` | Búsqueda de tarifa baja sin PNR | `JR.MEX/S-OYMAD10MARIB/S-OYMEX20MAR` | 📄 |
| `JR.<orig>¥MUSD/…` | Moneda | — | 📄 |
| `/P-2ADT1C09` | Pasajeros | — | 📄 |
| `/Z-19` | Hasta 19 opciones | — | 📄 |
| `/S-ARUNK<ciudad>` | Tramo terrestre (open jaw) | — | 📄 |
| `/MPR-ANY`, `/MPC-ANY` | Solo reembolsables / cambiables | — | 📄 (separador `/` o `¥` por confirmar) |
| Cabina, sin escalas y fechas flexibles en `JR.` | No aparecen en ninguna fuente | — | ❓ |

### 4.3 Leer las condiciones desde el pricing

| Formato | Qué hace | Estado |
|---|---|---|
| `WPRD*PE` o `WPRD*S1¥C16` | Penalidades de la tarifa recién cotizada | 📄 |
| `WPRD*S<seg>¥C5/6/7` | Anticipación y estancia por segmento | 📄 |
| `WPRD*L<n>` | Reglas de la opción n de `WPA` | 📄 |
| `WPDF` | Explicación del cálculo de tarifa e impuestos (el cargo de combustible aparece como YQ o YR) | 📄 |
| `WPP…¥AE-BG` | Equipaje por tipo de pasajero | 📄 |
| Pantalla gráfica: BAGGAGE DISCLOSURES · VIEW ALL | Equipaje por tramo | ✅ |
| Línea `LAST DAY TO PURCHASE` | Fecha límite de compra | ✅ |

**Errores frecuentes**
- `NO FARE FOR CLASS USED`: no hay tarifa para la clase cargada; probar `WPNC` o `WPA`.
- `NO COMBINABLE FARES FOR CLASS USED`: hay tarifas, pero sus reglas no permiten combinarlas.
- `EACH CNN REQUIRES ACCOMPANYING SAME CABIN ADT`: niño cotizado sin adulto en la misma cabina.

---

## 5. Estrategias para bajar el precio en cabina premium (todas legítimas)

1. **Redondo u open jaw antes que dos sencillos.** En largo radio el sencillo suele costar más de la mitad del redondo. El open jaw se tarifa como media ida y vuelta por dirección.
2. **Misma aerolínea, un solo boleto**, y comparar contra los tramos sueltos (ya es regla de TSL).
3. **Business en el tramo largo y cabina menor en el corto**, verificando tramo por tramo.
4. **Revisar estancia mínima y compra anticipada** antes de descartar una tarifa barata: mover un día puede abrirla.
5. **Stopovers como valor agregado.** Turkish da 2 noches de hotel 5 estrellas en business con conexión de 20 horas a 7 días (todo en TK, se solicita 72 horas antes). Iberia, TAP, Icelandair y Copa permiten parar sin costo de tarifa. Emirates da hotel con conexión de 6 a 26 horas en business si es la más corta disponible.
6. **Vuelta al mundo** de Star Alliance u oneworld cuando el viaje toca tres o más continentes.
7. **Pases regionales**, por ejemplo el JAL Japan Explorer Pass para vuelos internos en Japón (solo económica).
8. **Calendario de ventas** de Aeroméxico en 2026: Hot Sale (25 may – 2 jun), Venta Azul (7–14 sep), Buen Fin (13–17 nov). Que incluyan Clase Premier está sin confirmar.
9. **Verificar el producto real** (asiento-cama, configuración) en aeroLOPA o SeatMaps y con el mapa de asientos de Sabre; avisar que el equipo puede cambiar.

**Un boleto contra boletos separados.** Con un solo boleto la aerolínea responde por llevar al pasajero al destino final y el equipaje va documentado. Con boletos separados cada vuelo es un contrato aparte: si se pierde la conexión hay que comprar otro boleto, y el equipaje casi siempre se recoge y se vuelve a documentar. Dar conexión holgada y decirlo por escrito en la cotización.

---

## 6. Prácticas que NO se usan ni se sugieren (generan notas de débito)

Están listadas en la Resolución 830a de IATA y en las políticas de cada aerolínea; la multa llega a la agencia hasta 9 meses después del vuelo.

- Comprar un destino más lejano o un redondo para no volarlo completo (hidden city, throwaway).
- Boletos cruzados para saltarse la estancia mínima (back-to-back).
- Reservas duplicadas, de prueba, especulativas o con nombres ficticios.
- Cancelar y volver a reservar para retener espacio o alargar el límite de emisión (churning).
- Armar una conexión con disponibilidad de tramos sueltos (romper married segments). Multas de 150 a 1,000 EUR por pasajero en Lufthansa Group.
- Punto de venta u origen ficticio. Salir de otro país solo es válido si el viaje empieza ahí de verdad.
- Segmentos pasivos indebidos y dejar segmentos inactivos en el PNR.

Por eso, al cotizar: cargar solo lo necesario, descartar siempre con `I` y no repetir la misma venta una y otra vez.

---

## 7. Diferencias de canal que cambian el precio

- **Recargo por emitir en GDS.** Lufthansa Group cobra alrededor de €22 por boleto emitido por Sabre en canal tradicional; Air France-KLM, cerca de €24 por trayecto; British Airways e Iberia, un cargo por sector. Los montos para ventas desde México están sin confirmar.
- **NDC en Sabre.** Aeroméxico, Air Canada, Air France-KLM, American, British Airways, Emirates, Etihad, Finnair, Lufthansa Group, Qantas, Qatar, SAS, Singapore, TAP, United, Iberia, ANA, LATAM y Turkish tienen contenido NDC en Sabre; se activa por aerolínea y por PCC. En la pantalla gráfica cada tarifa dice de dónde viene (`NDC` o `SABRE`) ✅.
- **Consecuencia práctica.** Si la web de la aerolínea sale más barata que Sabre, la causa suele ser el recargo de canal o una tarifa NDC que no está activada en el PCC. Decirlo en el comparativo.

---

## 8. Pendiente de comprobar

Lo ya confirmado está en la sección 0. Falta, en este orden:
1. Si 6FK2 tiene multi-ticket activo en el TJR (probar `WPNC¥MT` en la próxima cotización real de ida y vuelta).
2. `WPNC¥P2ADT/C09/C08/C06¥TC-BB¥MUSD` en una cotización real con niños (el formato es oficial; falta ver cuánto baja contra cinco adultos).
3. `WPA` y `WPA¥OC-BC`.
4. `¥VN` y el rango de fechas en el `FQ`.
5. `JR.` con cabina, sin escalas y fechas flexibles.
6. `1…¤<aer>` (Direct Access).
7. Ayudas dentro de Sabre: `FQHELP`, `RDHELP`, `WPRDHELP`, `WQHELP`, `TXHELP`.
8. Los cursos de la Academia de Sabre Hub.

---

## Fuentes principales

- Sabre Finder (Sabre Hub, con la sesión de Mariana, 23 nov 2026): https://central.sabre.com/s/article/optional-qualifiers · https://central.sabre.com/s/article/low-fare-search-wpni · https://central.sabre.com/s/article/display-fare-quote · https://central.sabre.com/s/article/price-itinerary-wp · https://central.sabre.com/s/article/how-to-use-air-shopping-in-sabre-red-360-air-module

- Sabre, *Basic Pricing*: https://airts.ru/upload/Manuals_and_Installers/Manuals/en/Basic_Pricing.pdf
- Sabre, *Low Fare Search*: https://airts.ru/upload/Manuals_and_Installers/Manuals/en/Low_Fare_Search.pdf
- Sabre, *Command and Discount Pricing*: https://airts.ru/upload/Manuals_and_Installers/Manuals/en/Command_and_Discount_Pricing.pdf
- Sabre Indonesia, *Pricing* y *Fares Display*: https://sabretn.co.id/wp-content/uploads/2024/01/Pricing-Sabre-Fares-Ticketing-Guide.pdf · https://sabretn.co.id/wp-content/uploads/2024/01/Fares-Display-Sabre-Fares-Ticketing-Guide.pdf
- Sabre Taiwán, multi-ticket y penalidades: https://www.sabretn.com.tw/index/Other_instruction
- Sabre, *Air Pricing Training Workbook*: https://doczz.net/doc/1869077/sabre-air-pricing-training-workbook
- Sabre Nigeria, curso básico: https://portal.sabreng.com/files/resources/files/1454080752_1454080752_basic_reservation_course.pdf
- Zenon, *Fares and Pricing Manual*: https://www.cyraxx.de/stuff/zenon/Fares_and_Pricing_Manual.pdf
- *Sabre Guide de poche* (2020): https://www.yumpu.com/fr/document/view/63051869/sabre-guide-de-poche
- GDS Help, *Smart Pricing Reference Guide*: https://gdshelp.blogspot.com/2022/11/sabre-smart-pricing-reference-guide.html
- Sabre Developer Hub, Bargain Finder Max y multi-ticket: https://developer.sabre.com/about-bargain-finder-max-and-how-it-works · https://developer.sabre.com/multiple-ticket-pricing-and-shopping
- Qantas, vuelos casados: https://agencyconnect.qantas.com/en/policies/book-and-service/married-flights
- IATA, Resolución 830a: https://www.iata.org/en/fmc-documents/2fe5b311-3488-4a1d-be0a-e0175d26bd2e
- Lufthansa Group, política de reservas y emisión (jun 2026): https://cms.airdolomiti.it/wp-content/uploads/2026/06/LHG-Booking-and-Ticketing-Policy-effective-01JUN26.pdf
- Turkish Airlines, stopover: https://turkishairlines.com/en-int/flights/stopover
- The Points Guy, programas de stopover: https://thepointsguy.com/airline/guide-to-airline-stopover-programs/
- Activación de NDC en Sabre: https://atriis.zendesk.com/hc/en-us/articles/13079395670428-Sabre-NDC-activation-guidelines
- Recargo de Lufthansa Group en Sabre: https://www.businesstravelnewseurope.com/TMC-Distribution/Lufthansa-Group-lowers-EDIFACT-surcharge-on-Sabre
- Aeroméxico, Hot Sale y Venta Azul: https://www.aeromexico.com/es_mx/cuando-es-el-hot-sale · https://www.aeromexico.com/es_mx/venta-azul-aeromexico
