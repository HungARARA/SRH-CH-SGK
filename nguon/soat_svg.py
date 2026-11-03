# -*- coding: utf-8 -*-
"""SRH CH SGK - dựng PNG từ các sơ đồ <svg class="dg"> trong một bài .md để soát bằng mắt
(dùng khi khung trình duyệt bị ẩn, không chụp được trang).

Chạy bằng Python313 (có fitz):
  "C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I nguon/soat_svg.py "Bài 8.md" [thư mục ra]
  → <thư mục ra>/svg_0.png, svg_1.png… theo thứ tự sơ đồ trong bài (mặc định: thư mục tạm của máy).

Lớp màu (en, de, c1, k, ld, s, b…) đổi thành thuộc tính theo bảng màu giao diện sáng của build.py.
MuPDF không vẽ marker nên mũi tên chỉ hiện thân, không có đầu.
"""
import os, re, sys, tempfile

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
HINH = {
    'en': {'fill': '#f4f1e6', 'stroke': '#5d6675', 'stroke-width': '1.2'},
    'de': {'fill': '#f1dca8', 'stroke': '#5d6675', 'stroke-width': '1.2'},
    'pu': {'fill': '#f3b2b2', 'stroke': '#5d6675', 'stroke-width': '1.2'},
    'inf': {'fill': '#7a4517'}, 'aff': {'fill': '#e5bd5c'},
    'le': {'fill': '#cfc6b4', 'stroke': '#5d6675', 'stroke-width': '1'},
    'c1': {'fill': '#2563eb', 'fill-opacity': '.16', 'stroke': '#2563eb', 'stroke-width': '2'},
    'c2': {'fill': '#ea580c', 'fill-opacity': '.16', 'stroke': '#ea580c', 'stroke-width': '2'},
    'c3': {'fill': '#16a34a', 'fill-opacity': '.16', 'stroke': '#16a34a', 'stroke-width': '2'},
    'k': {'stroke': '#1d2433', 'stroke-width': '1.5', 'fill': 'none'},
    'ax': {'stroke': '#1d2433', 'stroke-width': '1.5', 'fill': 'none'},
    'd': {'stroke': '#5d6675', 'stroke-width': '1.3', 'stroke-dasharray': '6 4', 'fill': 'none'},
    'ld': {'stroke': '#5d6675', 'stroke-width': '1', 'fill': 'none'},
    'rl': {'stroke': '#dc2626', 'stroke-width': '2.5'},
    'mk': {'fill': '#1d2433'},
}
CHU = {'s': {'font-size': '13'}, 'big': {'font-size': '19'}, 'b': {'font-weight': 'bold'},
       'm': {'fill': '#5d6675'}, 'r': {'fill': '#dc2626'}}
BIEN = {'var(--card)': '#ffffff', 'var(--mut)': '#5d6675', 'var(--fg)': '#1d2433'}


def doi_the(m):
    """Một thẻ SVG: thay class (và style) bằng thuộc tính trình bày."""
    t = m.group(0)
    ten = re.match(r'<(\w+)', t).group(1)
    tt = {'fill': '#1d2433', 'font-size': '15', 'font-family': 'Arial'} if ten == 'text' else {}
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
    return re.sub(r'^<\w+', lambda x: x.group(0) + ''.join(' %s="%s"' % kv for kv in tt.items()), t)


def dung(svg):
    for a, b in BIEN.items():
        svg = svg.replace(a, b)
    svg = re.sub(r'<(?:path|rect|ellipse|circle|line|polyline|polygon|g|text)\b[^>]*>', doi_the, svg)
    svg = re.sub(r'\sclass="dg"|\sstyle="max-width:\d+px"', '', svg)
    w, h = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()][2:]
    svg = svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" ' % (w * 2, h * 2), 1)
    return fitz.open(stream=svg.encode('utf-8'), filetype='svg')[0].get_pixmap(alpha=False)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    md = sys.argv[1] if os.path.exists(sys.argv[1]) else os.path.join(HERE, sys.argv[1])
    ra = sys.argv[2] if len(sys.argv) > 2 else tempfile.gettempdir()
    svgs = re.findall(r'<svg class="dg".*?</svg>', open(md, encoding='utf-8').read(), re.S)
    for i, s in enumerate(svgs):
        duong = os.path.join(ra, 'svg_%d.png' % i)
        dung(s).save(duong)
        print('  ', duong)
