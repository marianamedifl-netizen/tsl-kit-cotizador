#!/usr/bin/env python3
"""TSL · Cotización de Hoteles (Formato Nuevo) — ejemplo: Japón (Tokio, Kioto, Osaka), familia en 2 habitaciones.
Uso: python3 cotizacion_hoteles_japon.py [salida.pdf]
Hojas: 1) portada compacta + comparativa (un precio «desde» por hotel y sus cuartos cotizados) · 2) una hoja por hotel con sus tipos de cuarto · 3) notas y cancelación.
Sirve para puros hoteles: una o varias ciudades, una o varias opciones de hotel por ciudad, una o varias habitaciones.
Las fotos van en img/: si un archivo no existe, la hoja deja el hueco marcado (no se rellena con otra foto).
Tarifas del ejemplo: Sabre, tarifa preferencial (NEM), consultadas el 16 nov 2026. No lleva códigos de tarifa, comisión ni plataforma."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import tsl_base as B
import tsl_formato as F

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'salida.pdf').resolve()
B.TRIP = 'Japón · Marzo 2027'
TITLE = 'Japón · Cotización de hoteles'

# ───────────────────────── datos ─────────────────────────
N_HAB = 2                                   # habitaciones que necesita el cliente
PORTADA = dict(img='img/japon_band.jpg', title='Japón', sub='Tokio · Kioto · Osaka',
               rows=[('Fechas', '12 – 20 mar 2027 · 8 noches'), ('Viajeros', '4 personas · 2 habitaciones'), ('Documento', 'Cotización de hoteles')])

# Por ciudad: opciones de hotel. Por hotel: cuartos = (nombre, datos, total por habitación con impuestos, nota de camas, recomendada)
CIUDADES = [
    dict(ciudad='Tokio', fechas='12 – 15 mar 2027', noches=3, hoteles=[
        dict(letra='A', nombre='Palace Hotel Tokyo', loc='Marunouchi, Chiyoda, Tokio', estrellas=5, regimen='Desayuno diario', fotos=['palace_1', 'palace_2'],
             cuartos=[('Deluxe Room', '45 m² · cama king', 3974.74, '', False, 'palace_deluxe'),
                      ('Grand Deluxe Room', '55 m² · vista al Palacio Imperial · 2 camas twin', 4901.13, '', True, 'palace_grand'),
                      ('Deluxe Room with Balcony', '45 m² · balcón · vista al Palacio Imperial · king o twin', 4972.39, '', False, 'palace_balcony')],
             beneficios=['Desayuno diario para 2 por habitación', 'Upgrade sujeto a disponibilidad', 'Early check-in y late check-out', 'Wi-Fi'],
             cancela=('11 mar 2027, 15:00 h', '1 noche con impuestos'), recomendado=False),
        dict(letra='B', nombre='Four Seasons Hotel Tokyo at Otemachi', loc='Otemachi, Chiyoda, Tokio', estrellas=5, regimen='Desayuno diario', fotos=['otemachi_1', 'otemachi_2'],
             cuartos=[('Superior Room · Skyline View', '49 m² · pisos 34 a 38 · cama king', 3180.05, 'Con 2 camas dobles: US$3,228', True, 'otemachi_superior'),
                      ('Deluxe Room · City View', 'Pisos 34 a 38 · cama king', 3243.39, 'Con 2 camas dobles: US$3,291', False, 'otemachi_deluxe'),
                      ('Deluxe Room · Imperial Garden View', 'Vista al jardín imperial y al skyline · cama king', 3615.53, 'Con 2 camas dobles: US$3,663', False, 'otemachi_garden')],
             beneficios=['Tercera noche de cortesía, ya aplicada', 'Desayuno diario para 2 por habitación', 'Crédito de hotel de US$100 por estancia',
                         'Upgrade de una categoría, sujeto a disponibilidad'],
             cancela=('26 feb 2027, 15:00 h', '1 noche con impuestos'), recomendado=True)]),
    dict(ciudad='Kioto', fechas='15 – 18 mar 2027', noches=3, hoteles=[
        dict(letra='C', nombre='Four Seasons Hotel Kyoto', loc='Higashiyama, Kioto', estrellas=5, regimen='Desayuno diario', fotos=['fskyoto_1', 'fskyoto_2'],
             cuartos=[('Premier Room', '53 a 61 m² · vista a la ciudad o al patio · cama king', 4351.79, 'Con 2 camas dobles: US$4,447', True, 'fskyoto_premier'),
                      ('Premier Heritage Garden', '52 a 53 m² · vista al jardín del estanque · cama king', 4525.98, 'Con 2 camas dobles: US$4,621', False, 'fskyoto_heritage'),
                      ('Four Seasons Heritage Garden', '53 m² · balcón · vista al jardín del estanque · cama king', 4763.52, 'Con 2 camas dobles: US$4,859', False, 'fskyoto_fsgarden')],
             beneficios=['Tercera noche de cortesía, ya aplicada', 'Desayuno diario para 2 por habitación', 'Crédito de hotel de US$100 por estancia',
                         'Upgrade de una categoría, sujeto a disponibilidad'],
             cancela=('8 mar 2027, 15:00 h', '1 noche con impuestos'), recomendado=True),
        dict(letra='D', nombre='Hotel The Mitsui Kyoto', loc='Luxury Collection · Nijo, Kioto', estrellas=5, regimen='Desayuno diario', fotos=['mitsui_1', 'mitsui_2'],
             cuartos=[('Deluxe Room', '43 a 51 m² · vista a la ciudad · king o 2 dobles', 5225.76, '', True, 'mitsui_deluxe'),
                      ('Premier Room', 'Vista a la ciudad · king o 2 dobles', 5748.33, '', False, 'mitsui_premier'),
                      ('Garden Room', 'Vista al jardín · king o 2 dobles', 6270.91, '', False, 'mitsui_garden')],
             beneficios=['Desayuno diario para 2 por habitación', 'Crédito de hotel de US$100 por estancia', 'Upgrade sujeto a disponibilidad',
                         'Early check-in y late check-out, sujetos a disponibilidad', 'Amenidad de bienvenida'],
             cancela=('13 mar 2027', 'JPY 209,000 por habitación (Deluxe Room)'), recomendado=False)]),
    dict(ciudad='Osaka', fechas='18 – 20 mar 2027', noches=2, hoteles=[
        dict(letra='E', nombre='Four Seasons Hotel Osaka', loc='Dojima, Osaka', estrellas=5, regimen='Desayuno diario', fotos=['fsosaka_1', 'fsosaka_2'],
             cuartos=[('Superior Room', '43 a 46 m² · vista a la ciudad · pisos 29 a 31 · king o twin', 1976.13, '', False, 'fsosaka_superior'),
                      ('Deluxe Room', '43 a 46 m² · vista al skyline · pisos 32 a 35 · king o twin', 2039.48, '', True, 'fsosaka_deluxe'),
                      ('Premier Room', '42 a 47 m² · 2 camas twin', 2086.98, '', False, 'fsosaka_premier')],
             beneficios=['Desayuno diario para 2 por habitación', 'Crédito de hotel de US$100 por estancia', 'Upgrade de una categoría, sujeto a disponibilidad',
                         'Nota de bienvenida'],
             cancela=('17 mar 2027, 15:00 h', '1 noche con impuestos'), recomendado=True)]),
]
NOTA_PRECIO = ('El precio corresponde a la primera habitación de cada lista, la más económica; el de cada habitación está en la hoja del hotel. '
               'Precios en dólares por la estancia completa, con impuestos y cargo de servicio, en tarifa preferencial reembolsable. Consultados el '
               '16 de noviembre de 2026 y sujetos a disponibilidad. Los hoteles cobran en yenes: el monto en dólares puede variar con el tipo de cambio.')
INCLUYE = ['Alojamiento en la habitación elegida por las noches indicadas, para 2 personas por habitación.', 'Impuestos y cargo de servicio del hotel.',
           'Desayuno diario para 2 personas por habitación.', 'Los beneficios The Suite Life indicados en la hoja de cada hotel.']
EXCLUYE = ['Vuelos, trenes y traslados.', 'Impuestos locales que se pagan en el hotel: en Hotel The Mitsui Kyoto, impuesto de alojamiento (JPY 200 a 10,000) e impuesto '
           'de baño (JPY 150), por persona y por noche. En los demás hoteles, pendiente de verificar.', 'Camas adicionales, alimentos y bebidas no especificados y spa.',
           'Seguro de viaje, gastos personales y propinas.']
RESERVAR = ('Cada reserva se garantiza con tarjeta de crédito y se paga directamente en el hotel. Palace Hotel Tokyo carga el total a la llegada o dentro del periodo '
            'de cancelación. La tercera noche de cortesía de Four Seasons requiere estancia mínima de 3 noches y reservar con anticipación.')
GENERAL = ['Precios, disponibilidad e inclusiones sujetos a cambio hasta confirmar la reserva.',
           'Los beneficios de upgrade, early check-in y late check-out dependen de la disponibilidad del hotel al momento de la llegada.',
           'El crédito de hotel aplica a consumos durante la estancia y no es reembolsable ni transferible.',
           'El cliente es responsable de contar con pasaporte vigente y los documentos de viaje requeridos.',
           'Se recomienda ampliamente contratar un seguro de viaje que cubra emergencias médicas, cancelaciones y demoras.']
CREDITOS = ('Fotografías de hoteles: sitios oficiales de Palace Hotel Tokyo, Four Seasons Hotels and Resorts y Hotel The Mitsui Kyoto. '
            'Portada: @mareklumi, vía Unsplash.')

# ───────────────────────── armado ─────────────────────────
def usd(x): return f'US${round(x):,}'
def foto(nombre, cls=''):
    """<img> si la foto existe en img/; si no, hueco marcado."""
    return (f'<img class="{cls}" src="img/{nombre}.jpg">' if (ROOT / 'img' / f'{nombre}.jpg').exists()
            else f'<div class="ph {cls}"><span>Foto</span></div>')
hoteles = [(c, h) for c in CIUDADES for h in c['hoteles']]
desde = lambda h: min(r[2] for r in h['cuartos']) * N_HAB
viaje_desde = sum(min(desde(h) for h in c['hoteles']) for c in CIUDADES)
hab = 'habitación' if N_HAB == 1 else f'{N_HAB} habitaciones'

# hoja 1: comparativa (aprobada por Mariana, maqueta A del consejo). Pocas cifras: un solo precio «desde» por hotel,
# el de su habitación más económica, sin «US$» (la moneda se declara una vez, en la banda del total).
# Fechas y noches van en el rótulo de la ciudad. Los tipos de habitación van en una línea, sin precio, de menor a mayor:
# el primero (el cotizado) en negro y los demás en gris. Sin cancelación ni «Recomendado»: eso vive en la hoja de cada hotel y en Notas.
def num(x): return f'{round(x):,}'
cmp_html = ''
for c in CIUDADES:
    cmp_html += f'<div class="city"><span>{c["ciudad"]}</span><span>{c["fechas"].replace(" 2027", "")} · {c["noches"]} noches</span></div>'
    for h in c['hoteles']:
        rs = sorted(h['cuartos'], key=lambda r: r[2])
        line = ' <i>·</i> '.join((f'<b>{r[0]}</b>' if k == 0 else r[0]) for k, r in enumerate(rs))
        cmp_html += (f'<div class="hb">{F.dot(h["letra"])}<div><p class="n">{h["nombre"]}{F.stars(h["estrellas"])}</p>'
                     f'<p class="z">{h["loc"]} · {h["regimen"].lower()}</p><p class="r">{line}</p></div>'
                     f'<div class="pz"><span class="lb">Desde</span><b>{num(desde(h))}</b></div></div>')
p1 = f'''<div class="page rap first hq">{F.band_cover(**PORTADA) if (ROOT / PORTADA['img']).exists() else
    F.band_cover(**PORTADA).replace(f'<img src="{PORTADA["img"]}">', '<div class="ph" style="width:100%;height:100%"><span>Foto del destino</span></div>')}
  <div class="bot">{F.logo(2)}<span>01</span></div>
  <div class="in">
    <h2>Comparativa</h2>
    <div class="ma">{cmp_html}</div>
    <div class="total"><span class="lb">Viaje completo desde · {hab} · {sum(c["noches"] for c in CIUDADES)} noches · USD</span><b>{usd(viaje_desde)}</b></div>
    <p class="fine">{NOTA_PRECIO}</p>
  </div>
</div>'''

# una hoja por hotel
def hoja(k, c, h, page):
    trs = ''
    for nombre, datos, total, alt, rec, img in h['cuartos']:
        tag = '<i class="rec">Recomendada</i>' if rec else ''
        trs += (f'<tr><td class="f">{foto(img)}</td><td class="r"><b>{nombre}{tag}</b><span>{datos}</span>{f"<span class=alt>{alt}</span>" if alt else ""}</td>'
                f'<td class="p"><b>{usd(total)}</b><span>{usd(total / c["noches"])} por noche</span></td><td class="t">{usd(total * N_HAB)}</td></tr>')
    cols = (f'<th style="width:1.2in">Por habitación</th><th style="width:1.2in">{hab.capitalize()}</th>' if N_HAB > 1
            else '<th style="width:1.2in"></th><th style="width:1.2in">Total</th>')
    ben = ''.join(f'<li>{b}</li>' for b in h['beneficios'])
    return f'''<div class="page rap stay4 hq">{F.furniture(f'.{k + 2:02d}', c['ciudad'], page, link='#')}
  <div class="head">
    <h2 class="hn{' lg' if len(h['nombre']) > 26 else ''}">{h['nombre']}</h2>
    <div class="loc">{F.dot(h['letra'])}<p class="sub">{h['loc']}</p>{F.stars(h['estrellas'])}</div>
    <dl><div><dt class="lb">Fechas</dt><dd>{c['fechas']}</dd></div><div><dt class="lb">Noches</dt><dd>{c['noches']}</dd></div>
        <div><dt class="lb">Habitaciones</dt><dd>{N_HAB} · 2 personas por habitación</dd></div><div><dt class="lb">Régimen</dt><dd>{h['regimen']}</dd></div></dl>
    <div class="two">{''.join(foto(f) for f in h['fotos'])}</div>
    <table class="rooms"><tr><th style="width:1.62in"></th><th>Habitación</th>{cols}</tr>{trs}</table>
    <div class="ben"><span class="lb">Beneficios The Suite Life</span><ul>{ben}</ul></div>
    <p class="can">Cancelación sin cargo hasta el {h['cancela'][0]} (hora del hotel). Después: {h['cancela'][1]}. Precios con impuestos y cargo de servicio.</p>
  </div>
</div>'''

n_h = len(hoteles)
canc = ''.join(f'<tr><td>{h["nombre"]}</td><td>{h["cancela"][0]}</td><td>{h["cancela"][1]}</td></tr>' for _, h in hoteles)
p_notas = f'''<div class="page rap notes">{F.furniture(f'.{n_h + 2:02d}', 'Notas', n_h + 2, link='#')}
  <div class="in">
    <h1 style="font-size:34pt">Notas &amp; Políticas de Cancelación</h1>
    <div class="cols">
      <div>{F.notes('El precio incluye', INCLUYE)}{F.notes('El precio excluye', EXCLUYE)}{F.notes('Para reservar', RESERVAR)}</div>
      <div>{F.notes('Información general', GENERAL)}
        <h4>Políticas de cancelación</h4>
        <table><tr><th>Hotel</th><th style="width:.95in">Sin cargo hasta</th><th style="width:1.05in">Después</th></tr>{canc}</table>
        <p class="cr">{CREDITOS}</p></div>
    </div>
  </div>{F.sign()}</div>'''

body = '\n'.join([p1] + [hoja(k, c, h, k + 2) for k, (c, h) in enumerate(hoteles)] + [p_notas])
EXTRA = '''
.ph { background:var(--almond); display:flex; align-items:center; justify-content:center; box-sizing:border-box; }
.ph span { font:400 6.8pt 'Karla'; letter-spacing:.22em; text-transform:uppercase; color:var(--stone); }
.rap .cr { font:300 6.5pt/1.5 'Karla'; color:var(--stone); margin-top:.2in; }
.hq i.rec { font:700 6.4pt 'Karla'; font-style:normal; letter-spacing:.18em; text-transform:uppercase; color:#927F68; margin-left:.1in; vertical-align:.12em; white-space:nowrap; }
.ma .city { display:flex; justify-content:space-between; font:400 6.8pt 'Karla'; letter-spacing:.2em; text-transform:uppercase; color:var(--soft);
  padding:.11in .14in .05in; border-bottom:.5pt solid var(--stone); }
.ma .city:first-child { padding-top:.02in; }
.hq.first .in { top:3.5in; }
.ma .hb { display:grid; grid-template-columns:.36in 1fr auto; align-items:start; padding:.095in .14in .085in; border-bottom:.5pt solid var(--oat); }
.ma .hb .dot { font-size:6.4pt; color:#FCF9F5; margin-top:.04in; }
.ma .n { font:300 14pt/1.15 'IvyOra'; }
.ma .n .stars { display:inline-flex; gap:.025in; margin-left:.09in; vertical-align:.14em; }
.ma .n .stars svg { width:.09in; height:.09in; fill:#A8937B; }
.ma .z { font:300 8.2pt/1.4 'Karla'; color:var(--soft); margin-top:.02in; }
.ma .r { font:300 8.6pt/1.45 'Karla'; color:var(--stone); margin-top:.05in; }
.ma .r b { font-weight:400; color:var(--ink); }
.ma .r i { font-style:normal; color:var(--oat); margin:0 .03in; }
.ma .pz { text-align:right; padding-left:.2in; }
.ma .pz .lb { display:block; font-size:6.2pt; }
.ma .pz b { display:block; font:300 15pt/1.15 'IvyOra'; margin-top:.02in; }
.hq .total { display:flex; justify-content:space-between; align-items:center; background:var(--oat); padding:.15in .14in; margin-top:.17in; }
.hq .total .lb { color:var(--ink); font-size:7pt; letter-spacing:.2em; }
.hq .total b { font:200 22pt/1 'IvyOra'; }
.hq .fine { font:300 7.4pt/1.5 'Karla'; color:var(--soft); margin-top:.12in; }
.hq.stay4 .head { top:1.2in; }
.hq h2.hn { font:200 32pt/1.05 'IvyOra'; margin:0; }
.hq h2.hn.lg { font-size:26pt; }
.hq.stay4 dl { grid-template-columns:1.35in .7in 2.6in 1fr; margin-top:.2in; }
.hq .two { display:grid; grid-template-columns:1fr 1fr; gap:.1in; margin-top:.2in; }
.hq .two img, .hq .two .ph { display:block; width:100%; height:1.9in; object-fit:cover; }
.hq .two .ph, .hq .rooms .ph { display:flex; }
.hq table.rooms { margin-top:.2in; }
.hq .rooms th { background:var(--oat); color:var(--ink); border-bottom:0; padding:.09in .1in .08in 0; }
.hq .rooms th:nth-child(n+3), .hq .rooms td.p, .hq .rooms td.t { text-align:right; }
.hq .rooms th:last-child, .hq .rooms td:last-child { padding-right:.14in; }
.hq .rooms td { padding:.09in .1in .09in 0; vertical-align:middle; }
.hq .rooms td.f { padding-left:0; }
.hq .rooms td.f img, .hq .rooms td.f .ph { width:1.5in; height:1.0in; object-fit:cover; }
.hq .rooms td.f img { display:block; }
.hq .rooms td.r b { display:block; font:300 13pt/1.2 'IvyOra'; }
.hq .rooms td.r span { display:block; font:300 8.6pt/1.4 'Karla'; color:var(--soft); margin-top:.03in; }
.hq .rooms td.r span.alt { color:var(--stone); font-size:8pt; }
.hq .rooms td.p b { display:block; font:400 9.4pt 'Karla'; }
.hq .rooms td.p span { display:block; font:300 7.8pt 'Karla'; color:var(--soft); margin-top:.02in; white-space:nowrap; }
.hq .rooms td.t { font:300 15pt/1 'IvyOra'; white-space:nowrap; }
.hq .ben { display:grid; grid-template-columns:1.25in 1fr; column-gap:.2in; align-items:baseline; background:var(--almond); padding:.15in .2in .13in; margin-top:.18in; }
.hq .ben .lb { color:#927F68; font-weight:700; }
.hq .ben ul { list-style:none; columns:2; column-gap:.3in; }
.hq .ben li { font:300 8.6pt/1.5 'Karla'; color:var(--soft); padding-left:.13in; text-indent:-.13in; break-inside:avoid; }
.hq .ben li::before { content:'–'; display:inline-block; width:.13in; text-indent:0; color:var(--stone); }
.hq .can { font:300 7.4pt/1.5 'Karla'; color:var(--stone); margin-top:.1in; }
.notes td:first-child { white-space:normal; }
.hq .dot { font-size:6.4pt; }
'''
F.print_pdf(F.html_doc(TITLE, body, F.RAPIDA_CSS + EXTRA), OUT, ROOT)
print('PDF ->', OUT)
