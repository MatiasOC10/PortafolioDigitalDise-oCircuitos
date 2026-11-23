"""
Genera los esquemas (SVG) del Cuaderno de Síntesis - Unidad 1 y
verifica por fuerza bruta que cada expresión simplificada cumple
la misma tabla de verdad que su forma original.

Uso:  pip install schemdraw pyparsing
      python scripts/generar_figuras.py
"""
import itertools
import os

import schemdraw
import schemdraw.logic as logic
from schemdraw.parsing import logicparse

schemdraw.use('svg')
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
os.makedirs(OUT, exist_ok=True)


def save_expr(expr, name, out='F', gateH=0.9):
    d = logicparse(expr, outlabel=out, gateH=gateH)
    d.save(os.path.join(OUT, name + '.svg'))


GRAY = {1: ['0', '1'], 2: ['00', '01', '11', '10']}


def _segmentos(idx, n):
    """Divide un conjunto de índices (con posible vuelta) en tramos contiguos."""
    idx = sorted(idx)
    if len(idx) == n:
        return [(0, n - 1)]
    tramos, ini, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i == prev + 1:
            prev = i
        else:
            tramos.append((ini, prev)); ini = prev = i
    tramos.append((ini, prev))
    return tramos


def save_kmap(names, table, groups, name):
    """Mapa de Karnaugh propio en SVG: columnas = primeras variables, filas = resto."""
    n = len(names)
    nc = 2 if n >= 3 else 1
    nr = n - nc
    cols, rows = GRAY[nc], GRAY[nr]
    val = {k: v for k, v in table}
    cw, ox, oy = 54, 70, 62
    W, H = ox + cw * len(cols) + 20, oy + cw * len(rows) + 20
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Helvetica, Arial, sans-serif">']
    o.append(f'<line x1="{ox-42}" y1="{oy-42}" x2="{ox}" y2="{oy}" stroke="#222" stroke-width="1.4"/>')
    o.append(f'<text x="{ox-8}" y="{oy-40}" font-size="15" font-weight="bold">{names[:nc]}</text>')
    o.append(f'<text x="{ox-62}" y="{oy-6}" font-size="15" font-weight="bold">{names[nc:]}</text>')
    for j, c in enumerate(cols):
        o.append(f'<text x="{ox+cw*j+cw/2}" y="{oy-8}" font-size="13" text-anchor="middle" fill="#555">{c}</text>')
    for i, r in enumerate(rows):
        o.append(f'<text x="{ox-8}" y="{oy+cw*i+cw/2+5}" font-size="13" text-anchor="end" fill="#555">{r}</text>')
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            code = c + r
            m = int(code, 2)
            v = val.get(code, '0')
            o.append(f'<rect x="{ox+cw*j}" y="{oy+cw*i}" width="{cw}" height="{cw}" fill="#fff" stroke="#222" stroke-width="1.4"/>')
            o.append(f'<text x="{ox+cw*j+4}" y="{oy+cw*i+12}" font-size="9" fill="#999">{m}</text>')
            colr = '#222' if v != 'X' else '#888'
            o.append(f'<text x="{ox+cw*j+cw/2}" y="{oy+cw*i+cw/2+7}" font-size="19" text-anchor="middle" fill="{colr}">{v}</text>')
    for k, (pat, color) in enumerate(groups.items()):
        cset = [j for j, c in enumerate(cols) if all(p in ('-', b) for p, b in zip(pat[:nc], c))]
        rset = [i for i, r in enumerate(rows) if all(p in ('-', b) for p, b in zip(pat[nc:], r))]
        ins = 5 + 4 * k
        for (r0, r1) in _segmentos(rset, len(rows)):
            for (c0, c1) in _segmentos(cset, len(cols)):
                x, y = ox + cw * c0 + ins, oy + cw * r0 + ins
                w, h = cw * (c1 - c0 + 1) - 2 * ins, cw * (r1 - r0 + 1) - 2 * ins
                o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" fill-opacity="0.13" '
                         f'stroke="{color}" stroke-width="2.4"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name + '.svg'), 'w').write('\n'.join(o))


def bits(n, k):
    return format(n, '0%db' % k)


# ---------------------------------------------------------------- verificación
def equivalentes(f, g, n):
    return all(f(*v) == g(*v) for v in itertools.product((0, 1), repeat=n))


# Semana 2: alarma de mayoría
canon = lambda a, b, c: ((not a) and b and c) or (a and (not b) and c) or (a and b and (not c)) or (a and b and c)
simpl = lambda a, b, c: (a and b) or (a and c) or (b and c)
assert equivalentes(lambda *v: bool(canon(*v)), lambda *v: bool(simpl(*v)), 3)

# Semana 3: F = Σm(1,3,7,11,15) + d(0,2,5)  ->  A'B' + CD
on, dc = {1, 3, 7, 11, 15}, {0, 2, 5}
fmin = lambda a, b, c, d: ((not a) and (not b)) or (c and d)
for m in range(16):
    a, b, c, d = map(int, bits(m, 4))
    if m not in dc:
        assert bool(fmin(a, b, c, d)) == (m in on), m
nand = lambda x, y: not (x and y)
fnand = lambda a, b, c, d: nand(nand(nand(a, a), nand(b, b)), nand(c, d))
assert equivalentes(lambda *v: bool(fmin(*v)), lambda *v: bool(fnand(*v)), 4)

# Semana 3: 3 variables  F = Σm(0,2,4,5,6) -> C' + AB'
f3 = lambda a, b, c: (not c) or (a and not b)
assert {m for m in range(8) if f3(*map(int, bits(m, 3)))} == {0, 2, 4, 5, 6}

# Semana 4: sumador completo
for a, b, ci in itertools.product((0, 1), repeat=3):
    s = a ^ b ^ ci
    co = (a & b) | (ci & (a ^ b))
    assert 2 * co + s == a + b + ci

# Semana 5: segmento a del display  a = A + C + BD + B'D'
seg_a_on = {0, 2, 3, 5, 6, 7, 8, 9}
for m in range(10):
    A, B, C, D = map(int, bits(m, 4))
    assert bool(A or C or (B and D) or ((not B) and (not D))) == (m in seg_a_on), m

print('Todas las verificaciones pasaron.')

# ---------------------------------------------------------------- figuras
# Semana 2
save_expr('(not a and b and c) or (a and not b and c) or (a and b and not c) or (a and b and c)',
          's2_alarma_canonica', 'Alarma', gateH=1.0)
save_expr('(a and b) or (a and c) or (b and c)', 's2_alarma_simplificada', 'Alarma')

# Semana 3
save_kmap('ABC', [('000', '1'), ('010', '1'), ('100', '1'), ('101', '1'), ('110', '1'),
                  ('001', '0'), ('011', '0'), ('111', '0')],
          {'--0': '#1f5fbf',
           '10-': '#c0392b'}, 's3_kmap3')
save_kmap('ABCD', [('0001', '1'), ('0011', '1'), ('0111', '1'), ('1011', '1'), ('1111', '1'),
                   ('0000', 'X'), ('0010', 'X'), ('0101', 'X')],
          {'--11': '#c0392b',
           '00--': '#1f5fbf'}, 's3_kmap4')
save_expr('(not a and not b) or (c and d)', 's3_and_or')
save_expr('((a nand a) nand (b nand b)) nand (c nand d)', 's3_solo_nand')

# Semana 4
save_expr('a xor b', 's4_ha_suma', 'S')
save_expr('a and b', 's4_ha_acarreo', 'C')
save_expr('a xor b xor cin', 's4_fa_suma', 'S')
save_expr('(a and b) or (cin and (a xor b))', 's4_fa_acarreo', 'Cout')
save_kmap('ABC', [('011', '1'), ('101', '1'), ('110', '1'), ('111', '1'),
                  ('000', '0'), ('001', '0'), ('010', '0'), ('100', '0')],
          {'-11': '#1f5fbf',
           '1-1': '#c0392b',
           '11-': '#2e8b57'}, 's4_kmap_cout')
save_expr('(a1 xnor b1) and (a0 xnor b0)', 's4_comparador_igual', 'A=B')

# Semana 5
tt = [(bits(m, 4), '1' if m in seg_a_on else '0') for m in range(10)]
tt += [(bits(m, 4), 'X') for m in range(10, 16)]
save_kmap('ABCD', tt,
          {'1---': '#c0392b',
           '--1-': '#1f5fbf',
           '-1-1': '#2e8b57',
           '-0-0': '#8e44ad'}, 's5_kmap_seg_a')
print('Figuras generadas en', os.path.abspath(OUT))

# Semana 1: símbolos de las siete compuertas
for nombre, cls in [('and', logic.And), ('or', logic.Or), ('not', logic.Not), ('nand', logic.Nand),
                    ('nor', logic.Nor), ('xor', logic.Xor), ('xnor', logic.Xnor)]:
    with schemdraw.Drawing(file=os.path.join(OUT, f's1_{nombre}.svg'), show=False) as d:
        d.config(fontsize=13)
        if nombre == 'not':
            d += cls().label('A', 'left').label('Y', 'right')
        else:
            g = cls(inputs=2)
            d += g
            d += logic.Line().at(g.in1).left(0.01).label('A', 'left')
            d += logic.Line().at(g.in2).left(0.01).label('B', 'left')
            d += logic.Line().at(g.out).right(0.01).label('Y', 'right')
print('Símbolos de compuertas generados.')
