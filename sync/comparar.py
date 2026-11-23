#!/usr/bin/env python3
"""Compara las skills instaladas en Claude contra los repositorios de GitHub.

Solo lee archivos y calcula huellas; no instala, no borra y no sube nada.

Uso:
  python3 -I comparar.py revisar  --estado sync/estado.json --repo mariana=RUTA --repo luis=RUTA [--instaladas RUTA]
  python3 -I comparar.py guardar  (mismos argumentos) [--registro sync/registro.md]
  python3 -I comparar.py iniciar  (mismos argumentos)

Por cada skill guarda:
  base   huella de la versión vigente (la más reciente que se dio por buena)
  visto  huella que tenía cada fuente en la revisión anterior

Estado de cada fuente (instalada, mariana, luis):
  al_dia     igual a la versión vigente
  atrasada   no cambió desde la revisión anterior y es distinta de la vigente
  cambio     cambió desde la revisión anterior y no es la vigente
  ausente    nunca ha estado en esa fuente
  eliminada  estaba en la revisión anterior y ya no está
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys

PREFIJOS = ('tsl-', 'nuba-')


def cuerpo(texto):
    """Texto de la skill sin el encabezado (frontmatter) ni espacios sobrantes."""
    lineas = texto.replace('\r\n', '\n').split('\n')
    if lineas and lineas[0].strip() == '---':
        for i in range(1, len(lineas)):
            if lineas[i].strip() == '---':
                lineas = lineas[i + 1:]
                break
    return '\n'.join(l.rstrip() for l in '\n'.join(lineas).strip().split('\n'))


def huella(ruta):
    with open(ruta, encoding='utf-8') as f:
        return hashlib.sha256(cuerpo(f.read()).encode('utf-8')).hexdigest()[:12]


def skills_en(carpeta):
    r = {}
    if carpeta and os.path.isdir(carpeta):
        for n in sorted(os.listdir(carpeta)):
            p = os.path.join(carpeta, n, 'SKILL.md')
            if n.startswith(PREFIJOS) and os.path.isfile(p):
                r[n] = p
    return r


def commit(repo, ruta):
    try:
        s = subprocess.run(['git', '-C', repo, 'log', '-1', '--format=%h %cI', '--', os.path.relpath(ruta, repo)],
                           capture_output=True, text=True, timeout=30).stdout.strip()
        return s or None
    except Exception:
        return None


def instaladas_por_defecto():
    for m in glob.glob('/root/.claude/skills/synced/*/manifest.json'):
        return os.path.dirname(m)
    return None


def leer(a):
    fuentes = {'instalada': skills_en(a.instaladas or instaladas_por_defecto())}
    repos = {}
    for r in a.repo:
        nombre, ruta = r.split('=', 1)
        repos[nombre] = ruta
        fuentes[nombre] = skills_en(os.path.join(ruta, 'skills'))
    estado = {'skills': {}}
    if os.path.isfile(a.estado):
        with open(a.estado, encoding='utf-8') as f:
            estado = json.load(f)
    return fuentes, repos, estado


def revisar(fuentes, repos, estado):
    nombres = set(estado['skills'])
    for d in fuentes.values():
        nombres |= set(d)
    informe = {}
    for n in sorted(nombres):
        e = estado['skills'].get(n, {'base': None, 'visto': {}})
        fila = {'base': e.get('base'), 'fuentes': {}, 'acciones': []}
        nuevos = set()
        for f, d in fuentes.items():
            antes = e.get('visto', {}).get(f)
            h = huella(d[n]) if n in d else None
            if h is None:
                st = 'eliminada' if antes else 'ausente'
            elif h == e.get('base'):
                st = 'al_dia'
            elif h == antes:
                st = 'atrasada'
            else:
                st = 'cambio'
                nuevos.add(h)
            info = {'huella': h, 'antes': antes, 'estado': st}
            if h and f in repos:
                info['commit'] = commit(repos[f], d[n])
            fila['fuentes'][f] = info
        fila['version_nueva'] = None
        if len(nuevos) == 1:
            fila['version_nueva'] = next(iter(nuevos))
        elif len(nuevos) > 1:
            fila['acciones'].append('CONFLICTO: cambió en más de una fuente; preparar fusión y mostrarla')
        vigente = fila['version_nueva'] or (fila['base'] if not nuevos else None)
        fila['vigente'] = vigente
        if vigente:
            for f, info in fila['fuentes'].items():
                if info['estado'] == 'eliminada':
                    fila['acciones'].append('AVISAR: ya no está en %s (no desinstalar)' % f)
                elif info['huella'] == vigente:
                    continue
                elif f == 'instalada':
                    fila['acciones'].append('TARJETA: %s en Claude con la versión %s' %
                                            ('instalar' if info['huella'] is None else 'reemplazar', vigente))
                elif f == 'mariana':
                    if info['huella'] is not None:
                        fila['acciones'].append('PENDIENTE: subir la versión %s al repo de Mariana (con su OK)' % vigente)
                elif info['huella'] is not None:
                    fila['acciones'].append('AVISAR: el repo de %s tiene una versión anterior' % f)
        informe[n] = fila
    return informe


def guardar(a, informe, estado):
    hoy = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
    filas = []
    for n, fila in informe.items():
        e = estado['skills'].setdefault(n, {'base': None, 'visto': {}})
        conflicto = any(x.startswith('CONFLICTO') for x in fila['acciones'])
        if fila['version_nueva'] and not conflicto:
            origen = ', '.join(f for f, i in fila['fuentes'].items() if i['huella'] == fila['version_nueva'])
            filas.append('| %s | `%s` | %s | `%s` | `%s` | Versión nueva detectada |' %
                         (hoy, n, origen, e.get('base') or 'ninguna', fila['version_nueva']))
            e['base'] = fila['version_nueva']
        for f, i in fila['fuentes'].items():
            if i['estado'] == 'eliminada':
                filas.append('| %s | `%s` | %s | `%s` | eliminada | Aviso; no se desinstaló |' % (hoy, n, f, i['antes']))
            if not conflicto:
                e.setdefault('visto', {})[f] = i['huella']
        if conflicto:
            filas.append('| %s | `%s` | varias | `%s` | en conflicto | Requiere fusión |' % (hoy, n, e.get('base')))
    estado['ultima_revision'] = hoy
    with open(a.estado, 'w', encoding='utf-8') as f:
        json.dump(estado, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    if a.registro:
        if not filas:
            filas = ['| %s | (todas) | | | | Revisión sin cambios |' % hoy]
        with open(a.registro, 'a', encoding='utf-8') as f:
            f.write('\n'.join(filas) + '\n')
    return filas


def iniciar(a, fuentes, repos):
    """Primer estado: la versión vigente es la del repo de Mariana y, si no está ahí, la del primer repo que la tenga."""
    estado = {'skills': {}}
    orden = [r for r in repos if r == 'mariana'] + [r for r in repos if r != 'mariana']
    nombres = set()
    for d in fuentes.values():
        nombres |= set(d)
    for n in sorted(nombres):
        base = None
        for r in orden:
            if n in fuentes[r]:
                base = huella(fuentes[r][n])
                break
        if base is None:
            base = huella(fuentes['instalada'][n])
        estado['skills'][n] = {'base': base,
                               'visto': {f: (huella(d[n]) if n in d else None) for f, d in fuentes.items()}}
    return estado


def main():
    p = argparse.ArgumentParser()
    p.add_argument('modo', choices=['revisar', 'guardar', 'iniciar'])
    p.add_argument('--estado', required=True)
    p.add_argument('--repo', action='append', default=[])
    p.add_argument('--instaladas')
    p.add_argument('--registro')
    a = p.parse_args()
    fuentes, repos, estado = leer(a)
    if not fuentes['instalada']:
        print('AVISO: no se encontraron las skills instaladas; la comparación contra la cuenta no es válida.', file=sys.stderr)
    if a.modo == 'iniciar':
        estado = iniciar(a, fuentes, repos)
        estado['ultima_revision'] = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
        with open(a.estado, 'w', encoding='utf-8') as f:
            json.dump(estado, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write('\n')
    informe = revisar(fuentes, repos, estado)
    if a.modo == 'guardar':
        if not fuentes['instalada']:
            sys.exit('No se guarda el estado sin las skills instaladas.')
        informe = {'registro': guardar(a, informe, estado), 'informe': informe}
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
