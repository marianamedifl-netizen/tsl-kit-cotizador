#!/usr/bin/env python3
"""TSL · Cotización Completa (Formato Nuevo) — ejemplo canónico: Laponia · Opción 2.
Uso: python3 cotizacion_completa_laponia.py [salida.pdf]
Para una cotización nueva: copia esta carpeta, cambia SOLO los bloques de datos (mapa, DAYS, HOTELS,
textos de portada/vuelos/hoteles/cotización/notas) y las fotos de img/ y himg_g/. No cambies el CSS."""
import sys, math, subprocess, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import tsl_base as B
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'salida.pdf').resolve()
B.TRIP = 'Laponia · Año Nuevo Ártico'
entry, frow, notes = B.entry, B.frow, B.notes
def logo(n, cls=''):
    return B.logo(n, cls).replace('viewBox="203 468 673 143"', 'viewBox="203 464 673 152"')
def furniture(num, name, page):
    return (f'<div class="top"><span><i>{num}</i>{name}</span><span>{B.TRIP}</span></div>'
            f'<div class="bot"><a href="#indice">{logo(2)}</a><span>{page:02d}</span></div>')

# ───────────────────────── mapa ─────────────────────────
B.LON0, B.LON1, B.LAT0, B.LAT1 = 4.0, 32.0, 55.1, 71.4
B.K = math.cos(math.radians((B.LAT0 + B.LAT1) / 2))
B.MAP_W, B.MAP_H = (B.LON1 - B.LON0) * B.K * B.S, (B.LAT1 - B.LAT0) * B.S
proj = B.proj
STOPS = [('Helsinki', 24.94, 60.17, 8, 3), ('Rovaniemi', 25.73, 66.50, 8, 3), ('Muonio', 23.9, 67.96, 8, 1),
         ('Fjellborg', 21.2, 67.9, -8, -6), ('Estocolmo', 18.07, 59.33, -8, 3)]
def map_svg():
    cp = B.country_paths({'246', '752', '578'})
    pts = [proj(lo, la) for _, lo, la, _, _ in STOPS]
    route = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    ac_y = proj(0, 66.56)[1]
    out = [f'<svg class="map" viewBox="0 0 {B.MAP_W:.1f} {B.MAP_H:.1f}" xmlns="http://www.w3.org/2000/svg">',
           f'<path d="{cp["578"]}" fill="#F0EDE8" stroke="#FCF9F5" stroke-width=".5" fill-rule="evenodd"/>',
           f'<path d="{cp["752"]}" fill="#DFD3C5" stroke="#FCF9F5" stroke-width=".5" fill-rule="evenodd"/>',
           f'<path d="{cp["246"]}" fill="#DFD3C5" stroke="#FCF9F5" stroke-width=".5" fill-rule="evenodd"/>',
           f'<path d="M0,{ac_y:.1f} L{B.MAP_W:.1f},{ac_y:.1f}" stroke="#7D766C" stroke-width=".35" stroke-dasharray=".8 2.2" fill="none"/>',
           f'<text class="it" x="2" y="{ac_y - 3:.1f}">Círculo Polar Ártico</text>',
           ]
    for lon, lat, t in [(15.2, 62.6, 'SUECIA'), (26.6, 63.2, 'FINLANDIA'), (9.3, 61.6, 'NORUEGA')]:
        x, y = proj(lon, lat); out.append(f'<text class="rg" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{t}</text>')
    for n, ((name, lo, la, dx, dy), (x, y)) in enumerate(zip(STOPS, pts), 1):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#232323"/>'
                   f'<text x="{x:.1f}" y="{y + 1.9:.1f}" text-anchor="middle" style="font:500 5.4px Karla;fill:#FCF9F5">{n}</text>'
                   f'<text class="ct b" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{"start" if dx > 0 else "end"}">{name}</text>')
    return '\n'.join(out) + '</svg>'

# ───────────────────────── itinerario (datos del documento original) ─────────────────────────
A = 'Alojamiento en '
DAYS = [
 ('Sábado 26 de diciembre', 'Ciudad de México', None, [
   ('7:45 PM', 'Vuelo LH 521 · México – Múnich', 'Lufthansa · Business · llegada a Múnich el 27 Dic a la 1:45 PM')]),
 ('Domingo 27 de diciembre', 'Helsinki', 'helsinki', [
   ('3:10 PM', 'Vuelo LH 2462 · Múnich – Helsinki', 'Lufthansa · Business · llegada a Helsinki a las 6:45 PM'),
   ('6:45 PM', 'Traslado privado Aeropuerto de Helsinki – hotel', 'Minivan Business (V-Class o similar)'),
   ('', A + 'Waldorf Astoria Helsinki', 'One Bedroom Suite con cama extra comunicada con Grand Deluxe Room')]),
 ('Lunes 28 de diciembre', 'Helsinki – Rovaniemi', 'aurora', [
   ('', 'Traslado privado hotel – Aeropuerto de Helsinki', 'Minivan Business (V-Class o similar)'),
   ('7:10 AM', 'Vuelo AY 541 · Helsinki – Rovaniemi', 'Finnair · Economy · llegada a Rovaniemi a las 8:40 AM'),
   ('', 'Check-in en Hidden Arctic Cloud Villa', 'Cena de bienvenida de 5 tiempos preparada por su chef privado.'),
   ('', 'Cacería de auroras boreales en auto con su anfitrión', ''),
   ('', A + 'Hidden Arctic Cloud Villa', 'Chef privado · todas las comidas')]),
 ('Martes 29 de diciembre', 'Rovaniemi', 'reindeer', [
   ('', 'Paseo en trineo en una granja de renos auténtica', 'Conozcan la vida de un pastor sámi y deslícense por el bosque nevado en un trineo tradicional; fogata, bebidas calientes e historias en un tipi lapón.'),
   ('', 'Almuerzo en un tipi lapón', 'Sopa, crepas finlandesas y jugo caliente, servidos por chef junto al fuego.'),
   ('', A + 'Hidden Arctic Cloud Villa', '')]),
 ('Miércoles 30 de diciembre', 'Rovaniemi', None, [
   ('', 'Visita privada a Santa Claus Secret Forest · Magical Toy Factory', 'Aprox. 2.5 horas en el taller de juguetes de los duendes, con el gran libro de deseos, encuentro privado con Santa Claus y un regalo especial.'),
   ('', 'Cacería de auroras boreales en auto con su anfitrión', ''),
   ('', A + 'Hidden Arctic Cloud Villa', '')]),
 ('Jueves 31 de diciembre', 'Rovaniemi', 'nye', [
   ('', 'Motos de nieve eléctricas', 'Recorrido silencioso por pistas privadas en el bosque, con pausa en una cabaña lapona junto a la chimenea. Niños menores de 140 cm van en trineo.'),
   ('', 'Fin de Año en Santa Claus Secret Forest', 'Después de la cena, celebración de Año Nuevo con lectura tradicional de la fortuna.'),
   ('', A + 'Hidden Arctic Cloud Villa', '')]),
 ('Viernes 1 de enero', 'Rovaniemi', 'icehotel', [
   ('', 'Visita al Arctic Snow Hotel', 'Recorrido guiado de 3 horas por el hotel de nieve y hielo: restaurante, capilla, bar y esculturas.'),
   ('', 'Sauna de nieve y jacuzzi', 'Traigan traje de baño.'),
   ('', 'Almuerzo de sopa en el Ice Restaurant', ''),
   ('', A + 'Hidden Arctic Cloud Villa', '')]),
 ('Sábado 2 de enero', 'Rovaniemi', None, [
   ('', 'Ice karting privado', 'Aprox. 2 horas con traslados. Edad mínima 10 años y 150 cm para conducir; peso máximo 100 kg.'),
   ('', A + 'Hidden Arctic Cloud Villa', '')]),
 ('Domingo 3 de enero', 'Rovaniemi – Muonio', 'huskyf', [
   ('', 'Traslado privado a Muonio con parada en Levi', 'Aprox. 4.5 horas; almuerzo en Levi a pagar directamente.'),
   ('', 'Safari privado con huskies bajo las auroras', '2 horas, 4–6 km, con fogata y bebidas calientes en una kota lejos de las luces de la ciudad.'),
   ('', A + 'Arcora Boutique Hotel &amp; Villas', '2x Junior Suite Kalle comunicadas')]),
 ('Lunes 4 de enero', 'Muonio', 'convoy', [
   ('', 'Safari privado en moto de nieve', '3 horas, 20–30 km en 2 motos de nieve. Menores de 14 años viajan en trineo.'),
   ('', 'Cena privada de 4 tiempos en una kota auténtica', '3.5 horas: un chef privado prepara cada tiempo al fuego con ingredientes del bosque y los lagos de Laponia.'),
   ('', A + 'Arcora Boutique Hotel &amp; Villas', '')]),
 ('Martes 5 de enero', 'Muonio', 'saunaf', [
   ('', 'Caminata privada con raquetas de nieve en el parque nacional', 'Aprox. 3.5 horas con traslados.'),
   ('', 'Private Shaman Mystery Tour', 'Aprox. 2 horas en una cabaña sámi junto a un lago congelado, con cantos joik y relatos de su pueblo.'),
   ('', 'Experiencia exclusiva de sauna ártica', '2.5 horas entre cinco saunas temáticas, jacuzzi y la opción de un baño en el hielo. Traigan traje de baño.'),
   ('', A + 'Arcora Boutique Hotel &amp; Villas', '')]),
 ('Miércoles 6 de enero', 'Muonio – Laponia Sueca', None, [
   ('', 'Traslado privado a la Laponia Sueca', 'Aprox. 3 horas hasta Fjellborg Homestead.'),
   ('', 'Trineo de perros privado a Fjellborg Arctic Lodge', 'Por la naturaleza invernal hasta el lago Väkkärä.'),
   ('', A + 'Fjellborg Arctic Lodge', 'Master Lodge de uso exclusivo · pensión completa')]),
 ('Jueves 7 de enero', 'Laponia Sueca', 'icefish', [
   ('', 'Raquetas de nieve y pesca en hielo privadas', 'Aprox. 2–3 horas desde el lodge; si pescan algo, el chef lo prepara para la cena.'),
   ('', 'Clase privada de escultura en hielo en ICEHOTEL', ''),
   ('', 'Ritual de sauna en el lodge', 'Traigan traje de baño.'),
   ('', A + 'Fjellborg Arctic Lodge', 'Pensión completa')]),
 ('Viernes 8 de enero', 'Laponia Sueca – Estocolmo', 'sthlm', [
   ('', 'Moto de nieve a Fjellborg Homestead y traslado privado al aeropuerto de Kiruna', ''),
   ('11:30 AM', 'Vuelo SK 1047 · Kiruna – Estocolmo', 'SAS · Business · llegada a Estocolmo Arlanda a la 1:15 PM'),
   ('1:15 PM', 'Traslado privado Aeropuerto de Arlanda – hotel', 'Minivan Business (V-Class o similar)'),
   ('', 'Caminata privada por Gamla Stan', 'Aprox. 2 horas por la Ciudad Vieja de Estocolmo.'),
   ('', A + 'Grand Hôtel Stockholm', 'Superior Suite Harbour View + Deluxe Harbour View')]),
 ('Sábado 9 de enero', 'Estocolmo – Ciudad de México', None, [
   ('', 'Traslado privado Grand Hôtel – Aeropuerto de Arlanda', 'Minivan Business (V-Class o similar)'),
   ('7:30 AM', 'Vuelo LH 2421 · Estocolmo – Múnich', 'Lufthansa · Business · llegada a Múnich a las 9:40 AM'),
   ('12:20 PM', 'Vuelo LH 520 · Múnich – México', 'Lufthansa · Business · llegada a México el mismo día a las 6:05 PM')]),
]
CAPS = {'helsinki': 'Helsinki', 'aurora': 'Auroras boreales', 'reindeer': 'Trineo de renos', 'nye': 'Noche ártica',
        'icehotel': 'Hotel de hielo', 'huskyf': 'Trineo de perros', 'convoy': 'Motos de nieve', 'saunaf': 'Sauna',
        'icefish': 'Pesca en hielo', 'sthlm': 'Estocolmo'}

def day_html(n, d, nh=None):
    date, place, _, ents = d
    if nh is None: nh = not any(e[0] for e in ents)
    return (f'<section class="dayf{" nh" if nh else ""}"><p class="dt">Día {n} &nbsp;·&nbsp; {date}</p><h3>{place}</h3>'
            f'<div class="ag">{"".join(entry(*e) for e in ents)}</div></section>')

HOTELS = [
 ((0,1,2,3), 5, 'Waldorf Astoria Helsinki', 'Helsinki, Finlandia', '27 – 28 dic', '1 noche', 'One Bedroom Suite + Grand Deluxe Room', 'Desayuno',
  'En el corazón de Helsinki, el Waldorf Astoria ocupa un elegante edificio histórico restaurado del siglo XIX que combina el encanto clásico con el lujo contemporáneo. Habitaciones refinadas con candelabros y baños tipo spa, un patio interior con jardín y fuente, restaurante de autor y centro de bienestar, a pasos de los principales sitios culturales y comerciales de la capital finlandesa: el inicio perfecto para el viaje nórdico.'),
 ((6,7,8,9), 0, 'Hidden Arctic Cloud Villa', 'Rovaniemi, Laponia Finlandesa', '28 dic – 03 ene', '6 noches', 'Villa privada de 3 recámaras', 'Chef privado',
  'Un refugio privado cerca de Rovaniemi que fusiona elegancia moderna y lujo lapón, con grandes ventanales hacia la naturaleza ártica. Incluye chef privado (cena de bienvenida de 5 tiempos, desayunos, comidas y cenas de 3 tiempos), selección diaria de snacks locales, vinos, licores y bebidas, ropa de invierno premium para todos, housekeeping con servicio de cortesía, sauna privada y jacuzzi exterior con vista al norte.'),
 ((12,13,15,14), 0, 'Arcora Boutique Hotel &amp; Villas', 'Torassieppi, Muonio · Laponia Finlandesa', '03 – 06 ene', '3 noches', '2x Junior Suite Kalle comunicadas', 'Desayuno',
  'En la aldea lacustre de Torassieppi, junto al Parque Nacional Pallas-Yllästunturi, Arcora es un hotel boutique de diseño nórdico construido alrededor de las vistas árticas y el ritmo de las ocho estaciones de Laponia. Sus Junior Suites Kalle, de 30 m², tienen ventanales a ras de piso que llevan el paisaje y el cielo nocturno directo a la cama; cuenta con saunas finlandesas tradicionales y piscina exterior infinita con vista al bosque.'),
 ((19,32,33,21), 0, 'Fjellborg Arctic Lodge', 'Lago Väkkärä · Laponia Sueca', '06 – 08 ene', '2 noches', 'Master Lodge de 4 recámaras (uso exclusivo)', 'Pensión completa',
  'Nueve generaciones de la familia Fjellborg han vivido en armonía con la naturaleza a orillas del río Torne, 200 km al norte del Círculo Polar Ártico. Su Master Lodge de uso exclusivo es una cabaña de troncos rústica y elevada, con estufas de leña, vigas expuestas y vistas al río. La cocina se inspira en el entorno —pescado, reno, bayas y hongos silvestres— e incluye pensión completa y ropa ártica Fjällräven.'),
 ((30,25,26,31), 5, 'Grand Hôtel Stockholm', 'Södra Blasieholmshamnen 8, Estocolmo, Suecia', '08 – 09 ene', '1 noche', 'Superior Suite + Deluxe Room Harbour View', 'Desayuno',
  'Desde 1874, el Grand Hôtel es la dirección más legendaria de Estocolmo: frente al Palacio Real y Gamla Stan, sobre el agua, ha recibido a premios Nobel, celebridades y viajeros exigentes. Alberga el clásico restaurante Veranda con su tradicional smörgåsbord, los galardonados restaurantes de Mathias Dahlgren, el Cadier Bar y un spa nórdico con saunas: el cierre perfecto para esta aventura invernal.'),
]

import tsl_formato as F
CSS = F.CSS

# ───────────────────────── paginar el itinerario midiendo alturas ─────────────────────────
def measure():
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
           f'<div id="c" style="width:4.45in">' + ''.join(day_html(i + 1, d) for i, d in enumerate(DAYS)) + '</div></body></html>')
    (ROOT / 'measure.html').write_text(doc, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_page(); pg.goto(f'file://{ROOT}/measure.html'); pg.wait_for_timeout(800)
        hs = pg.evaluate("[...document.querySelectorAll('.dayf')].map(e=>e.getBoundingClientRect().height/96)")
        b.close()
    return hs

HS = measure()
pages, cur, used = [], [], 0.0
for i, h in enumerate(HS):
    cap = 8.55
    extra = h + (0.24 if cur else 0)
    if cur and used + extra > cap:
        pages.append(cur); cur, used = [], 0.0; extra = h
    cur.append(i); used += extra
pages.append(cur)
print('alturas', [round(h, 2) for h in HS]); print('hojas', pages)

FIRST_ITIN = 7                                  # la hoja 6 es la apertura
def itin_pages():
    out = []
    for k, idxs in enumerate(pages):
        cap, want, y = 8.55, [], 0.0
        for i in idxs:                                   # cada foto arranca en la línea «DÍA n» de su día
            if DAYS[i][2]: want.append([y + 0.03, DAYS[i][2]])
            y += HS[i] + 0.24
        want = want[:2]
        assert len(want) >= 2, f'la hoja {k + 1} del itinerario necesita al menos 2 fotos'
        for j in range(1, len(want)): want[j][0] = max(want[j][0], want[j - 1][0] + 3.52)
        for j in range(len(want) - 1, -1, -1):
            lim = (cap - 3.3) if j == len(want) - 1 else want[j + 1][0] - 3.52
            want[j][0] = max(0.0, min(want[j][0], lim))
        side = ''.join(f'<figure style="top:{t:.2f}in"><img src="img/{ph}.jpg"><figcaption>{CAPS[ph]}</figcaption></figure>' for t, ph in want)
        top, title = '1.3in', ''
        out.append(f'''<div class="page">{furniture('.04', 'Itinerario Diario', FIRST_ITIN + k)}{title}
  <div class="itin{' flip' if k % 2 else ''}" style="top:{top}"><div class="side">{side}</div>
  <div class="days">{''.join(day_html(i + 1, DAYS[i], not any(e[0] for j in idxs for e in DAYS[j][3])) for i in idxs)}</div></div></div>''')
    return '\n'.join(out)

N_IT = len(pages); P_HOTEL = FIRST_ITIN + N_IT; P_COT = P_HOTEL + len(HOTELS); P_NOT = P_COT + 1

STAR = '<svg viewBox="0 0 20 20"><path d="M10 1.2l2.7 5.6 6.1.8-4.5 4.2 1.1 6-5.4-2.9-5.4 2.9 1.1-6L1.2 7.6l6.1-.8z"/></svg>'
def hotel_pages():
    out = []
    for k, (ids, stars, name, loc, dates, nights, room, plan, desc) in enumerate(HOTELS):
        st = f'<span class="stars">{STAR * stars}</span>' if stars else ''
        out.append(f'''<div class="page stay4" id="s{5 + k}">{furniture(f'.{5 + k:02d}', 'Hotel', P_HOTEL + k)}
  <div class="head">
    <h2>{name}</h2>
    <div class="loc"><span class="dot">{k + 1}</span><p class="sub">{loc}</p>{st}</div>
    <dl><div><dt class="lb">Fechas</dt><dd>{dates}</dd></div><div><dt class="lb">Noches</dt><dd>{nights.split()[0]}</dd></div>
        <div><dt class="lb">Habitación</dt><dd>{room}</dd></div><div><dt class="lb">Régimen</dt><dd>{plan}</dd></div></dl>
    <p class="desc">{desc}</p>
  </div>
  <div class="four">{''.join(f'<img src="himg_g/h-{i:03d}.jpg">' for i in ids)}</div>
</div>''')
    return '\n'.join(out)

def idx(num, name, page): return f'<li><a href="#s{num}"><i>.{num:02d}</i><b>{name}</b><span>{page:02d}</span></a></li>'
INDEX = ''.join([idx(1, 'Resumen', 3), idx(2, 'Vuelos', 4), idx(3, 'Hoteles', 5), idx(4, 'Itinerario Diario', FIRST_ITIN - 1)] +
                [idx(5 + k, h[2], P_HOTEL + k) for k, h in enumerate(HOTELS)] +
                [idx(10, 'Cotización', P_COT), idx(11, 'Notas &amp; Políticas de Cancelación', P_NOT)])

def stage(n, f, nt, d, p, a): return f'<tr><td><span class="dot">{n}</span></td><td class="f">{f}</td><td>{nt}</td><td>{d}</td><td>{p}</td><td>{a}</td></tr>'
_hn = [0]
def hrow(a, b, n, dest, hotel, room, plan):
    _hn[0] += 1
    d = f'{a.split()[0]} – {b}' if a.split()[1] == b.split()[1] else f'{a} – {b}'
    return (f'<tr><td><span class="dot">{_hn[0]}</span></td><td class="g">{d}</td><td>{n}</td><td>{dest}</td><td class="h">{hotel}</td>'
            f'<td class="r"><b>{room}</b><span>{plan}</span></td></tr>')

HTML = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Laponia · Año Nuevo Ártico · Cotización Opción 2</title><style>{CSS}</style></head><body>

<div class="page cover">
  <img src="img/cover.jpg">
  <div class="card">
    {logo(1)}
    <h1>Laponia</h1>
    <p class="t2">Año Nuevo Ártico</p>
    <p class="sub">Familia Porcayo González</p>
    <dl>
      <dt>Fechas</dt><dd>26 dic 2026 – 9 ene 2027</dd>
      <dt>Viajeros</dt><dd>5 personas · 13 noches de hotel</dd>
      <dt>Documento</dt><dd>Cotización · Opción 2</dd>
    </dl>
  </div>
</div>

<div class="page index" id="indice">
  <div class="panel"><h1>Índice</h1><span>Luxury Travel Design</span></div>
  <div class="list"><ol>{INDEX}</ol></div>
  <div class="meta">
    <div><span class="lb">Propuesta para</span><p>Familia Porcayo González<br>5 personas</p></div>
    <div><span class="lb">Diseñado por</span><p>Mariana Medina<br>Luxury Travel Designer</p></div>
  </div>
</div>

<div class="page res" id="s1">
  {furniture('.01', 'Resumen', 3)}
  <div class="in">
    <h1>Resumen</h1>
    {map_svg()}
    <table class="stages">
      <tr><th style="width:.35in">#</th><th style="width:1.3in">Fechas</th><th style="width:.75in">Noches</th><th style="width:1.35in">Destino</th><th style="width:.95in">País</th><th>Alojamiento</th></tr>
      {stage(1, '27 – 28 dic', 1, 'Helsinki', 'Finlandia', 'Waldorf Astoria Helsinki')}
      {stage(2, '28 dic – 03 ene', 6, 'Rovaniemi', 'Finlandia', 'Hidden Arctic Cloud Villa')}
      {stage(3, '03 – 06 ene', 3, 'Muonio', 'Finlandia', 'Arcora Boutique Hotel &amp; Villas')}
      {stage(4, '06 – 08 ene', 2, 'Laponia Sueca', 'Suecia', 'Fjellborg Arctic Lodge')}
      {stage(5, '08 – 09 ene', 1, 'Estocolmo', 'Suecia', 'Grand Hôtel Stockholm')}
    </table>
  </div>
</div>

<div class="page fly" id="s2">
  {furniture('.02', 'Vuelos', 4)}
  <div class="in">
    <h1>Vuelos</h1>
    <div class="pax"><span class="lb">Pasajeros · 5</span><p class="names">Guadalupe Xiomara González Soria<i></i>Carlos Eugenio Porcayo González<i></i>Carlos Eduardo Porcayo Guevara<i></i>Valentina Porcayo González<i></i>Paulina Porcayo González</p></div>
    <table class="flights">
      <tr><th>Fecha</th><th>Aerolínea</th><th>No.</th><th>Desde</th><th>Hacia</th><th>Clase</th><th>Salida</th><th>Llegada</th><th>Duración</th></tr>
      <tr class="grp"><td colspan="9">Ida · 26 – 27 dic</td></tr>
      {frow('26 dic', 'Lufthansa', 'LH 521', 'México (MEX)', 'Múnich (MUC)', 'Business', '19:45', '13:45<sup>+1</sup>', '11 h 00 m')}
      {frow('27 dic', 'Lufthansa', 'LH 2462', 'Múnich (MUC)', 'Helsinki (HEL)', 'Business', '15:10', '18:45', '2 h 35 m')}
      <tr class="grp"><td colspan="9">Vuelos internos</td></tr>
      {frow('28 dic', 'Finnair', 'AY 541', 'Helsinki (HEL)', 'Rovaniemi (RVN)', '<b>Economy</b>', '07:10', '08:40', '1 h 30 m')}
      {frow('08 ene', 'SAS', 'SK 1047', 'Kiruna (KRN)', 'Estocolmo (ARN)', 'Business', '11:30', '13:15', '1 h 45 m')}
      <tr class="grp"><td colspan="9">Regreso · 9 ene</td></tr>
      {frow('09 ene', 'Lufthansa', 'LH 2421', 'Estocolmo (ARN)', 'Múnich (MUC)', 'Business', '07:30', '09:40', '2 h 10 m')}
      {frow('09 ene', 'Lufthansa', 'LH 520', 'Múnich (MUC)', 'México (MEX)', 'Business', '12:20', '18:05', '12 h 45 m')}
    </table>
  </div>
  <div class="fnotes">
    <h4>Equipaje</h4>
    <p>Lufthansa 1&nbsp;×&nbsp;32&nbsp;kg &nbsp;·&nbsp; Finnair 1&nbsp;×&nbsp;23&nbsp;kg &nbsp;·&nbsp; SAS 2&nbsp;×&nbsp;23&nbsp;kg</p>
    <h4>Políticas de cancelación</h4>
    <p>Tarifas aéreas sujetas a disponibilidad y a cambio hasta la emisión de los boletos. Una vez emitidos, los boletos suelen ser no reembolsables; los cambios generan diferencia de tarifa y cargo de la aerolínea. Las condiciones exactas dependen de la tarifa emitida y se confirman antes de emitir.</p>
  </div>
</div>

<div class="page hot" id="s3">
  {furniture('.03', 'Hoteles', 5)}
  <div class="in">
    <h1>Hoteles</h1>
    <table>
      <tr><th style="width:.38in">#</th><th style="width:1.0in">Fechas</th><th style="width:.38in">Nts</th><th style="width:1.0in">Destino</th><th style="width:2.08in">Hotel</th><th>Habitación / Régimen</th></tr>
      {hrow('27 dic', '28 dic', 1, 'Helsinki', 'Waldorf Astoria Helsinki', 'One Bedroom Suite (cama extra) + Grand Deluxe Room comunicadas', 'Desayuno incluido')}
      {hrow('28 dic', '03 ene', 6, 'Rovaniemi', 'Hidden Arctic Cloud Villa', 'Villa privada de 3 recámaras', 'Chef privado · todas las comidas y bebidas')}
      {hrow('03 ene', '06 ene', 3, 'Muonio', 'Arcora Boutique Hotel &amp; Villas', '2x Junior Suite Kalle comunicadas (cama extra)', 'Desayuno incluido')}
      {hrow('06 ene', '08 ene', 2, 'Laponia Sueca', 'Fjellborg Arctic Lodge', 'Master Lodge de 4 recámaras · uso exclusivo', 'Pensión completa')}
      {hrow('08 ene', '09 ene', 1, 'Estocolmo', 'Grand Hôtel Stockholm', 'Superior Suite Harbour View + Deluxe Harbour View comunicadas', 'Desayuno incluido')}
    </table>
  </div>
</div>

<div class="page cover open" id="s4"><img src="img/opener.jpg"><div class="card"><span class="lb">.04</span><h1>Itinerario Diario</h1></div></div>

{itin_pages()}

{hotel_pages()}

<div class="page quote" id="s10">
  {furniture('.10', 'Cotización', P_COT)}
  <div class="in">
    <h1>Cotización <i>Opción 2</i></h1>
    <table>
      <tr><th>Concepto</th><th>Costo total</th></tr>
      <tr><td><b>Paquete Terrestre · Laponia Finlandesa &amp; Sueca</b>
        <span>12 noches: Waldorf Astoria Helsinki · Hidden Arctic Cloud Villa (chef privado) · Arcora · Fjellborg Arctic Lodge (uso exclusivo) · Grand Hôtel Stockholm</span>
        <span>Traslados privados en V-Class, ropa ártica premium y Fjällräven</span>
        <span>Actividades privadas: renos y almuerzo en tipi, Santa Claus Secret Forest, motos de nieve, Fin de Año, Arctic Snow Hotel, ice karting, huskies, cena en kota, chamán, sauna ártica, pesca en hielo, escultura en hielo y Gamla Stan</span></td><td>€227,345.00</td></tr>
      <tr><td><b>Vuelos Internacionales &amp; Regionales · 5 PAX</b>
        <span>México – Múnich – Helsinki – Rovaniemi · Kiruna – Estocolmo – Múnich – México</span>
        <span>Lufthansa Business · Finnair Economy (Helsinki – Rovaniemi) · SAS Business (Kiruna – Estocolmo)</span>
        <span>US$7,885.07 por persona</span></td><td>US$39,425.35</td></tr>
    </table>
    <div class="total"><span class="lb">Total del viaje · 5 personas · aprox. en EUR</span><b>≈ €262,408.32</b></div>
    <p class="fine">Paquete terrestre en euros (EUR) y vuelos en dólares (USD) para 5 personas. El total aproximado en EUR convierte los vuelos al tipo de cambio Nuba del 09 Nov 2026 (USD 18.89 MXN · EUR 21.24 MXN; 1 USD ≈ 0.8894 EUR) y puede variar según el tipo de cambio del día de pago. Precios sujetos a disponibilidad al momento de la reserva; no se ha realizado ninguna reservación.</p>
  </div>
</div>

<div class="page notes" id="s11">
  {furniture('.11', 'Notas', P_NOT)}
  <div class="in">
    <h1 style="font-size:34pt">Notas &amp; Políticas de Cancelación</h1>
    <div class="cols">
      <div>{notes('El precio incluye', [
          'Vuelos según el itinerario (tarifas en USD).',
          'Alojamiento según el itinerario con desayuno; chef privado con todas las comidas y bebidas en Hidden Arctic Cloud Villa y pensión completa en Fjellborg.',
          'Traslados privados en minivan Business (V-Class o similar).',
          'Ropa de invierno premium en la villa y ropa ártica Fjällräven en Fjellborg.',
          'Actividades privadas indicadas en el itinerario.'])}
        {notes('El precio excluye', [
          'Almuerzo en Levi durante el traslado a Muonio.',
          'Comidas y bebidas no especificadas en el itinerario.',
          'Seguro de viaje (muy recomendado).',
          'Gastos personales y propinas.'])}
        {notes('Para reservar', 'Se requiere un depósito no reembolsable del 30% al momento de reservar para confirmar. El saldo restante vence 60 días antes de la salida. Los pagos tardíos pueden resultar en la cancelación de la reserva y la pérdida del depósito.')}</div>
      <div>{notes('Información general', [
          'Los precios, disponibilidad e inclusiones están sujetos a cambios según las políticas de los proveedores y las fluctuaciones del mercado.',
          'El precio puede variar dependiendo del tipo de cambio.',
          'El cliente es responsable de contar con todos los documentos de viaje (pasaportes, visas, permisos) vigentes antes de la salida.',
          'Se recomienda ampliamente contratar un seguro de viaje que cubra emergencias médicas, cancelaciones y demoras.',
          'Las auroras boreales son un fenómeno natural y no pueden garantizarse. Las actividades al aire libre dependen de las condiciones climáticas.',
          'Para conducir motos de nieve se requiere licencia de manejo vigente y edad mínima; aplican restricciones de edad, estatura y peso en algunas actividades.'])}
        <h4>Políticas de cancelación</h4>
        <table>
          <tr><th>Periodo de aviso</th><th>Cargo por cancelación</th></tr>
          <tr><td>61 días o más</td><td>30% del valor total</td></tr>
          <tr><td>60 días o menos</td><td>100% del valor total</td></tr>
          <tr><td>No Show</td><td>100% del valor total</td></tr>
        </table></div>
    </div>
  </div>
</div>

<div class="page end">
  {logo(1)}
  <div class="follow">
    <span class="lb">Síguenos en Instagram</span>
    <a class="h" href="https://instagram.com/thesuitelife.mx">@thesuitelife.mx</a>
    <a class="u" href="https://thesuitelife.com.mx">thesuitelife.com.mx</a>
  </div>
  <div class="who"><b>Mariana Medina</b><p>Luxury Travel Designer</p>
    <p class="ct"><a href="tel:+525518500549">55 1850 0549</a> &nbsp;·&nbsp; <a href="mailto:mariana.medina@nuba.com">mariana.medina@nuba.com</a></p></div>
  <p class="cred">Fotografías de hoteles: las de la cotización original y los sitios oficiales de Grand Hôtel Stockholm y Fjellborg Arctic Lodge. Portada, apertura e itinerario, vía Unsplash: @hendrikmorkel, @tanelah, @saidaqqa, @thejohnnyme, @judithprins, @seancdavis, @earthwandering, @windagh, @skyhung1228, @claybanks, @grury y @jonflobrant.</p>
</div>
</body></html>'''

(ROOT / 'proto.html').write_text(HTML, encoding='utf-8')
OUT.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu',
                '--no-pdf-header-footer', '--generate-pdf-document-outline', f'--print-to-pdf={OUT}',
                f'file://{ROOT}/proto.html'], check=True, capture_output=True)
print('PDF ->', OUT)
