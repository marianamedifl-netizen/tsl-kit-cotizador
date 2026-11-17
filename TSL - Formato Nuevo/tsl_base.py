#!/usr/bin/env python3
"""TSL · Formato Nuevo — base compartida: tipografías, logos, mapa, CSS y ayudantes.
Se importa desde el script de cada cotización (ver ejemplo_laponia/cotizacion_completa_laponia.py).
Al final conserva la maqueta original de Marrakech (solo se ejecuta si se corre este archivo directamente)."""
import json, math, os, re, subprocess, pathlib
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).parent
# Carpeta de marca (fuentes IvyOra y Karla). Cámbiala con la variable de entorno TSL_BRAND.
BRAND = pathlib.Path(os.environ.get('TSL_BRAND', '/mnt/user-data/uploads/Travel Agent Portal/TSL - Brand Files'))
OUT = pathlib.Path('/mnt/user-data/outputs/TSL_FormatoNuevo_v3_Marrakech.pdf')

# ───────────────────────── tipografías ─────────────────────────
F = BRAND / 'Fonts'
def face(name, path, weight=400, style='normal'):
    return (f"@font-face{{font-family:'{name}';src:url('file://{path}');"
            f"font-weight:{weight};font-style:{style};}}")
FONTS = '\n'.join([
    face('IvyOra', F / 'IvyOra/IvyOraDisplay-Thin.ttf', 200),
    face('IvyOra', F / 'IvyOra/IvyOraDisplay-ThinItalic.ttf', 200, 'italic'),
    face('IvyOra', F / 'IvyOra/IvyOraDisplay-Light.ttf', 300),
    face('Karla', F / 'Karla/static/Karla-Light.ttf', 300),
    face('Karla', F / 'Karla/static/Karla-Regular.ttf', 400),
    face('Karla', F / 'Karla/static/Karla-Medium.ttf', 500),
    face('Karla', F / 'Karla/static/Karla-Bold.ttf', 700),
])

# ───────────────────────── logos (vector) ─────────────────────────
def logo(n, cls=''):
    box_ = {1: (203, 468, 673, 143), 2: (197, 496, 684, 87), 3: (255, 436, 569, 194)}[n]
    src = (ROOT / f'logo/l{n}.svg').read_text()
    inner = re.search(r'</defs>(.*)</svg>', src, re.S).group(1).replace(' class="st0"', '')
    return (f'<svg class="logo {cls}" viewBox="{box_[0]} {box_[1]} {box_[2]} {box_[3]}" '
            f'fill="currentColor" xmlns="http://www.w3.org/2000/svg">{inner}</svg>')

# ───────────────────────── mapa ─────────────────────────
LON0, LON1, LAT0, LAT1 = -19.5, 5.5, 27.0, 44.6
K = math.cos(math.radians((LAT0 + LAT1) / 2)); S = 20
def proj(lon, lat): return ((lon - LON0) * K * S, (LAT1 - lat) * S)
MAP_W, MAP_H = (LON1 - LON0) * K * S, (LAT1 - LAT0) * S

def country_paths(ids):
    topo = json.loads((ROOT / 'geo/countries-50m.json').read_text())
    sx, sy = topo['transform']['scale']; tx, ty = topo['transform']['translate']
    arcs = []
    for arc in topo['arcs']:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    def ring(idx):
        out = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(a if not out else a[1:])
        return out
    view = box(LON0, LAT0, LON1, LAT1); res = {}
    for g in topo['objects']['countries']['geometries']:
        if g.get('id') not in ids: continue
        polys = []
        for poly in (g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]):
            ext = ring(poly[0])
            if len(ext) < 4: continue
            pg = Polygon(ext, [ring(h) for h in poly[1:] if len(ring(h)) >= 4])
            if not pg.is_valid: pg = pg.buffer(0)
            if pg.intersects(view): polys.append(pg.intersection(view))
        geom = unary_union(polys); d = []
        for pg in (geom.geoms if hasattr(geom, 'geoms') else [geom]):
            if pg.geom_type != 'Polygon': continue
            for r in [pg.exterior] + list(pg.interiors):
                d.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in (proj(a, b) for a, b in r.coords)) + 'Z')
        res[g['id']] = ''.join(d)
    return res

def map_svg():
    cp = country_paths({'724', '620', '504'})
    mad = proj(-3.70, 40.42); rak = proj(-8.00, 31.63); west = proj(LON0, 41.9)
    ctrl = proj(-8.6, 36.4)
    lab = lambda lon, lat, t, cls='rg': (
        f'<text class="{cls}" x="{proj(lon, lat)[0]:.1f}" y="{proj(lon, lat)[1]:.1f}" text-anchor="middle">{t}</text>')
    return f'''<svg class="map" viewBox="0 0 {MAP_W:.1f} {MAP_H:.1f}" xmlns="http://www.w3.org/2000/svg">
  <path d="{cp['620']}" fill="#F0EDE8" stroke="#FCF9F5" stroke-width=".6" fill-rule="evenodd"/>
  <path d="{cp['724']}" fill="#DFD3C5" stroke="#FCF9F5" stroke-width=".6" fill-rule="evenodd"/>
  <path d="{cp['504']}" fill="#DFD3C5" stroke="#FCF9F5" stroke-width=".6" fill-rule="evenodd"/>
  <path d="M{west[0]:.1f},{west[1]:.1f} L{mad[0]:.1f},{mad[1]:.1f}" class="rt"/>
  <path d="M{mad[0]:.1f},{mad[1]:.1f} Q{ctrl[0]:.1f},{ctrl[1]:.1f} {rak[0]:.1f},{rak[1]:.1f}" class="rt"/>
  <circle cx="{mad[0]:.1f}" cy="{mad[1]:.1f}" r="2.6" fill="#FCF9F5" stroke="#232323" stroke-width=".7"/>
  <circle cx="{rak[0]:.1f}" cy="{rak[1]:.1f}" r="3" fill="#232323"/>
  {lab(-1.3, 38.9, 'ESPAÑA')}{lab(-4.6, 32.9, 'MARRUECOS')}{lab(-14.2, 35.6, 'OCÉANO ATLÁNTICO')}
  <text class="ct" x="{mad[0] + 7:.1f}" y="{mad[1] + 2.6:.1f}">Madrid</text>
  <text class="ct b" x="{rak[0] + 8:.1f}" y="{rak[1] + 3:.1f}">Marrakech</text>
  <text class="it" x="{west[0] + 2:.1f}" y="{west[1] - 6:.1f}">desde Ciudad de México</text>
</svg>'''

# ───────────────────────── piezas comunes ─────────────────────────
TRIP = 'Marrakech · Marzo 2027'
def furniture(num, name, page):
    return (f'<div class="top"><span><i>{num}</i>{name}</span><span>{TRIP}</span></div>'
            f'<div class="bot">{logo(2)}<span>{page:02d}</span></div>')

SUG = 'sugerencia, por cotizar'
def entry(when, title, text='', tag=None):
    t = f' <em>{tag[0].upper() + tag[1:]}.</em>' if tag else ''
    d = f'<p class="d">{text}{t}</p>' if (text or t) else ''
    return f'<div class="w">{when}</div><div><p class="t">{title}</p>{d}</div>'

def day(date, place, entries, img=None, cap='', flip=False, top=''):
    body = (f'<div class="txt"><p class="dt">{date}</p><h3>{place}</h3>'
            f'<div class="ag">{"".join(entries)}</div></div>')
    if not img:
        return f'<section class="day solo" style="top:{top}">{body}</section>'
    fig = f'<figure><img src="img/{img}"><figcaption>{cap}</figcaption></figure>'
    return f'<section class="day{" flip" if flip else ""}" style="top:{top}">{body + fig if flip else fig + body}</section>'

def frow(d, airline, no, fr, to, cl, dep, arr, dur):
    return (f'<tr><td>{d}</td><td>{airline}</td><td>{no}</td><td>{fr}</td><td>{to}</td>'
            f'<td>{cl}</td><td>{dep}</td><td>{arr}</td><td>{dur}</td></tr>')

def leg(code, city, times, note=''):
    n = f'<small>{note}</small>' if note else ''
    return f'<div class="ap"><b>{code}</b><span class="lb">{city}</span><p>{times}</p>{n}</div>'
def hop(flight, dur): return f'<div class="hop"><span>{flight}</span><i></i><span>{dur}</span></div>'

def notes(title, items):
    if isinstance(items, str): return f'<h4>{title}</h4><p>{items}</p>'
    return f'<h4>{title}</h4><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

CSS = f'''
{FONTS}
@page {{ size: 8.5in 11in; margin: 0; }}
:root {{ --paper:#FCF9F5; --almond:#F0EDE8; --oat:#DFD3C5; --stone:#7D766C; --ink:#232323; --soft:#55504A; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ background:var(--paper); color:var(--ink); font:300 8.8pt/1.6 'Karla';
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.page {{ position:relative; width:8.5in; height:11in; overflow:hidden; page-break-after:always; background:var(--paper); }}
.page:last-child {{ page-break-after:auto; }}
img {{ display:block; width:100%; height:100%; object-fit:cover; }}
.logo {{ display:block; }}
.lb {{ font:400 6.3pt/1.4 'Karla'; letter-spacing:.3em; text-transform:uppercase; color:var(--stone); }}
h1 {{ font:200 43pt/1 'IvyOra'; letter-spacing:-.01em; }}
.sub {{ font:italic 200 13.5pt/1.3 'IvyOra'; color:var(--stone); margin-top:.1in; }}
.top {{ position:absolute; left:.7in; right:.7in; top:.5in; border-top:.5pt solid var(--stone); padding-top:.09in;
  display:flex; justify-content:space-between; font:400 6pt 'Karla'; letter-spacing:.3em; text-transform:uppercase; color:var(--stone); }}
.top i {{ font-style:normal; margin-right:.14in; color:var(--ink); }}
.bot {{ position:absolute; left:.7in; right:.7in; bottom:.42in; border-top:.5pt solid var(--oat); padding-top:.11in;
  display:flex; justify-content:space-between; align-items:center; color:var(--stone);
  font:400 6pt 'Karla'; letter-spacing:.3em; }}
.bot .logo {{ width:.92in; }}
.in {{ position:absolute; left:.7in; right:.7in; top:1.2in; }}

/* portada */
.cover > img {{ position:absolute; inset:0; }}
.cover .card {{ position:absolute; left:.7in; bottom:.95in; width:3.75in; padding:.38in .4in .36in; background:rgba(223,211,197,.82); color:var(--ink); }}
.cover .card .logo {{ width:1.25in; }}
.cover .card h1 {{ font-size:47pt; margin:.5in 0 .04in -.02in; }}
.cover .card .sub {{ color:var(--ink); opacity:.78; margin:0 0 .26in; }}
.cover .card dl {{ border-top:.5pt solid rgba(35,35,35,.4); padding-top:.17in; display:grid; grid-template-columns:.78in 1fr; row-gap:.05in; }}
.cover .card dt {{ font:400 5.8pt/1.9 'Karla'; letter-spacing:.3em; text-transform:uppercase; color:var(--stone); }}
.cover .card dd {{ font:300 8.6pt/1.45 'Karla'; }}
.cover .side {{ position:absolute; right:.52in; bottom:.95in; writing-mode:vertical-rl; transform:rotate(180deg);
  font:400 6pt 'Karla'; letter-spacing:.42em; text-transform:uppercase; color:var(--ink); opacity:.6; }}

/* índice */
.index .panel {{ position:absolute; left:0; top:0; bottom:0; width:2.95in; background:var(--oat); }}
.index .panel h1 {{ position:absolute; left:.7in; top:1.2in; }}
.index .panel span {{ position:absolute; left:.7in; bottom:1.05in; writing-mode:vertical-rl; transform:rotate(180deg);
  font:400 6pt 'Karla'; letter-spacing:.42em; text-transform:uppercase; color:var(--stone); }}
.index .list {{ position:absolute; left:3.75in; right:.7in; top:1.2in; }}
.index ol {{ list-style:none; margin-top:.1in; }}
.index li {{ display:grid; grid-template-columns:.62in 1fr auto; align-items:baseline; padding:.165in 0 .15in; border-bottom:.5pt solid var(--oat); }}
.index li:first-child {{ border-top:.5pt solid var(--oat); }}
.index li i {{ font:200 15pt 'IvyOra'; font-style:normal; color:var(--stone); }}
.index li b {{ font:300 13.5pt 'IvyOra'; }}
.index li span {{ font:400 7pt 'Karla'; letter-spacing:.2em; color:var(--stone); }}
.index .meta {{ position:absolute; left:3.75in; right:.7in; bottom:1.05in; display:grid; grid-template-columns:1fr 1fr; gap:.3in; }}
.index .meta p {{ font:300 8.6pt/1.55 'Karla'; margin-top:.05in; }}

/* resumen */
.map {{ width:5.9in; height:auto; display:block; margin:.35in auto 0; }}
.map .rt {{ fill:none; stroke:#232323; stroke-width:.55; stroke-dasharray:2 2.6; }}
.map .rg {{ font:400 5px 'Karla'; letter-spacing:.34em; fill:#7D766C; }}
.map .ct {{ font:300 7.4px 'Karla'; fill:#232323; }}
.map .ct.b {{ font:300 10.5px 'IvyOra'; }}
.map .it {{ font:italic 200 8px 'IvyOra'; fill:#7D766C; }}
.kv {{ display:grid; row-gap:.21in; align-content:start; padding-top:.04in; }}
.kv p {{ font:300 13pt/1.25 'IvyOra'; margin-top:.035in; }}
.kv small {{ display:block; font:300 8pt/1.5 'Karla'; color:var(--stone); margin-top:.02in; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ font:400 6pt 'Karla'; letter-spacing:.26em; text-transform:uppercase; color:var(--stone); text-align:left;
  padding:0 .1in .1in 0; border-bottom:.5pt solid var(--stone); }}
td {{ padding:.125in .1in .115in 0; border-bottom:.5pt solid var(--oat); font:300 8.6pt/1.35 'Karla'; vertical-align:baseline; }}
td:last-child, th:last-child {{ padding-right:0; }}
.stages {{ margin-top:.4in; }}
.stages td.s {{ font:300 12.5pt/1.2 'IvyOra'; }}
.band {{ margin-top:.55in; background:var(--stone); color:#FCF9F5;
  display:flex; justify-content:space-between; align-items:center; padding:.2in .3in; }}
.band .lb {{ color:#FCF9F5; opacity:.8; }}
.band p {{ font:300 9.2pt 'Karla'; letter-spacing:.02em; }}

/* vuelos */
.pax {{ display:flex; align-items:baseline; gap:.3in; margin-top:.55in; padding-bottom:.16in; }}
.pax p {{ font:300 14pt/1.2 'IvyOra'; }}
.flights td:nth-child(1), .flights td:nth-child(6) {{ color:var(--stone); }}
.flights td:nth-child(3) {{ font-weight:500; }}
.fnotes {{ display:grid; grid-template-columns:1fr 1fr; column-gap:.55in; margin-top:.6in; }}
.fnotes h4 {{ font:italic 200 14pt/1.2 'IvyOra'; margin-bottom:.1in; }}
.fnotes ul {{ list-style:none; }}
.fnotes li {{ font:300 8.3pt/1.56 'Karla'; color:var(--soft); padding-left:.15in; text-indent:-.15in; margin-bottom:.05in; }}
.fnotes li::before {{ content:'–'; display:inline-block; width:.15in; text-indent:0; color:var(--stone); }}

/* hotel */
.stay .mos {{ position:absolute; left:.7in; right:.7in; top:1.2in; }}
.stay .r1 {{ display:grid; grid-template-columns:4.6in 2.4in; column-gap:.1in; height:3.55in; }}
.stay .r2 {{ display:grid; grid-template-columns:2.9in 1.75in 2.25in; column-gap:.1in; height:2.35in; margin-top:.1in; }}
.stay .r3 {{ display:grid; grid-template-columns:1fr 1.75in 1.75in; column-gap:.1in; height:2.6in; margin-top:.1in; }}
.stay .mos img {{ height:100%; }}
.stay .r1 img {{ height:3.55in; }} .stay .r2 img {{ height:2.35in; }} .stay .r3 img {{ height:2.6in; }}
.stay .name {{ padding:.16in .3in 0 0; }}
.stay .name h2 {{ font:200 31pt/1 'IvyOra'; margin-top:.1in; }}
.stay .name .sub {{ margin-top:.05in; }}
.stay .name dl {{ display:grid; grid-template-columns:1fr 1fr; column-gap:.2in; row-gap:.13in; margin-top:.24in; }}
.stay .name dd {{ font:300 10.5pt/1.25 'IvyOra'; margin-top:.02in; }}
.stay .name dd small {{ display:block; font:300 7.4pt/1.4 'Karla'; color:var(--stone); }}

/* itinerario */
.day {{ position:absolute; left:.7in; right:.7in; display:grid; grid-template-columns:1.9in 1fr; column-gap:.5in; }}
.day.flip {{ grid-template-columns:1fr 1.9in; }}
.day.solo {{ grid-template-columns:1fr; }}
.day figure {{ height:2.52in; position:relative; }}
.day figcaption {{ position:absolute; left:0; bottom:-.21in; font:italic 200 8.5pt 'IvyOra'; color:var(--stone); }}
.day.flip figcaption {{ left:auto; right:0; }}
.day .dt {{ font:italic 200 12.5pt/1.2 'IvyOra'; color:#A8937B; }}
.day h3 {{ font:200 25pt/1.08 'IvyOra'; margin:.05in 0 .2in; }}
.ag {{ display:grid; grid-template-columns:.68in 1fr; row-gap:.1in; }}
.ag .w {{ font:700 8pt/1.62 'Karla'; letter-spacing:.02em; color:var(--ink); }}
.ag .t {{ font:400 9pt/1.4 'Karla'; }}
.ag .d {{ font:300 8.3pt/1.48 'Karla'; color:var(--soft); margin-top:.01in; }}
.ag .d em {{ font:italic 200 9.5pt 'IvyOra'; color:var(--stone); white-space:nowrap; }}
.rule {{ position:absolute; left:.7in; right:.7in; border-top:.5pt solid var(--oat); }}

/* cotización */
.quote table {{ margin-top:.5in; }}
.quote th:last-child, .quote td:last-child {{ text-align:right; white-space:nowrap; }}
.quote td {{ padding:.22in .1in .2in 0; vertical-align:top; }}
.quote td b {{ display:block; font:300 14.5pt/1.2 'IvyOra'; }}
.quote td span {{ display:block; color:var(--soft); margin-top:.04in; font-size:8.4pt; }}
.quote td:last-child {{ font:300 14.5pt/1.2 'IvyOra'; padding-right:0; }}
.quote .total {{ display:flex; justify-content:space-between; align-items:baseline; background:var(--oat); color:var(--ink);
  padding:.2in .3in .19in; margin-top:.3in; }}
.quote .total .lb {{ color:var(--soft); }}
.quote .total b {{ font:200 24pt/1 'IvyOra'; }}
.quote .opt {{ display:grid; grid-template-columns:1.05in 1fr auto; column-gap:.2in; align-items:baseline; margin-top:.34in;
  padding-bottom:.2in; border-bottom:.5pt solid var(--oat); }}
.quote .opt p {{ color:var(--soft); font-size:8.4pt; }}
.quote .opt p b {{ display:block; font:300 12pt/1.3 'IvyOra'; color:var(--ink); }}
.quote .opt i {{ font:300 12pt 'IvyOra'; font-style:normal; }}
.quote .fine {{ margin-top:.24in; color:var(--soft); font-size:7.9pt; line-height:1.62; }}
.quote .valid {{ position:absolute; left:.7in; right:.7in; bottom:1.0in; background:var(--almond); padding:.26in .3in .24in;
  display:grid; grid-template-columns:1.5in 1fr; column-gap:.3in; }}
.quote .valid p {{ font-size:8.5pt; color:var(--soft); }}

/* notas */
.notes .cols {{ display:grid; grid-template-columns:1fr 1fr; column-gap:.55in; margin-top:.45in; }}
.notes h4 {{ font:italic 200 14pt/1.2 'IvyOra'; margin:0 0 .09in; }}
.notes ul {{ list-style:none; margin-bottom:.3in; }}
.notes li, .notes .cols p {{ font:300 8.1pt/1.56 'Karla'; color:var(--soft); }}
.notes li {{ padding-left:.15in; text-indent:-.15in; margin-bottom:.045in; }}
.notes li::before {{ content:'–'; display:inline-block; width:.15in; text-indent:0; color:var(--stone); }}
.notes .cols p {{ margin-bottom:.3in; }}
.notes td, .notes th {{ font-size:7.9pt; }}
.notes td {{ padding:.085in .1in .075in 0; color:var(--soft); }}
.notes th {{ font-size:5.8pt; }}

/* cierre */
.end {{ background:var(--stone); color:#FCF9F5; }}
.end .logo {{ position:absolute; left:50%; top:46%; width:3.1in; transform:translate(-50%,-50%); }}
.end .who {{ position:absolute; left:.7in; right:.7in; bottom:1.25in; text-align:center; }}
.end .who b {{ display:block; font:200 17pt 'IvyOra'; }}
.end .who p {{ font:300 8.6pt/1.7 'Karla'; opacity:.88; margin-top:.05in; }}
.end .cred {{ position:absolute; left:1.4in; right:1.4in; bottom:.5in; text-align:center; font:300 6.2pt/1.6 'Karla'; opacity:.62; }}
'''

HTML = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>

<!-- 01 PORTADA -->
<div class="page cover">
  <img src="img/cover.jpg">
  <div class="card">
    {logo(2)}
    <h1>Marrakech</h1>
    <p class="sub">Para Nombre del Cliente</p>
    <dl>
      <dt>Fechas</dt><dd>15 – 18 de marzo de 2027</dd>
      <dt>Viajeros</dt><dd>2 adultos</dd>
      <dt>Documento</dt><dd>Cotización</dd>
    </dl>
  </div>
  <span class="side">Luxury Travel Design</span>
</div>

<!-- 02 ÍNDICE -->
<div class="page index">
  <div class="panel"><h1>Índice</h1><span>Luxury Travel Design</span></div>
  <div class="list">
    <ol>
      <li><i>.01</i><b>Resumen</b><span>03</span></li>
      <li><i>.02</i><b>Vuelos</b><span>04</span></li>
      <li><i>.03</i><b>Itinerario Diario</b><span>05</span></li>
      <li><i>.04</i><b>La Mamounia</b><span>07</span></li>
      <li><i>.05</i><b>Cotización</b><span>08</span></li>
      <li><i>.06</i><b>Notas &amp; Políticas de Cancelación</b><span>09</span></li>
    </ol>
  </div>
  <div class="meta">
    <div><span class="lb">Propuesta para</span><p>Nombre del Cliente<br>2 adultos</p></div>
    <div><span class="lb">Diseñado por</span><p>Mariana Medina<br>15 de noviembre de 2026</p></div>
  </div>
</div>

<!-- 03 RESUMEN -->
<div class="page res">
  {furniture('.01', 'Resumen', 3)}
  <div class="in">
    <h1>Resumen</h1>
    {map_svg()}
    <table class="stages">
      <tr><th style="width:.4in">#</th><th style="width:1.25in">Fechas</th><th style="width:.8in">Noches</th><th style="width:1.4in">Destino</th><th style="width:1.2in">País</th><th>Alojamiento</th></tr>
      <tr><td>1</td><td>15 – 18 mar</td><td>3</td><td class="s">Marrakech</td><td>Marruecos</td><td class="s">La Mamounia</td></tr>
    </table>
  </div>
</div>

<!-- 04 VUELOS -->
<div class="page fly">
  {furniture('.02', 'Vuelos', 4)}
  <div class="in">
    <h1>Vuelos</h1>
    <div class="pax"><span class="lb">Pasajeros</span><p>Nombre del Cliente y acompañante</p></div>
    <table class="flights">
      <tr><th>Fecha</th><th>Aerolínea</th><th>No.</th><th>Desde</th><th>Hacia</th><th>Clase</th><th>Salida</th><th>Llegada</th><th>Duración</th></tr>
      {frow('14 mar', 'Iberia', 'IB 304', 'Ciudad de México (MEX)', 'Madrid (MAD)', 'Business', '12:50', '06:00 +1', '10 h 10 m')}
      {frow('15 mar', 'Iberia', 'IB 1853', 'Madrid (MAD)', 'Marrakech (RAK)', 'Business', '11:50', '12:50', '2 h 00 m')}
      {frow('18 mar', 'Iberia', 'IB 1856', 'Marrakech (RAK)', 'Madrid (MAD)', 'Business', '16:30', '19:30', '2 h 00 m')}
      {frow('18 mar', 'Iberia', 'IB 303', 'Madrid (MAD)', 'Ciudad de México (MEX)', 'Business', '23:55', '05:10 +1', '12 h 15 m')}
    </table>
    <div class="fnotes">
      <div><h4>Qué incluye</h4><ul>
        <li>Los cuatro tramos en cabina Business.</li>
        <li>Impuestos de aeropuerto y cargos de combustible vigentes.</li>
        <li>Equipaje documentado y de mano según la tarifa emitida; franquicia por confirmar al emitir.</li>
        <li>Selección de asiento y alimentos a bordo según la aerolínea.</li></ul></div>
      <div><h4>Políticas de cancelación</h4><ul>
        <li>Tarifa sujeta a disponibilidad y a cambio hasta la emisión de los boletos.</li>
        <li>Una vez emitidos, los boletos suelen ser no reembolsables; los cambios generan diferencia de tarifa y cargo de la aerolínea.</li>
        <li>Las condiciones exactas dependen de la tarifa emitida y se confirman antes de emitir.</li></ul></div>
    </div>
  </div>
</div>

<!-- 05 ITINERARIO 1 -->
<div class="page">
  {furniture('.03', 'Itinerario Diario', 5)}
  <div class="in"><h1>Itinerario Diario</h1></div>
  {day('Domingo 14 de marzo', 'Ciudad de México – Madrid', [
      entry('12:50', 'Vuelo IB 304 a Madrid', 'Noche a bordo; llegada el lunes 15 a las 06:00.'),
  ], top='2.1in')}
  <div class="rule" style="top:3.45in"></div>
  {day('Lunes 15 de marzo', 'Madrid – Marrakech', [
      entry('11:50', 'Vuelo IB 1853 a Marrakech', 'Tras una conexión de 5 h 50 m en Madrid; llegada a las 12:50 a Marrakech-Menara.'),
      entry('', 'Traslado privado a La Mamounia', 'Mercedes V-Class con chofer. Opcional; ver Cotización.'),
      entry('15:00', 'Check-in en La Mamounia', 'Habitación Classic Hivernage Twin.'),
      entry('Tarde', 'Libre', 'Jardines, alberca y spa del hotel.'),
  ], 'day1.jpg', 'Marrakech', top='3.68in')}
  <div class="rule" style="top:6.62in"></div>
  {day('Martes 16 de marzo', 'Marrakech', [
      entry('Mañana', 'Medina y zocos con guía privado', 'Madrasa Ben Youssef, zocos y plaza Jemaa el-Fnaa, a pie.', SUG),
      entry('Tarde', 'Jardín Majorelle y Museo Yves Saint Laurent', 'Con entradas reservadas.', SUG),
      entry('Noche', 'Cena', 'Reserva a elegir; la gestionamos con gusto.'),
  ], 'day2.jpg', 'Madrasa Ben Youssef', flip=True, top='6.85in')}
</div>

<!-- 06 ITINERARIO 2 -->
<div class="page">
  {furniture('.03', 'Itinerario Diario', 6)}
  {day('Miércoles 17 de marzo', 'Marrakech', [
      entry('Día', 'Excursión privada al Alto Atlas', 'Valles y pueblos bereberes, con chofer y guía.', SUG),
      entry('Tarde', 'Hammam en el spa del hotel', 'Al regresar de la montaña.', SUG),
  ], 'day3.jpg', 'Alto Atlas', top='1.3in')}
  <div class="rule" style="top:4.3in"></div>
  {day('Jueves 18 de marzo', 'Marrakech – Ciudad de México', [
      entry('Mañana', 'Libre', 'El hotel o unas últimas compras en la medina.'),
      entry('12:00', 'Check-out de La Mamounia'),
      entry('', 'Traslado privado al aeropuerto', 'Mercedes V-Class con chofer. Opcional; ver Cotización.'),
      entry('16:30', 'Vuelo IB 1856 a Madrid', 'Llegada a las 19:30; conexión de 4 h 25 m.'),
      entry('23:55', 'Vuelo IB 303 a Ciudad de México', 'Llegada el viernes 19 a las 05:10.'),
  ], 'day4.jpg', 'Marrakech', flip=True, top='4.53in')}
  <p class="cap" style="position:absolute;left:.7in;bottom:1.0in">Las experiencias marcadas como sugerencia son ilustrativas y se cotizan por separado.</p>
</div>

<!-- 07 HOTEL -->
<div class="page stay">
  {furniture('.04', 'Hotel', 7)}
  <div class="mos">
    <div class="r1"><img src="img/h_aerial.jpg"><img src="img/h_menzeh.jpg"></div>
    <div class="r2"><img src="img/h_room.jpg"><img src="img/h_spa.jpg"><img src="img/h_garden.jpg"></div>
    <div class="r3">
      <div class="name"><span class="lb">Dónde dormir</span><h2>La Mamounia</h2><p class="sub">Marrakech, Marruecos</p>
        <dl>
          <div><dt class="lb">Fechas</dt><dd>15 – 18 mar 2027<small>3 noches</small></dd></div>
          <div><dt class="lb">Habitación</dt><dd>Classic Hivernage Twin<small>2 adultos</small></dd></div>
          <div><dt class="lb">Tarifa</dt><dd>Best Available Rate<small>Reembolsable</small></dd></div>
          <div><dt class="lb">Horarios</dt><dd>Check-in 15:00<small>Check-out 12:00</small></dd></div>
        </dl></div>
      <img src="img/h_spadoor.jpg"><img src="img/h_balcony.jpg">
    </div>
  </div>
</div>

<!-- 08 COTIZACIÓN -->
<div class="page quote">
  {furniture('.05', 'Cotización', 8)}
  <div class="in">
    <h1>Cotización</h1>
    <p class="sub">Para 2 adultos, en dólares estadounidenses</p>
    <table>
      <tr><th>Concepto</th><th>Costo total (USD)</th></tr>
      <tr><td><b>Vuelos, Ciudad de México – Marrakech</b><span>Iberia vía Madrid · Business · 2 adultos · 14 – 19 de marzo de 2027</span><span>US$6,351.00 por persona · tarifa pública de referencia, por confirmar en Sabre</span></td><td>US$12,702.00</td></tr>
      <tr><td><b>Hospedaje, La Mamounia</b><span>Classic Hivernage Twin · 3 noches (15 – 18 de marzo de 2027) · 2 adultos</span><span>Best Available Rate, reembolsable · incluye IVA, cargo de servicio e impuesto municipal</span></td><td>US$2,796.80</td></tr>
    </table>
    <div class="total"><span class="lb">Total estimado (USD)</span><b>US$15,498.80</b></div>
    <div class="opt"><span class="lb">Opcional</span>
      <p><b>Traslados privados, aeropuerto y hotel</b>Mercedes V-Class con chofer · no incluido en el total</p><i>EUR 175 por trayecto</i></div>
    <p class="fine">Tarifa aérea consultada el 15 de noviembre de 2026; los tramos Madrid – Marrakech son operados por Iberia Express. Tarifa del hotel en dirhams marroquíes: MAD 27,297 por la estancia completa, impuestos incluidos. Conversión de referencia: 1 USD = 9.76 MAD. El hotel cobra en MAD, por lo que el monto en dólares puede variar según el tipo de cambio al momento del pago. Desayuno no incluido.</p>
  </div>
  <div class="valid"><span class="lb">Vigencia y reservación</span>
    <p>Cotización válida hasta el 17 de noviembre de 2026, sujeta a disponibilidad al momento de reservar. El hotel se garantiza con tarjeta de crédito y la estancia se paga directamente en el hotel. La tarifa aérea se confirma al emitir los boletos.</p></div>
</div>

<!-- 09 NOTAS -->
<div class="page notes">
  {furniture('.06', 'Notas', 9)}
  <div class="in">
    <h1 style="font-size:34pt">Notas &amp; Políticas de Cancelación</h1>
    <div class="cols">
      <div>
        {notes('Información general', [
          'Los precios, disponibilidad e inclusiones están sujetos a cambios según las políticas de los proveedores hasta confirmar la reserva.',
          'El hotel cobra en dirhams marroquíes (MAD); el monto en USD puede variar según el tipo de cambio.',
          'El cliente es responsable de contar con pasaporte vigente y los documentos de viaje requeridos.',
          'Se recomienda ampliamente contratar un seguro de viaje que cubra emergencias médicas, cancelaciones y demoras.',
          'Cualquier modificación tras la confirmación está sujeta a disponibilidad y a la tarifa vigente.'])}
        {notes('El precio incluye', [
          'Vuelos Ciudad de México – Marrakech – Ciudad de México en Business para 2 adultos.',
          'Alojamiento por 3 noches en Classic Hivernage Twin Room para 2 adultos.',
          'IVA, cargo de servicio e impuesto municipal del hotel.',
          'Wi-Fi y valet parking.'])}
        {notes('El precio excluye', [
          'Traslados (traslado del hotel desde el aeropuerto: aprox. MAD 600 por vehículo, por trayecto).',
          'Desayuno (aprox. MAD 490 por adulto, por día).',
          'Experiencias sugeridas, tratamientos de spa, alimentos y bebidas no especificados.',
          'Seguro de viaje, gastos personales y propinas.'])}
      </div>
      <div>
        {notes('Información del hotel', [
          'Check-in a partir de las 15:00; check-out antes de las 12:00.',
          'Código de vestimenta: no se permiten shorts en áreas comunes, bares y restaurantes después de las 18:00.',
          'Se solicita tarjeta de crédito al check-in para gastos incidentales; el hotel no acepta efectivo.',
          'Cama adicional disponible por MAD 950 por día; cunas sin costo bajo solicitud.'])}
        {notes('Políticas del vuelo', [
          'Tarifas aéreas sujetas a disponibilidad y a cambio hasta la emisión de los boletos.',
          'Las condiciones de cambio y reembolso dependen de la tarifa emitida y se confirman antes de emitir.',
          'El pasajero es responsable de la documentación que exija cada aerolínea y país.'])}
        {notes('Política de pago', 'La reserva del hotel se garantiza con tarjeta de crédito y la estancia se paga directamente en el hotel en MAD; no se requiere pago por adelantado con esta tarifa. Los boletos de avión se pagan al emitirse.')}
        <h4>Cancelación del hotel</h4>
        <table>
          <tr><th>Periodo de aviso</th><th>Cargo por cancelación</th></tr>
          <tr><td>Hasta el 22 feb 2027, 15:00 h</td><td>Sin cargo</td></tr>
          <tr><td>Del 22 feb al 14 mar 2027</td><td>50% del total de la estancia</td></tr>
          <tr><td>Desde el 14 mar 2027, 15:00 h</td><td>100% del total de la estancia</td></tr>
          <tr><td>No show o salida anticipada</td><td>100% del total de la estancia</td></tr>
        </table>
      </div>
    </div>
  </div>
</div>

<!-- 10 CIERRE -->
<div class="page end">
  {logo(1)}
  <div class="who"><b>Mariana Medina</b><p>Luxury Travel Designer<br>55 1850 0549 &nbsp;·&nbsp; mariana.medina@nuba.com</p></div>
  <p class="cred">Fotografías del hotel: La Mamounia. Otras imágenes: Sven Siebel, Alba Iglesias, Alex Azabache, Louis Hansel y Jean Carlo Emer, vía Unsplash.</p>
</div>
</body></html>'''

if __name__ == '__main__':
    (ROOT / 'proto.html').write_text(HTML, encoding='utf-8')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu',
                    '--no-pdf-header-footer', f'--print-to-pdf={OUT}',
                    f'file://{ROOT}/proto.html'], check=True, capture_output=True)
    print('PDF ->', OUT)
