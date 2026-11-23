# TSL · Kit Cotizador

Todo lo necesario para trabajar con el mismo flujo de cotización de The Suite Life en Claude: las skills, las plantillas del formato nuevo, los archivos de marca y la guía de Sabre.

## Qué hay en el repositorio

| Carpeta | Contenido |
|---|---|
| `1 Skills` | 10 archivos ZIP, uno por skill, listos para subir a Claude |
| `skills` | El texto de cada skill (`SKILL.md`), para leerlo y ver cambios |
| `TSL - Formato Nuevo` | Generadores y ejemplos de cada documento |
| `TSL - Brand Files` | Tipografías (IvyOra y Karla), logos y guía de marca |
| `4 Guias` | `Guia_Sabre_TSL.md` e instrucciones para el proyecto |
| `sync` | Registro de sincronización de skills (`registro.md`), estado (`estado.json`) y el comparador (`comparar.py`) |

## Instalación (una sola vez)

1. **Descarga el repositorio.** Botón verde **Code** > **Download ZIP**, y descomprímelo.
2. **Skills.** En Claude, entra a Customize > Skills, crea una skill nueva con la opción de subir y sube cada ZIP de `1 Skills`. Deja las 10 activadas.
3. **Carpeta de trabajo.** En tu computadora crea la carpeta `Travel Agent Portal` y copia dentro `TSL - Formato Nuevo` y `TSL - Brand Files`. Crea también, vacía, `Travel Agent Portal/Cotizaciones/Formato Nuevo/`.
   
   Los nombres deben quedar idénticos: las skills buscan las plantillas y las tipografías en esas rutas.
4. **Conecta la carpeta.** En la app de escritorio de Claude, conecta `Travel Agent Portal` a tu proyecto.
5. **Proyecto.** Crea un proyecto en Claude y pega en sus instrucciones el texto de `4 Guias/Instrucciones del proyecto.md`. Sube `Guia_Sabre_TSL.md` a los documentos del proyecto.
6. **Accesos que se piden aparte a Mariana.** Usuario de Sabre, acceso a Expedia TAAP, Virtuoso y Four Seasons Preferred Partner, y el conector de traslados Rolzo. Ninguna contraseña ni enlace privado viene en este repositorio.
7. **Conectores.** Unsplash (fotos de ambiente) y la extensión de Claude en Chrome.

## Actualizaciones

Cuando cambie una skill o una plantilla, se actualiza aquí. Vuelve a descargar el repositorio, reemplaza las carpetas y vuelve a subir a Claude el ZIP de la skill que cambió.

Una tarea programada de Claude revisa una vez al día este repositorio y `luisbtrejo77-max/nuba-tsl-skills`, compara cada skill contra las instaladas en la cuenta de Mariana y prepara la tarjeta de actualización. Cada revisión queda anotada en `sync/registro.md`.

## Las skills y cuándo se usan

| Skill | Para qué |
|---|---|
| `tsl-cotizar-hoteles-sabre` | Cotizar y comparar hoteles y vuelos en Sabre, Expedia y el sitio directo. Siempre primero, antes de cualquier documento |
| `tsl-cotizar-traslados-rolzo` | Cotizar traslados privados y chofer por horas con el conector Rolzo |
| `tsl-cotizacion-completa` | Cotización Completa: portada, índice, mapa, vuelos, hoteles, itinerario, hoja por hotel, cotización, notas |
| `tsl-cotizacion-rapida` | Viaje rápido en 2 hojas: vuelos, hoteles, servicios y total |
| `tsl-cotizacion-vuelos` | Solo vuelos: comparativa de opciones |
| `tsl-cotizacion-hoteles` | Solo hoteles: ciudades, opciones y tipos de cuarto |
| `tsl-entrega-final-formato-nuevo` | Entrega Final con confirmaciones |
| `tsl-guia-viaje-formato-nuevo` | Guía de Viaje: clima, qué empacar, propinas |
| `tsl-buscar-ofertas-hoteles` | Ofertas de noches gratis en Virtuoso y Four Seasons Preferred Partner |
| `tsl-ads-instagram` | Anuncios y stories de Instagram con la marca |

## Reglas del flujo

- No se inventan precios, disponibilidad, horarios ni políticas. Lo que no se ve en pantalla se marca "pendiente de verificar".
- Antes de hacer documentos se entrega en el chat el comparativo Sabre, Expedia y sitio directo; Mariana elige y entonces se arma el PDF.
- En hoteles se prefieren las tarifas reembolsables, y siempre se avisa si hay una reembolsable más barata.
- Nunca se reserva, se emite, se guarda un PNR ni se envía nada a un cliente sin confirmación de Mariana.
- Los vuelos que se cargan en Sabre para cotizar se descartan siempre con `I`.
- Claude nunca escribe contraseñas: cada quien inicia sesión.
- En los PDF para clientes no aparecen códigos de tarifa, comisiones ni el nombre de la plataforma donde se cotizó.
- Las skills hablan de "Mariana" como quien decide; en tu proyecto aplica igual: las decisiones se le consultan a ella.

## Ejemplos

`TSL - Formato Nuevo` trae un ejemplo de cada documento: Cotización Completa (Laponia), Cotización Rápida, Cotización Vuelos, Cotización de Hoteles, Entrega Final y Guía de Viaje.

Los ejemplos de Cotización Completa, Entrega Final y Guía de Viaje usan datos reales de clientes. Son solo referencia de formato: no se comparten fuera del equipo ni se reutilizan sus datos.

## Dónde guardar lo que se produce

Los PDF finales van a la carpeta `Salidas` del Drive compartido "TSL · Kit Cotizador", en la subcarpeta de su tipo, con el nombre `TSL_<Documento>_<Cliente o destino>_FormatoNuevo.pdf`.
