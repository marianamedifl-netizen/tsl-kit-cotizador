---
name: tsl-cotizar-traslados-rolzo
description: Cotiza traslados privados y chofer por horas con el conector Rolzo de The Suite Life y entrega la tabla en el chat. Úsala cuando Mariana pida cotizar un Rolzo, un traslado, un transfer o un chofer a disposición.
---

# TSL · Cotizar traslados (Rolzo)

Úsala siempre que se pida cotizar un Rolzo, un traslado aeropuerto – hotel, un traslado entre ciudades o un chofer por horas. El resultado es una tabla en el chat; el PDF se arma después con `tsl-cotizacion-rapida` o `tsl-cotizacion-completa`.

## Reglas que no se rompen

1. **El conector solo cotiza.** No reserva, no modifica y no cancela. Las reservas de Rolzo las hace Mariana.
2. **No inventar** precios, vehículos, capacidades ni políticas. Lo que el conector no devuelve se marca "pendiente de verificar".
3. **El enlace del conector es privado.** Nunca se escribe en un chat, documento o archivo. Si el conector no aparece conectado, se dice de inmediato y se le pide a Mariana.
4. **En documentos para clientes** no aparece la palabra Rolzo, la comisión ni el descuento.

## Datos que se necesitan

- Origen y destino con nombre completo (hotel, aeropuerto o dirección) y país.
- Fecha y hora local de recogida.
- Número de pasajeros y de maletas.
- Si es llegada o salida de aeropuerto: el vuelo y su horario real.
- Tipo de servicio: traslado punto a punto, o chofer por horas (cuántas horas).

Si falta el horario del vuelo, se cotiza con una hora de referencia y se avisa que es de referencia. Si faltan pasajeros o maletas, se pregunta: de eso depende el vehículo.

## Pasos

1. **Revisar el conector.** `estado_rolzo` debe responder `ok: true`, `llave: true` y `ambiente: "produccion"`. Si dice otro ambiente, las tarifas no son reales: avisar y detenerse.
2. **Ubicar cada lugar.** `buscar_lugar` con el nombre completo y, de preferencia, `pais` (dos letras: MA, FR, ZA).
   - Aeropuertos: escribir el nombre ("Marrakech Menara airport"). El código IATA solo (RAK, CDG) no funciona.
   - Revisar que el resultado sea el correcto por su `tipo`: `aeroway/aerodrome` para aeropuertos, `google/hotel` para hoteles. Suelen salir lugares con nombre parecido (un spa o una clínica con el nombre del hotel).
3. **Limpiar el objeto `rolzo`** del lugar elegido antes de usarlo: si `fullAddress`, `city` o `state` vienen en otro alfabeto, se reescriben en caracteres latinos. `lat`, `lng` y `country` no se tocan.
4. **Cotizar el traslado.** `cotizar_traslado` con `origen_lugar`, `destino_lugar`, `fecha` (AAAA-MM-DD), `hora` local y `tipo: "transfer"`.
   - Una llamada por trayecto. Llegada y salida se cotizan por separado, cada una con su fecha y hora; el redondo es la suma de las dos.
5. **Chofer por horas.** `tipo: "hourly"` y `horas`. También pide destino: si el servicio empieza y termina en el mismo lugar, se manda el mismo objeto como origen y destino.
6. **Comprobar la respuesta.** `origen_usado` y `destino_usado` deben ser los lugares pedidos. Si hay `origen_alternativas` o `destino_alternativas`, se revisa cuál corresponde antes de dar un precio.

## Cómo leer cada opción

| Campo | Qué es |
|---|---|
| `vehiculo`, `categoria` | Modelo y categoría (minivan, suvs, first, etc.) |
| `pax`, `maletas` | Capacidad. En chofer por horas `pax` puede venir vacío: se toma la del mismo vehículo en traslado o se marca pendiente |
| `precio`, `moneda` | Precio por trayecto (o por el bloque de horas) en la moneda de Rolzo |
| `aUSD` | Factor de conversión: `precio × aUSD` da el equivalente en dólares, solo como referencia |
| `km`, `minutos` | Distancia y tiempo estimado (vacíos en chofer por horas) |
| `aeropuerto`, `esperaIlimitada` | Si es recogida en aeropuerto y si la espera por retraso del vuelo no tiene límite |
| `cancelacion` | Texto con el plazo de cancelación sin costo, la espera incluida y el costo de la espera extra |
| `comisionPct`, `descuentoPct` | Comisión y descuento de la cuenta. Solo para Mariana |
| `markupRolzo`, `tarifaConMarkup` | No cuadran entre sí y **no se usan** |

## Elegir el vehículo

- Debe caber el grupo completo con su equipaje: se comparan pasajeros **y** maletas contra la capacidad.
- Si el grupo no cabe en un vehículo, se cotizan los que hagan falta y se dice cuántos son.
- Se recomienda el vehículo más económico en el que el grupo cabe con holgura, y se muestra la categoría siguiente como alternativa.

## Qué se entrega en el chat

Primero una línea con la ruta, la fecha, la hora y, si aplica, distancia y tiempo. Luego una tabla por trayecto:

| Vehículo | Capacidad | Precio por trayecto | Redondo | Equivalente USD | Cancelación sin costo | Espera incluida | Comisión |
|---|---|---|---|---|---|---|---|

Después:
- La recomendación y por qué.
- El tipo de cambio usado para el equivalente y que es de referencia.
- Lo pendiente de verificar. El conector no devuelve sillas para niños, recepción con letrero, paradas extra ni recargos; si se necesitan, Mariana los confirma en Rolzo.
- La pregunta de qué vehículo usar y si el precio va tal cual o con ajuste. No se asume un markup.

## Ejemplo comprobado (17 nov 2026)

Aeropuerto de Marrakech – La Mamounia, 15 mar 2027, 18:00 (5.4 km, 31 min). Los precios cambian; sirve para reconocer la forma de la respuesta.

| Vehículo | Capacidad | Traslado | 4 horas a disposición |
|---|---|---|---|
| Mercedes-Benz V-Class (minivan) | 6 pasajeros, 6 maletas | EUR 175 | EUR 255 |
| Toyota Land Cruiser Prado (SUV) | 3 pasajeros, 3 maletas | EUR 210 | EUR 275 |
| Mercedes-Benz S-Class (first) | 2 pasajeros, 2 maletas | EUR 355 | EUR 445 |

- Traslado: cancelación sin costo hasta 4 horas antes; 15 minutos de espera incluidos; espera extra con cargo por cada 15 minutos.
- Por horas: cancelación sin costo hasta 24 horas antes.
- Comisión de la cuenta: 15 %.

## Si algo falla

- **"Falta el destino"**: el servicio por horas también necesita destino (paso 5).
- **Sin opciones**: revisar que la fecha sea futura, que la hora sea local y que el lugar sea el correcto; probar con el objeto de `buscar_lugar` en lugar de texto.
- **Lugar equivocado en `origen_usado` o `destino_usado`**: repetir `buscar_lugar` con el nombre completo y el país.

## Después

Cuando Mariana elija, el traslado entra en "Servicios adicionales" del documento como "Traslado privado aeropuerto – hotel", con vehículo y capacidad, en la moneda cotizada y con el tipo de cambio si se convierte.
