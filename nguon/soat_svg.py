# -*- coding: utf-8 -*-
"""SRH CH SGK - dựng PNG từ các sơ đồ <svg class="dg"> trong một bài .md để soát bằng mắt
(dùng khi khung trình duyệt bị ẩn, không chụp được trang).

Chạy bằng Python313 (có fitz):
  "C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I nguon/soat_svg.py "Bài 8.md" [thư mục ra] [--toi]
  → <thư mục ra>/svg_0.png, svg_1.png… theo thứ tự sơ đồ trong bài (mặc định: thư mục tạm của máy).
  --toi: dựng theo giao diện tối (ra svg_0_toi.png…), để soát chữ và màu trên nền tối.

Lớp màu (en, de, c1, k, ld, s, b…) đổi thành thuộc tính; mọi var(--…) (trong lớp lẫn trong style="…")
lấy đúng bảng màu sáng/tối của build.py, nên nét tô bằng var(--note), var(--ok)… hiện đúng màu.
MuPDF không vẽ marker nên mũi tên chỉ hiện thân, không có đầu.
"""
import os, re, sys, tempfile

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
HINH = {
    'en': {'fill': 'var(--en)', 'stroke': 'var(--mut)', 'stroke-width': '1.2'},
    'de': {'fill': 'var(--de)', 'stroke': 'var(--mut)', 'stroke-width': '1.2'},
    'pu': {'fill': 'var(--pu)', 'stroke': 'var(--mut)', 'stroke-width': '1.2'},
    'inf': {'fill': 'var(--inf)'}, 'aff': {'fill': 'var(--aff)'}, 'phf': {'fill': 'var(--phf)'},
    'le': {'fill': 'var(--le)', 'stroke': 'var(--mut)', 'stroke-width': '1'},
    'c1': {'fill': '#2563eb', 'fill-opacity': '.16', 'stroke': '#2563eb', 'stroke-width': '2'},
    'c2': {'fill': '#ea580c', 'fill-opacity': '.16', 'stroke': '#ea580c', 'stroke-width': '2'},
    'c3': {'fill': '#16a34a', 'fill-opacity': '.16', 'stroke': '#16a34a', 'stroke-width': '2'},
    'k': {'stroke': 'var(--fg)', 'stroke-width': '1.5', 'fill': 'none'},
    'ax': {'stroke': 'var(--fg)', 'stroke-width': '1.5', 'fill': 'none'},
    'd': {'stroke': 'var(--mut)', 'stroke-width': '1.3', 'stroke-dasharray': '6 4', 'fill': 'none'},
    'ld': {'stroke': 'var(--mut)', 'stroke-width': '1', 'fill': 'none'},
    'rl': {'stroke': 'var(--bad)', 'stroke-width': '2.5'},
    'phl': {'fill': 'none', 'stroke': 'var(--note)', 'stroke-width': '2'},
    'mk': {'fill': 'var(--fg)'},
}
CHU = {'s': {'font-size': '13'}, 'big': {'font-size': '19'}, 'b': {'font-weight': 'bold'},
       'm': {'fill': 'var(--mut)'}, 'r': {'fill': 'var(--bad)'}}


def bang_mau(toi):
    """Biến màu (--en, --note…) đọc thẳng từ CSS của build.py: giao diện sáng, hoặc tối nếu toi."""
    css = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read()
    sang = re.search(r':root\{(.*?)\}', css, re.S).group(1)
    bien = dict(re.findall(r'--([\w-]+):([^;}]+)', sang))
    if toi:
        bien.update(re.findall(r'--([\w-]+):([^;}]+)',
                               re.search(r'prefers-color-scheme:dark\)\{:root\{(.*?)\}', css, re.S).group(1)))
    return {k: v.strip() for k, v in bien.items()}


def doi_the(m, bien):
    """Một thẻ SVG: thay class (và style) bằng thuộc tính trình bày, var(--…) bằng mã màu."""
    t = m.group(0)
    ten = re.match(r'<(\w+)', t).group(1)
    tt = {'fill': 'var(--fg)', 'font-size': '15', 'font-family': 'Arial'} if ten == 'text' else {}
    lop = re.search(r'\sclass="([^"]*)"', t)
    if lop:
        for c in lop.group(1).split():
            tt.update((CHU if ten == 'text' else HINH).get(c, {}))
        t = t.replace(lop.group(0), '')
    kieu = re.search(r'\sstyle="([^"]*)"', t)
    if kieu:
        for kv in kieu.group(1).split(';'):
            if ':' in kv:
                k, v = kv.split(':', 1)
                tt[k.strip()] = v.strip()
        t = t.replace(kieu.group(0), '')
    for k in list(tt):
        tt[k] = re.sub(r'var\(--([\w-]+)\)', lambda x: bien.get(x.group(1), '#000'), tt[k])
        mau = re.match(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)', tt[k])
        if mau and k in ('fill', 'stroke'):  # MuPDF không hiểu rgba(): tách thành màu + độ đục
            tt[k] = '#%02x%02x%02x' % tuple(int(x) for x in mau.groups()[:3])
            tt[k + '-opacity'] = mau.group(4)
    return re.sub(r'^<\w+', lambda x: x.group(0) + ''.join(' %s="%s"' % kv for kv in tt.items()), t)


def dung(svg, toi=False):
    bien = bang_mau(toi)
    svg = re.sub(r'<(?:path|rect|ellipse|circle|line|polyline|polygon|g|text)\b[^>]*>', lambda m: doi_the(m, bien), svg)
    svg = re.sub(r'\sclass="dg"|\sstyle="max-width:\d+px"', '', svg)
    w, h = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()][2:]
    svg = svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" ' % (w * 2, h * 2), 1)
    svg = re.sub(r'(<svg\b[^>]*>)', r'\1<rect x="-9999" y="-9999" width="99999" height="99999" fill="%s"/>' % bien['bg'], svg, count=1)
    return fitz.open(stream=svg.encode('utf-8'), filetype='svg')[0].get_pixmap(alpha=False)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    thamso = [a for a in sys.argv[1:] if a != '--toi']
    toi = '--toi' in sys.argv[1:]
    md = thamso[0] if os.path.exists(thamso[0]) else os.path.join(HERE, thamso[0])
    ra = thamso[1] if len(thamso) > 1 else tempfile.gettempdir()
    svgs = re.findall(r'<svg class="dg".*?</svg>', open(md, encoding='utf-8').read(), re.S)
    for i, s in enumerate(svgs):
        duong = os.path.join(ra, 'svg_%d%s.png' % (i, '_toi' if toi else ''))
        dung(s, toi).save(duong)
        print('  ', duong)
