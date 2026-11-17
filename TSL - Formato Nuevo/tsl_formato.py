#!/usr/bin/env python3
"""TSL · Formato Nuevo — estilos aprobados y piezas comunes a todas las plantillas
(Cotización Completa, Cotización Rápida, Entrega Final, Guía de Viaje)."""
import subprocess, pathlib
import tsl_base as B

entry, frow, notes = B.entry, B.frow, B.notes

def logo(n, cls=''):
    """Logo vectorial; el 1 (con lema) lleva margen para que el lema no se corte."""
    return B.logo(n, cls).replace('viewBox="203 468 673 143"', 'viewBox="203 464 673 152"')

def furniture(num, name, page, trip=None, link='#indice'):
    """Filete superior con sección y nombre del viaje; pie con logo y folio."""
    return (f'<div class="top"><span><i>{num}</i>{name}</span><span>{trip or B.TRIP}</span></div>'
            f'<div class="bot"><a href="{link}">{logo(2)}</a><span>{page:02d}</span></div>')

STAR = '<svg viewBox="0 0 20 20"><path d="M10 1.2l2.7 5.6 6.1.8-4.5 4.2 1.1 6-5.4-2.9-5.4 2.9 1.1-6L1.2 7.6l6.1-.8z"/></svg>'
def stars(n): return f'<span class="stars">{STAR * n}</span>' if n else ''
def dot(n): return f'<span class="dot">{n}</span>'

EXTRA = '''
/* hoteles (tabla) */
.hot table {{ margin-top:.55in; }}
.hot td {{ padding:.17in .12in .16in 0; vertical-align:middle; }}
.hot td.h {{ font:300 13pt/1.2 'IvyOra'; }}
.hot td.r b {{ display:block; font:400 8.8pt/1.4 'Karla'; }}
.hot td.r span {{ display:block; color:var(--stone); font-size:8pt; margin-top:.02in; }}
.hot td.g {{ color:var(--stone); }}
/* resumen */
.map {{ display:block; width:4.55in; margin:0 auto; }}
.map .ct.b {{ font:300 9.5px 'IvyOra'; }}
.map .it {{ font:italic 200 7px 'IvyOra'; }}
.stages {{ margin-top:.22in; }}
.stages td {{ padding:.1in .1in .09in 0; }}
.stages td {{ font:300 8.8pt/1.35 'Karla'; }}
.stages td.f {{ font-weight:700; }}
/* banda beige en encabezados de Vuelos y Hoteles */
.flights th, .hot th {{ background:var(--oat); color:var(--ink); border-bottom:0; padding:.1in .1in .09in 0; }}
.flights th:first-child, .hot th:first-child, .flights td:first-child, .hot td:first-child {{ padding-left:.14in; }}
.flights th:last-child, .hot th:last-child, .flights td:last-child, .hot td:last-child {{ padding-right:.14in; }}
/* vuelos */
.fly .fnotes {{ position:absolute; left:.7in; right:.7in; bottom:1.0in; margin:0; border-top:.5pt solid var(--oat); padding-top:.16in; column-gap:.5in; }}
.fly .fnotes h4 {{ font:400 6pt 'Karla'; letter-spacing:.26em; text-transform:uppercase; color:var(--stone); margin-bottom:.07in; }}
.fly .fnotes li {{ font:300 7pt/1.5 'Karla'; color:var(--stone); margin-bottom:.02in; padding-left:.12in; text-indent:-.12in; }}
.fly .fnotes li::before {{ width:.12in; }}
.pax p {{ font:300 11.5pt/1.45 'IvyOra'; }}
.pax {{ align-items:flex-start; }}
.pax .lb {{ padding-top:.05in; white-space:nowrap; }}
/* itinerario en flujo */
.itin {{ position:absolute; left:.7in; right:.7in; display:grid; grid-template-columns:1.9in 1fr; column-gap:.5in; }}
.itin.flip {{ grid-template-columns:1fr 1.9in; }}
.itin.flip .side {{ order:2; }}
.side {{ position:relative; }}
.side figure {{ height:2.52in; width:1.9in; position:absolute; left:0; }}
.side figcaption {{ position:absolute; left:0; bottom:-.21in; font:italic 200 8.5pt 'IvyOra'; color:var(--stone); }}
.itin.flip .side figcaption {{ left:auto; right:0; }}
.dayf {{ padding-bottom:.24in; margin-bottom:.24in; border-bottom:.5pt solid var(--oat); }}
.dayf:last-child {{ border-bottom:0; margin-bottom:0; padding-bottom:0; }}
.dayf .dt {{ font:700 7.3pt/1.2 'Karla'; letter-spacing:.2em; text-transform:uppercase; color:#B9A791; }}
.dayf h3 {{ font:200 23pt/1.08 'IvyOra'; margin:.07in 0 .17in; }}
.dayf .ag {{ grid-template-columns:.7in 1fr; row-gap:.09in; }}
/* hotel: texto arriba, 4 fotos grandes */
.stay4 .head {{ position:absolute; left:.7in; right:.7in; top:1.2in; }}
.stay4 h2 {{ font:200 34pt/1.05 'IvyOra'; }}
.stay4 .loc {{ display:flex; align-items:center; gap:.16in; margin-top:.09in; }}
.stay4 .loc .sub {{ font-size:12.5pt; margin:0; }}
.stay4 .stars {{ display:inline-flex; gap:.035in; }}
.stay4 .stars svg {{ width:.125in; height:.125in; fill:#A8937B; }}
.stay4 dl {{ display:grid; grid-template-columns:1.25in .8in 3.2in 1fr; column-gap:.2in; margin-top:.26in;
  border-top:.5pt solid var(--stone); border-bottom:.5pt solid var(--oat); padding:.12in 0 .11in; }}
.stay4 dd {{ font:300 10.5pt/1.25 'IvyOra'; margin-top:.03in; }}
.stay4 .desc {{ font:300 8.7pt/1.62 'Karla'; color:var(--soft); margin-top:.2in; }}
.stay4 .four {{ position:absolute; left:.7in; right:.7in; bottom:.95in; display:grid; grid-template-columns:1fr 1fr; gap:.1in; }}
.stay4 .four img {{ height:2.8in; }}
/* cierre: minimalista, tono sobre tono */
.end {{ background:var(--oat); color:var(--ink); }}
.end .logo {{ top:3.75in; width:2.85in; color:var(--stone); }}
.end .follow {{ position:absolute; left:0; right:0; top:5.25in; text-align:center; }}
.end .follow::before {{ content:''; display:block; width:.42in; border-top:.5pt solid var(--stone); margin:0 auto .42in; }}
.end .follow a {{ color:inherit; text-decoration:none; display:block; }}
.end .follow .lb {{ color:var(--stone); }}
.end .follow .h {{ font:200 27pt/1.1 'IvyOra'; margin-top:.1in; }}
.end .follow .u {{ font:italic 200 14pt/1.2 'IvyOra'; margin-top:.2in; color:var(--soft); }}
.end .who {{ bottom:1.2in; }}
.end .who b {{ font:300 12.5pt 'IvyOra'; }}
.end .who p {{ font:300 7.6pt/1.7 'Karla'; color:var(--stone); opacity:1; letter-spacing:.04em; margin-top:.04in; }}
.end .cred {{ left:1.7in; right:1.7in; bottom:.48in; font-size:5.6pt; color:var(--stone); opacity:.75; }}
/* cotización */
.quote .sums {{ margin-top:.3in; }}
.quote .sums div {{ display:flex; justify-content:space-between; align-items:baseline; padding:.13in 0 .12in; border-bottom:.5pt solid var(--oat); }}
.quote .sums div b {{ font:300 13pt 'IvyOra'; }}
.quote .total {{ margin-top:.22in; }}
.index li {{ padding:.125in 0 .115in; }}
.index li b {{ font-size:12.5pt; }}
.cover .card h1 {{ font-size:50pt; margin-top:.45in; }}
.cover .card .t2 {{ font:200 19pt/1.1 'IvyOra'; margin:.02in 0 .1in; }}

/* ── cambios del consejo de diseño ── */
.lb {{ font-size:6.8pt; letter-spacing:.22em; }}
th {{ font-size:6.8pt; letter-spacing:.2em; }}
.top, .bot {{ font-size:6.6pt; letter-spacing:.24em; }}
.bot a {{ display:block; color:inherit; }}
td {{ font-size:9pt; }}
.cover .card {{ bottom:.7in; width:3.9in; padding:.34in .4in .32in; background:rgba(223,211,197,.9); }}
.cover .card .logo {{ width:1.75in; }}
.cover .card h1 {{ margin-top:.3in; }}
.cover .card .sub {{ color:var(--stone); opacity:1; }}
.cover .card dl {{ grid-template-columns:.9in 1fr; }}
.cover .card dt {{ font-size:6.4pt; letter-spacing:.24em; }}
.open .card {{ width:4.6in; padding:.3in .4in .32in; }}
.hot td:nth-child(4) {{ white-space:nowrap; }}
.open .card h1 {{ font-size:36pt; margin:.14in 0 0; }}
.index li {{ display:block; padding:0; }}
.index li a {{ display:grid; grid-template-columns:.62in 1fr auto; align-items:baseline; padding:.125in 0 .115in; color:inherit; text-decoration:none; }}
.dot {{ display:inline-flex; align-items:center; justify-content:center; width:11pt; height:11pt; border-radius:50%;
  background:var(--ink); color:var(--paper); font:500 6.6pt 'Karla'; letter-spacing:0; }}
.stages th, .notes table th {{ background:var(--oat); color:var(--ink); border-bottom:0; padding:.1in .1in .09in 0; }}
.stages th:first-child, .stages td:first-child, .notes table th:first-child, .notes table td:first-child {{ padding-left:.14in; }}
.stages td {{ font-size:9pt; }}
.fly .pax {{ display:block; margin-top:.5in; }}
.fly .pax .lb {{ display:block; padding:0; }}
.fly .pax .names {{ display:grid; grid-template-columns:repeat(3, auto); justify-content:start; column-gap:.45in; row-gap:.02in; margin-top:.07in; }}
.fly .pax .names span {{ font:300 9pt/1.5 'Karla'; color:var(--ink); white-space:nowrap; }}
.flights td {{ font-size:8.8pt; }}
.flights td:nth-child(1) {{ color:var(--ink); font-weight:700; }}
.flights td:nth-child(6) {{ color:var(--ink); }}
.flights td:nth-child(6) b {{ font-weight:500; }}
.flights th:nth-child(9), .flights td:nth-child(9) {{ text-align:right; }}
.flights tr.grp td {{ font:400 6.6pt 'Karla'; letter-spacing:.22em; text-transform:uppercase; color:var(--soft); padding:.2in 0 .07in .14in; border-bottom:.5pt solid var(--stone); }}
.flights sup {{ font:500 6.5pt 'Karla'; vertical-align:2pt; margin-left:.03in; }}
.fly .fnotes h4 {{ font-size:6.8pt; letter-spacing:.22em; }}
.fly .fnotes li {{ font-size:8pt; color:var(--soft); }}
.hot td.g {{ color:var(--ink); font-weight:700; white-space:nowrap; }}
.hot td.h {{ font-size:11.5pt; white-space:nowrap; }}
.hot td.r b {{ font-size:9pt; text-wrap:balance; }}
.hot td.r span {{ color:var(--soft); font-size:8.4pt; }}
.itin {{ grid-template-columns:2.35in 1fr; column-gap:.3in; }}
.itin.flip {{ grid-template-columns:1fr 2.35in; }}
.side figure {{ height:3.1in; width:2.35in; }}
.side figcaption {{ font-size:10pt; color:var(--soft); bottom:-.24in; }}
.dayf .dt {{ font-size:7.8pt; letter-spacing:.16em; color:#927F68; }}
.dayf.nh .ag {{ grid-template-columns:0 1fr; }}
.ag .t, .ag .d {{ max-width:4.3in; text-wrap:pretty; }}
.stay4 .desc {{ column-count:2; column-gap:.3in; font-size:9pt; }}
.stay4 .loc .dot {{ margin-right:-.04in; }}
.quote h1 i {{ font:italic 200 19pt 'IvyOra'; color:var(--stone); margin-left:.12in; }}
.quote td:last-child {{ font-size:16pt; }}
.quote .total {{ margin:.3in -.3in 0; align-items:center; padding:.22in .3in; }}
.quote .total .lb {{ font-size:7pt; letter-spacing:.2em; color:var(--ink); }}
.quote .fine {{ font-size:8.3pt; }}
.notes .cols {{ row-gap:.04in; }}
.notes li, .notes .cols p {{ font-size:8.5pt; }}
.notes td {{ font-size:8.5pt; }}
.notes th {{ font-size:6.4pt; }}
.end .who b {{ font-size:16pt; }}
.end .who p {{ font-size:8pt; }}
.end .who p.ct {{ margin-top:.09in; font:400 10pt/1.6 'Karla'; color:var(--ink); letter-spacing:.02em; }}
.end .who a {{ color:inherit; text-decoration:none; }}
.end .cred {{ font-size:6.5pt; opacity:1; }}

.logo {{ overflow:visible; }}
.fly .pax .names {{ display:block; margin-top:.07in; font:300 7pt/1.5 'Karla'; color:var(--ink); white-space:nowrap; }}
.fly .pax .names i {{ display:inline-block; width:2.4pt; height:2.4pt; border:.5pt solid var(--stone); border-radius:50%; margin:0 .045in; vertical-align:.08em; }}
.notes h4 {{ font:700 9pt/1.3 'Karla'; color:var(--soft); letter-spacing:.01em; margin:0 0 .08in; }}
.notes ul {{ margin-bottom:.26in; }}
.notes .cols p {{ margin-bottom:.26in; }}

.fly .fnotes {{ display:block; padding-top:.12in; }}
.fly .fnotes h4 {{ font-size:5.6pt; letter-spacing:.24em; margin:0 0 .03in; }}
.fly .fnotes p {{ font:300 6.4pt/1.5 'Karla'; color:var(--soft); max-width:5.6in; margin:0 0 .09in; }}
.fly .fnotes p:last-child {{ margin-bottom:0; }}
'''
CSS = B.CSS + EXTRA.replace('{{', '{').replace('}}', '}')

# ───────────────────────── Cotización Rápida ─────────────────────────
RAPIDA_CSS = """
.rap .rband { position:absolute; left:0; top:0; width:8.5in; height:3.25in; overflow:hidden; }
.rap .rband img { width:100%; height:100%; object-fit:cover; display:block; }
.rap .bcard { position:absolute; left:.7in; top:.42in; width:4.1in; box-sizing:border-box; background:rgba(223,211,197,.9);
  padding:.3in .36in .28in; color:var(--ink); }
.rap .bcard .logo { width:1.5in; }
.rap .bcard h1 { font:200 31pt/1.02 'IvyOra'; margin:.26in 0 0; }
.rap .bcard .sub { font:italic 200 12pt/1.25 'IvyOra'; color:var(--stone); margin-top:.06in; }
.rap .bcard dl { display:grid; grid-template-columns:.88in 1fr; row-gap:.045in; margin-top:.2in; }
.rap .bcard dt { font:400 6.2pt 'Karla'; letter-spacing:.24em; text-transform:uppercase; color:var(--stone); padding-top:.035in; }
.rap .bcard dd { font:300 8.8pt/1.35 'Karla'; }
.rap.first .in { top:3.62in; }
.rap h2 { font:200 22pt/1.1 'IvyOra'; margin:0 0 .13in; }
.rap h2.sp { margin-top:.34in; }
.rap p.tx { font:300 8.6pt/1.6 'Karla'; color:var(--soft); max-width:6.2in; }
.rap .opt { margin-top:.36in; }
.rap .opt:first-child { margin-top:0; }
.rap .oh { display:grid; grid-template-columns:auto 1fr auto; column-gap:.2in; align-items:baseline; margin-bottom:.11in; }
.rap .oh h3 { font:200 17pt/1.1 'IvyOra'; }
.rap .oh .pr b { font:300 15pt 'IvyOra'; }
.rap .oh .pr span { font:300 7.6pt 'Karla'; color:var(--soft); margin-left:.1in; }
.rap .on { font:300 7.6pt/1.55 'Karla'; color:var(--soft); margin-top:.1in; max-width:6.5in; }
.rap .cmp th { background:var(--oat); color:var(--ink); border-bottom:0; padding:.1in .1in .09in 0; }
.rap .cmp th:first-child, .rap .cmp td:first-child { padding-left:.14in; }
.rap .cmp th:last-child, .rap .cmp td:last-child { padding-right:.14in; text-align:right; }
.rap .cmp td { padding:.1in .1in .09in 0; vertical-align:middle; }
.rap .cmp td b { display:block; font:300 12.5pt/1.2 'IvyOra'; }
.rap .cmp td span { display:block; font-size:8pt; color:var(--soft); margin-top:.02in; }
.rap .flights td { padding-top:.085in; padding-bottom:.075in; }
.rap .flights tr.grp td { padding-top:.13in; }
.rap .fineprint { font:300 7.4pt/1.55 'Karla'; color:var(--soft); margin-top:.3in; padding-top:.14in; border-top:.5pt solid var(--oat); }
.rap .sign { position:absolute; left:.7in; right:.7in; bottom:.95in; display:flex; justify-content:space-between; align-items:baseline;
  border-top:.5pt solid var(--stone); padding-top:.13in; }
.rap .sign b { font:300 12pt 'IvyOra'; }
.rap .sign span { font:300 7.6pt 'Karla'; color:var(--stone); margin-left:.12in; letter-spacing:.04em; }
.rap .sign a { font:400 8.6pt 'Karla'; color:var(--ink); text-decoration:none; }
.rap .sign i { display:inline-block; width:2.4pt; height:2.4pt; border:.5pt solid var(--stone); border-radius:50%; margin:0 .08in; vertical-align:.08em; }
.rap .stay4 .head, .rap.stay4 .head { top:1.2in; }
.rap.stay4 ul.am { columns:2; column-gap:.3in; margin-top:.2in; list-style:none; }
.rap.stay4 ul.am li { font:300 8.8pt/1.5 'Karla'; color:var(--soft); padding-left:.14in; text-indent:-.14in; margin-bottom:.04in; break-inside:avoid; }
.rap.stay4 ul.am li::before { content:'–'; display:inline-block; width:.14in; text-indent:0; color:var(--stone); }
.rap .quote-in table { margin-top:0; }
"""

def band_cover(img, title, sub, rows):
    """Portada compacta de la Cotización Rápida: franja de foto con tarjeta beige (logo, título, datos)."""
    dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
    return (f'<div class="rband"><img src="{img}"></div>'
            f'<div class="bcard">{logo(1)}<h1>{title}</h1><p class="sub">{sub}</p><dl>{dl}</dl></div>')

def sign():
    """Firma de contacto al pie de la última hoja de una Cotización Rápida."""
    return ('<div class="sign"><div><b>Mariana Medina</b><span>Luxury Travel Designer</span></div>'
            '<div><a href="tel:+525518500549">55 1850 0549</a><i></i><a href="mailto:mariana.medina@nuba.com">mariana.medina@nuba.com</a>'
            '<i></i><a href="https://instagram.com/thesuitelife.mx">@thesuitelife.mx</a></div></div>')


def flights_table(groups):
    """groups = [(rótulo, [tuplas de frow])]. Tabla de vuelos agrupada (Ida / Vuelos internos / Regreso)."""
    out = ['<table class="flights">',
           '<tr><th>Fecha</th><th>Aerolínea</th><th>No.</th><th>Desde</th><th>Hacia</th><th>Clase</th><th>Salida</th><th>Llegada</th><th>Duración</th></tr>']
    for label, rows in groups:
        if label: out.append(f'<tr class="grp"><td colspan="9">{label}</td></tr>')
        out += [frow(*r) for r in rows]
    return '\n'.join(out) + '</table>'

def html_doc(title, body, css=''):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{CSS}{css}</style></head><body>\n{body}\n</body></html>')

def print_pdf(html, out, root, name='documento.html'):
    """Imprime con Chrome headless: sin encabezados, con marcadores."""
    root = pathlib.Path(root); out = pathlib.Path(out)
    (root / name).write_text(html, encoding='utf-8'); out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    '--generate-pdf-document-outline', f'--print-to-pdf={out}', f'file://{root}/{name}'],
                   check=True, capture_output=True)
    (root / name).unlink()
    return out


# ───────────────────────── piezas de documento largo (Entrega Final, Guía de Viaje) ─────────────────────────
import json, math

DOC_CSS = """
.cover .card .t2.sm { font:200 12.5pt/1.3 'IvyOra'; margin:.06in 0 .12in; }
.stay4 h2.lg { font-size:27pt; }
.stay4 .four.n3 img:first-child { grid-column:1 / 3; width:100%; }
.res .emer { margin-top:.2in; display:flex; gap:.3in; align-items:baseline; padding:.12in .14in .11in; background:var(--almond); }
.res .emer p { font:300 9pt 'Karla'; color:var(--ink); }
.res .emer a { color:inherit; text-decoration:none; }
.fly .pax.nx { margin-top:.32in; }
.fly.c .flights td { padding-top:.06in; padding-bottom:.052in; font-size:8.6pt; line-height:1.25; }
.stay4 .four.n2 { grid-template-columns:1fr; }
.stay4 .four.n2 img { width:100%; height:2.85in; }
.fly.c .flights { margin-top:.1in; }
.fly.c .pax { padding-bottom:.1in; }
.fly.c .pax.nx { margin-top:.27in; }
"""

def measure(blocks, root, css='', wrap='<div class="page"><div class="in">{}</div></div>'):
    """Altura real (in) de cada bloque HTML, medida con Chrome dentro de `wrap` (márgenes incluidos)."""
    from playwright.sync_api import sync_playwright
    root = pathlib.Path(root)
    inner = ''.join(f'<div class="mz" style="display:flow-root">{b}</div>' for b in blocks)
    (root / 'medir.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{css}</style></head><body>'
                                     + wrap.format(inner) + '</body></html>', encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_page(); pg.goto(f'file://{root}/medir.html'); pg.wait_for_timeout(800)
        hs = pg.evaluate("[...document.querySelectorAll('.mz')].map(e=>e.getBoundingClientRect().height/96)")
        b.close()
    (root / 'medir.html').unlink()
    return hs

def fit(heights, first_cap, cap):
    """Reparte bloques en hojas según su altura (in). Devuelve listas de índices, una por hoja."""
    pages, cur, used = [], [], 0.0
    for i, h in enumerate(heights):
        if cur and used + h > (cap if pages else first_cap):
            pages.append(cur); cur, used = [], 0.0
        cur.append(i); used += h
    pages.append(cur); return pages

def cover_page(img, title, t2, client, rows, t2_small=False, h1_pt=None):
    """Portada: foto vertical a página completa y tarjeta beige con logo, título, cliente y datos."""
    dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
    return (f'<div class="page cover"><img src="{img}"><div class="card">{logo(1)}<h1{f" style={chr(34)}font-size:{h1_pt}pt;white-space:nowrap{chr(34)}" if h1_pt else ""}>{title}</h1>'
            f'<p class="t2{" sm" if t2_small else ""}">{t2}</p><p class="sub">{client}</p><dl>{dl}</dl></div></div>')

def index_page(entries, para, por='Mariana Medina<br>Luxury Travel Designer', label='Propuesta para'):
    """entries = [(número, nombre, página)]; cada renglón enlaza a #s<número>."""
    li = ''.join(f'<li><a href="#s{n}"><i>.{n:02d}</i><b>{name}</b><span>{pg:02d}</span></a></li>' for n, name, pg in entries)
    return (f'<div class="page index" id="indice"><div class="panel"><h1>Índice</h1><span>Luxury Travel Design</span></div>'
            f'<div class="list"><ol>{li}</ol></div><div class="meta"><div><span class="lb">{label}</span><p>{para}</p></div>'
            f'<div><span class="lb">Diseñado por</span><p>{por}</p></div></div></div>')

def opener_page(img, num, title, sid):
    return (f'<div class="page cover open" id="{sid}"><img src="{img}"><div class="card"><span class="lb">{num}</span>'
            f'<h1>{title}</h1></div></div>')

def map_svg(bbox, trip, stops, labels=(), italics=(), width=None):
    """Mapa de fondo transparente. bbox=(lon0, lon1, lat0, lat1); trip = ids ISO de los países del viaje (Oatmeal);
    el resto del recuadro va en Soft Almond. stops = [(nombre, lon, lat, dx, dy, [números])]. Sin líneas entre paradas.
    dx > 0: etiqueta a la derecha y números hacia la derecha; dx < 0: etiqueta a la izquierda y números hacia la izquierda.
    width (in) fija el ancho impreso; el alto del mapa siempre mide 330 unidades."""
    B.LON0, B.LON1, B.LAT0, B.LAT1 = bbox
    B.S = 330 / (B.LAT1 - B.LAT0)
    B.K = math.cos(math.radians((B.LAT0 + B.LAT1) / 2))
    W, H = (B.LON1 - B.LON0) * B.K * B.S, (B.LAT1 - B.LAT0) * B.S
    topo = json.loads((B.ROOT / 'geo/countries-50m.json').read_text())
    ids = {str(g.get('id')) for g in topo['objects']['countries']['geometries'] if g.get('id') is not None}
    cp = B.country_paths(ids)
    st = f' style="width:{width}in"' if width else ''
    out = [f'<svg class="map"{st} viewBox="0 0 {W:.1f} {H:.1f}" xmlns="http://www.w3.org/2000/svg">']
    for cid, d in cp.items():
        if d and cid not in trip:
            out.append(f'<path d="{d}" fill="#F0EDE8" stroke="#FCF9F5" stroke-width=".5" fill-rule="evenodd"/>')
    for cid in trip:
        out.append(f'<path d="{cp[cid]}" fill="#DFD3C5" stroke="#FCF9F5" stroke-width=".5" fill-rule="evenodd"/>')
    for lon, lat, t in labels:
        x, y = B.proj(lon, lat); out.append(f'<text class="rg" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{t}</text>')
    for lon, lat, t in italics:
        x, y = B.proj(lon, lat); out.append(f'<text class="it" x="{x:.1f}" y="{y:.1f}">{t}</text>')
    for name, lon, lat, dx, dy, nums in stops:
        x, y = B.proj(lon, lat)
        for j, n in enumerate(nums):
            cx = x + j * 9.2 if dx > 0 else x - (len(nums) - 1 - j) * 9.2
            out.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="4" fill="#232323"/>'
                       f'<text x="{cx:.1f}" y="{y + 1.9:.1f}" text-anchor="middle" style="font:500 5.4px Karla;fill:#FCF9F5">{n}</text>')
        lx = x + dx + (len(nums) - 1) * 9.2 if dx > 0 else x + dx - (len(nums) - 1) * 9.2
        out.append(f'<text class="ct b" x="{lx:.1f}" y="{y + dy:.1f}" text-anchor="{"start" if dx > 0 else "end"}">{name}</text>')
    return '\n'.join(out) + '</svg>'

def day_html(label, place, ents, nh=None):
    if nh is None: nh = not any(e[0] for e in ents)
    return (f'<section class="dayf{" nh" if nh else ""}"><p class="dt">{label}</p><h3>{place}</h3>'
            f'<div class="ag">{"".join(entry(*e) for e in ents)}</div></section>')

def paginate_days(days, root, css='', cap=8.55):
    """days = [dict(label, place, ents, photo)]. Mide cada día con Chrome y reparte en hojas. Devuelve (alturas, hojas)."""
    from playwright.sync_api import sync_playwright
    root = pathlib.Path(root)
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{css}</style></head><body><div style="width:4.45in">'
           + ''.join(day_html(d['label'], d['place'], d['ents']) for d in days) + '</div></body></html>')
    (root / 'medir.html').write_text(doc, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_page(); pg.goto(f'file://{root}/medir.html'); pg.wait_for_timeout(800)
        hs = pg.evaluate("[...document.querySelectorAll('.dayf')].map(e=>e.getBoundingClientRect().height/96)")
        b.close()
    (root / 'medir.html').unlink()
    pages, cur, used = [], [], 0.0
    for i, h in enumerate(hs):
        extra = h + (0.24 if cur else 0)
        if cur and used + extra > cap:
            pages.append(cur); cur, used = [], 0.0; extra = h
        cur.append(i); used += extra
    pages.append(cur)
    return hs, pages

def itin_pages(days, hs, pages, first_page, caps, num='.04', name='Itinerario Diario', cap=8.55, min_photos=2):
    """Hojas del itinerario: fotos de 2.35 x 3.1 in alineadas con su día, alternando de lado; mínimo 2 fotos por hoja."""
    out = []
    for k, idxs in enumerate(pages):
        want, y = [], 0.0
        for i in idxs:
            if days[i].get('photo'): want.append([y + 0.03, days[i]['photo']])
            y += hs[i] + 0.24
        want = want[:2]
        assert len(want) >= min_photos, f'la hoja {k + 1} del itinerario necesita al menos {min_photos} fotos'
        for j in range(1, len(want)): want[j][0] = max(want[j][0], want[j - 1][0] + 3.52)
        for j in range(len(want) - 1, -1, -1):
            lim = (cap - 3.3) if j == len(want) - 1 else want[j + 1][0] - 3.52
            want[j][0] = max(0.0, min(want[j][0], lim))
        side = ''.join(f'<figure style="top:{t:.2f}in"><img src="img/{ph}.jpg"><figcaption>{caps[ph]}</figcaption></figure>' for t, ph in want)
        nh = not any(e[0] for i in idxs for e in days[i]['ents'])
        body = ''.join(day_html(days[i]['label'], days[i]['place'], days[i]['ents'], nh) for i in idxs)
        out.append(f'<div class="page">{furniture(num, name, first_page + k)}'
                   f'<div class="itin{" flip" if k % 2 else ""}" style="top:1.3in"><div class="side">{side}</div><div class="days">{body}</div></div></div>')
    return '\n'.join(out)

def hotel_sheet(num, page, sid, n, name, loc, nstars, facts, desc, photos, section='Hotel'):
    """Hoja de hotel: nombre, punto numerado, ubicación, estrellas, franja de 4 datos, descripción a dos columnas y fotos grandes.
    4 fotos -> retícula 2 x 2; 3 -> una ancha y dos; 2 -> una fila."""
    dl = ''.join(f'<div><dt class="lb">{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    return (f'<div class="page stay4" id="{sid}">{furniture(num, section, page)}<div class="head">'
            f'<h2{" class=lg" if len(name) > 28 else ""}>{name}</h2><div class="loc">{dot(n)}<p class="sub">{loc}</p>{stars(nstars)}</div>'
            f'<dl>{dl}</dl><p class="desc">{desc}</p></div>'
            f'<div class="four n{len(photos)}">{"".join(f"<img src={chr(34)}{p}{chr(34)}>" for p in photos)}</div></div>')

def closing_page(credits):
    return (f'<div class="page end">{logo(1)}<div class="follow"><span class="lb">Síguenos en Instagram</span>'
            '<a class="h" href="https://instagram.com/thesuitelife.mx">@thesuitelife.mx</a>'
            '<a class="u" href="https://thesuitelife.com.mx">thesuitelife.com.mx</a></div>'
            '<div class="who"><b>Mariana Medina</b><p>Luxury Travel Designer</p>'
            '<p class="ct"><a href="tel:+525518500549">55 1850 0549</a> &nbsp;·&nbsp; <a href="mailto:mariana.medina@nuba.com">mariana.medina@nuba.com</a></p></div>'
            f'<p class="cred">{credits}</p></div>')
