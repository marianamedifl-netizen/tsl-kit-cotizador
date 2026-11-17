# Guía Sabre · The Suite Life

Referencia de comandos de Sabre Agency Workspace (srw.sabre.com) para cotizar, armada el 10 nov 2026.
Tiene cuatro partes:
1. Lo **comprobado en vivo** en la cuenta de TSL (PCC 6FK2).
2. Las reglas de Mariana para cotizar hoteles.
3. Tres guías de investigación (hoteles, aéreo y general), hechas solo con fuentes públicas. Lo que no se pudo confirmar dice **sin confirmar**.

> Regla de oro: los formatos que **reservan, emiten, envían o cobran** (`0H…`, `01…`, `E`/`ER`, `W‡…`, `EM…`, `X…`) nunca se usan sin confirmación explícita de Mariana. Todo lo demás es solo consulta.

---

## A. Comprobado en vivo en la cuenta de TSL (10 nov 2026)

| Formato | Resultado |
|---|---|
| `HOTRAK/15MAR-18MAR2` | ✅ Disponibilidad en Marrakech, 2 adultos. La `/` antes de las fechas es obligatoria. |
| `HOTRAK15MAR-18MAR2` (sin `/`) | ❌ "The command you entered is not supported" |
| `HOTRAK¥NEM¥API/15MAR-18MAR2/C-USD/N-MAMOUNIA` | ✅ Funciona. El `¥` se escribe tal cual en la línea de comandos. `/C-USD` convierte a dólares; `/N-` filtra por nombre. En La Mamounia salieron 38 tarifas Virtuoso del código **API** (19 "Tarif Virtuoso …AVI" y 19 "Virtuoso …API") y **ninguna NEM**. |
| `DC¥MAD27297/USD` | ✅ Convierte con el tipo de cambio BSR de Sabre (1 MAD = 0.10253 USD). |
| `DCMAD27297/USD` (sin `¥`) | ❌ "RESTRICTED". El problema era el formato, no un permiso de la cuenta. |
| `HOD1` | ⚠️ Toma el 1 como **Sabre ID** del hotel, no como número de línea, y abrió el Hyatt Regency Tulsa. Para ver una línea de la lista, usa la pantalla gráfica o `HOD*`/`HRD*` + línea (sin confirmar). |

**Ruta gráfica que funciona para ver tarifas:** lanzar `HOT…` → dar clic en la tarjeta del hotel para desplegarla → botón **View Rates** → lista de tarifas.
- **Filtros de la lista:** Room Type, Bed Type, Cancellation Policy, **Client ID** y Currency.
- **Detalle de una tarifa:** desplegar la tarifa → **Rate Details**. Ahí salen los impuestos, la garantía, la política de cancelación, la **comisión** y las amenidades.
- **El botón Book reserva:** no se usa sin confirmar con Mariana.
- **Panel Trip Summary:** si el panel lateral tapa la lista, se cierra con el ícono "Trip Summary" de la barra derecha.

## B. Cómo cotiza hoteles Mariana

- **Formato base:** `HOT<ciudad>¥NEM¥API/<entrada>-<salida><adultos>/C-<moneda>/N-<hotel>`
  - Ejemplo: `HOTRAK¥NEM¥API/02MAR-05MAR2/C-EUR/N-MAMOUNIA`
- **NEM y API** son las tarifas preferenciales de la agencia. Orden de prioridad: **primero NEM, luego API, luego las normales.** Si se necesita separar el origen de cada tarifa, se busca por separado (`¥NEM` solo, `¥API` solo y luego sin código) o se usa el filtro **Client ID**.
- **Tarifas reembolsables**, de la más barata a la más cara.
- **Siempre revisar Rate Details** de la tarifa preferencial: en La Mamounia, la Tarif Virtuoso costaba **igual** que la Best Available Rate e incluía desayuno diario, upgrade sujeto a disponibilidad, early check-in y late check-out, y un crédito de 100 en spa o restaurante.

---



---

# Sabre: formatos de hotel (Content Services for Lodging, CSL) — referencia práctica

Para cotizar hoteles en línea de comandos en Sabre Red 360 y en Sabre Agency Workspace (srw.sabre.com).
Investigado en noviembre de 2026, solo con fuentes públicas (ver "Fuentes"). Todo lo que no encontré en una fuente dice **sin confirmar**.

## Resumen

- En Sabre Red 360 los comandos de hotel "clásicos" (`HOT`, `HOD`, `HRD`, `0H`, `HOM`, `X`) pasan por **CSL**. CSL acepta solo **una parte** de los calificadores antiguos. Si un `HOT`/`HOD` lleva un elemento no soportado, sale un error que explica qué no se soporta, una ayuda con las opciones válidas y un botón para seguir en el formulario gráfico de hotel [F1].
- El formato de la agencia, `HOTCDG¥NEM¥API/02MAR-05MAR2/C-EUR/N-MAMOUNIA`, **coincide con un patrón documentado**: los códigos cliente van pegados a la ciudad, cada uno precedido de `¥`, y después vienen `/fechas+adultos` y los calificadores [F5][F6]. El desglose está en la sección 1.
- **La barra `/` antes de las fechas es obligatoria.** Todas las fuentes escriben `HOT(ciudad)/(entrada)-(salida)(adultos)` [F1][F2][F3]. `HOTRAK15MAR-18MAR2` se sale de la sintaxis documentada, y por eso CSL contesta "command not supported". La única excepción es el `¥`: también separa campos, así que va pegado a la ciudad (`HOTRAK¥NEM/...`).
- **Ojo con el ejemplo:** La Mamounia está en **Marrakech (RAK)**, no en París (CDG). `HOTCDG.../N-MAMOUNIA` probablemente no traerá nada. Lo correcto sería `HOTRAK¥NEM¥API/02MAR-05MAR2/C-EUR/N-MAMOUNIA`.
- **El carácter `¥`:** es la cruz de Lorena (tecla de fin de ítem). Según la fuente aparece como `¥`, `‡`, `#` o `+`. Por ejemplo, `0H1#3` en [F3] y `HOTBOS‡BCD‡WTT` en [F6] son el mismo carácter. En el teclado de Sabre siempre es la misma tecla.

---

## 1. Cómo se lee el formato de la agencia

`HOTCDG¥NEM¥API/02MAR-05MAR2/C-EUR/N-MAMOUNIA`

| Parte | Significado | Fuente |
|---|---|---|
| `HOT` | Búsqueda de disponibilidad de hoteles | [F1][F2] |
| `CDG` | Código de ciudad o aeropuerto. Con un código de aeropuerto la búsqueda se centra en el aeropuerto. Con el de ciudad (`PAR`, `RAK`) se centra en la ciudad | [F2][F4] |
| `¥NEM¥API` | **Client ID** (código de identificación de cliente de la agencia, de la tabla `HIC`) para tarifas **negociadas (N)** o de **contrato/consorcio (X)**. Se pueden encadenar | [F5][F6] |
| `/02MAR-05MAR` | Entrada y salida. También se acepta `02MAR-3NT` (entrada + noches) | [F1][F2] |
| `2` (pegado a la fecha) | Número de adultos, de 1 a 9 y en una sola habitación | [F1][F4] |
| `/C-EUR` | Moneda en que se muestran las tarifas | [F1][F7] |
| `/N-MAMOUNIA` | Nombre de la propiedad. En el sistema clásico, de 3 a 10 caracteres | [F3][F7] |

**Límites de los Client ID**
- **Sistema clásico:** "A maximum of four negotiated and/or contract codes can be combined in one request" [F5]. Es decir, hasta 4 por comando.
- **Formulario gráfico de CSL:** "Request up to 8 Client IDs with Include or Include Only options" [F1][F8].
- **En comando de CSL:** el máximo **sin confirmar**.

**Orden de los Client ID en el comando.** La guía de CSL los escribe *después* de las fechas: `HOTJFK/22DEC-24DEC1/¥IMB` [F1]. La guía de tarifas negociadas y The Travel Institute los escriben *pegados a la ciudad*: `HOTBOS‡BCD‡WTT‡GHL/15MAY-2NT1/RC-ALL/EH,EM` [F5][F6]. La agencia reporta que las dos formas funcionan en su sistema. Que CSL acepte siempre ambas posiciones: **sin confirmar**.

**"Primero NEM, luego API, luego públicas, reembolsables de menor a mayor"**
- **Lo documentado:** en la respuesta de una propiedad, CSL ordena las tarifas por precio, **salvo las negociadas, que salen primero** [F1].
- **Sin confirmar:** que NEM salga antes que API por estar escrito primero en el comando.
- **Sin confirmar:** que exista un calificador de línea de comandos para "solo reembolsables". "Refundable Only" sí existe en el formulario gráfico de búsqueda y de propiedad [F1][F8], y el panel de tarifas se puede filtrar por política de cancelación [F1].
- **Cómo lograr ese orden con lo que sí está documentado:**
  1. Correr el `HOD` de la propiedad con un solo código cada vez: `HOD(id)/02MAR-05MAR2/¥NEM`, después `.../¥API`, después sin código.
  2. Filtrar "Refundable" en el panel gráfico.
- **Tipos de tarifa:** `N` (Negotiated) es para empresas y corporativos. `X` (Contract) es para agencias y consorcios [F5]. Si NEM/API son códigos de consorcio, lo esperable es que sean tipo X (**sin confirmar**, lo define la tabla `HIC` de la agencia).

---

## 2. Disponibilidad y búsqueda (HOT)

### 2.1 Formatos básicos

| Formato | Qué hace | Ejemplo | Fuente |
|---|---|---|---|
| `HOT(ciudad)/(entrada)-(salida)(adultos)` | Busca por ciudad o aeropuerto con fechas | `HOTJFK/22DEC-24DEC1` | [F1] |
| `HOT(ciudad)/(entrada)-(n)NT(adultos)` | Busca por noches en lugar de fecha de salida | `HOTJFK/22DEC-2NT1` | [F1] |
| `HOT(seg)/(salida)(adultos)` | Busca usando el segmento aéreo del PNR | `HOT1/2FEB2` | [F1] |
| `HOT(seg)/(n)NT(adultos)` | Segmento aéreo + noches | `HOT1/3NT2` | [F1] |
| `HOT(ciudad)/(cadena)/N-(nombre)` | Busca sin fechas (lista de propiedades) | `HOTJFK/MC/N-PROPERTY NAME` | [F1] |
| `HOT(ciudad)/.../¥(ClientID)` | Agrega un código cliente (CSL) | `HOTJFK/22DEC-24DEC1/¥IMB` | [F1] |
| `HOT(ciudad)¥(ID)¥(ID)/(fechas)` | Varios códigos cliente, hasta 4 en el sistema clásico | `HOTBOS‡BCD‡WTT‡GHL/15MAY-2NT1/RC-ALL` | [F5][F6] |
| `HOT**` | Vuelve a mostrar la última búsqueda | `HOT**` | [F1][F3] |
| `HOTHELP` | Lista las opciones que CSL soporta en `HOT` | `HOTHELP` | [F1] (en 2020 aparecía como "coming soon" [F2]) |

### 2.2 Calificadores (se agregan con `/`)

En la columna "¿En CSL?", "Sí" significa que aparece en los ejemplos de la guía CSL 22.6 [F1]. "Clásico" significa que solo lo encontré en guías anteriores a CSL, así que en CSL está sin confirmar.

| Calificador | Qué hace | Ejemplo | ¿En CSL? | Fuente |
|---|---|---|---|---|
| `/C-(moneda)` | Moneda de la tarifa | `/C-EUR` | Sí | [F1][F7] |
| `/N-(nombre)` | Nombre de la propiedad | `/N-MAMOUNIA` | Sí | [F1] |
| `/(cadena)` o `/(c1),(c2)` | Una o varias cadenas | `/MC`, `/RT,HY` | Sí | [F1][F9] |
| `/RC-(cat)` | Categoría de tarifa | `/RC-C`, `/RC-ALL` | Sí | [F1] |
| `/RC-N¥(ID)` | Categoría negociada + código cliente | `/RC-N¥IMB` | Sí | [F1] |
| `/D-(distancia)` | Radio | `/D-10` | Sí | [F1] |
| `/PC-(postal)` | Código postal | `/PC-76092` | Sí | [F1] |
| `/A-(texto)` | Palabra de la dirección | `/A-REFORMA` | Clásico | [F7][F6] |
| `/CA-(ciudad)` | Ciudad o zona de la propiedad | `HOTDFW/CA-FRISCO/20AUG-5NT2` | Clásico | [F4] |
| `/PH-(tel)` | Busca por teléfono | `HOTLAX/PH-310-540-0500` | Clásico | [F6] |
| `/D-(dist)(dir)` | Distancia y dirección desde el punto de referencia | `/D-5N` | Clásico | [F4] |
| `/DM-KM` | Distancia en kilómetros | `/DM-KM` | Clásico | [F7] |
| `/*SD` | Ordena por distancia | `HOTGEOC¥.../*SD` | Clásico | [F4] |
| `/G` | Solo propiedades geocodificadas | `/G` | Clásico | [F4][F7] |
| `/SQ-(códigos)` | Amenidades, hasta 3 | `/SQ-POOL,FITN` | Clásico | [F4][F7] |
| `/PT-(tipo)` | Tipo de propiedad | `/PT-RSRT` | Clásico | [F3] |
| `/RT-(programa)` | Programa de clasificación | `/RT-NTM3` | Clásico | [F7] |
| `/R-(monto)` y `/R¥(monto)` | Tarifa máxima y mínima | `/R-200` | **No** (limitación de CSL) | [F1][F3][F7] |
| `/CD-(número)` | Número de descuento corporativo | `/CD-5863ABC` | **No** (limitación de CSL) | [F1][F7] |
| `/ID-(cadena)(número)` | Número de huésped frecuente | `/ID-MC4622853` | **No** (limitación de CSL) | [F1][F7] |
| `/*NR` | Excluye tarifas rack | `/*NR` | Clásico | [F7] |

**Habitaciones y huéspedes**
- El número pegado a la fecha es de **adultos, de 1 a 9, en una habitación** [F4].
- **Niños:** formato de comando **sin confirmar**. La API de CSL sí maneja edades de menores, con un máximo de 9 huéspedes por habitación [F10].
- **Varias habitaciones:** CSL vende **una habitación por comando** [F1].

**Códigos de categoría `RC-`**
- La guía de CSL solo muestra los ejemplos `C`, `N` y `ALL` [F1].
- En el sistema clásico, `C` es corporativa y `P` promocional [F3]. Hay grupos como `GOV`, `MIL` y `ALL` [F7]. `N` es negociada y `X` es contrato [F5].
- La lista completa de categorías de CSL está **sin confirmar**.

### 2.3 Por propiedad, por punto de referencia o por coordenadas

| Formato | Qué hace | Ejemplo | Fuente |
|---|---|---|---|
| `HOD(id)/(entrada)-(salida)(adultos)/¥(ID)/RC-(cat)/C-(mon)` | Disponibilidad de **una propiedad** por su número Sabre (CSL) | `HOD12345/10DEC-5NT1/¥IMB/RC-ALL` | [F1] |
| `HOD(id)¥(ID)¥(ID)/(fechas)` | Una propiedad con varios códigos cliente | `HOD3416‡BCD‡WTT‡GHL/15MAY-1NT1/RC-ALL` | [F6] |
| `HOD12345` | Propiedad sin fechas | `HOD12345` | [F1] |
| `HOD*` / `HODHELP` | Repite la respuesta / lista las opciones de `HOD` | | [F1] |
| `HOT(estado)-(punto)/(fechas)/*SD` | Punto de referencia en EE. UU. | `HOTFL-EPCOT CENTER/20MAY-INT1/RC-ALL` | [F3][F4] |
| `HOTC/(país)-(punto)/...` | Punto de referencia fuera de EE. UU. | `HOTC/FR-LOUVRE/20MAY-INT2/RC-ALL` | [F3] |
| `HCCC/(país)*(letra)` | Lista puntos de referencia por país | `HCCC/FR*E` | [F3][F4] |
| `HOTGEOC¥(lat),(long)/(fechas)/*SD` | Por coordenadas, hasta 4 decimales, con `-` para S/O | | [F4] (clásico) |
| `HOTGEOP¥(id)/(fechas)/*SD` | Propiedades cercanas a otra propiedad | | [F4] (clásico) |
| `HOG(id)` / `HOX(id)` | Puntos de interés cerca de una propiedad / índice de la propiedad | | [F4] (clásico) |

En CSL hay número Sabre clásico y "Global Property Number" [F8]. Qué número acepta `HOD` en comando está **sin confirmar**.

### 2.4 Más resultados y modificar la búsqueda (sistema clásico)

| Formato | Qué hace | Fuente |
|---|---|---|
| `HOT*` | Muestra más resultados | [F3][F9] (en CSL sin confirmar) |
| `HOT*1` | Repite la lista desde la línea 1 | [F3][F4] |
| `HOT/HI,SI,MC` | Cambia a otras cadenas | [F3] |
| `HOT/RC-C` | Cambia la categoría de tarifa | [F3] |
| `HOT/24JUN-27JUN2` | Cambia las fechas | [F3] |
| `HOT¥3` / `HOT-3` | Suma / resta días (hasta 90) | [F3][F4] |
| `HOT/N-X`, `HOT/D-X`, `HOT/PC-X`, `HOT/XX` | Borra el calificador de nombre, distancia, código postal o cadena | [F3] |

---

## 3. Tarifas, habitaciones, reglas y descripción

| Formato | Qué hace | Ejemplo | Fuente |
|---|---|---|---|
| `HOD*(línea)` | Descripción de la propiedad desde la línea de búsqueda | `HOD*1` | [F1] |
| `HRD*(línea)` | **Detalle de la tarifa** desde la respuesta de la propiedad | `HRD*1` | [F1][F4] |
| `HOD¥(seg)` | Descripción desde un segmento de hotel del PNR | `HOD¥3` (aparece como `HOD#3` / `HOD+3`) | [F3][F11] |
| `HOD*G` | Política de garantía y depósito | `HOD*G` | [F3][F4][F9] (clásico) |
| `HOD*/*R` | Solo tarifas, después de un `HOD` | | [F4] (clásico) |
| `HOD*(moneda)` | Muestra las tarifas en otra moneda | `HOD*EUR` | [F3][F4] (clásico) |
| `MD/DIRECTIONS`, `MD/TRANSP` | Cómo llegar y transporte, dentro de la descripción | | [F6] (clásico) |
| `*IH` | Muestra solo los segmentos de hotel del PNR | `*IH` | [F12] |

**Qué incluye el detalle de tarifa en CSL** [F1]
- Cada línea de tarifa muestra la categoría (Promotional, Senior, Net, etc.).
- Al expandir una tarifa se ven los impuestos y cargos.
- El modal "Rate Details" incluye las políticas de **garantía, depósito, cancelación y comisión**, más una sección de detalles adicionales.
- Las tarifas **comisionables** salen en **verde** y las no comisionables en **gris**. La comisión depende de los contratos de la agencia.
- El panel de tarifas se puede filtrar por fuente, política de cancelación, comisionable, tipo de cama y ClientID.

Que `HOD*G` funcione en CSL está **sin confirmar**. En CSL, `HRD*` es la vía documentada para ver las condiciones.

---

## 4. Venta, garantía, modificación, cancelación y pasivos

> **ATENCIÓN: los formatos `0H...` CREAN UNA RESERVA real en el PNR.** Al cerrar con `E`/`ER`/`ET`, se envía al hotel o al agregador. Confirma siempre antes de vender. Esta sección es solo de sintaxis.

### 4.1 Venta y garantía

| Formato | Qué hace | Ejemplo | Fuente |
|---|---|---|---|
| `0H1¥(línea)` | Vende 1 habitación de la línea de tarifa | `0H1¥1` | [F1] |
| `.../G(tarjeta)(número)EXP mm aa-(titular)` | Garantía con tarjeta | `0H1¥1/GVI4444333322221111EXP 10 22-TEST` | [F1] |
| `.../GDPST(tarjeta)(número)EXP mm aa-(titular)` | **Depósito** con tarjeta | `0H1¥1/GDPSTVI4444...EXP 10 22-TEST` | [F1] |
| `.../AGT(número)` | Tipo de garantía con número de agencia (el significado exacto está **sin confirmar**) | `0H1¥1/AGT12345678` | [F1] |
| `.../SI-(texto)` | Información especial | `/SI-TOP FLOOR` | [F1] |
| `.../NM-(n.n)` | Asocia el segmento a un nombre del PNR | `/NM-1.1` | [F9] |
| `.../GSAME` / `.../GDPSTSAME` | Copia la garantía / el depósito del hotel anterior | | [F4] (clásico) |

**Limitaciones de venta en CSL** [F1][F13]
- Una habitación por comando.
- Las tarifas de agregador no aceptan Sabre Virtual Payments.
- Al reservar, CSL exige nombre y apellido del titular de la tarjeta.

### 4.2 Modificar, cancelar y cerrar

| Formato | Qué hace | Ejemplo | Fuente |
|---|---|---|---|
| `HOM(seg)O/(opción)` | Agrega o cambia un dato opcional | `HOM1O/SI-TOP FLOOR REQUEST` | [F1] |
| `HOM(seg)D/(entrada)-(salida)` | Cambia fechas (CSL: solo tarifas GDS y **dentro** del rango original) | `HOM2D/08JAN-12JAN`, `HOM2D/08JAN-6NT` | [F1] |
| `HOM(seg)X/(opción)` | Borra un dato opcional | `HOM3X/CD` | [F4][F11] (clásico) |
| `HOM(seg)R/...` | Cambia habitación o tarifa. **No se soporta en CSL**: hay que cancelar y volver a reservar | | [F1] |
| `X(seg)`, `X1/3/5/`, `X1-3` | Cancela uno o varios segmentos | `X2` | [F1][F9] |
| `XIH` | Cancela todos los segmentos de hotel | `XIH` | [F3][F9] |
| `XI` | Cancela todo el itinerario | `XI` | [F1] |
| `E` / `ER` / `ET` | Cierra y guarda el PNR | | [F1] |
| `I` / `IR` | Ignora los cambios | | [F1] |

Notas:
- Las reservas de **agregador** (Expedia, Booking.com, Bedsonline) solo se modifican cancelando y volviendo a reservar [F1].
- Antes de cancelar, verifica que el segmento tenga número de confirmación. Si no lo tiene, llama al helpdesk del hotel [F4].

### 4.3 Segmento pasivo (hotel reservado fuera de Sabre)

| Formato | Qué hace | Fuente |
|---|---|---|
| `0HHT(cadena)GK(hab)(ciudad)IN(fecha)-OUT(fecha)/(hotel)/(tipo hab)/(tarifa)/SI-(dirección)¥(ciudad, estado, CP)¥FONE(tel)/CF-(confirmación)` | Plantilla de segmento pasivo. Usa `YY` si no aplica cadena | [F14] |
| `0HHTAAGK1CAKIN8DECOUT9DEC/HI-HOLIDAY INN/SGLB /60.00/G/SI-.../CF-123456` | Ejemplo publicado, con caracteres alterados en la fuente | [F11] |

En CSL también existe el botón "Add Passive" en la interfaz [F2].
- **Sin confirmar:** si `IN...-OUT` lleva guion (las fuentes difieren).
- **Sin confirmar:** la puntuación exacta en CSL.
- Antes de usar este formato, pruébalo en un PNR de prueba o con `0HHT HELP` (que exista ese help también está sin confirmar).

---

## 5. Moneda, impuestos y "total aproximado"

| Formato | Qué hace | Ejemplo | Fuente |
|---|---|---|---|
| `/C-(moneda)` en `HOT`/`HOD` | Tarifas en la moneda pedida (CSL) | `HOD12345/10DEC-5NT1/C-USD` | [F1] |
| `HOD*(moneda)` | Convierte la descripción mostrada (clásico) | `HOD*EUR` | [F3][F4] |
| `DC¥(mon)(monto)/(mon)` | Convierte una cantidad entre monedas | `DC¥USD300/CAD` (aparece como `DC#`/`DC+`) | [F15][F11] |
| `DC*(mon)` | Tipo de cambio "Bankers' Buying Rate" de una moneda | `DC*EUR` | [F15] |
| `DC*CUR` | Lista de códigos de moneda | `DC*CUR` | [F15] |

**Cómo muestra CSL la moneda y los totales**
- Sin `/C-`, la moneda la define la configuración **TJR** del PCC. Con `/C-`, o después de una conversión por TJR, aparece un selector para cambiar de moneda [F1].
- Las confirmaciones de agregador muestran la **tarifa por noche y un "approximate total amount"** [F1].
- Un ícono de **"+ cargos / + impuestos"** significa que hay cargos **no incluidos** en el total. Esto se debe aclarar al cliente: el total puede no incluir impuestos locales, como la tasa turística [F1].
- La API muestra "Total Amount" y "Average Nightly Rate", antes y después de impuestos [F16].
- Para cotizar al cliente, toma siempre el desglose de impuestos que sale al expandir la tarifa o en `HRD*` [F1].

---

## 6. Mensajes de error frecuentes

| Mensaje | Qué significa | Fuente |
|---|---|---|
| Error de comando no soportado (en esta agencia: "command not supported") | Un `HOT`/`HOD` con un elemento que CSL no acepta, o fuera de la sintaxis. Ejemplo: `HOTRAK15MAR-18MAR2` sin `/` antes de la fecha. La pantalla ofrece ayuda y un botón al formulario gráfico. Sabre no publica el texto exacto | [F1] |
| `¥CATEGORY CODE DOES NOT MATCH THOSE IN TABLE¥` / `¥CHECK RATE CODE¥` | La categoría del código cliente en la tabla `HIC` no coincide con la que cargó el hotel, o el hotel no ha creado ese código | [F5] |
| `¥PROPERTY NOT AVAILABLE FOR DATES REQUESTED¥` | El hotel no ofrece esa tarifa o código en esas fechas, o está lleno | [F5] |

**Errores de la API CSL** [F10]. Son útiles para entender respuestas parecidas en pantalla; que la línea de comandos use exactamente el mismo texto está **sin confirmar**.

| Error | Significado |
|---|---|
| 0404 | Combinación de fechas inválida |
| 0414 | Entrada a más de 330 días |
| 5024 | Más de 9 huéspedes por habitación |
| 0852 | Edad de menores inválida |
| 0061 | Moneda inválida |
| 0322 | Sin disponibilidad |
| 0424 | No hay hoteles con esos datos |
| 0392 | Código de hotel inválido o inactivo |
| 5262 | No hay tarifas para la combinación pedida |
| 5300 | Tarifas negociadas o de contrato no válidas para el PCC |
| 5275 | Agregador deshabilitado en el PCC |
| 0790 | Nada en ese punto de referencia o distancia |

**Si un código cliente (NEM/API) no aparece**, revisa en este orden [F5]:
1. `HIC*ALL`: confirma que el código existe y que su categoría (N o X) es correcta.
2. `W/HV*`: confirma que el PCC principal abrió la visibilidad.
3. Prueba con `HOT(ciudad)/(fechas)/RC-(X o N)¥(código)`.
4. Si sigue sin aparecer, pídele al hotel que confirme que la tarifa está cargada.

---

## 7. Plantillas sugeridas para la agencia

Están armadas solo con piezas documentadas. Valida cada una una vez en el sistema.

| Objetivo | Formato |
|---|---|
| Búsqueda en ciudad con códigos preferentes | `HOTRAK¥NEM¥API/02MAR-05MAR2/C-EUR` |
| Una propiedad por nombre | `HOTRAK¥NEM¥API/02MAR-05MAR2/C-EUR/N-MAMOUNIA` |
| Una propiedad por número, solo NEM | `HOD(id)/02MAR-05MAR2/¥NEM/C-EUR` |
| Luego solo API | `HOD(id)/02MAR-05MAR2/¥API/C-EUR` |
| Luego tarifas públicas | `HOD(id)/02MAR-05MAR2/RC-ALL/C-EUR` |
| Detalle, cancelación y comisión de la línea 3 | `HRD*3` |

---

## Fuentes

- [F1] Sabre, *Content Services for Lodging in Sabre Red 360, v22.6* (oct. 2022): https://airts.ru/upload/Manuals_and_Installers/Manuals/Practice_manuals/ContentServices_for_Lodging_October2022.pdf
- [F2] Sabre, *Content Services for Lodging in Sabre Red 360, v20.10* (nov. 2020): https://airts.ru/upload/Manuals_and_Installers/Manuals/Practice_manuals/ContentServices_for_Lodging_November2020.pdf
- [F3] GDS Help, *Sabre Quick Reference Guide CH7 – Hotel Booking*: https://gdshelp.blogspot.com/2020/04/sabre-quick-reference-guide-ch7-hotel.html
- [F4] Sabre, *Sabre Hotels – Search Techniques… Student Guide* (ed. 1.2, 2013): https://silo.tips/download/sabre-hotels-search-techniques-to-find-the-right-property-fast-student-guide
- [F5] Travel Leaders, *Hotel Negotiated Rates Quick Reference (Sabre troubleshooting tips)*: https://ebooks.hotels.travelleadersgroup.com/wp-content/uploads/2014/08/SABRE-troubleshooting-tips.pdf
- [F6] The Travel Institute, *Sabre Shortcuts* (2016): https://www.thetravelinstitute.com/2016/04/17/sabre-shortcuts/
- [F7] Sabre, *Hotel Availability Qualifiers* (copia en Yumpu): https://www.yumpu.com/en/document/view/42427196/en-hotel-availability-qualifiers-sabre-holdings
- [F8] WorldVia Helpdesk, *Sabre Red 360 – CSL – Hotel Shopping*: https://helpdesk.worldvia.com/support/solutions/articles/8000101126-sabre-red-360-csl-hotel-shopping
- [F9] Sabre Travel Network Indonesia, *Cue card*: https://www.sabretn.co.id/wp-content/uploads/2016/03/Cue-card.pdf
- [F10] Sabre Dev Studio, *Get Hotel List – errors*: https://developer.sabre.com/docs/soap_apis/hotel/search/get_hotel_list/errors
- [F11] Travelport, *GDS Format Comparison (mar. 2025, columna Sabre)*: https://support.travelport.com/webhelp/Formats/Content/Resources/MiniGuide/GDSCompareWord-11Mar2025.pdf
- [F12] Sabre, *Working in the Sabre System – Training Workbook 2.7*: https://portal.sabreng.com/files/resources/files/1454080752_1454080752_basic_reservation_course.pdf
- [F13] Sabre Dev Studio, *Enhanced Hotel Book – Legacy to CSL migration guide*: https://developer.sabre.com/enhanced-hotel-book-legacy-hotel-content-services-lodging-csl-migration-guide
- [F14] Trams/TRES Help, *PF Key para hoteles pasivos (Sabre)*: https://trestechnologieshelp.zendesk.com/hc/en-us/articles/31542864857747
- [F15] GDS Help, *Sabre Quick Reference Guide CH1 – Miscellaneous*: https://gdshelp.blogspot.com/2020/04/sabre-quick-reference-guide-ch1.html
- [F16] Sabre, *Virtual Developer Bench – CSL*: https://developer.sabre.com/sites/default/files/inline-files/Virtual%20Developer%20Bench_MAY_CSL_external.pdf ; *Get Hotel Avail release notes*: https://developer.sabre.com/docs/soap_apis/hotel/search/get_hotel_avail/release-notes

No pude consultar el Format Finder de Sabre ni Agency eServices: requieren iniciar sesión. Lo que aquí dice **sin confirmar** conviene verificarlo con `HOTHELP` / `HODHELP` dentro del sistema o con Format Finder.


---

# Sabre – Referencia de formatos AÉREOS (The Suite Life)

Referencia práctica para cotizar vuelos en Sabre Red 360 / Sabre Agency Workspace (línea de comandos), con foco en
clientes de lujo que salen de MEX: pocas escalas, buenos horarios y la tarifa más baja razonable, a menudo en Business.

## Resumen

- **Disponibilidad:** `1` + fecha + par de ciudades (+ hora, conexión, `‡`aerolínea, `-`clase, `//BB` cabina, `/D` solo directos).
- **Tarifa más baja sin rebook:** `WPNC` (lo disponible) y `WPNCS` (lo más bajo aunque no haya espacio). `WPNCB` **sí re-reserva** las clases.
- **Alternativas de itinerario:** `WPNI` toma el itinerario reservado y busca opciones más baratas. `JR.` hace una búsqueda
  de tarifa baja por fechas y ciudades, sin PNR (es el equivalente en host de Bargain Finder Max).
- **Cabina en pricing:** `¥TC-BB` (Business), `¥TC-FB` (First), `¥TC-YB` (Economy). Solo lo confirma una fuente de capacitación; ver §2.
- **Tarifas y reglas:** `FQ` muestra la tarifa y `RD<línea>*M` el menú de reglas (`RD1*16` = penalidades, por patrón).
  Para cotizar equipaje y extras: `WPAE` / `WP*AE-BG`.
- **PNR:** nombre `-`, teléfono `9`, ticketing `7TAW…/`, recibido de `6`, cierre `E`/`ER`.
  **Todo lo que vende, cancela, re-reserva, guarda PQ o emite boleto modifica la reserva.** La columna "¿Modifica reserva?" lo marca.
- **Separadores:** las fuentes escriben la "cruz de Lorena" como `‡` o `¥`, y la "tecla de cambio" como `¤`. Son el mismo carácter
  según cómo se renderiza el teclado. Qué tecla física los produce en Agency Workspace web está **sin confirmar**;
  revisa la ayuda del teclado en SRW.
- Varias fuentes son de Abacus (Sabre Asia) o tienen años. Algunas sintaxis pueden variar según la PCC o la región:
  prueba siempre en una consulta (display) antes de vender.

Leyenda de la columna **¿Modifica reserva?**
- **No**: solo muestra información.
- **Sí (PNR)**: modifica o crea el PNR. Puede vender espacio con la aerolínea.
- **Sí (re-reserva)**: cambia clases o segmentos.
- **⚠ IRREVERSIBLE / COSTO**: emite boletos o EMD, o genera cargos. Confírmalo con Mariana antes.

---

## 1. Disponibilidad, horarios, retorno, más disponibilidad

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `1<fecha><orig><dest>` | Disponibilidad básica por par de ciudades | `115DECMEXMAD` (patrón `121NOVSANSFO`) | No |
| `1<fecha><orig><dest><hora>` | Con hora de salida deseada | `110MARLCAATH0900` | No |
| `1<fecha><orig><dest>/<hora>` | Por hora de **llegada** | `110MARLCAATH/1400` | No |
| `1<fecha><orig><dest><hora><conexión>` | Forzar el punto de conexión | `128APRLHRSYD0900BKK`; cambiar después con `1SIN` | No |
| `1<fecha><orig><dest>‡<aerolínea>` | Filtrar por aerolínea | `112JULLHRSIN‡BA`; luego `1‡QF` o `1‡ALL` | No |
| `1<fecha><orig><dest><hora>-<clase>` | Filtrar por clase de reserva | `124AUGLHRJFK1200-Y`; luego `1-F` | No |
| `1<fecha><orig><dest>‡<aer>//<cabina>` | Filtrar por cabina: `YB` económica, `SB` premium economy, `BB` business, `FB` first | `113NOVLHRDXB‡BA//BB` | No |
| `1<fecha><orig><dest>/D` | **Solo vuelos directos o sin escala** | `120MAYLHRDEL/D`; seguimiento `1/D` | No |
| `1*` | Más disponibilidad (siguiente pantalla) | `1*` (también `MD` para bajar) | No |
| `1*R` / `1*OA` | Volver a mostrar la última / la disponibilidad original | `1*OA` | No |
| `1*<hora>` / `1<fecha>` | Cambiar hora o fecha sobre la última consulta | `1*1900`, `117JAN` | No |
| `1‡<n>` / `1-<n>` | Mover la fecha n días adelante o atrás | `1‡1`, `1-3` | No |
| `1*D<ciudad>` / `1*A<ciudad>` | Cambiar origen / destino | `1*DMAN`, `1*AFRA` | No |
| `1R` / `1R<fecha><hora>` | Disponibilidad de regreso | `1R`, `1R12FEB2100`, `1R‡14`, `1R-4` | No |
| `S<fecha><orig><dest>/ES` | Horarios extendidos (schedule) | `S10MARLCALHR/ES` (`‡CY` agrega aerolínea) | No |
| `T*CT-<ciudad>` | Tiempos mínimos de conexión de una ciudad | `T*CT-JFK`; `T*CT-SIN/BG` (por aerolínea) | No |
| `VI` | Tiempo de viaje (journey time) | `VI` | No |

Notas:
- La clase en availability (`-Y`) y la cabina (`//BB`) están confirmadas en fuentes independientes. Un ejemplo de clue card
  de Lufthansa usa `¤LH` para aerolínea (`104NOVSYDATH¤LH`), que probablemente es otra representación del mismo separador.
- Ejemplo típico para TSL: `115DECMEXMAD1000‡IB//BB`, que combina hora, aerolínea y cabina por patrón.
  La combinación exacta de los tres calificadores **sin confirmar**; pruébala.

## 2. Búsqueda de tarifa baja / shopping

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `WP` | Cotiza el itinerario tal como está reservado | `WP` | No (solo display) |
| `WPNC` | Tarifa más baja **disponible**, sin re-reservar | `WPNC` | No |
| `WPNCS` | Tarifa más baja posible **aunque no haya disponibilidad** | `WPNCS` | No |
| `WPNCB` | Tarifa más baja disponible **y re-reserva** las clases | `WPNCB` | **Sí (re-reserva)** |
| `WPNI` | Bargain Finder Plus: sobre el itinerario reservado muestra itinerarios alternos más baratos | `WPNI`, `WPNI/AAC`, `WPNI/ALX` | No (hasta vender una opción) |
| `WPNI/A<aer>¥BRALL` | Alternativas con varias marcas tarifarias | `WPNI/AAC¥BRALL` | No |
| `JR.<orig>/S-OY<dest><fecha><aer>/…` | Búsqueda de tarifa baja sin PNR (por fechas, ciudades y pasajeros) | `JR.SIN/S-OYLON20APRLH/S-OYSIN27APRLH/BRALL` | No |
| `JR.…/P-<pax>` | JR con tipos de pasajero | `JR.DAC/S-OYLON15APR/S-OYDAC20APR/P-2ADT1C091INF` | No |
| `JR<n>*BR…` | Seguimiento: detalle de marcas de la opción n | `JRxx*BRALL`, `JRxx*BRx/x/x` | No |
| `WPNCB ¥TC-BB` | Más bajo en **Business** (re-reserva) | `WPNCB¥TC-BB` | **Sí (re-reserva)** |
| `WPNCB ¥TC-FB` / `¥TC-YB` | Más bajo en First / Economy | `WPNCB¥TC-FB` | **Sí (re-reserva)** |
| `WPNC¥TC-BB` | Lo mismo sin re-reservar | **sin confirmar** (por analogía) | No |
| `¥TC-SB` | Premium Economy en pricing | **sin confirmar** (`SB` = premium solo está confirmado en availability) | — |
| `WPQF` | Cotiza en una cabina o clase específica (F) | `WPQF` | No |
| `WPNC¥BR<marca>` / `WPBR<marca>` | Cotiza una marca tarifaria (fare family) | `WPNC¥BRECOFLEX`, `WPBRFL`, `WPC-LH¥ALH¥BRBUSFLEX` | No (`WPNCB¥BR…` sí re-reserva) |
| `WPNC¥MPC-ANY` | Excluye tarifas sin cambios (p. ej. Basic Economy de AA) | `WPNC¥MPC-ANY` | No |
| `WPNCB‡MPR-0` / `WPNCB‡MPC-0` | Más bajo **reembolsable** / **cambiable sin penalidad** | `WPNCB‡MPR-0` | **Sí (re-reserva)** |
| `WPXP` / `WPXR` | Sin penalidades / sin restricciones | `WPXR` | No |
| `WPS<segs>` | Cotiza solo algunos segmentos | `WPS1/3-7`, `WPS1/2` | No |
| `WPN<n.n>` | Cotiza solo un pasajero | `WPN1.1` | No |
| `WPA<aer>` | Fuerza la aerolínea validadora | `WPAAM`, `WPABA‡PITX` | No |
| `WPQ<fare basis>` / `WPS1*Q…¥S2*Q…` | Fuerza el fare basis (total o por segmento) | `WPS1*QL0C4TG¥S2*QL0C4FL` | No |
| `WPX<seg>` / `WPO<seg>` | Indica conexión / escala (stopover) en un segmento | `WPX2`, `WPO2` | No |
| `WPB<fecha>` | Cotiza a una fecha pasada o futura (como si se hubiera reservado ese día) | `WPB01JAN16` | No |
| `WPQ//DP<n>` / `WPQ//DA<n>` | Descuento por % / por monto | `WPQ//DP10` | No |
| `WPAC*<código>` / `WPI<corp ID>` | Tarifas privadas por account code / corporate ID | `WPAC*ABC123¥XC` | No |
| `WPA` / `WP<n>` | Varias opciones de tarifa para el itinerario reservado / ver la opción n | `WPA`, `WP2` | No |

Tipos de pasajero (calificador `P`)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `WPP<ptc>` | Cotiza por tipo de pasajero | `WPPCNN` (niño), `WPPINF` (infante sin asiento), `WPPINS` (infante con asiento) | No |
| `WPPC<edad>` | Niño con edad | `WPPC7` | No |
| `WPP1ADT¥AE` | Adulto, con Air Extras | `WPP1ADT¥AE` | No |
| `WPP2ADT/1CNN` | Combinar varios PTC en una entrada | **sin confirmar** (patrón no visto textual) | — |

**Moneda en pricing** (p. ej. `WPM…` o `¥MUSD`): **sin confirmar**. No se encontró en fuentes públicas.
Para convertir, usa `DC` (§5).

## 3. Fare Quote (FQ), reglas, equipaje, historial de tarifa

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `FQ<orig><dest><fecha>-<aer>` | Fare display de una aerolínea en una fecha | `FQMEXMAD15DEC-IB` (patrón `FQYYZYVR14MAR-AC`) | No |
| `FQ<orig><dest>` | Sin aerolínea, todas | `FQJKTSIN` | No |
| `FQ…-<aer>-<aer>` | Varias aerolíneas | `FQ SINLAX-SQ-CX-CI` | No |
| `FQ…¥P<ptc>` | Por tipo de pasajero | `FQLONMCO01JAN¥PITX-BA` | No |
| `FQ…-<aer>¥B<clase>` | Por clase de reserva | `FQBNEBCN-LH¥BP` | No |
| `FQ<orig><dest>JB-<aer>` | "Fare quote by cabin" según la clue card de Lufthansa | `FQMELLISJB-OS` (significado exacto de `JB` **sin confirmar**) | No |
| `FQ…‡AC*<código>` / `‡UI<corp>` / `‡PV` | Tarifas privadas | `FQBNESYD15OCT‡AC*{code}-VA` | No |
| `FQ…/ACX/FF` y follow-ups `FQ*:BF<n>` | Marcas tarifarias (ejemplo de Cathay; mezcla varios GDS) | **sin confirmar para Sabre** | No |
| `FQ*<fecha>` / `FQ*-<aer>` / `FQ*¥OW` | Seguimientos: cambiar fecha, aerolínea, solo ida | `FQ*17JUN`, `FQ*-DL`, `FQ*¥BY` | No |
| `FQ¤` / `FQ¤ R` | Mismo par y aerolínea / dirección inversa | `FQ¤ R` | No |
| `FQD*` | Volver a mostrar el fare quote anterior | `FQD*` | No |
| `FQ<fecha pasada><orig><dest><fecha viaje>-<aer>` | **Historial**: tarifa vigente en una fecha pasada (incluye el año) | `FQ10JAN07JKTSIN15JAN07-GA`; `FQ30MAY18LHRDXB13NOV18-BA` | No |
| `RD<línea>*M` | Menú de reglas de la línea del FQ | `RD1*M` | No |
| `RD<línea>*<cat>` | Regla por categoría ATPCO (5 = anticipación/emisión, 19 = niños, 50 = marca) | `RD1*5`, `RD1*4/5/26`, `RD2*50`; penalidades `RD1*16` (por patrón) | No |
| `RD<fare basis completo>` | Reglas por fare basis | `RDJKTSIN10DECYEE1M-GA` | No |
| `RD<línea>*RTG` / `RD<línea>*IC` | Ruteo / construcción de la tarifa | `RD3*RTG` | No |
| `RB<línea>` | Clases alternas (RBD) de la tarifa | `RB1` | No |
| `RD*1` | Todas las reglas de la línea 1 | `RD*1` | No |
| `WP*RULES` | Reglas desde el pricing | **sin confirmar** | — |
| `WPDF` | Desglose de tarifa e impuestos del pricing (Abacus) | `WPDF`, `WPDF1` | No |
| `WPAE` | Cotiza y muestra **todos** los Air Extras (equipaje, asientos, comidas…) | `WPAE` | No |
| `WP*AE` / `WP*AE-BG` | Seguimiento: Air Extras / solo equipaje (`BG`) | `WP*AE-BG/ML/IE` | No |
| `WPP1ADT¥AE-BG¥FFS-<aer><nivel>` | Equipaje con estatus de viajero frecuente | `WPP1ADT¥AE-BG/ML¥FFS-XX2/YY7` | No |
| Franquicia de equipaje dentro del `WP` | La franquicia aparece en la respuesta del pricing | Formato dedicado de display **sin confirmar** | — |
| `*AE` | Air Extras del PNR (incluye montos de asiento) | `*AE` | No |

Códigos AE: `BG` equipaje, `ML` comida, `SA` asiento, `IE` entretenimiento, `LG` lounge, `UN` menor no acompañado, `PT` mascotas, `MD` médico, `GT` transporte terrestre.
El calificador AE **no** funciona con `WPA`, `WD`, `WPNET` ni `WQ` (da error de formato).
Rango de fechas del FQ (fuente Abacus): hasta 500 días en el pasado (con año) y 366 días en el futuro.

## 4. Vender, construir el PNR, asientos, SSR/OSI, recuperar

### 4.1 Vender y cancelar segmentos

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `0<pax><clase><línea>` | Vende desde disponibilidad | `01Y2` (1 asiento Y de la línea 2), `02J1` | **Sí (PNR)**, toma espacio |
| `0<pax><clase><línea>*` | Vende una conexión en la misma clase | `01K1*`, `01Y1*` | **Sí (PNR)** |
| `0<pax><cl><lín><cl><lín>` | Conexión con clases distintas | `01L1K2`, `02Y1Y2` | **Sí (PNR)** |
| `0<pax><cl><lín>LL` | Lista de espera | `01V2LL` | **Sí (PNR)** |
| `0<aer><vuelo><cl><fecha><orig><dest>NN<n>` | Venta larga (long sell) | `0BA11J24JANLHRSINNN2` | **Sí (PNR)** |
| `0…GK` / `01J3AK¥<loc>` | Segmento pasivo | `01Y1GK` | **Sí (PNR)**. Ojo con las políticas de la aerolínea |
| `X<seg>` / `X1-3` / `X2/4` / `XI` / `XIA` | Cancela segmento(s) / todo / solo aéreo | `X2`, `XI` | **Sí (PNR)**, libera espacio |
| `X<seg>‡0<n><cl><lín>` / `X1‡00<fecha>` | Cancela y vende otro / mismo vuelo en otra fecha | `X1‡02Y1`, `X1‡0019JUN` | **Sí (PNR)** |
| `WC<seg><clase>` | Cambia la clase de un segmento | `WC1Y/2Y` | **Sí (re-reserva)** |
| `.<seg>HK` | Cambia estatus (p. ej. TK→HK tras cambio de horario) | `.3HK` | **Sí (PNR)** |
| `/<seg>` / `/1/3` | Inserta después de un segmento / mueve segmentos | `/2`, `/1/6` | **Sí (PNR)** |

### 4.2 Campos del PNR (obligatorios: nombre, teléfono, recibido de, itinerario, ticketing)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `-APELLIDO/NOMBRE TRAT` | Nombre | `-MEDINA/ANA MRS`; varios `-2SMITH/JOHN MR/ANNE MRS` | Sí (PNR) |
| `-I/APELLIDO/NOMBRE` + `3INFT/…/<fnac>-1.1` | Infante sin asiento + SSR ligado al adulto | `-I/SMITH/EMILY MISS`; `3INFT/SMITH/EMILY MISS/01OCT17-1.1` | Sí (PNR) |
| `-<n>¤<nuevo nombre>` / `-<n>¤` | Cambia / borra un nombre | `-1¤JENSEN/KURT MR` | Sí (PNR) |
| `9<teléfono>-<tipo>` | Teléfono (A agencia, B negocio, H casa, M móvil) | `90181-577-4670-A` | Sí (PNR) |
| `PE‡<email>‡` | Correo electrónico | `PE‡JUAN@EJEMPLO.COM‡` | Sí (PNR) |
| `7TAW<fecha>/` | Límite de emisión (coloca el PNR en la cola de ticketing) | `7TAW15DEC/` | Sí (PNR). **No** emite boleto |
| `7T-A` | Marca como ya emitido / sin límite | `7T-A` | Sí (PNR) |
| `6<nombre>` | Recibido de | `6MARIANA` | Sí (PNR) |
| `5<texto>` / `5H-` / `5‡` / `5.` | Observaciones: general / historial / itinerario / factura | `5 CLIENTE VIP` | Sí (PNR) |
| `FF<aer><número>` | Viajero frecuente | `FFAM123456789-1.1` | Sí (PNR) |
| `E` | **Cierra y guarda** el PNR (genera el localizador) | `E` | **Sí: confirma la reserva** |
| `ER` | Cierra y vuelve a mostrar | `ER` | **Sí** |
| `EM` | Cierra y envía el itinerario por correo al `PE‡` | `EM` | **Sí + envía al cliente** ⚠ |
| `I` / `IR` | Ignora los cambios / ignora y recupera el PNR | `IR` | No (descarta) |
| `WPRQ` / `PQ` | Guarda la tarifa como Price Quote (PQ record) | `WPRQ`, `WPBRFL¥RQ`, `WPNCB¥BRFL¥RQ` | Sí (PNR) |
| `PQD-ALL` / `PQD1` | Borra PQ(s) | `PQD1` | Sí (PNR) |
| `W‡…` / `W¥PQ…` | **Emisión de boleto** | `W¥PQ1N1.1` (Abacus) | **⚠ IRREVERSIBLE / COSTO** |
| `AE¥1A1` + `W¥EMD*AE1¥F<fop>` | Vende un Air Extra y emite EMD | `W¥EMD*AE1¥FCASH` | **⚠ IRREVERSIBLE / COSTO** |

### 4.3 Asientos

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `4G<seg>*` | Mapa de asientos del segmento | `4G1*` (`MD`/`MU` para desplazarse) | No |
| `4G<seg>/<asiento>-<pax>` | Asigna un asiento | `4G1/10B-2`, `4G2/32AB-1.1` | Sí (PNR). Puede tener costo (asientos de pago, EMD) |
| `4GA/<asiento>` / `4GA/NW` / `4GA/NA` | En todos los segmentos / ventana / pasillo | `4GA/NA` | Sí (PNR) |
| `4GX<seg>` / `4GXALL` | Cancela asiento(s) | `4GXALL` | Sí (PNR) |
| `*B` | Muestra los asientos asignados | `*B` | No |

### 4.4 SSR / OSI

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `3<SSR>` / `3<SSR>-<pax>` | Servicio especial (silla de ruedas, comida, mascota) | `3WCHR`, `3VGML1`, `ZZSRVGML/S4/P1` (BA) | Sí (PNR), se envía a la aerolínea |
| `3DOCS/…` | Datos APIS / Secure Flight | `3DOCS/DB/20NOV50/M/SMITH/LUKE-1.1` | Sí (PNR) |
| `3CTCM1/<tel>-1.1` / `3CTCE1/<email>-1.1` | Contacto IATA del pasajero (`//` = @) | `3CTCE1/BOB.SMITH//AOL.COM-1.1` | Sí (PNR) |
| `3OSI <aer> <texto>` | Información (OSI) a la aerolínea | `3OSI AM VIP CLIENTE FRECUENTE` | Sí (PNR) |
| `3EXST/…` + `-<n>APELLIDO/NOMBRE/EXST` | Asiento extra de confort | `3EXST/REQUIRED FOR PERSONAL COMFORT-2.1` | Sí (PNR) |

Nota: la fuente de 2008 indica el prefijo `4` en lugar de `3` para American Airlines.

### 4.5 Recuperar y mostrar

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `*<localizador>` | Recupera por localizador | `*ABCDEF` | No |
| `*-<apellido>` / `*-<apellido>/<nombre>` | Por apellido | `*-PERKINS/BRON` | No |
| `*<aer><vuelo>/<fecha>-<apellido>` | Por vuelo, fecha y apellido | `*AA81/5JUN-MCMILLER` | No |
| `*A` / `*I` / `*N` | PNR completo / itinerario / nombres | `*A` | No |
| `*P9` / `*P6` / `*P5` / `*T` | Teléfonos / recibido / observaciones / ticketing | `*P9` | No |
| `*H` / `*HIA` | Historial / historial solo aéreo | `*HIA` | No |
| `*PQ` / `*PQS` | Price Quotes guardados (detalle / resumen) | `*PQS` | No |
| `*IM` | Mensajes direct connect de la aerolínea | `*IM` | No |
| `*L` | Lista de nombres similares | `*L` | No |

## 5. Codificar / decodificar, info de vuelo, hora, moneda

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `W/*<código>` | Decodifica ciudad, aeropuerto o aerolínea | `W/*MEX`, `W/*AM` | No |
| `W/-CC<nombre>` | Codifica ciudad | `W/-CCMEXICO CITY` | No |
| `W/-AP<nombre>` | Codifica aeropuerto | `W/-APBARAJAS` | No |
| `W/-AL<nombre>` | Codifica aerolínea | `W/-ALAEROMEXICO` | No |
| `W/EQ*<código>` / `W/EQ-<nombre>` | Decodifica / codifica equipo (avión) | `W/EQ*789` | No |
| `HCCC/<país>` / `HCCC/<código>` | Codifica / decodifica país | `HCCC/MX` | No |
| `DU*/MLS` | Tabla de códigos de comida | `DU*/MLS` | No |
| `W/-CY<ciudad>, <país>` | Los 10 aeropuertos más cercanos | `W/-CYMANCHESTER, GB` | No |
| `2<aer><vuelo>/<fecha>` | Información del vuelo (flifo) | `2UA123/11APR` | No |
| `V*<aer><vuelo>/<fecha>` | Verifica los detalles de un vuelo | `V*CX228/10MAY` | No |
| `VA*<línea>` / `VI*` / `VI*<seg>` | Detalle de una línea de disponibilidad / del itinerario (equipo, escalas, servicio) | `VA*1`, `VI*` | No |
| `VCT*1/2` | Verifica la conexión mínima entre segmentos | `VCT*1/2` | No |
| `T*<ciudad>` | Hora local de una ciudad | `T*MAD` | No |
| `T¤<cálculo>` | Calculadora de fechas y horas | `T¤12JUN‡3` | No |
| `DC¥<moneda><monto>/<moneda>` | Convierte moneda | `DC¥USD1000/MXN` (patrón `DC¥BDT31000/USD`) | No |
| `DC*<moneda>/<fecha>` / `DC*<país>/<moneda>` | Tipo de cambio histórico / por país | `DC*SGD/16SEP02` | No |
| `DC*<código>` / `DC*<nombre>/C` | Decodifica / codifica moneda | `DC*MXN` | No |
| `FC*<moneda>` | Tipo de cambio IATA (ROE) | `FC*THB` | No |
| `TXN*<país>` | Códigos de impuestos de un país | `TXN*MX` | No |

## 6. Mensajes de error y respuestas comunes

| Mensaje | Significado | Qué hacer |
|---|---|---|
| `NEED PHONE FIELD - USE 9` | Falta el teléfono | Agrega `9…` y vuelve a cerrar con `E` |
| `NEED TICKETING/TIMELIMIT - USE 7 OR 8` | Falta el campo de ticketing | `7TAW<fecha>/` o `7T-A` |
| `TIME LIMIT IS PRIOR TO CURRENT TIME - MODIFY AND REENTER` | El límite de emisión ya pasó | Cámbialo a hoy o a una fecha futura |
| `TICKET/TIMELIMIT MUST PRECEDE TRAVEL DATE-UPDATE TICKET FIELD` | El límite cae después de la salida | Pon una fecha anterior a la salida o `7T-A` |
| `INCORRECT TIME LIMIT - VERIFY *PQ DATE` | El límite no cuadra con la fecha de compra del PQ | Revisa `*PQ`, borra y vuelve a cotizar |
| `ITINERARY REQUIRED TO COMPLETE TRANSACTION` | El PNR no tiene segmentos | Vende un segmento (o agrega un OTH) |
| `SEGMENTS NOT IN DATE ORDER - VERIFY AND REENTER` | Segmentos fuera de orden | Revisa con `VI*` y reordena con `/x/y` |
| `PQ REQUIRED BEFORE END TRANSACTION` | La PCC exige un Price Quote | `WPRQ` antes de `E` |
| `DIRECT CONNECT MESSAGES RECEIVED - ENTER *A OR *IM` | La aerolínea envió mensajes | `*IM` y luego `E` |
| `INFANT DETAILS REQUIRED IN SSR - ENTER 3INFT/...` | Falta el SSR del infante | `3INFT/APELLIDO/NOMBRE/<fnac>-1.1` |
| `NUMBER OF SEATS DOES NOT EQUAL NUMBER IN PARTY FOR SEGMENT` | Los asientos no cuadran con el número de pasajeros | Revisa `*B` y los asientos pendientes |
| `PSGR NOT ELIGIBLE FOR P SEATS-CXL AND SELECT NEW SEAT` | El pasajero no puede tener ese asiento premium | `4GX…` y elige otro |
| `NEED CUSTOMER NUMBER - USE DK` | La PCC exige número de cliente (DK) | Agrega el DK |
| Error de formato con AE | `¥AE` usado con `WPA`/`WD`/`WPNET`/`WQ` | Usa `WP`/`WPNC` con AE |
| `SEG NN`, `SEG 2 KK`, `PNR FILED`, `NO HIST`, `END OF DISPLAY FOR REQUESTED DATA` | Respuestas normales del sistema | Informativas |
| `NEED RECEIVED FROM…`, `SIMULTANEOUS CHANGES TO PNR…`, `NO COMBINABLE FARES FOR CLASS USED` | Se citan con frecuencia | **Texto exacto sin confirmar** en fuentes públicas. Para cambios simultáneos, la práctica habitual es `IR` |

Estatus de segmento: `HK` confirmado, `KK` confirmado por la aerolínea, `TK` cambio de horario,
`UN`/`NO` no operado o rechazado, `HL` lista de espera, `HX` cancelado por la aerolínea, `GK` pasivo.

---

## Flujo sugerido para una cotización Business desde MEX (solo display, sin reservar)

1. `115DECMEXMAD/D` para ver directos, y luego `1*`, `1‡IB` o `1‡AM` con `//BB` para Business.
2. `FQMEXMAD15DEC-IB` → `RD1*M` / `RD1*16` → tarifas, reglas y penalidades.
3. Si ya hay un itinerario en PNR de trabajo: `WPNC` (y `WPNCS` como referencia) → `WPNI` para alternativas → `WPAE` para equipaje.
4. Solo con la aprobación de Mariana: vender (`0…`), cerrar (`E`), guardar PQ (`WPRQ`). **Nunca** emitir (`W‡…`) sin confirmación.

Nota: incluso vender y luego ignorar (`I`) toma espacio de forma temporal. Para cotizar sin tocar inventario, usa `JR.` o `FQ` + `RD`.

---

## Fuentes

- Travelport – GDS Formats Comparison (incluye columna Sabre), mar 2025: https://support.travelport.com/webhelp/Formats/Content/Resources/MiniGuide/GDSCompareWord-11Mar2025.pdf
- Travelport – Smartpoint GDS translator (comparaciones 1G/1S): https://support.travelport.com/webhelp/Smartpoint1G1V/Content/Other_Features/SmartpointTranslator/SmartpointTranslator_Comparisons.htm
- Zenon NDC – Sabre Reservation Manual (2008, SlideShare): https://www.slideshare.net/slideshow/sabre-reservation-manual/11665174
- British Airways – Group Guide Sabre: https://www.britishairways.com/cms/b2b/tradeOnline/UK_I/content/trade_support_and_groups/group_guide_sabre_0304.pdf
- Sabre Travel Network Indonesia – Fares Display Guide: https://sabretn.co.id/wp-content/uploads/2024/01/Fares-Display-Sabre-Fares-Ticketing-Guide.pdf
- Sabre Travel Network Indonesia – Pricing Guide: https://sabretn.co.id/wp-content/uploads/2024/01/Pricing-Sabre-Fares-Ticketing-Guide.pdf
- Sabre – EMD Pricing Formats (Air Extras): https://aviacenter.ru/files/help-desk/news%202017/май/26/EMD%20PRICING%20FORMATS_06MAR.pdf
- Lufthansa Group – Sabre clue card: https://www.lufthansaexperts.com/shared/files/lufthansa/public/mcms/folder_6672/file_154296.pdf
- Air Canada – Branded Fares GDS (Sabre): https://aviacenter.ru/helpdesk/files/help-desk/news-OLD/AC/AC-2019-04-RULES-3-Branded-Fares-GDS.pdf
- American Airlines – Basic Economy Agency Reference Guide: https://www.americanairlines.co.uk/content/images/uk/PDF/Agency_Reference_Guide_-_Basic_Economy_EMEA1.pdf
- Virgin Australia – Sabre Clue Card: https://www.virginaustralia.com/content/dam/vaa/documents/agency-hub/clue-cards/Virgin-Australia-Sabre-Clue-Card.pdf
- LIME Management – Sabre user guide: https://www.lime-management.com/media/3137/lime-sabre-user-guide-it.pdf
- LIME Management – Flights Sabre: https://www.lime-management.com/media/eydczmae/lime-flights-sabre.pdf
- BT Res – GDS help manual: https://www.btres.com/pdf/GDS-help-manual-for-fares-and-queuing.pdf
- Google Sheet "Basic Sabre Commands" (códigos de cabina YB/SB/BB/FB): https://docs.google.com/spreadsheets/d/1kQ3Cougb4l3EsBgNncmvF6U9W6PnU4ys8CjSLUcIq7w/edit
- Sitio de capacitación Sabre (TC-BB/FB/YB, JR): https://sites.google.com/diit.info/shaifullar-rabbi/sabre-gds-online-training
- Sabre Dev Studio – Errores de End Transaction: https://developer.sabre.com/docs/soap_apis/utility/reservation/enhanced_end_transaction/errors
- Sabre Dev Studio – Error/Cause/Resolution: https://developer.sabre.com/node/2276
- Sabre Dev Studio – About Bargain Finder Max (WPNI vs JR): https://developer.sabre.com/about-bargain-finder-max-and-how-it-works
- Sabre Dev Studio – Cabin type codes: https://developer.sabre.com/cabin-type

No se pudieron leer (bloqueadas o con error): Sabre Israel QR Guide (robots), las páginas de airts.ru "Basic Pricing" y
"Low Fare Search" (error del servidor) y los documentos de Scribd (requieren JavaScript). Sabre Format Finder y Sabre Central
requieren inicio de sesión, así que no se consultaron.


---

# Sabre Agency Workspace: referencia general (todo lo que no es reserva de aéreo ni de hotel)

Para The Suite Life (TSL). Se armó solo con páginas públicas (Travelport Format Compare, Sabre Developer Hub, guías y manuales de capacitación Sabre publicados en la web). No se entró a Sabre.
Fecha: 10-nov-2026. Todo lo que no se pudo confirmar en una fuente dice **"sin confirmar"**.

## Resumen corto

- **Caracteres especiales de Sabre.** Cada fuente los dibuja distinto según su fuente tipográfica (`‡`, `#`, `+`, `¥` o `³`), así que conviene conocerlos antes de copiar un formato:
  - `‡` (Cross of Lorraine, separador): la tecla a la izquierda de Enter, según la guía de 2006 (la tecla exacta en el teclado en español está sin confirmar).
  - `¤` (Change key, cambiar/borrar): la tecla `[`.
  - `§` (End item / comandos personalizados): en Sabre Red 360 está en la tecla `\`, según Sabre Developer Hub.
  - En este documento siempre uso `‡` y `¤`.
- **Conversión de moneda.** El formato correcto lleva `‡` después de `DC`: **`DC‡MAD27297/USD`**. La entrada que devolvió RESTRICTED (`DCMAD27297/USD`) no lo llevaba. Ver la sección 5.
- **Ayuda dentro de Sabre.** `HELP/palabra clave` abre Format Finder. Por ejemplo, `HELP/CURRENCY` o `HELP/SELL CAR`.
- **Campos mínimos de un PNR: "PRINT".** Phone (9), Received (6), Itinerary, Name (-), Ticketing (7). Se guarda con `E` o `ER` y se descarta con `I` o `IR`.
- **Leyenda de la columna "¿Modifica reserva?":**
  - **No**: solo consulta.
  - **Sí (pendiente)**: cambia el PNR en el área de trabajo, y no queda guardado hasta `E`/`ER`.
  - **Sí (inmediato)**: el sistema actúa en ese momento, o se guarda o se envía.
  - **Sí (vende)**: pide espacio real a un proveedor.

---

## 1. Cómo funciona Agency Workspace (Sabre Red 360 web)

Las fuentes públicas sobre la interfaz son escasas, y gran parte de la ayuda de Sabre requiere iniciar sesión.

**Lo que sí se confirmó:**
- Sabre lanzó una vista gráfica que se puede usar con teclado, mouse o ambos.
- Se puede cambiar a la pantalla clásica (cryptic), y los comandos tradicionales también funcionan dentro de la vista gráfica (Travel Market Report).
- Sabre Mosaic Agency Workspace se describe como un espacio unificado: aéreo, hospedaje, auto, tren y tours con los mismos flujos para cambios, cambios de boleto y reembolsos (new.sabre.com).

| Elemento | Qué es / cómo se usa | Estado de la información |
|---|---|---|
| Línea de comandos | Escribes el formato cryptic y presionas Enter. La respuesta sale en texto o en un panel gráfico, según la configuración. | Confirmado que conviven los dos modos. El ajuste exacto para alternarlos está sin confirmar. |
| Command Helper (barra) | Barra de botones con *popovers* junto a la línea de comandos. Las Red Apps pueden agregar botones (clave técnica `novice-buttons`), es decir, está pensada como ayuda para usuarios nuevos. | Confirmado su existencia (Sabre Developer Hub). El contenido exacto de cada botón está sin confirmar. |
| Comandos personalizados `§` | Comandos que empiezan con `§` (tecla `\`) y que llama una Red App. Ejemplo: `§TEST§ABC`. | Confirmado (Developer Hub). Solo existen si tu agencia instaló esa Red App. |
| PF Keys | Atajos que envían formatos ya preparados, con campos para llenar. Ejemplo de sintaxis vista en un proveedor: `^T` pide un dato, `^E` envía. | Sintaxis de editor sin confirmar en documentación oficial. Dónde están en el menú del web: sin confirmar. |
| Trip Summary (panel) | Panel con el resumen del PNR activo. Las Red Apps pueden forzar que se refresque. | Confirmado que existe ("Trip Summary Refresh" en el SDK). Detalle de campos sin confirmar. |
| Workflows (panel lateral) | Flujos guiados ("Custom Workflows" en Side Panels del SDK). | Existencia confirmada. Contenido sin confirmar. |
| End & Retrieve | Equivale a `ER`: guarda el PNR y lo vuelve a mostrar. | `ER` confirmado. El botón gráfico está sin confirmar. |
| Repetir entradas | `ALT + flecha arriba/abajo` recorre entradas anteriores, para editarlas y reenviarlas. | Confirmado en guía de 2006. En la versión web: sin confirmar. |

### Sign-in, PCC y áreas de trabajo (A–F)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `SI*` + número de agente | Firma en todas las áreas (A–F). `SI` sin `*` firma solo en el área actual. | `SI*1234` | No |
| `SO` / `SO*` | Cierra sesión del área actual / de todas | `SO*` | No (pero se pierde lo no guardado) |
| `¤` + letra | Cambia de área de trabajo | `¤B` | No |
| `*S` / `*S*` / `*S*P` | Área actual / estado de todas / con impresoras | `*S*` | No |
| `S/*` | Vuelve a mostrar el mensaje de sign-in | `S/*` | No |
| `W/*` + PCC | Decodifica un PCC (pseudo city code) | `W/*B4T0` | No |
| `H*AS` + PCC | Lista de *sines* (agentes) del PCC | `H*AS(PCC)` | No |

Cada área tiene su propio PNR. Puedes tener un cliente abierto en A y consultar otro en B sin mezclar los datos.

### Desplazamiento, redisplay e ignorar

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `MD` / `MU` | Bajar / subir una pantalla de la respuesta | `MD` | No |
| `MB` / `MT` | Ir al final / al inicio de la respuesta | `MT` | No |
| `*A` | Muestra el PNR completo | `*A` | No |
| `*I` / `*IA` | Solo itinerario / solo segmentos aéreos | `*I` | No |
| `*N`, `*P9`, `*P6`, `*T`, `*P5`, `*-` | Muestran por separado: nombres, teléfonos, received from, ticketing, remarks, forma de pago | `*P5` | No |
| `I` | Ignora los cambios no guardados y saca el PNR del área | `I` | Descarta cambios (no borra la reserva guardada) |
| `IR` | Ignora los cambios y vuelve a mostrar el PNR | `IR` | Descarta cambios |
| `IC`, `ICAPD`, `IC‡7` | Ignora y clona el itinerario o los datos (por ejemplo, el mismo viaje 7 días después, máximo 30) | `ICAPD` | Crea un PNR nuevo en el área (pendiente) |

---

## 2. PNR: campos, remarks, historial, colas y cierre

### Campos obligatorios ("PRINT")
La capacitación oficial de Sabre lo dice así: *"You must complete all mandatory PNR fields (PRINT) before you end a new PNR."*

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `-APELLIDO/NOMBRE TÍTULO` | Agrega un nombre | `-MEDINA/ANA MRS` | Sí (pendiente) |
| `-2¤` | Borra el nombre 2 (siempre revisa antes de borrar) | `-2¤` | Sí (pendiente) |
| `9` + teléfono + `-` + identificador | Agrega teléfono (A=agencia, B=negocio, H=casa, M=móvil…) | `9525-555-1234-A` | Sí (pendiente) |
| `9`n`¤` | Borra el teléfono n | `92¤` | Sí (pendiente) |
| `PE‡correo‡` | Agrega correo electrónico | `PE‡CLIENTE@MAIL.COM‡` | Sí (pendiente) |
| `7TAW` + fecha + `/` | Campo de ticketing: pone el PNR en la cola de emisión en esa fecha | `7TAW15DEC/` | Sí (pendiente) |
| `7T-A` | Marca el PNR como ya emitido o sin boleto | `7T-A` | Sí (pendiente) |
| `7¤TAW` + fecha + `/` | Cambia la fecha de ticketing | `7¤TAW20DEC/` | Sí (pendiente) |
| `6` + nombre | Received from: quién pidió el cambio. `6P` significa "el pasajero". | `6MARIANA` | Sí (pendiente) |
| `6¤` + nombre | Corrige el received from | `6¤ANA` | Sí (pendiente) |

### Remarks (campo 5)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `5` + texto | Remark general interno (no se manda a aerolíneas) | `5CLIENTE VIP PREFIERE PISO ALTO` | Sí (pendiente) |
| `5H-` + texto | Remark histórico: queda permanente en el historial después de `E` | `5H-TARIFA COTIZADA 500 USD` | Sí (pendiente, luego permanente) |
| `5‡` + texto | Remark que se imprime en el itinerario del cliente | `5‡GRACIAS POR VIAJAR CON TSL` | Sí (pendiente) |
| `5‡S2 ` + texto | Remark de itinerario ligado al segmento 2 | `5‡S2 TRASLADO PRIVADO INCLUIDO` | Sí (pendiente) |
| `5.` + texto | Remark que se imprime en la factura | `5.SERVICIO DE DISEÑO DE VIAJE` | Sí (pendiente) |
| `5`letra`‡` + texto | Remark codificado (no se imprime) | `5X‡NOTA INTERNA` | Sí (pendiente) |
| `5-CASH` / `5-CK` | Forma de pago en remarks | `5-CASH` | Sí (pendiente) |
| `5`n`¤` | Borra el remark n | `51¤` | Sí (pendiente) |
| `5Q-` + fecha + cola | Programa el PNR a una cola en fecha futura | `5Q-01DEC101/51` | Sí (pendiente) |

### Historial

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `*H` | Historial completo del PNR | `*H` | No |
| `*HI` / `*HIA` | Historial de itinerario / solo de aéreo | `*HI` | No |
| `*H5` / `*P5H` | Historial de remarks / remarks históricos | `*P5H` | No |
| `*H9` | Historial de teléfonos | `*H9` | No |
| `*H3` | Historial de OSI/SSR | `*H3` | No |

### Recuperar un PNR

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `*` + localizador | Recupera por localizador | `*RDSQXT` | No |
| `*-APELLIDO` | Recupera por apellido | `*-MEDINA` | No |
| `*-APELLIDO/NOMBRE` | Recupera por apellido y nombre | `*-MEDINA/ANA` | No |
| `*1`, `*L`, `*0` | Elegir de la lista de nombres similares / volver a mostrarla / ver más | `*1` | No |

### Colas (queues)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `QC/` | Cuenta los PNR en todas las colas | `QC/` | No |
| `QC/` + n | Cuenta los PNR de una cola | `QC/40` | No |
| `Q/` + n | Entra a trabajar una cola | `Q/40` | No (abre PNRs) |
| `QP/` + cola + `/` + PIC | Coloca el PNR activo en una cola (PIC = código de instrucción) | `QP/40/11` | Sí (inmediato: coloca en cola) |
| `QP/101/51¤102/51` | Colocación en varias colas | (igual) | Sí (inmediato) |
| `QR` | Saca de la cola el PNR actual sin cambios | `QR` | Sí (inmediato: lo quita de la cola) |
| `QXI` | Sale de la cola e ignora el último PNR | `QXI` | No (descarta) |
| `I` (estando en cola) | Deja el PNR en la cola sin cambios | `I` | No |
| `QN*` | Tabla de nombres de colas | `QN*` | No |
| `QZAP/`, `QCL/`, `QMOVE/` | Borran, limpian o mueven colas completas | — | **Sí, masivo. No usar sin consultar.** |

### Cerrar la transacción

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `E` | Guarda el PNR (End) y lo saca del área | `E` | **Sí (inmediato: guarda)** |
| `ER` | Guarda y vuelve a mostrar (End & Retrieve) | `ER` | **Sí (inmediato)** |
| `EM` | Guarda y **envía por correo** el itinerario al email del PNR | `EM` | **Sí (inmediato + envía al cliente)** |
| `EMT` / `EMI` | Guarda y envía aviso de e-ticket / e-factura | `EMT` | **Sí (inmediato + envía)** |
| `EC`, `ECAPD` | Guarda y clona el itinerario o los datos | `ECAPD` | Sí (inmediato) |

> **Regla TSL:** `E`, `ER`, `EM`, `EMT` y `EMI` son irreversibles para efectos prácticos. Las tres de envío (`EM`, `EMT`, `EMI`) le mandan algo al cliente. Confirmar con Mariana antes de usarlas.

---

## 3. Autos (resumen)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `CF` + ciudad + `/` + fechas + `/` + horas | Disponibilidad y tarifas por ciudad, fechas y horas | `CFMEX/12DEC-15DEC/10A-10A` | No |
| `CF1/2` | Disponibilidad usando los segmentos 1 y 2 del PNR (llegada y salida) | `CF1/2` | No |
| `CF1/2/ECAR,CCAR` | Filtra por tipo de auto (código SIPP) | — | No |
| `CF3/4-ZE,ZD,ZI` | Filtra por arrendadoras | — | No |
| `CF*-ZE` / `CF*/LCAR` / `CF*+USD` | Modifica la última búsqueda: arrendadora / tipo / moneda | `CF*+USD` | No |
| `CF*` | Vuelve a mostrar la disponibilidad | `CF*` | No |
| `CF*R3` | Reglas de la tarifa de la línea 3 | `CF*R3` | No |
| `CF*P1` / `CP*2` | Descripción del auto (de la disponibilidad / del segmento 2) | `CP*2` | No |
| `CQ1/2ZT` / `CQ*R1` | Car quote para una arrendadora / reglas | — | No |
| `CARMEX` | Índice de arrendadoras por ciudad | `CARMEX` | No |
| `0C` + línea | Vende el auto de la línea | `0C2` | **Sí (vende)** |
| `CM`n`/...` | Modifica un segmento de auto (fechas, tipo, campos opcionales) | `CM2/PD-2SEP/RD-5SEP` | **Sí (modifica segmento vendido)** |
| `XIC` | Cancela todos los autos del PNR | `XIC` | **Sí (cancela)** |
| `DU*/CAR/TYPES`, `CARTYPEHELP` | Referencia de tipos de auto | — | No |

---

## 4. Segmentos pasivos y "otros" (para documentar servicios reservados fuera de Sabre)

Un segmento pasivo (estatus **GK**) registra en el PNR algo que ya se confirmó por fuera: directo con el hotel, con un DMC, en Expedia TAAP, etc. **No** manda mensaje al proveedor. Sirve para que el itinerario y el back office queden completos.

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `0` + aerolínea + vuelo + clase + fecha + ruta + `GK1` | Vuelo pasivo | `0QR162Y25JULBAHLHRGK1` | Sí (pendiente; sin mensaje a la aerolínea) |
| `0CAR` + arrendadora + `GK1` + ciudad + fechas + `/` + tipo + `/CF-` + confirmación | Auto pasivo | `0CARZIGK1SAN1JAN-4JAN/ICAR/CF-12345` | Sí (pendiente) |
| `0HHT` + cadena (o `YY`) + `GK` + habitaciones + ciudad + `IN` fecha + `-OUT` fecha + `/`nombre`/`tipo hab`/`tarifa`/`... `/CF-`conf | Hotel pasivo (plantilla de una PF key publicada por un proveedor de back office) | Plantilla: `0HHTYYGK1MEXIN10DEC-OUT14DEC/NOMBRE HOTEL/STD/450.00/.../CF-ABC123` | Sí (pendiente). **Los separadores de dirección y teléfono están sin confirmar: verificar con `HELP/PASSIVE HOTEL`.** |
| `0A` | Segmento ARNK (tramo terrestre o sin información) | `0A` | Sí (pendiente) |
| `.3XK` | Cancela el segmento 3 sin mandar mensaje | `.3XK` | Sí (pendiente) |
| `.3HK` / `HKALL` | Cambia el estatus del segmento 3 / de todos a HK | `.3HK` | Sí (pendiente) |

- **Segmentos "OTH" (otros servicios) e "INS" (seguro).** La API de Sabre (`MiscSegmentSellLLSRQ`) confirma que existen los tipos MCO, **OTH** (otro producto), PTA e **INS** (seguro), con estatus GK. El formato host exacto (por ejemplo `0OTH...`) está **sin confirmar**: usa `HELP/OTH` o `HELP/MISCELLANEOUS SEGMENT` en Format Finder.
- **Estatus MK.** No se encontró en fuentes Sabre (sí aparece en Travelport). Está **sin confirmar** para Sabre.

---

## 5. Utilidades

### Codificar y decodificar (W/, HCC)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `W/-CC` + ciudad | Código de una ciudad | `W/-CCMARRAKECH` | No |
| `W/*` + código | Decodifica una ciudad o aeropuerto, o una aerolínea | `W/*RAK`, `W/*AM` | No |
| `W/-AL` + nombre | Código de una aerolínea | `W/-ALAEROMEXICO` | No |
| `W/-AP` + nombre | Código de un aeropuerto por nombre | `W/-APHEATHROW` | No |
| `W/-CR` / `W/CR*` | Codifica / decodifica una arrendadora | `W/CR*ZE` | No |
| `W/-HL` / `W/HL*` | Codifica / decodifica una cadena hotelera | `W/HL*HY` | No |
| `W/EQ*` | Decodifica un tipo de avión | `W/EQ*789` | No |
| `HCCC/` + país o código | Codifica o decodifica un país | `HCCC/MOROCCO`, `HCCC/MA` | No |
| `W/-ATMEX` / `W/-CY`ciudad,país | Los 10 aeropuertos más cercanos | `W/-ATMEX` | No |
| `W/-ATMEX‡ATCUN` | Distancia entre dos aeropuertos | — | No |

### Conversión de moneda (DC)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `DC‡` + moneda + monto + `/` + moneda destino | **Convierte un monto** | `DC‡MAD27297/USD`, `DC‡USD300/MXN` | No |
| `DC‡` + moneda + monto | Convierte a la moneda local del PCC | `DC‡EUR100` | No |
| `DC*CUR` | Lista de países, códigos de moneda y tasas | `DC*CUR` | No |
| `DC*` + moneda | Tasa bancaria de esa moneda (una guía dice *Bankers' Buying Rate*; otra dice que Sabre usa *Bankers' Selling Rate*, BSR) | `DC*MAD` | No |
| `DC*` + país | Tasa por país | `DC*MOROCCO` | No |

**Por qué `DCMAD27297/USD` respondió "RESTRICTED"** (son hipótesis, ninguna se confirmó en una fuente):
1. **Falta `‡` después de `DC`.** Todas las fuentes ponen el separador: `DC‡SAR100/USD`, `DC‡USD500.00/GBP`, `DC‡VEF100/COP`. Sin él, el sistema puede interpretar otra entrada. Es la causa más probable. Prueba primero `DC‡MAD27297/USD`.
2. **MAD (dirham marroquí) es moneda de convertibilidad restringida.** Sabre podría no publicar tasa de conversión libre para monedas controladas. Comprueba con `DC*MAD` o `DC*CUR`, y compara contra una moneda libre: `DC‡EUR100/USD`.
3. **Permisos del EPR o PCC.** Que la función de moneda esté bloqueada para tu firma (*sin confirmar*). Si `DC‡EUR100/USD` también responde RESTRICTED, hay que pedírselo al administrador de Sabre de la agencia o a Sabre Help Desk.
4. Para el formato oficial y la lista de respuestas de error: `HELP/CURRENCY CONVERSION` o `HELP/DC`.

> Para cotizar a clientes, la tasa de Sabre es de referencia (bancaria). No sustituye el tipo de cambio que aplique el proveedor o la tarjeta del cliente.

### Calculadora, fecha y hora (T)

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `T¤22‡3` / `T¤350-18` / `T¤45*6` / `T¤925/3` | Calculadora: suma (con `‡`), resta, multiplica, divide | `T¤27297/10.85` | No |
| `T¤MENU` | Menú de cálculos y conversiones | `T¤MENU` | No |
| `T¤15DEC‡30` / `T¤15DEC-30` | Fecha 30 días después / antes | `T¤15DEC‡30` | No |
| `T¤JUL/26` | Calendario del mes | `T¤JUL/26` | No |
| `T*` + ciudad | Hora local en esa ciudad | `T*RAK` | No |
| `T¤ET` + ciudad`/`ciudad | Diferencia horaria entre dos ciudades | `T¤ETMEX/RAK` | No |
| `T¤ET` + HHMM + ciudad`/`ciudad | Qué hora será en la ciudad 2 a esa hora de la ciudad 1 | `T¤ET1000MEX/PAR` | No |
| `T*CT-` + aeropuerto | Tiempos mínimos de conexión | `T*CT-MAD` | No |
| `VCT*` | Verifica las conexiones del itinerario | `VCT*` | No |
| `TX/B` + monto / `TX/T` + monto | Calculadora de impuestos sobre tarifa base / total | `TX/B173.15` | No |
| `¤WEA/CF*` + ciudad | Pronóstico del clima | `¤WEA/CF*CUN` | No |

### Timatic (pasaporte, visa, salud)

- El documento de IATA sobre el Timatic CLI usa estas entradas:
  - `TIDFT/MX`: texto completo de un país.
  - `TIRV/NAMX/DEMA`: visa según nacionalidad (NA) y destino (DE).
  - `TIRH/...`: salud.
  - `TIRA`: visa y salud.
  - `TIFV`, `TIFA`, `TIFH`: formularios simplificados.
  - `TIRULES`: índice de reglas.
  - `TIBACK`: regresa a la respuesta anterior.
- **Si Sabre las acepta tal cual, y con qué variantes: sin confirmar.** Las entradas `TIMV/1`, `TIMP/4` que aparecen en internet son de Travelport. No las uses como si fueran de Sabre.
- **Recomendación:** escribe `HELP/TIMATIC` en Sabre. Para un cliente, confirma siempre en el portal oficial del país o con la aerolínea.

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `TIDFT/` + país | Texto completo de requisitos (Timatic CLI) | `TIDFT/MA` | No (sin confirmar en Sabre) |
| `TIRV/NA`xx`/DE`yy | Visa para nacionalidad xx con destino yy | `TIRV/NAMX/DEMA` | No (sin confirmar en Sabre) |

### Ayuda y referencias dentro de Sabre

| Formato | Qué hace | Ejemplo | ¿Modifica reserva? |
|---|---|---|---|
| `HELP/` + palabras clave o formato | Abre Format Finder y busca. Acepta formatos parciales y mensajes de error. | `HELP/SELL CAR`, `HELP/MISF‡TM` | No |
| `Ctrl+Z` | Abre la ayuda (Red Workspace) | — | No (en Agency Workspace web: sin confirmar) |
| `N*/SHORTCUTS` | Lista de atajos comunes de Sabre | `N*/SHORTCUTS` | No |
| `DU*/CLS`, `DU*/MLS`, `DU*/SPM`, `DU*/HTL/TYPES`, `DU*/CAR/TYPES` | Tablas de referencia: clases, comidas, comidas especiales, tipos de habitación, tipos de auto | `DU*/SPM` | No |
| `WPRDHELP`, `WQRDHELP` | Ayuda de formatos de reglas de tarifa | — | No |
| Agency eServices | Portal con Format Finder, Quick References y capacitación: https://agencyeservices.sabre.com (se entra con EPR, contraseña y PCC) | — | No |

- **Format Finder sin línea de comandos.** Está en Agency eServices (menú Support) y también como herramienta lateral en Red Workspace.
- **"Send to Sabre".** Desde la herramienta lateral, este botón pega un ejemplo de formato en el área de trabajo.

---

## 6. Hoteles: nota breve (otro documento cubre el tema a fondo)

- Los **formatos host clásicos de hotel** (disponibilidad y descripción vía GDS) funcionan con contenido de cadenas conectadas a Sabre.
- **Content Services for Lodging (CSL)** es el conjunto de APIs de hospedaje de Sabre. Junta propiedades y tarifas *"from GDS and aggregator sources"* (Developer Hub).
  - En 2018 se anunció con contenido de Bedsonline, TravelBound y Expedia Affiliate Network.
  - En ese momento se aclaró que no estaría en el Sabre nativo (cryptic), sino en interfaces gráficas: *"Any graphical interface can see this"* (Travel Market Report).
- **Qué significa en la práctica.** Las tarifas de agregadores normalmente aparecen en la búsqueda **gráfica** de hotel de Agency Workspace, no en los formatos cryptic clásicos.
- **Comandos específicos (`HOT` frente a `HOD`/`HOA`) y fechas de retiro de formatos legacy: sin confirmar** con fuentes públicas. Usa `HELP/HOTEL` y consulta `sabre_hoteles.md`.

---

## Fuentes

- Travelport, comparación de formatos entre GDS (columna Sabre): https://support.travelport.com/webhelp/Formats/Content/FormatCompare/LandingQuickRef.htm
  - Basic: https://support.travelport.com/webhelp/Formats/Content/FormatCompare/Basic.htm
  - Miscellaneous: https://support.travelport.com/webhelp/Formats/Content/FormatCompare/Miscellaneous.htm
  - Queues: https://support.travelport.com/webhelp/Formats/Content/FormatCompare/Queues.htm
  - Cars: https://support.travelport.com/webhelp/Formats/Content/FormatCompare/Cars.htm
  - Guía PDF: https://support.travelport.com/webhelp/Formats/Content/Resources/MiniGuide/GDSCompareWord-11Mar2025.pdf (ahí los símbolos de Sabre salen como `+` y `³`)
- Sabre Quick Reference, Miscellaneous formats (DC, T¤, W/, DU*, N*/SHORTCUTS, teclas especiales): https://gdshelp.blogspot.com/2020/04/sabre-quick-reference-guide-ch1.html
- Sabre Quick Reference Guide (DC, T*, remarks, colas, pasivos, autos, E/I/IC): https://gdshelp.blogspot.com/2017/11/sabre-quick-reference-guide.html
- Sabre Important Commands (DC‡, colas, historial): https://gdshelp.blogspot.com/2022/02/sabre-important-commands.html
- Basic Sabre Formats and Functions (áreas, W/, PNR, E/I): https://sktravelsystem.blogspot.com/2023/05/basic-sabre-formats-and-functions.html
- Sabre, Basic Sabre Formats and Functions Training Guide, 2006 (teclado ‡/¤, remarks, E/EM): https://www.slideshare.net/slideshow/sabregdsbookinginstructionsfortransaviapdf/255710127
- Sabre Training Workbook "Working in the Sabre System" (PRINT, 6, 7TAW, 9, PE, E/ER/EM, I/IR, *H): https://portal.sabreng.com/files/resources/files/1454080752_1454080752_basic_reservation_course.pdf
- Format Finder Help System Student Guide (HELP/, Ctrl+Z, Send to Sabre): https://silo.tips/download/format-finder-help-system-student-guide
- Sabre Agency eServices Quick Reference: https://www.sabretn.co.id/wp-content/uploads/2013/10/New-Agency-eServices-Quick-Ref_Nov2016.pdf
- Lime Management, Sabre user guide (PE‡, 7TAW, ER, *H, W/): https://www.lime-management.com/media/3137/lime-sabre-user-guide-it.pdf
- British Airways, Sabre group guide (QP/, QC/, QR, I, 6): https://www.britishairways.com/cms/b2b/tradeOnline/UK_I/content/trade_support_and_groups/group_guide_sabre_0304.pdf
- Scribd, "Sabre GDS User Guide" (ejemplo DC‡VEF100/COP; contenido parcial): https://www.scribd.com/document/966069162/saber
- Sabre Developer Hub, Command Helper Button: https://developer.sabre.com/command-helper-button
- Sabre Developer Hub, Custom Commands (§ en la tecla \): https://developer.sabre.com/custom-commands
- Sabre Developer Hub, Trip Summary Refresh: https://developer.sabre.com/trip-summary-refresh
- Sabre Developer Hub, índice de ayuda del SDK de Sabre Red 360: https://developer.sabre.com/sdks/travel-agency/sabre-red-360/help
- Sabre Developer Hub, Sell Miscellaneous Segments (OTH/INS/MCO/PTA, GK): https://developer.sabre.com/docs/soap_apis/air/book/Sell_Miscellaneous_Segments
- TRES Technologies, PF keys de hotel y auto pasivos en Sabre: https://trestechnologieshelp.zendesk.com/hc/en-us/articles/31542864857747
- Sabre Developer Hub, Content Services for Lodging: https://developer.sabre.com/content-services-for-lodging
- Travel Market Report, Lodging Content Services (2018): https://travelmarketreport.com/retail-strategies/articles/can-new-booking-tools-help-level-the-lodging-playing-field-for-agents
- Travel Market Report, vista gráfica de Red Workspace: https://www.travelmarketreport.com/technology/articles/sabre-introduces-fully-graphical-version-of-red-workspace
- Sabre Mosaic, Experience Suite (Agency Workspace): https://new.sabre.com/agency-mosaic/experience-suite
- IATA, Using the Timatic CLI: https://www.iata.org/contentassets/0f1d2957c3a44395900d8c12a2dbe026/using_timatic_v3.pdf
