#!/usr/bin/env python3
"""TSL · Cotización Vuelos (comparativa de opciones de vuelo) — ejemplo canónico: Ciudad de México – El Cairo, marzo 2027.
Uso: python3 cotizacion_vuelos.py [salida.pdf]
Para una cotización nueva: copia esta carpeta y cambia SOLO los datos (portada, OPCIONES, notas) y la foto de img/."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import tsl_base as B
import tsl_formato as F

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'salida.pdf').resolve()
B.TRIP = 'El Cairo · Marzo 2027'
TITLE = 'Opciones de Vuelo · Ciudad de México – El Cairo · Marzo 2027'

# ───────────────────────── datos ─────────────────────────
PORTADA = dict(img='img/cairo_band.jpg', title='Opciones de Vuelo', sub='Ciudad de México – El Cairo',
               rows=[('Fechas', '17 – 28 mar 2027'), ('Viajeros', '2 pasajeros'), ('Documento', 'Cotización · Vuelos')])

# (letra, aerolínea, ruta, boleto, cabina, escalas, total, equivalente, grupos de vuelos, notas)
OPCIONES = [
 ('A', 'British Airways', 'vía Londres', 'Dos boletos separados', 'Business + Turista', '2 h 50 m · 6 h 15 m', 'MXN 354,301.54', '≈ US$19,050',
  [('Ida · 17 – 18 mar', [('17 mar', 'British Airways', 'BA 242', 'México (MEX)', 'Londres (LHR)', 'Business', '21:00', '13:10<sup>+1</sup>', '10 h 10 m'),
                          ('18 mar', 'British Airways', 'BA 398', 'Londres (LHR)', 'El Cairo (CAI)', '<b>Turista</b>', '16:00', '23:10', '5 h 10 m')]),
   ('Regreso · 28 mar', [('28 mar', 'British Airways', 'BA 397', 'El Cairo (CAI)', 'Londres (LHR)', '<b>Turista</b>', '04:35', '08:55', '5 h 20 m'),
                         ('28 mar', 'British Airways', 'BA 243', 'Londres (LHR)', 'México (MEX)', 'Business', '15:10', '19:45', '11 h 35 m')])],
  'Business en los vuelos México – Londres – México; Turista (tarifa Basic, sin maleta documentada) entre Londres y El Cairo. '
  'Dos boletos separados: la conexión en Londres no queda protegida. Escalas: 2 h 50 m a la ida · 6 h 15 m al regreso. '
  'Boleto Business: cambios MXN 5,115, reembolso con penalidad de MXN 36,434. Boleto Turista: cambios MXN 1,497, no reembolsable.'),
 ('B', 'Air France', 'vía París', 'Un solo boleto', 'Business', '3 h 30 m · 6 h 10 m', 'MXN 326,020.10', '≈ US$17,530',
  [('Ida · 17 – 18 mar', [('17 mar', 'Air France', 'AF 175', 'México (MEX)', 'París (CDG)', 'Business', '23:05', '16:35<sup>+1</sup>', '10 h 30 m'),
                          ('18 mar', 'Air France', 'AF 510', 'París (CDG)', 'El Cairo (CAI)', 'Business', '20:05', '01:35<sup>+1</sup>', '4 h 30 m')]),
   ('Regreso · 28 mar', [('28 mar', 'Air France', 'AF 551', 'El Cairo (CAI)', 'París (CDG)', 'Business', '02:25', '07:00', '4 h 35 m'),
                         ('28 mar', 'Air France', 'AF 178', 'París (CDG)', 'México (MEX)', 'Business', '13:10', '16:55', '11 h 45 m')])],
  'Business en los cuatro vuelos, en un solo boleto. Escalas en París: 3 h 30 m a la ida · 6 h 10 m al regreso. '
  'Cambios con cargo de MXN 3,720. Reembolso sujeto a las reglas de la tarifa.'),
 ('C', 'Lufthansa', 'vía Fráncfort', 'Un solo boleto', 'Business', '1 h 10 m · 5 h 15 m', 'MXN 201,177.00', '≈ US$10,817',
  [('Ida · 17 – 18 mar', [('17 mar', 'Lufthansa', 'LH 499', 'México (MEX)', 'Fráncfort (FRA)', 'Business', '21:00', '14:45<sup>+1</sup>', '10 h 45 m'),
                          ('18 mar', 'Lufthansa', 'LH 584', 'Fráncfort (FRA)', 'El Cairo (CAI)', 'Business', '15:55', '21:10', '4 h 15 m')]),
   ('Regreso · 28 mar', [('28 mar', 'Lufthansa', 'LH 585', 'El Cairo (CAI)', 'Fráncfort (FRA)', 'Business', '03:40', '08:15', '4 h 35 m'),
                         ('28 mar', 'Lufthansa', 'LH 498', 'Fráncfort (FRA)', 'México (MEX)', 'Business', '13:30', '17:30', '12 h 00 m')])],
  'Business en los cuatro vuelos, en un solo boleto. Escalas en Fráncfort: 1 h 10 m a la ida · 5 h 15 m al regreso. '
  'Cambios sin cargo. Reembolso con penalidad de MXN 5,580.'),
]
TOTAL_DE = 'Total 2 pasajeros'
NOTA = ('Tarifas totales para 2 adultos, con impuestos incluidos, cotizadas el 11 de noviembre de 2026. Sujetas a disponibilidad y a cambio hasta la emisión de los boletos. '
        'Vigencia: opción B hasta el 12 de noviembre de 2026; opciones A y C hasta el 14 de noviembre de 2026. Equivalente en dólares al tipo de cambio 1 USD = 18.5983 MXN. '
        'Horarios locales; +1 indica llegada al día siguiente. Franquicia de equipaje por confirmar al momento de reservar. Fotografía: @starkie_pics, vía Unsplash.')
POR_HOJA = [1, 2]            # opciones en la hoja 1 (bajo la comparativa) y en cada hoja siguiente

# ───────────────────────── armado ─────────────────────────
def resumen():
    rows = ''.join(f'<tr><td>{F.dot(l)}</td><td><b>{air}</b><span>{via} · {tk.lower()}</span></td><td>{cab}</td><td>{esc}</td>'
                   f'<td><b>{tot}</b><span>{usd}</span></td></tr>' for l, air, via, tk, cab, esc, tot, usd, _, _ in OPCIONES)
    return ('<table class="cmp"><tr><th style="width:.42in">Opción</th><th>Aerolínea</th><th style="width:1.35in">Cabina</th>'
            f'<th style="width:1.45in">Escalas ida · regreso</th><th style="width:1.5in">{TOTAL_DE}</th></tr>{rows}</table>')

def opcion(o):
    l, air, via, tk, cab, esc, tot, usd, groups, nota = o
    return (f'<section class="opt"><div class="oh"><span class="lb">Opción {l}</span><h3>{air} · {via}</h3>'
            f'<div class="pr"><b>{tot}</b><span>{usd} · {TOTAL_DE.lower()}</span></div></div>'
            f'{F.flights_table(groups)}<p class="on">{nota}</p></section>')

pages, i = [], 0
for n, k in enumerate(POR_HOJA + [len(OPCIONES)] * 9):
    chunk = OPCIONES[i:i + k]; i += k
    if not chunk: break
    last = i >= len(OPCIONES)
    body = ''.join(opcion(o) for o in chunk) + (f'<p class="fineprint">{NOTA}</p>' if last else '')
    if n == 0:
        pages.append(f'''<div class="page rap first fly">{F.band_cover(**PORTADA)}
  <div class="bot">{F.logo(2)}<span>01</span></div>
  <div class="in"><h2>Comparativa</h2>{resumen()}<div style="height:.36in"></div>{body}</div>{F.sign() if last else ''}</div>''')
    else:
        pages.append(f'''<div class="page rap fly">{F.furniture('.01', 'Opciones de vuelo', n + 1, link='#')}
  <div class="in">{body}</div>{F.sign() if last else ''}</div>''')

F.print_pdf(F.html_doc(TITLE, '\n'.join(pages), F.RAPIDA_CSS), OUT, ROOT)
print('PDF ->', OUT)
