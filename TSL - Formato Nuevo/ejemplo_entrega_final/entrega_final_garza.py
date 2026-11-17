#!/usr/bin/env python3
"""TSL · Entrega Final (Formato Nuevo) — ejemplo canónico: Familia Garza · Europa & África, julio 2026.
Uso: python3 entrega_final_garza.py [salida.pdf]
Hojas: portada · índice · resumen · vuelos · hoteles · apertura · itinerario diario · una hoja por hotel ·
confirmaciones de vuelos, hoteles y restaurantes · cierre.
Para un viaje nuevo: copia esta carpeta, cambia datos_garza.py, los bloques de portada y mapa de este archivo y las fotos."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import tsl_base as B
import tsl_formato as F
import datos_garza as D

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'salida.pdf').resolve()
B.TRIP = 'Europa &amp; África · Julio 2026'
TITLE = 'Europa & África · Familia Garza · Entrega Final'

# ───────────────────────── portada, mapa y textos fijos ─────────────────────────
PORTADA = dict(img='img/cover.jpg', title='Europa &amp; África', t2='Madrid · Londres · Nairobi · Serengeti', client='Familia Garza', t2_small=True,
               rows=[('Fechas', '5 – 21 jul 2026'), ('Viajeros', '10 personas · 16 noches'), ('Documento', 'Entrega Final')])
PARA = 'Familia Garza<br>10 personas'
MAPA = dict(bbox=(-21.0, 53.0, -7.5, 59.5), width=4.55, trip=['724', '826', '404', '834'],
            stops=[('Madrid', -3.70, 40.42, 8, 3, [1, 6]), ('Londres', -0.13, 51.51, 8, 3, [2]), ('Nairobi', 36.82, -1.29, 8, 0, [3]),
                   ('Serengeti', 34.4, -2.2, -8, 6, [4, 5])],
            labels=[(-3.9, 37.9, 'ESPAÑA'), (-1.9, 55.6, 'REINO UNIDO'), (38.0, 1.9, 'KENIA'), (35.0, -5.6, 'TANZANIA')])
EMERGENCIA = ('Contacto de emergencia', 'Nuba México (24 h)', [('55 5255 4455', '+525552554455'), ('55 5250 6277', '+525552506277')])
CAPS = {'madrid': 'Madrid', 'london': 'Londres', 'towerbridge': 'Tower Bridge', 'bigben': 'Westminster', 'cotswolds': 'Cotswolds',
        'elephants': 'Sabana', 'wildebeest': 'La Gran Migración', 'safari': 'Safari', 'lion': 'Serengeti', 'elephant': 'Sabana',
        'retiro': 'Parque del Retiro', 'plazamayor': 'Plaza Mayor'}
FOTOS_HOTEL = [['rosewood_1', 'rosewood_2', 'rosewood_3', 'rosewood_4'], ['fourseasons_1', 'fourseasons_2', 'fourseasons_3', 'fourseasons_4'],
               ['fourpoints_1', 'fourpoints_2'], ['grumeti_1', 'grumeti_2', 'grumeti_3'], ['singita_1', 'singita_2', 'singita_3']]
PUNTO_HOTEL = [1, 2, 3, 4, 5]          # número de etapa de cada hoja de hotel
CREDITOS = ('Fotografías de hoteles: biblioteca de The Suite Life y sitios oficiales de Rosewood Villa Magna y Four Seasons London at Park Lane. '
            'Portada, apertura e itinerario, vía Unsplash: @hitobywong, @highteawithelephants, @alexazabache, @josilito, @fabiankuehne, @yoavaziz, '
            '@shawnanggg, @audie_rae_08, @timbar, @aguyonecam, @oemerkarakus y @lucasricci.')

EXTRA = '''
.conf h1 { font-size:34pt; }
.conf .grp { margin-top:.3in; }
.conf h1 + .grp { margin-top:.42in; }
.conf .grp .lb { display:block; }
.conf .grp .nm { font:300 7.4pt/1.5 'Karla'; color:var(--ink); margin:.05in 0 .08in; }
.conf table { margin-top:0; }
.conf th { background:var(--oat); color:var(--ink); border-bottom:0; padding:.1in .1in .09in 0; }
.conf th:first-child, .conf td:first-child { padding-left:.14in; }
.conf th:last-child, .conf td:last-child { padding-right:.14in; }
.conf td { padding:.064in .1in .056in 0; font-size:8.6pt; line-height:1.25; vertical-align:middle; }
.conf td.b { font-weight:700; white-space:nowrap; }
.conf td.k { font-weight:700; letter-spacing:.05em; white-space:nowrap; }
.conf td span { display:block; font-size:7.8pt; color:var(--soft); margin-top:.01in; }
.conf td.h { font:300 11.5pt/1.2 'IvyOra'; }
.conf .hc { margin-top:.3in; }
.conf h1 + .hc { margin-top:.42in; }
.conf .hh { display:flex; align-items:center; gap:.14in; }
.conf .hh h3 { font:200 18pt/1.1 'IvyOra'; }
.conf .hh .stars { display:inline-flex; gap:.03in; }
.conf .hh .stars svg { width:.11in; height:.11in; fill:#A8937B; }
.conf .inf { font:300 8.4pt/1.5 'Karla'; color:var(--soft); margin:.04in 0 .1in; }
.conf .inc { font:300 7.8pt/1.5 'Karla'; color:var(--soft); margin-top:.09in; }
'''

# ───────────────────────── armado ─────────────────────────
def v_block(g, first=False):
    names, rows = g
    return (f'<div class="pax{"" if first else " nx"}"><span class="lb">Pasajeros</span><p class="names">{names}</p></div>'
            + F.flights_table([(None, rows)]))
def cv_block(g):
    names, rows = g
    trs = ''.join(f'<tr><td class="b">{f}</td><td>{ruta}</td><td>{v}</td><td>{c}</td><td>{s}</td><td>{e}</td><td class="k">{cod}</td></tr>'
                  for f, ruta, v, c, s, e, cod in rows)
    return (f'<div class="grp"><span class="lb">Pasajeros</span><p class="nm">{names}</p><table><tr><th style="width:.72in">Fecha</th>'
            f'<th>Ruta</th><th style="width:.72in">Vuelo</th><th style="width:1.0in">Clase</th><th style="width:1.45in">Asientos</th>'
            f'<th style="width:.85in">Equipaje</th><th style="width:.85in">Código</th></tr>{trs}</table></div>')
def ch_block(h):
    trs = ''.join(f'<tr><td>{a}</td><td class="k">{b}</td></tr>' for a, b in h['rooms'])
    return (f'<div class="hc"><div class="hh"><h3>{h["hotel"]}</h3>{F.stars(h["stars"])}</div><p class="inf">{h["loc"]} &nbsp;·&nbsp; {h["info"]}</p>'
            f'<table><tr><th>Huéspedes y habitación</th><th style="width:1.6in">Confirmación</th></tr>{trs}</table><p class="inc">{h["incl"]}</p></div>')

# reparto en hojas con alturas medidas (la primera hoja lleva el título)
CSS_ALL = F.DOC_CSS + EXTRA
FIRST, CAP = 8.3, 9.1
v_pages = F.fit(F.measure([v_block(g) for g in D.VUELOS], ROOT, CSS_ALL, '<div class="page fly c"><div class="in">{}</div></div>'), FIRST, CAP)
cv_pages = F.fit(F.measure([cv_block(g) for g in D.CONF_VUELOS], ROOT, CSS_ALL, '<div class="page conf"><div class="in">{}</div></div>'), FIRST, CAP)
ch_pages = F.fit(F.measure([ch_block(h) for h in D.CONF_HOTELES], ROOT, CSS_ALL, '<div class="page conf"><div class="in">{}</div></div>'), FIRST, CAP)
print('vuelos:', v_pages, '· conf. vuelos:', cv_pages, '· conf. hoteles:', ch_pages)
# itinerario
HS, it_pages = F.paginate_days(D.DIAS, ROOT, F.DOC_CSS)
print('itinerario:', it_pages)

NV, NI, NH = len(v_pages), len(it_pages), len(D.HOJAS_HOTEL)
P_RES, P_VUE = 3, 4
P_HOT = P_VUE + NV; P_OPEN = P_HOT + 1; P_IT = P_OPEN + 1; P_HH = P_IT + NI
P_CV = P_HH + NH; P_CH = P_CV + len(cv_pages); P_CR = P_CH + len(ch_pages)
S_CV, S_CH, S_CR = 5 + NH, 6 + NH, 7 + NH

INDEX = ([(1, 'Resumen', P_RES), (2, 'Vuelos', P_VUE), (3, 'Hoteles', P_HOT), (4, 'Itinerario Diario', P_OPEN)]
         + [(5 + k, h['name'], P_HH + k) for k, h in enumerate(D.HOJAS_HOTEL)]
         + [(S_CV, 'Confirmaciones · Vuelos', P_CV), (S_CH, 'Confirmaciones · Hoteles', P_CH), (S_CR, 'Confirmaciones · Restaurantes', P_CR)])

pages = [F.cover_page(**PORTADA), F.index_page(INDEX, PARA, label='Preparado para')]

# resumen
st_rows = ''.join(f'<tr><td>{F.dot(n)}</td><td class="f">{f}</td><td>{nt}</td><td>{d}</td><td>{p}</td><td>{a}</td></tr>'
                  for n, (f, nt, d, p, a) in enumerate(D.ETAPAS, 1))
tel = ' &nbsp;·&nbsp; '.join(f'<a href="tel:{t}">{s}</a>' for s, t in EMERGENCIA[2])
pages.append(f'''<div class="page res" id="s1">{F.furniture('.01', 'Resumen', P_RES)}<div class="in"><h1>Resumen</h1>
  {F.map_svg(**MAPA)}
  <table class="stages"><tr><th style="width:.35in">#</th><th style="width:1.2in">Fechas</th><th style="width:.75in">Noches</th>
    <th style="width:1.5in">Destino</th><th style="width:1.05in">País</th><th>Alojamiento</th></tr>{st_rows}</table>
  <div class="emer"><span class="lb">{EMERGENCIA[0]}</span><p>{EMERGENCIA[1]} &nbsp;·&nbsp; {tel}</p></div>
</div></div>''')

# vuelos
for k, chunk in enumerate(v_pages):
    h1 = '<h1>Vuelos</h1>' if k == 0 else ''
    pages.append(f'''<div class="page fly c"{' id="s2"' if k == 0 else ''}>{F.furniture('.02', 'Vuelos', P_VUE + k)}
  <div class="in">{h1}{''.join(v_block(D.VUELOS[i], j == 0 and k == 0) for j, i in enumerate(chunk))}</div></div>''')

# hoteles (tabla)
h_rows = ''.join(f'<tr><td>{F.dot(n)}</td><td class="g">{f}</td><td>{nt}</td><td>{d}</td><td class="h">{h}</td>'
                 f'<td class="r"><b>{room}</b><span>{plan}</span></td></tr>' for n, (f, nt, d, h, room, plan) in enumerate(D.HOTELES, 1))
pages.append(f'''<div class="page hot" id="s3">{F.furniture('.03', 'Hoteles', P_HOT)}<div class="in"><h1>Hoteles</h1>
  <table><tr><th style="width:.38in">#</th><th style="width:.95in">Fechas</th><th style="width:.38in">Nts</th><th style="width:1.42in">Destino</th>
    <th style="width:2.25in">Hotel</th><th>Habitación / Régimen</th></tr>{h_rows}</table></div></div>''')

# itinerario
pages.append(F.opener_page('img/opener.jpg', '.04', 'Itinerario Diario', 's4'))
pages.append(F.itin_pages(D.DIAS, HS, it_pages, P_IT, CAPS))

# una hoja por hotel
for k, h in enumerate(D.HOJAS_HOTEL):
    facts = [('Fechas', h['fechas']), ('Noches', h['noches']), ('Habitación', h['room']), ('Régimen', h['plan'])]
    pages.append(F.hotel_sheet(f'.{5 + k:02d}', P_HH + k, f's{5 + k}', PUNTO_HOTEL[k], h['name'], h['loc'], h['stars'], facts, h['desc'],
                               [f'himg/{p}.jpg' for p in FOTOS_HOTEL[k]]))

# confirmaciones · vuelos
for k, chunk in enumerate(cv_pages):
    h1 = '<h1>Confirmaciones · Vuelos</h1>' if k == 0 else ''
    blocks = ''.join(cv_block(D.CONF_VUELOS[i]) for i in chunk)
    pages.append(f'''<div class="page conf"{f' id="s{S_CV}"' if k == 0 else ''}>{F.furniture(f'.{S_CV:02d}', 'Confirmaciones', P_CV + k)}
  <div class="in">{h1}{blocks}</div></div>''')

# confirmaciones · hoteles
for k, chunk in enumerate(ch_pages):
    h1 = '<h1>Confirmaciones · Hoteles</h1>' if k == 0 else ''
    blocks = ''.join(ch_block(D.CONF_HOTELES[i]) for i in chunk)
    pages.append(f'''<div class="page conf"{f' id="s{S_CH}"' if k == 0 else ''}>{F.furniture(f'.{S_CH:02d}', 'Confirmaciones', P_CH + k)}
  <div class="in">{h1}{blocks}</div></div>''')

# confirmaciones · restaurantes
r_rows = ''.join(f'<tr><td class="b">{f}</td><td>{hr}</td><td>{pax}</td><td class="h">{n}<span style="font:300 7.8pt Karla">{addr}</span></td><td>{tit}</td></tr>'
                 for f, hr, pax, n, addr, tit in D.RESTAURANTES)
pages.append(f'''<div class="page conf" id="s{S_CR}">{F.furniture(f'.{S_CR:02d}', 'Confirmaciones', P_CR)}
  <div class="in"><h1>Confirmaciones · Restaurantes</h1><div class="grp"><table><tr><th style="width:.72in">Fecha</th><th style="width:.8in">Hora</th>
    <th style="width:.5in">Pax</th><th>Restaurante</th><th style="width:1.5in">Titular</th></tr>{r_rows}</table></div></div></div>''')

pages.append(F.closing_page(CREDITOS))
F.print_pdf(F.html_doc(TITLE, '\n'.join(pages), CSS_ALL), OUT, ROOT)
print('PDF ->', OUT)
