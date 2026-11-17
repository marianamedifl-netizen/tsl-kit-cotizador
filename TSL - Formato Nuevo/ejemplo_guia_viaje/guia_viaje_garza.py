#!/usr/bin/env python3
"""TSL · Guía de Viaje (Formato Nuevo) — ejemplo canónico: Familia Garza · Europa & África, julio 2026.
Uso: python3 guia_viaje_garza.py [salida.pdf]
Hojas: portada · índice · clima diario · qué empacar (una hoja por destino) · inspiración (mujer y hombre) · guía de maletas · guía de propinas ·
esenciales · cierre. Se entrega aparte de la Entrega Final. Únicos íconos: los de clima en la tabla (línea fina); lo demás, fotos y listas.
Para un viaje nuevo: copia esta carpeta y cambia los bloques de datos de este archivo y las fotos."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import tsl_base as B
import tsl_formato as F

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'salida.pdf').resolve()
B.TRIP = 'Europa &amp; África · Julio 2026'
TITLE = 'Europa & África · Familia Garza · Guía de Viaje'

# ───────────────────────── datos ─────────────────────────
# En la portada el título es «Guía de Viaje» y el destino va debajo, para distinguirla de un vistazo de la Entrega Final.
PORTADA = dict(img='img/cover.jpg', title='Guía de Viaje', t2='Europa &amp; África', client='Familia Garza', h1_pt=41,
               rows=[('Ruta', 'Madrid · Londres · Nairobi · Serengeti'), ('Fechas', '5 – 21 jul 2026'), ('Viajeros', '10 personas · 16 noches')])
PARA = 'Familia Garza<br>10 personas'

# (fecha, día, destino, clima esperado, mín, máx, ícono) — ícono: sol, parcial, nublado, llovizna o '' (días de vuelo, sin temperatura)
CLIMA = [('05 jul', 'Domingo', 'Vuelo Monterrey – Madrid', 'Vuelo nocturno internacional', '', '', ''),
         ('06 jul', 'Lunes', 'Madrid, España', 'Soleado y seco, calor por la tarde', '19°', '33°', 'sol'),
         ('07 jul', 'Martes', 'Londres, Inglaterra', 'Parcialmente nublado, agradable', '14°', '23°', 'parcial'),
         ('08 jul', 'Miércoles', 'Londres, Inglaterra', 'Intervalos de sol y nubes', '14°', '23°', 'parcial'),
         ('09 jul', 'Jueves', 'Londres, Inglaterra', 'Posible llovizna ligera', '14°', '22°', 'llovizna'),
         ('10 jul', 'Viernes', 'Londres / Cotswolds', 'Fresco por la mañana, despejando', '13°', '23°', 'parcial'),
         ('11 jul', 'Sábado', 'Nairobi, Kenia', 'Nublado y fresco (estación seca)', '11°', '21°', 'nublado'),
         ('12 jul', 'Domingo', 'Grumeti, Tanzania', 'Soleado y seco, madrugada fría', '14°', '26°', 'sol'),
         ('13 jul', 'Lunes', 'Grumeti, Tanzania', 'Soleado y seco, madrugada fría', '14°', '26°', 'sol'),
         ('14 jul', 'Martes', 'Serengeti · Singita', 'Despejado, cálido al mediodía', '14°', '27°', 'sol'),
         ('15 jul', 'Miércoles', 'Serengeti · Singita', 'Despejado, cálido al mediodía', '14°', '27°', 'sol'),
         ('16 jul', 'Jueves', 'Serengeti · Singita', 'Mayormente soleado, brisa seca', '15°', '27°', 'sol'),
         ('17 jul', 'Viernes', 'Serengeti · Singita', 'Despejado, cálido al mediodía', '15°', '27°', 'sol'),
         ('18 jul', 'Sábado', 'Nairobi · vuelo nocturno', 'Fresco y nublado en Nairobi', '11°', '21°', 'nublado'),
         ('19 jul', 'Domingo', 'Madrid, España', 'Soleado y seco, calor por la tarde', '19°', '33°', 'sol'),
         ('20 jul', 'Lunes', 'Madrid, España', 'Soleado, máxima intensa al mediodía', '19°', '34°', 'sol'),
         ('21 jul', 'Martes', 'Vuelo Madrid – Monterrey', 'Vuelo internacional de regreso', '', '', '')]
CLIMA_NOTA = ('Temperaturas en grados Celsius, promedios históricos de julio por destino. '
              'Recomendamos verificar el pronóstico unos días antes de cada traslado.')

# una hoja por destino: lugar, fechas, clima, foto, pie de foto, imprescindibles (8), recomendaciones, tip
EMPACAR = [
    dict(lugar='Madrid', fechas='6 de julio y 19 – 21 de julio', foto='retiro', pie='Parque del Retiro',
         clima='Verano pleno: días soleados y secos de 33 – 34 °C, noches templadas de ~19 °C.',
         must=['Camisa de lino', 'Vestido ligero', 'Shorts', 'Sombrero y lentes', 'Chanclas', 'Blazer para cenas', 'Protector solar', 'Traje de baño'],
         recs=['Ropa ligera de lino y algodón en tonos claros.', 'Sombrero o gorra y lentes de sol.', 'Protector solar FPS 50 y labial con FPS.',
               'Chanclas o tenis muy cómodos para caminar.',
               'Atuendo smart-casual para las cenas (El Qüenco de Pepa, Ten con Ten, Filandón).',
               'Blazer o pashmina ligera para interiores con aire acondicionado.', 'Traje de baño para la alberca del Rosewood Villa Magna.'],
         tip='En Madrid el sol pega fuerte entre 14:00 y 18:00 h. Planeen paseos por la mañana y reserven la tarde para la alberca o siesta '
             'antes de las cenas de las 19:30 h.'),
    dict(lugar='Londres', fechas='7 – 11 de julio', foto='towerbridge', pie='Tower Bridge',
         clima='Verano templado e impredecible: 13 – 23 °C, con sol, nubes y llovizna ocasional el mismo día.',
         must=['Trench o impermeable', 'Suéter ligero', 'Pantalón o jeans', 'Paraguas compacto', 'Tenis para caminar', 'Calzado para cenas',
               'Bufanda ligera', 'Saco o blazer'],
         recs=['Trench o impermeable ligero y capas fáciles de poner y quitar.', 'Suéter ligero y una bufanda para las noches frescas.',
               'Pantalón o jeans y tenis cómodos para caminar la ciudad.', 'Paraguas compacto siempre a la mano.',
               'Atuendo elegante para las cenas (Carbone, Oswald’s, ROKA, Carlotta) y el teatro (SIX Musical).',
               'Saco para caballeros: varios restaurantes y clubes piden dress code.', 'Un impermeable con capucha para los Cotswolds y Windsor.'],
         tip='El clima de Londres cambia en minutos: vestir en capas es clave. Guarden un atuendo formal a la mano para las reservaciones de la noche.'),
    dict(lugar='Safari', fechas='11 – 18 de julio · Serengeti y Grumeti, Tanzania', foto='safari', pie='Serengeti',
         clima='Estación seca: madrugadas frías de ~14 °C en los game drives, mediodías cálidos de 26 – 27 °C.',
         must=['Camisa de manga larga', 'Fleece', 'Chamarra abrigada', 'Gorro y guantes', 'Binoculares', 'Cámara con zoom', 'Botas o tenis',
               'Sombrero y lentes'],
         recs=['Ropa en tonos neutros: khaki, oliva, beige y café (eviten azul marino y negro: atraen a la mosca tsetsé).',
               'Capas abrigadas: fleece, chamarra, gorro y guantes para los game drives del amanecer.',
               'Camisas de manga larga y pantalones ligeros; sombrero y lentes de sol.',
               'Binoculares (un par por pareja) y cámara con buen zoom.', 'Repelente con DEET, protector solar FPS 50 y bálsamo labial.',
               'Traje de baño (los lodges tienen piscina) y botas o tenis cómodos ya domados.'],
         tip='Eviten estampados de camuflaje (restringidos). La lavandería está incluida en los lodges: con 4 – 5 cambios de ropa de safari es suficiente.'),
]

# hojas de inspiración: prendas sueltas en retícula 4 x 3 (fotos en img/ins/<archivo>.jpg, 287 x 355 px)
INSPIRACION = [
    dict(quien='Mujer', paleta='Khaki, oliva, beige, crema y café', para='Safari · Serengeti y Grumeti',
         prendas=[('m_camisa', 'Camisa de lino'), ('m_playera', 'Playera básica'), ('m_sueter', 'Suéter ligero'), ('m_sobrecamisa', 'Sobrecamisa olivo'),
                  ('m_pantalon', 'Pantalón khaki'), ('m_pashmina', 'Pashmina'), ('m_sombrero', 'Sombrero'), ('m_lentes', 'Lentes de sol'),
                  ('m_panuelo', 'Pañuelo de seda'), ('m_tenis', 'Tenis blancos'), ('m_sandalias', 'Sandalias'), ('m_tote', 'Tote')]),
    dict(quien='Hombre', paleta='Khaki, oliva, beige, crema y café', para='Safari · Serengeti y Grumeti',
         prendas=[('h_camisa', 'Camisa de lino'), ('h_polo', 'Polo'), ('h_sueter', 'Suéter'), ('h_sobrecamisa', 'Sobrecamisa'),
                  ('h_chinos', 'Chinos'), ('h_botas', 'Botas'), ('h_gorra', 'Gorra'), ('h_lentes', 'Lentes de sol'),
                  ('h_cinturon', 'Cinturón'), ('h_duffel', 'Duffel'), ('h_camara', 'Cámara con zoom'), ('h_binoculares', 'Binoculares')]),
]
INSPIRACION_NOTA = 'Fotografías de inspiración: sugieren estilo y paleta, no prendas específicas.'

MALETAS = dict(
    foto='elephants', pie='Sabana',
    specs=[('Sí', 'Duffel blando 60 – 90 L', 'Equipaje principal al safari'), ('No', 'Maleta rígida', 'No permitida en la avioneta'),
           ('Sí', 'Daypack 20 – 30 L', 'Para los game drives')],
    cols=[('Reglas del chárter', ['Máximo 20 kg por persona, incluyendo el duffel y el daypack.', 'Solo bolsas blandas sin estructura, ruedas ni marco rígido.',
                                  'Medida sugerida: duffel de aprox. 70 × 36 cm (60 – 90 L).', 'Un daypack de 20 – 30 L por persona para los game drives.']),
          ('Qué evitar', ['Maletas rígidas o con ruedas: no caben en el compartimento de la avioneta.',
                          'Exceder los 20 kg: el sobrepeso puede quedarse en tierra.',
                          'Empacar de más: la lavandería diaria está incluida en ambos lodges.', 'Drones: requieren permisos especiales en Tanzania.'])],
    tip='Dos opciones para el equipaje grande: (1) llevarlo hasta Nairobi y dejarlo en custodia del hotel del 11 al 18 de julio (lo coordinamos con el '
        'equipo VIP), recuperándolo el 18 antes del vuelo nocturno a Londres; o (2) dejar las maletas grandes en el Rosewood Villa Magna de Madrid, '
        'ya que regresan al mismo hotel el 19 de julio, y viajar a Londres y al safari solo con lo necesario.')

PROPINAS = dict(
    intro='Las propinas en safari son discrecionales pero esperadas, y se entregan en efectivo (USD) al final de la estancia en cada lodge. '
          'Los montos siguientes son los sugeridos por los lodges por pareja; calculamos el total del grupo considerando 5 parejas (10 PAX) '
          'y 6 días de safari (2 en andBeyond y 4 en Singita).',
    cab=['Posición', 'Sugerido por pareja / día', 'Grupo (5 parejas) / día', 'Total · 6 días'],
    filas=[('Guía', 'desde US$30', 'US$150', 'US$900'), ('Mesero / Host', 'desde US$15', 'US$75', 'US$450'),
           ('Fondo general del staff', 'desde US$30', 'US$150', 'US$900')],
    total=('Total grupo', 'US$75', 'US$375', 'US$2,250'),
    lodges=[('andBeyond Grumeti · 12 – 14 jul', '2 días × US$375', 'US$750'), ('Singita Milele · 14 – 18 jul', '4 días × US$375', 'US$1,500')],
    tip='Preparen desde México unos US$2,300 – 2,500 en efectivo en billetes pequeños y nuevos, organizados en sobres por lodge. En Singita Milele, '
        'con guía privado, host y mayordomo, pueden entregar las propinas directamente a cada persona o al gerente para distribuirlas. '
        'Los montos son sugerencias mínimas («desde»): si el servicio los sorprende, siempre pueden dar más.',
    foto='manada')

# {prop} se sustituye por el enlace a la hoja de propinas
ESENCIALES = [
    ('Moneda &amp; Efectivo', ['España: Euro (€) · Reino Unido: Libra (£) · Tanzania: se maneja USD en los lodges (chelín TZS para gastos menores).',
                               'Lleven efectivo en €, £ y USD (billetes en buen estado, posteriores a 2009). Visa y Mastercard se aceptan en hoteles y tiendas.']),
    ('Enchufes &amp; Electricidad', ['España tipo C/F · Reino Unido tipo G · Tanzania tipo D/G, todos a 220 – 240 V. Adaptador universal por persona.',
                                     'Power bank para los game drives; los lodges tienen puntos de carga en las habitaciones.']),
    ('Documentos &amp; Salud', ['Pasaporte con vigencia mínima de 6 meses. Visa electrónica de Tanzania (e-Visa) tramitada por adelantado.',
                                'Certificado de fiebre amarilla si se transita por zona endémica; profilaxis antimalárica para el Serengeti (consulten a su médico).',
                                'Seguro de viaje con cobertura médica y evacuación (requerido por los lodges remotos).']),
    ('Propinas en Europa', ['España: propina opcional (5 – 10 % en restaurantes). Reino Unido: el service charge (~12.5 %) suele venir incluido en la cuenta.',
                            'Choferes y guías privados: €10 – 20 por servicio. Para el safari, consulten la {prop}.']),
    ('Husos &amp; Contacto', ['Madrid / Londres (verano) UTC+2 / +1 · Nairobi y Tanzania UTC+3 (9 – 10 h adelante de CDMX).',
                              'En destino · Triumph Travel (24 h): <a href="tel:+27769819129">+27 (0)76 981 9129</a> &nbsp;·&nbsp; '
                              'Nuba México: <a href="tel:+525552554455">55 5255 4455</a>.']),
]
# íconos de clima, de línea fina (trazos de Feather, licencia MIT), en el arena de la marca
_SOL = ('<circle cx="12" cy="12" r="4.6"/><path d="M12 1.5v2.2M12 20.3v2.2M4.6 4.6l1.5 1.5M17.9 17.9l1.5 1.5M1.5 12h2.2M20.3 12h2.2M4.6 19.4l1.5-1.5M17.9 6.1l1.5-1.5"/>')
_NUBE = '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>'
ICONOS = {
    'sol': _SOL,
    'nublado': _NUBE,
    'parcial': ('<circle cx="8.6" cy="8.2" r="3.3"/><path d="M8.6 1.6v1.7M2 8.2h1.7M3.9 3.5l1.2 1.2M13.3 3.5l-1.2 1.2M3.9 12.9l1.2-1.2"/>'
                f'<g transform="translate(7.6 8.6) scale(.64)" stroke-width="1.72" fill="#FCF9F5">{_NUBE}</g>'),
    'llovizna': ('<path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/><path d="M8 13v2M8 19v2M12 15v2M12 21v2M16 13v2M16 19v2"/>'),
}
NOMBRES = [('sol', 'Soleado'), ('parcial', 'Parcial'), ('nublado', 'Nublado'), ('llovizna', 'Llovizna')]
def icono(k): return f'<svg class="wx" viewBox="0 0 24 24">{ICONOS[k]}</svg>' if k else ''

CREDITOS = ('Fotografías vía Unsplash: @hitobywong, @oemerkarakus, @fabiankuehne, @aguyonecam, @audie_rae_08 y @highteawithelephants. '
            'Inspiración: @tonnnyj, @avtar9w, @yuliia_pak, @denebapparel, @saeedkarimistudio, @vicbils, @shocking57, @annietheby, @susan_wilkinson, '
            '@pixelapse, @sincerelymedia, @brandomakesbranding, @chriscreations__, @dapperprofessional, @let_hho, @reddfrancisco, @gallocody, @palon, '
            '@habibdadkhah, @mostafa_mahmoudi24, @kaviaq, @jediahowen y @john_vowles.')

GUIA_CSS = '''
.guia h1 i { font:italic 200 19pt 'IvyOra'; color:var(--stone); margin-left:.12in; letter-spacing:0; }
.guia .gf { display:grid; grid-template-columns:2.55in 1fr; column-gap:.3in; margin-top:.3in; padding:.14in 0 .13in;
  border-top:.5pt solid var(--ink); border-bottom:.5pt solid var(--oat); }
.guia .gf dd { font:300 10.5pt/1.3 'IvyOra'; margin-top:.03in; }
.guia .gp { display:grid; grid-template-columns:3in 1fr; column-gap:.4in; margin-top:.32in; }
.guia .gp.flip { grid-template-columns:1fr 3in; }
.guia .gp.rl { border-top:.5pt solid var(--ink); padding-top:.3in; margin-top:.3in; }
.guia .gp.flip figure { order:2; }
.guia figure { position:relative; }
.guia figure img { display:block; width:3in; height:3.97in; object-fit:cover; }
.guia figcaption { font:italic 200 10pt 'IvyOra'; color:var(--soft); margin-top:.06in; }
.guia .gp.flip figcaption { text-align:right; }
.guia ol.must { list-style:none; display:grid; grid-template-columns:1fr 1fr; column-gap:.3in; margin:.08in 0 .3in; }
.guia ol.must li { font:300 12.5pt/1.2 'IvyOra'; padding:.115in 0 .105in; border-bottom:.5pt solid var(--oat); }
.guia ul.recs { list-style:none; margin-top:.1in; }
.guia ul.recs li { font:300 9pt/1.55 'Karla'; color:var(--soft); padding-left:.15in; text-indent:-.15in; margin-bottom:.055in; }
.guia ul.recs li::before { content:'–'; display:inline-block; width:.15in; text-indent:0; color:var(--stone); }
.guia .tip { display:grid; grid-template-columns:.85in 1fr; column-gap:.2in; align-items:baseline; margin-top:.36in; background:var(--almond);
  padding:.2in .26in .19in; }
.guia .tip .lb { color:#927F68; font-weight:700; }
.guia .tip p { font:300 9pt/1.6 'Karla'; color:var(--soft); }
.guia .specs { margin:.08in 0 0; }
.guia .specs div { display:grid; grid-template-columns:.42in 1fr; align-items:baseline; padding:.15in 0 .14in; border-bottom:.5pt solid var(--oat); }
.guia .specs i { font:700 6.8pt 'Karla'; font-style:normal; letter-spacing:.2em; text-transform:uppercase; color:#927F68; }
.guia .specs i.no { color:var(--stone); }
.guia .specs b { display:block; font:300 14pt/1.2 'IvyOra'; }
.guia .specs span { display:block; font:300 8.8pt/1.4 'Karla'; color:var(--soft); margin-top:.03in; }
.guia .cols2 { display:grid; grid-template-columns:1fr 1fr; column-gap:.5in; margin-top:.34in; }
.guia h4 { font:700 9pt/1.3 'Karla'; color:var(--soft); letter-spacing:.01em; margin:0 0 .02in; }
.guia p.intro { font:300 9.4pt/1.65 'Karla'; color:var(--soft); max-width:6.4in; margin-top:.3in; }
.guia table.bnd { margin-top:.36in; }
.guia table.bnd th { background:var(--oat); color:var(--ink); border-bottom:0; padding:.1in .1in .09in 0; }
.guia table.bnd th:first-child, .guia table.bnd td:first-child { padding-left:.14in; }
.guia table.bnd th:last-child, .guia table.bnd td:last-child { padding-right:.14in; }
.guia table.bnd td { vertical-align:middle; }
.clima td { padding:.088in .1in .078in 0; }
.clima td:first-child { font-weight:700; white-space:nowrap; }
.clima td.n, .clima th.n, .tips td.n, .tips th.n { text-align:right; }
.clima td.dim { color:var(--stone); }
.wx { display:block; width:.2in; height:.2in; fill:none; stroke:#927F68; stroke-width:1.1; stroke-linecap:round; stroke-linejoin:round; }
.clima td.i { width:.3in; padding-top:.04in; padding-bottom:.03in; padding-right:0; }
.clima .ley { display:flex; gap:.34in; align-items:center; margin-top:.2in; }
.clima .ley span { display:flex; align-items:center; gap:.08in; font:400 6.8pt 'Karla'; letter-spacing:.2em; text-transform:uppercase; color:var(--stone); }
.clima .ley .wx { width:.17in; height:.17in; }
.clima .fine { font:300 7.6pt/1.55 'Karla'; color:var(--soft); margin-top:.16in; max-width:5.6in; }
.tips td { padding:.14in .1in .13in 0; }
.tips td:first-child { font:300 12.5pt/1.2 'IvyOra'; }
.tips tr.tt td { background:var(--oat); border-bottom:0; font-weight:500; padding:.17in .1in .16in 0; }
.tips tr.tt td:first-child { font:400 7pt 'Karla'; letter-spacing:.2em; text-transform:uppercase; padding-left:.14in; }
.tips tr.tt td:last-child { font:200 19pt/1 'IvyOra'; padding-right:.14in; }
.guia .lodges { display:grid; grid-template-columns:1fr 1fr; column-gap:.5in; margin-top:.36in; }
.guia .lodges div { border-top:.5pt solid var(--ink); padding-top:.13in; }
.guia .lodges p { font:300 9pt/1.4 'Karla'; color:var(--soft); margin-top:.05in; }
.guia .lodges b { display:block; font:200 24pt/1 'IvyOra'; margin-top:.1in; }
.guia .mood { display:grid; grid-template-columns:repeat(4, 1fr); column-gap:.16in; row-gap:.2in; margin-top:.3in; }
.guia .mood img { display:block; width:100%; height:1.84in; object-fit:cover; }
.guia .mood span { display:block; margin-top:.08in; font:400 6.8pt/1.3 'Karla'; letter-spacing:.2em; text-transform:uppercase; color:var(--soft); }
.guia .mnote { font:300 7.6pt/1.5 'Karla'; color:var(--stone); margin-top:.22in; }
.guia .wide { margin-top:.3in; }
.end .cred { left:.9in; right:.9in; bottom:.42in; }
.guia .wide img { display:block; width:100%; height:1.3in; object-fit:cover; }
.ess .rows { margin-top:.4in; border-top:.5pt solid var(--ink); }
.ess .rows > div { display:grid; grid-template-columns:2.1in 1fr; column-gap:.3in; padding:.26in 0 .22in; border-bottom:.5pt solid var(--oat); }
.ess .rows h3 { font:200 17pt/1.15 'IvyOra'; }
.ess .rows p { font:300 9.2pt/1.62 'Karla'; color:var(--soft); margin-bottom:.07in; }
.ess .rows a { color:var(--ink); text-decoration:none; }
'''

# ───────────────────────── armado ─────────────────────────
NE, NI = len(EMPACAR), len(INSPIRACION)
P_CLIMA, P_EMP = 3, 4
P_INS = P_EMP + NE; P_MAL = P_INS + NI; P_PROP = P_MAL + 1; P_ESE = P_PROP + 1
S_INS = 2 + NE; S_MAL = S_INS + NI; S_PROP = S_MAL + 1; S_ESE = S_PROP + 1
INDEX = ([(1, 'Clima Diario', P_CLIMA)] + [(2 + k, f'Qué Empacar · {e["lugar"]}', P_EMP + k) for k, e in enumerate(EMPACAR)]
         + [(S_INS + k, f'Inspiración · {e["quien"]}', P_INS + k) for k, e in enumerate(INSPIRACION)]
         + [(S_MAL, 'Guía de Maletas', P_MAL), (S_PROP, 'Guía de Propinas', P_PROP), (S_ESE, 'Esenciales', P_ESE)])

def fig(foto, pie): return f'<figure><img src="img/{foto}.jpg"><figcaption>{pie}</figcaption></figure>'
def tip(t): return f'<div class="tip"><span class="lb">Tip TSL</span><p>{t}</p></div>'
def ul(items): return '<ul class="recs">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

pages = [F.cover_page(**PORTADA), F.index_page(INDEX, PARA, label='Preparado para')]

# clima diario
rows = ''.join(f'<tr><td>{f}</td><td>{d}</td><td>{l}</td><td class="i">{icono(ic)}</td><td{"" if mn else " class=dim"}>{c}</td>'
               f'<td class="n">{mn or "—"}</td><td class="n">{mx or "—"}</td></tr>' for f, d, l, c, mn, mx, ic in CLIMA)
ley = ''.join(f'<span>{icono(k)}{n}</span>' for k, n in NOMBRES)
pages.append(f'''<div class="page guia clima" id="s1">{F.furniture('.01', 'Clima Diario', P_CLIMA)}<div class="in"><h1>Clima Diario</h1>
  <table class="bnd"><tr><th style="width:.75in">Fecha</th><th style="width:.85in">Día</th><th style="width:1.75in">Destino</th><th colspan="2">Clima esperado</th>
    <th class="n" style="width:.5in">Mín</th><th class="n" style="width:.6in">Máx</th></tr>{rows}</table>
  <div class="ley">{ley}</div><p class="fine">{CLIMA_NOTA}</p></div></div>''')

# qué empacar
for k, e in enumerate(EMPACAR):
    must = ''.join(f'<li>{m}</li>' for m in e['must'])
    pages.append(f'''<div class="page guia" id="s{2 + k}">{F.furniture(f'.{2 + k:02d}', 'Qué Empacar', P_EMP + k)}<div class="in">
  <h1>Qué Empacar <i>{e['lugar']}</i></h1>
  <dl class="gf"><div><dt class="lb">Fechas</dt><dd>{e['fechas']}</dd></div><div><dt class="lb">Clima</dt><dd>{e['clima']}</dd></div></dl>
  <div class="gp{' flip' if k % 2 else ''}">{fig(e['foto'], e['pie'])}<div><span class="lb">Imprescindibles</span><ol class="must">{must}</ol>
    <span class="lb">Recomendaciones</span>{ul(e['recs'])}</div></div>
  {tip(e['tip'])}</div></div>''')

# inspiración
for k, e in enumerate(INSPIRACION):
    tiles = ''.join(f'<figure><img src="img/ins/{f}.jpg"><span>{n}</span></figure>' for f, n in e['prendas'])
    pages.append(f'''<div class="page guia" id="s{S_INS + k}">{F.furniture(f'.{S_INS + k:02d}', 'Inspiración', P_INS + k)}<div class="in">
  <h1>Inspiración <i>{e['quien']}</i></h1>
  <dl class="gf"><div><dt class="lb">Para</dt><dd>{e['para']}</dd></div><div><dt class="lb">Paleta</dt><dd>{e['paleta']}</dd></div></dl>
  <div class="mood">{tiles}</div><p class="mnote">{INSPIRACION_NOTA}</p></div></div>''')

# guía de maletas
m = MALETAS
specs = ''.join(f'<div><i{" class=no" if s == "No" else ""}>{s}</i><p><b>{n}</b><span>{d}</span></p></div>' for s, n, d in m['specs'])
pages.append(f'''<div class="page guia" id="s{S_MAL}">{F.furniture(f'.{S_MAL:02d}', 'Guía de Maletas', P_MAL)}<div class="in">
  <h1>Guía de Maletas <i>África</i></h1>
  <div class="gp rl{' flip' if NE % 2 else ''}">{fig(m['foto'], m['pie'])}<div><span class="lb">Equipaje para el safari</span><div class="specs">{specs}</div>
    <div style="margin-top:.24in">{''.join(f'<h4 style="margin-top:.2in">{h}</h4>{ul(items)}' for h, items in m['cols'])}</div></div></div>
  {tip(m['tip'])}</div></div>''')

# guía de propinas
p = PROPINAS
th = ''.join(f'<th{" class=n" if j else ""}>{c}</th>' for j, c in enumerate(p['cab']))
tr = ''.join('<tr>' + ''.join(f'<td{" class=n" if j else ""}>{c}</td>' for j, c in enumerate(r)) + '</tr>' for r in p['filas'])
tt = '<tr class="tt">' + ''.join(f'<td{" class=n" if j else ""}>{c}</td>' for j, c in enumerate(p['total'])) + '</tr>'
lod = ''.join(f'<div><span class="lb">{a}</span><p>{b}</p><b>{c}</b></div>' for a, b, c in p['lodges'])
pages.append(f'''<div class="page guia" id="s{S_PROP}">{F.furniture(f'.{S_PROP:02d}', 'Guía de Propinas', P_PROP)}<div class="in">
  <h1>Guía de Propinas <i>Safari</i></h1><p class="intro">{p['intro']}</p>
  <table class="bnd tips"><tr>{th}</tr>{tr}{tt}</table>
  <div class="lodges">{lod}</div>{tip(p['tip'])}
  <div class="wide"><img src="img/{p['foto']}.jpg"></div></div></div>''')

# esenciales
link = f'<a href="#s{S_PROP}">Guía de Propinas · Safari (pág. {P_PROP:02d})</a>'
er = ''.join(f'<div><h3>{h}</h3><div>{"".join(f"<p>{t.replace("{prop}", link)}</p>" for t in ps)}</div></div>' for h, ps in ESENCIALES)
pages.append(f'''<div class="page guia ess" id="s{S_ESE}">{F.furniture(f'.{S_ESE:02d}', 'Esenciales', P_ESE)}<div class="in">
  <h1>Esenciales</h1><div class="rows">{er}</div></div></div>''')

pages.append(F.closing_page(CREDITOS))
F.print_pdf(F.html_doc(TITLE, '\n'.join(pages), F.DOC_CSS + GUIA_CSS), OUT, ROOT)
print('PDF ->', OUT)
