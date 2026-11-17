#!/usr/bin/env python3
"""TSL · Formato Nuevo — tratamiento de fotos.

Las fotos se capturan desde Chrome (el proxy bloquea descargar de images.unsplash.com y de la mayoría de los hoteles):
se pinta la imagen en un <img> fijo con object-fit:cover y se toma captura a escala 1.
  · Portada / apertura: 1710 x 2213 px CSS en 3 capturas (offset 0, 927, 1854) -> unir() -> 1496 x 1937 px.
  · Itinerario: dos retratos de 700 x 927 px CSS por captura (x = 0 y x = 720) -> recortes L y R -> 611 x 810 px.
  · Hotel: dos apaisadas de 840 x 672 px CSS por captura (x = 0 y x = 860) -> recortes HL y HR -> 736 x 588 px.
La captura mide 1498 x 812 px para un viewport de 1710 x 927 px CSS (factor 0.876).
"""
import numpy as np
from PIL import Image, ImageEnhance

L, R = (1, 1, 612, 811), (632, 1, 1243, 811)             # retratos de itinerario
HL, HR = (0, 0, 736, 588), (754, 0, 1489, 588)           # fotos de hotel

def _hsv(im, global_k, bands):
    a = np.asarray(im.convert('HSV')).astype(float); h, s, v = a[..., 0], a[..., 1], a[..., 2]; hue = h * 360 / 255
    k = global_k * np.ones_like(s)
    for c, w, amt in bands:
        k = k * (1 - amt * np.clip(1 - np.abs(((hue - c + 180) % 360) - 180) / w, 0, 1))
    return Image.fromarray(np.stack([h, s * k, v], -1).clip(0, 255).astype('uint8'), 'HSV').convert('RGB')

def ambiente(im, naranja=0.0):
    """Fotos de portada, apertura e itinerario: tonos apagados y arenosos (saturación x0.8, azules x0.56)."""
    out = _hsv(im.convert('RGB'), 0.8, [(220, 50, 0.44), (30, 35, naranja)])
    r, g, b = out.split()
    return Image.merge('RGB', (r.point(lambda x: min(255, int(x * 1.01))), g, b.point(lambda x: int(x * 0.975))))

def hotel(im, azul=0.42, naranja=0.22, verde=0.30):
    """Fotos de hotel: una sola gradación para todas (saturación x0.72, contraste -7 %, negros levantados).
    Sube azul a 0.55 en hoteles muy azules y naranja a 0.36 en interiores muy cálidos."""
    out = _hsv(im.convert('RGB'), 0.72, [(215, 55, azul), (30, 35, naranja), (125, 45, verde)])
    out = ImageEnhance.Contrast(out).enhance(0.93)
    arr = np.asarray(out).astype(float)
    return Image.fromarray((14 + arr * (241 / 255.0)).clip(0, 255).astype('uint8'))

def unir(t1, t2, t3):
    """Une las 3 capturas de una foto a página completa (portada o apertura)."""
    out = Image.new('RGB', (1496, 812 + 812 + 313))
    out.paste(t1.crop((1, 0, 1497, 812)), (0, 0)); out.paste(t2.crop((1, 0, 1497, 812)), (0, 812)); out.paste(t3.crop((1, 0, 1497, 313)), (0, 1624))
    return out
