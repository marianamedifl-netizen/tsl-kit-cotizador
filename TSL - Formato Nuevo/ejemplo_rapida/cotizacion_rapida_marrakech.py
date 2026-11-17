#!/usr/bin/env python3
"""TSL · Cotización Rápida (viaje rápido en 2 hojas: vuelos + hoteles + servicios adicionales) — ejemplo canónico: Marrakech, marzo 2027.
Uso: python3 cotizacion_rapida_marrakech.py [salida.pdf] [agrupado|detalle]

Propuesta cerrada (sin opciones), solo tablas:
  Hoja 1) portada delgada (destino y, debajo, el nombre del cliente) + tabla de Vuelos + tabla de Hoteles + tabla de Servicios adicionales + costo agrupado y total
  Hoja 2) notas y políticas de cancelación + firma
Si algo no cabe, el documento crece solo: los bloques se miden y pasan a la hoja siguiente.
MODO (preguntar a Mariana cada vez): 'agrupado' → tres cifras y total · 'detalle' → además, el costo de cada concepto en su tabla.
Para una cotización nueva: copia esta carpeta y cambia SOLO los datos y la foto de portada."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import tsl_base as B
import tsl_formato as F

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'salida.pdf').resolve()
MODO = sys.argv[2] if len(sys.argv) > 2 else 'agrupado'
B.TRIP = 'Marrakech · La Mamounia'
TITLE = 'Marrakech · La Mamounia · Cotización'

# ───────────────────────── datos ─────────────────────────
N_PAX = 2
PORTADA = dict(img='img/marrakech_band.jpg', title='Marrakech', cliente='Nombre del Cliente',   # bajo el destino va SIEMPRE el nombre del cliente
               rows=[('Fechas', '14 – 19 mar 2027'), ('Viajeros', '2 personas'), ('Documento', 'Cotización')])

# vuelos: grupos para F.flights_table + costo total de los vuelos
VUELOS = [('Ida · 14 – 15 mar', [
              ('14 mar', 'Iberia', 'IB 304', 'México (MEX)', 'Madrid (MAD)', 'Business', '12:50', '06:00<sup>+1</sup>', '10 h 10 m'),
              ('15 mar', 'Iberia', 'IB 1853', 'Madrid (MAD)', 'Marrakech (RAK)', 'Business', '11:50', '12:50', '2 h 00 m')]),
          ('Regreso · 18 – 19 mar', [
              ('18 mar', 'Iberia', 'IB 1856', 'Marrakech (RAK)', 'Madrid (MAD)', 'Business', '16:30', '19:30', '2 h 00 m'),
              ('18 mar', 'Iberia', 'IB 303', 'Madrid (MAD)', 'México (MEX)', 'Business', '23:55', '05:10<sup>+1</sup>', '12 h 15 m')])]
VUELOS_USD = 12713
VUELOS_NOTAS = ['Escalas en Madrid: 5 h 50 m a la ida y 4 h 25 m al regreso. Los tramos Madrid – Marrakech los opera Iberia Express.',
                'Dos maletas documentadas y equipaje de mano por persona.',
                'Tarifa Business Optima: cambios con cargo, no reembolsable; selección de asiento con cargo.']

# (fechas, noches, hotel, estrellas, destino, habitación, régimen, USD)
HOTELES = [('15 – 18 mar', 3, 'La Mamounia', 5, 'Marrakech', 'Classic Hivernage Twin', 'Solo alojamiento', 2796)]

# (fecha, servicio, detalle, horario, USD)
SERVICIOS = [('Lun 15 mar', 'Traslado privado', 'Aeropuerto Marrakech-Menara – La Mamounia · Mercedes-Benz Clase V', '12:50', 192.89),
             ('Mar 16 mar', 'Excursión privada', 'Valle de Imlil &amp; Alto Atlas · día completo con guía y comida bereber', '8:00', 165.34),
             ('Jue 18 mar', 'Traslado privado', 'La Mamounia – Aeropuerto Marrakech-Menara · Mercedes-Benz Clase V', '13:30', 192.89)]

GRUPOS = [('Vuelos', 'Business · 2 personas', VUELOS_USD),
          ('Hospedaje', '3 noches · 1 habitación', sum(h[-1] for h in HOTELES)),
          ('Servicios adicionales', '2 traslados privados · 1 excursión', sum(s[-1] for s in SERVICIOS))]
NOTA_PRECIO = ('Vuelos cotizados en dólares. Hotel en dirhams marroquíes: MAD 27,297 con impuestos (1 USD = 9.76 MAD). Traslados y excursión en euros '
               '(1 EUR = 1.1022 USD). Los montos en USD pueden variar con el tipo de cambio del día de pago. La excursión es un precio de referencia, '
               'por confirmar al reservar.')
PIE_PRECIO = 'Importes en dólares americanos. Tipos de cambio y condiciones en la hoja de notas.'

INCLUYE = ['Vuelos México – Marrakech – México en Business con Iberia, vía Madrid, para 2 personas.',
           'Alojamiento por 3 noches en La Mamounia, Classic Hivernage Twin, con IVA, cargo de servicio e impuesto municipal.',
           'Traslados privados aeropuerto – hotel – aeropuerto, hasta 6 pasajeros y 6 maletas.',
           'Excursión privada al valle de Imlil: transporte desde el hotel, guía de habla inglesa y comida.']
EXCLUYE = ['Desayuno en el hotel (aprox. MAD 490 por adulto, por día).',
           'Selección de asientos en los vuelos.',
           'Alimentos y bebidas no especificados, tratamientos de spa y gastos personales.',
           'Propinas y seguro de viaje.']
RESERVAR = ('Precios consultados el 16 de noviembre de 2026, sujetos a disponibilidad al momento de reservar. Los vuelos se garantizan al emitir los boletos. '
            'El hotel se garantiza con tarjeta de crédito y la estancia se paga directamente en el hotel, en MAD.')
GENERAL = ['Los precios, disponibilidad e inclusiones pueden cambiar hasta confirmar cada reserva.',
           'El cliente es responsable de contar con pasaporte vigente y los documentos de viaje requeridos.',
           'Se recomienda ampliamente contratar un seguro de viaje que cubra emergencias médicas, cancelaciones y demoras.',
           'Check-in del hotel a partir de las 15:00; check-out antes de las 12:00.']
# cancelación por concepto: (concepto, [(periodo, cargo)])
CANCELACION = [('Vuelos', [('Una vez emitidos', 'No reembolsables · cambios con cargo')]),
               ('Hotel', [('Hasta el 22 feb 2027, 15:00 h', 'Sin cargo'), ('Del 22 feb al 14 mar 2027', '50% de la estancia'),
                          ('Desde el 14 mar 2027, 15:00 h · No Show', '100% de la estancia')]),
               ('Traslados', [('Hasta 4 horas antes del servicio', 'Sin cargo')]),
               ('Excursión', [('Política del operador', 'Por confirmar al reservar')])]
CREDITOS = ''   # créditos de fotos, si la portada los requiere

# ───────────────────────── armado ─────────────────────────
def num(x): return f'{round(x):,}'
def usd(x): return f'US${round(x):,}'
det = MODO == 'detalle'
total = sum(g[2] for g in GRUPOS)
assert round(total) == sum(round(g[2]) for g in GRUPOS), 'los grupos redondeados no suman el total'
if det:
    assert round(total) == round(VUELOS_USD) + sum(round(h[-1]) for h in HOTELES) + sum(round(s[-1]) for s in SERVICIOS), 'el detalle redondeado no suma el total'

c_th = '<th class="c">USD</th>' if det else ''
def c_td(x): return f'<td class="c">{num(x)}</td>' if det else ''

b_vuelos = '<h2>Vuelos</h2>' + F.flights_table(VUELOS)
if det:
    b_vuelos = b_vuelos.replace('</table>', f'<tr class="sum"><td colspan="8">Vuelos · {N_PAX} personas · USD</td><td>{num(VUELOS_USD)}</td></tr></table>')

b_hoteles = ('<h2 class="sp">Hoteles</h2><table><tr><th style="width:.95in">Fechas</th><th style="width:.4in">Nts</th>' f'<th style="width:{2.35 if det else 2.75}in">Hotel</th>'
             f'<th>Habitación</th><th style="width:{1.15 if det else 1.3}in">Régimen</th>{c_th}</tr>'
             + ''.join(f'<tr><td class="g">{f}</td><td>{n}</td><td class="h">{h}{F.stars(st)}<span class="d">{d}</span></td><td>{room}</td><td>{reg}</td>{c_td(a)}</tr>'
                       for f, n, h, st, d, room, reg, a in HOTELES) + '</table>')

b_serv = ('<h2 class="sp">Servicios adicionales</h2><table><tr>' f'<th style="width:{.82 if det else .95}in">Fecha</th><th style="width:{1.08 if det else 1.2}in">Servicio</th><th>Detalle</th>'
          f'<th style="width:{.5 if det else .6}in">Horario</th>{c_th}</tr>'
          + ''.join(f'<tr><td class="g">{f}</td><td>{s}</td><td>{d}</td><td>{h}</td>{c_td(a)}</tr>' for f, s, d, h, a in SERVICIOS) + '</table>')

g3 = '' if det else ('<div class="g3">' + ''.join(f'<div><span class="lb">{r}</span><b>{num(a)}</b><span class="d">{d}</span></div>' for r, d, a in GRUPOS) + '</div>')
b_cot = ('<div class="cot"><h2 class="sp">Cotización</h2>' + g3 +
         f'<div class="total"><span class="lb">Total del viaje · {N_PAX} personas · USD</span><span class="pp">{usd(total / N_PAX)} por persona</span><b>{usd(total)}</b></div><p class="fine">{PIE_PRECIO}</p></div>')

canc = ''.join(''.join(f'<tr{" class=\"c1\"" if j == 0 else ""}><td class="cc">{c if j == 0 else ""}</td><td>{a}</td><td>{b}</td></tr>' for j, (a, b) in enumerate(rows))
               for c, rows in CANCELACION)
b_notas = (f'<h2 class="nt">Notas &amp; Cancelación</h2><div class="cols">'
           f'<div>{F.notes("El precio incluye", INCLUYE)}{F.notes("El precio excluye", EXCLUYE)}{F.notes("Sobre los precios", NOTA_PRECIO)}</div>'
           f'<div>{F.notes("Sobre los vuelos", VUELOS_NOTAS)}{F.notes("Para reservar", RESERVAR)}{F.notes("Información general", GENERAL)}</div></div>')
b_canc = ('<h4 class="ch">Políticas de cancelación</h4>'
          f'<table class="canc"><tr><th style="width:1.2in">Concepto</th><th>Periodo de aviso</th><th style="width:2.6in">Cargo por cancelación</th></tr>{canc}</table>'
          + (f'<p class="cr">{CREDITOS}</p>' if CREDITOS else ''))

EXTRA = '''
.rap.cq .rband { height:2.22in; }
.rap.cq .bcard { top:.34in; width:5.9in; padding:.26in .34in .24in; display:grid; grid-template-columns:1fr auto; column-gap:.4in; align-items:end; }
.rap.cq .bcard h1 { margin-top:.2in; }
.rap.cq .bcard dl { margin:0 0 .03in; }
.rap.cq.first .in { top:2.52in; }
.rap.cq h2 { font-size:16.5pt; margin:0 0 .07in; }
.rap.cq h2.sp { margin-top:.21in; }
.rap.cq table { margin-top:0; }
.rap.cq th { padding-bottom:.07in; }
.rap.cq td { padding:.074in .1in .064in 0; }
.rap.cq td.h { font:300 11.5pt/1.2 'IvyOra'; color:var(--ink); white-space:nowrap; }
.rap.cq td.h .d { font:300 7.8pt 'Karla'; color:var(--soft); margin-left:.1in; }
.rap.cq td.h .stars { display:inline-flex; gap:.025in; margin-left:.08in; vertical-align:.05em; }
.rap.cq td.h .stars svg { width:.095in; height:.095in; fill:#A8937B; }
.rap.cq .flights td { padding-top:.07in; padding-bottom:.06in; }
.rap.cq .flights tr.grp td { padding-top:.11in; padding-bottom:.05in; }
.rap.cq th.c, .rap.cq td.c { text-align:right; width:.62in; padding-right:.14in; }
.rap.cq tr.sum td:last-child { padding-right:.14in; }
.rap.cq td.c { font:300 11.5pt 'IvyOra'; color:var(--ink); }
.rap.cq tr.sum td { font:400 6.6pt 'Karla'; letter-spacing:.2em; text-transform:uppercase; color:var(--stone); text-align:right; border-bottom:0; }
.rap.cq tr.sum td:last-child { font:300 11.5pt 'IvyOra'; letter-spacing:0; color:var(--ink); }
.rap.cq .g3 { display:grid; grid-template-columns:repeat(3, 1fr); column-gap:.3in; border-top:.5pt solid var(--stone); padding-top:.12in; }
.rap.cq .g3 div + div { border-left:.5pt solid var(--oat); padding-left:.3in; margin-left:-.15in; }
.rap.cq .g3 b { display:block; font:200 18pt/1.1 'IvyOra'; margin:.05in 0 .02in; }
.rap.cq .g3 .d { font:300 7.6pt 'Karla'; color:var(--soft); }
.rap.cq .total { display:flex; justify-content:space-between; align-items:center; background:var(--oat); color:var(--ink); margin:.16in 0 0; padding:.15in .22in; }
.rap.cq .cot > h2 + .total { margin-top:0; }
.rap.cq .total .lb { font-size:7pt; letter-spacing:.2em; color:var(--ink); }
.rap.cq .total .pp { font:300 8.2pt 'Karla'; color:var(--soft); margin-left:auto; margin-right:.22in; }
.rap.cq .total b { font:200 22pt/1 'IvyOra'; }
.rap.cq .fine { margin-top:.11in; font:300 7.1pt/1.5 'Karla'; color:var(--soft); }
.rap.cq .cot.alone h2.sp { margin-top:0; }
.rap.cq h2.nt { font-size:26pt; margin:0; }
.rap.cq h2.nt.sp { margin-top:.45in; }
.rap.cq .cols { display:grid; grid-template-columns:1fr 1fr; column-gap:.55in; margin-top:.3in; }
.rap.cq.notes ul, .rap.cq.notes .cols p { margin-bottom:.19in; }
.rap.cq.notes li, .rap.cq.notes .cols p { font-size:8pt; line-height:1.5; }
.rap.cq.notes .canc td { padding-top:.075in; padding-bottom:.065in; }
.rap.cq .canc td.cc { color:var(--ink); font-weight:400; }
.rap.cq .canc td { border-bottom:0; border-top:.5pt solid var(--oat); }
.rap.cq .canc tr:not(.c1) td { border-top:0; padding-top:0; }
.rap.cq .canc { border-bottom:.5pt solid var(--oat); }
.rap .cr { font:300 6.5pt/1.5 'Karla'; color:var(--stone); margin-top:.16in; }
'''
CSS_ALL = F.RAPIDA_CSS + EXTRA

# reparto en hojas: se mide cada bloque y lo que no cabe pasa a la hoja siguiente
blocks = [b_vuelos, b_hoteles, b_serv, b_cot, b_notas, b_canc]
hs = F.measure(blocks, ROOT, CSS_ALL, '<div class="page rap cq notes"><div class="in">{}</div></div>')
FIRST, CAP = 7.72, 8.25           # alto útil (in) de la hoja 1 (bajo la portada) y de las siguientes (dejan sitio a la firma)
first = F.fit(hs[:4], FIRST, 99)[0]                         # qué tablas caben bajo la portada
rest = list(range(len(first), len(blocks)))
later = [[rest[i] for i in p] for p in F.fit([hs[i] + (.5 if i == 4 and rest[0] != 4 else 0) for i in rest], CAP, CAP)]

def portada(img, title, cliente, rows):
    dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
    return (f'<div class="rband"><img src="{img}"></div>'
            f'<div class="bcard"><div>{F.logo(1)}<h1>{title}</h1><p class="sub">{cliente}</p></div><dl>{dl}</dl></div>')

pages = [f'''<div class="page rap cq first notes">{portada(**PORTADA)}
  <div class="bot">{F.logo(2)}<span>01</span></div>
  <div class="in">{''.join(blocks[i] for i in first)}</div>
</div>''']
for n, idx in enumerate(later, 2):
    html = ''.join(blocks[i] for i in idx)
    if idx[0] == 3: html = html.replace('class="cot"', 'class="cot alone"')
    if 4 in idx and idx[0] != 4: html = html.replace('class="nt"', 'class="nt sp"')
    name = 'Notas' if 4 in idx or 5 in idx else 'Cotización'
    pages.append(f'''<div class="page rap cq notes">{F.furniture(f'.{n:02d}', name, n, link='#')}
  <div class="in">{html}</div>{F.sign() if n == len(later) + 1 else ''}</div>''')

F.print_pdf(F.html_doc(TITLE, '\n'.join(pages), CSS_ALL), OUT, ROOT)
print('PDF ->', OUT, '·', MODO, '· total', usd(total), '· hojas', len(pages), '· altos', [round(h, 2) for h in hs])
