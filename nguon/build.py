# -*- coding: utf-8 -*-
"""SRH CH SGK - dựng file học .html (1 file tự chứa, mở offline, chạy cả trên điện thoại)
từ nguồn Markdown "nguon/Bài N.md".

Chạy bằng Python313 (có PIL):
  "C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I build.py "Bài 1.md"
  (bỏ trống đối số = dựng lại mọi "Bài *.md" trong thư mục nguon)
Mỗi lần chạy cũng dựng lại "../index.html" = trang chủ web (GitHub Pages), liệt kê 10 bài.

Cú pháp Markdown mở rộng: xem "../QUY TRÌNH CHUẨN HOÁ.md", mục 9.
"""
import base64, glob, html, io, math, os, re, sys, unicodedata, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)

CALLOUT = {'NOTE': ('note', '💡 Hiểu nhanh'), 'TIP': ('tip', '🧠 Mẹo nhớ'),
           'IMPORTANT': ('imp', '📌 Lưu ý'), 'WARNING': ('warn', '⚠️ Đề hay gài'),
           'CAUTION': ('cau', '⚖️ Hai cách hiểu'), 'WHY': ('why', '🔍 Vì sao?')}
BAI = [  # 10 bài SGK (QUY TRÌNH CHUẨN HOÁ.md, mục 4): số bài, tên, trang sách
    (1, 'Quan niệm mới trong chẩn đoán và điều trị bệnh sâu răng', '1–16'),
    (2, 'Quá trình mất khoáng và tái khoáng mô cứng', '17–31'),
    (3, 'Chẩn đoán bệnh sâu răng', '32–47'),
    (4, 'Điều trị và phòng ngừa bệnh sâu răng', '48–92'),
    (5, 'Phân loại xoang sâu răng', '94–108'),
    (6, 'Các yếu tố sinh học trong sửa soạn xoang', '109–113'),
    (7, 'Nguyên tắc tạo xoang và trám bằng xi măng glass ionomer (GIC)', '114–122'),
    (8, 'Nguyên tắc tạo xoang và trám bằng vật liệu composite', '123–170'),
    (9, 'Che tủy', '171–187'),
    (10, 'Mòn răng', '188–197')]
BLOCK_HTML = re.compile(r'^<(figure|div|svg|details|table|section|aside)\b')
LIST = re.compile(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$')
NUM = re.compile(r'^(\d+(?:\.\d+)*)\.?\s')
INLINE_RAW = re.compile(r'`[^`]+`|</?[a-zA-Z][\w-]*(?:\s[^<>]*)?/?>')
QBAR = ('<div class="qbar"><button data-act="reset">Làm lại</button>'
        '<button data-act="wrong">Chỉ xem câu sai</button>'
        '<button data-act="all">Hiện hết đáp án</button></div>')


class Doc:
    def __init__(self, md_path):
        self.base = os.path.dirname(os.path.abspath(md_path))
        self.toc, self.ids, self.links, self.q = [], set(), [], []
        self.uid = 0

    # ---------- chữ trong dòng ----------
    def fmt(self, t):
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
        t = re.sub(r'(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])', r'<i>\1</i>', t)
        t = re.sub(r'==(.+?)==', r'<mark>\1</mark>', t)

        def link(m):
            if m.group(2).startswith('#'):
                self.links.append(m.group(2)[1:])
            return '<a href="%s">%s</a>' % (m.group(2), m.group(1))
        return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)

    def inline(self, s):
        out, pos = [], 0
        for m in INLINE_RAW.finditer(s):
            out.append(self.fmt(html.escape(s[pos:m.start()], quote=False)))
            t = m.group(0)
            out.append('<code>%s</code>' % html.escape(t[1:-1]) if t[0] == '`' else t)
            pos = m.end()
        out.append(self.fmt(html.escape(s[pos:], quote=False)))
        return ''.join(out)

    # ---------- khối ----------
    def starts_block(self, lines, i):
        s = lines[i].strip()
        return (s.startswith(('```', '#', '>', '|', '![')) or bool(BLOCK_HTML.match(s))
                or bool(LIST.match(lines[i])) or bool(re.match(r'^-{3,}$', s)))

    def blocks(self, lines):
        out, i, n = [], 0, len(lines)
        while i < n:
            ln, s = lines[i], lines[i].strip()
            if not s:
                i += 1
                continue
            if s.startswith('```'):
                kind, buf, i = s[3:].strip(), [], i + 1
                while i < n and not lines[i].strip().startswith('```'):
                    buf.append(lines[i])
                    i += 1
                out.append(self.fence(kind, buf))
                i += 1
                continue
            m = BLOCK_HTML.match(s)
            if m:
                tag, depth, buf = m.group(1), 0, []
                while i < n:
                    buf.append(lines[i])
                    depth += len(re.findall(r'<%s\b' % tag, lines[i])) - len(re.findall(r'</%s>' % tag, lines[i]))
                    i += 1
                    if depth <= 0:
                        break
                out.append('\n'.join(buf))
                continue
            m = re.match(r'^(#{1,4})\s+(.*)$', s)
            if m:
                lv, text = len(m.group(1)), m.group(2).strip()
                if lv == 2 and 'trắc nghiệm' in text.lower():
                    j = i + 1
                    while j < n and not lines[j].startswith('## '):
                        j += 1
                    out.append(self.heading(2, text, 'trac-nghiem') + QBAR + self.quiz(lines[i + 1:j]))
                    i = j
                    continue
                out.append(self.heading(lv, text))
                i += 1
                continue
            if re.match(r'^-{3,}$', s):
                out.append('<hr>')
                i += 1
                continue
            if s.startswith('>'):
                buf = []
                while i < n and lines[i].strip().startswith('>'):
                    buf.append(re.sub(r'^\s*> ?', '', lines[i]))
                    i += 1
                out.append(self.quote(buf))
                continue
            if s.startswith('|') and i + 1 < n and re.match(r'^\s*\|?\s*:?-{2,}', lines[i + 1]):
                buf = []
                while i < n and lines[i].strip().startswith('|'):
                    buf.append(lines[i])
                    i += 1
                out.append(self.table(buf))
                continue
            m = re.match(r'^!\[(.*)\]\(([^)]+)\)$', s)
            if m:
                out.append(self.image(m.group(2), m.group(1)))
                i += 1
                continue
            if LIST.match(ln):
                buf = []
                while i < n and lines[i].strip() and (LIST.match(lines[i]) or lines[i].startswith((' ', '\t'))):
                    buf.append(lines[i])
                    i += 1
                out.append(self.lst(buf))
                continue
            buf = []
            while i < n and lines[i].strip() and not self.starts_block(lines, i):
                buf.append(lines[i].strip())
                i += 1
            if not buf:
                buf, i = [s], i + 1
            out.append('<p>%s</p>' % self.inline(' '.join(buf)))
        return '\n'.join(out)

    def heading(self, lv, text, hid=None):
        if not hid:
            m = NUM.match(text + ' ')
            hid = 'm' + m.group(1).replace('.', '-') if m else self.slug(text)
        base, k = hid, 2
        while hid in self.ids:
            hid, k = '%s-%d' % (base, k), k + 1
        self.ids.add(hid)
        if lv in (2, 3):
            self.toc.append((lv, hid, text))
        return '<h%d id="%s">%s</h%d>' % (lv, hid, self.inline(text), lv)

    @staticmethod
    def slug(s):
        s = re.sub(r'<[^>]+>', '', s).replace('đ', 'd').replace('Đ', 'D')
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
        return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') or 'muc'

    def quote(self, buf):
        m = re.match(r'^\[!(\w+)\]\s*(.*)$', buf[0].strip()) if buf else None
        if m and m.group(1).upper() in CALLOUT:
            cls, title = CALLOUT[m.group(1).upper()]
            if m.group(2).strip():
                title = title.split(' ', 1)[0] + ' ' + m.group(2).strip()
            return '<div class="co %s"><div class="ct">%s</div>%s</div>' % (cls, self.inline(title), self.blocks(buf[1:]))
        return '<blockquote>%s</blockquote>' % self.blocks(buf)

    @staticmethod
    def cells(row):
        row = row.strip()
        row = row[1:] if row.startswith('|') else row
        row = row[:-1] if row.endswith('|') else row
        return [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', row)]

    def table(self, buf):
        rows = [self.cells(r) for r in buf]
        al = ['center' if c.startswith(':') and c.endswith(':') else 'right' if c.endswith(':') else '' for c in rows[1]]

        def tr(cs, tag):
            return '<tr>%s</tr>' % ''.join(
                '<%s%s>%s</%s>' % (tag, ' style="text-align:%s"' % al[k] if k < len(al) and al[k] else '',
                                   self.inline(c), tag) for k, c in enumerate(cs))
        return '<div class="tw"><table><thead>%s</thead><tbody>%s</tbody></table></div>' % (
            tr(rows[0], 'th'), ''.join(tr(r, 'td') for r in rows[2:]))

    def lst(self, buf):
        items = []
        for ln in buf:
            m = LIST.match(ln)
            if m:
                items.append([len(m.group(1).expandtabs(2)), m.group(2), m.group(3)])
            elif items:
                items[-1][2] += ' ' + ln.strip()
        out, i = [], 0
        while i < len(items):
            h, i = self._lst(items, i, items[i][0])
            out.append(h)
        return ''.join(out)

    def _lst(self, items, i, ind):
        ordered = items[i][1][0].isdigit()
        tag, st = ('ol', int(items[i][1][:-1])) if ordered else ('ul', 1)
        out = ['<%s%s>' % (tag, ' start="%d"' % st if st != 1 else '')]
        while i < len(items) and items[i][0] >= ind:
            if items[i][0] > ind:
                sub, i = self._lst(items, i, items[i][0])
                out[-1] = out[-1][:-5] + sub + '</li>'
                continue
            out.append('<li>%s</li>' % self.inline(items[i][2]))
            i += 1
        out.append('</%s>' % tag)
        return ''.join(out), i

    def image(self, src, alt):
        p = os.path.join(self.base, src)
        cap = '<figcaption>%s</figcaption>' % self.inline(alt) if alt else ''
        if not os.path.exists(p):
            print('  ! thiếu hình:', src)
            return '<figure><p class="miss">[Thiếu hình: %s]</p>%s</figure>' % (html.escape(src), cap)
        from PIL import Image
        im = Image.open(p).convert('RGB')
        if im.width > 1000:
            im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        b = io.BytesIO()
        im.save(b, 'JPEG', quality=70, optimize=True)
        return '<figure><img loading="lazy" alt="%s" src="data:image/jpeg;base64,%s">%s</figure>' % (
            html.escape(re.sub(r'[*=]', '', alt)), base64.b64encode(b.getvalue()).decode(), cap)

    # ---------- khối có rào ``` ----------
    def fence(self, kind, buf):
        if kind == 'flow':
            return self.flow(buf)
        if kind == 'ph':
            return self.ph(buf)
        return '<pre><code>%s</code></pre>' % html.escape('\n'.join(buf))

    def flow(self, buf):
        rows = []
        for ln in buf:
            if not ln.strip():
                continue
            nodes = []
            for t in re.split(r'\s+(?:->|→)\s+', ln.strip()):
                cls = 'nd'
                if t[:1] in ('!', '+'):
                    cls, t = cls + (' hot' if t[0] == '!' else ' ok'), t[1:].strip()
                nodes.append('<span class="%s">%s</span>' % (cls, self.inline(t)))
            rows.append('<div class="fr">%s</div>' % '<span class="ar">→</span>'.join(nodes))
        return '<div class="flow">%s</div>' % ''.join(rows)

    @staticmethod
    def drop(x):
        """pH mảng bám tụt sau 1 lần ăn đường (phút): tụt nhanh, giữ ~15 phút, hồi dần."""
        if x < 0:
            return 0.0
        if x < 3:
            return 2.3 * x / 3
        if x < 15:
            return 2.3
        return 2.3 * math.exp(-(x - 15) / 14)

    @staticmethod
    def hm(s):
        h, _, m = s.partition(':')
        return int(h) * 60 + int(m or 0)

    def ph(self, buf):
        cap, rng, panels = '', None, []
        for ln in buf:
            s = ln.strip()
            if not s:
                continue
            if s.lower().startswith('caption:'):
                cap = s[8:].strip()
                continue
            m = re.match(r'^(\d{1,2})\s*-\s*(\d{1,2})$', s)
            if m:
                rng = (int(m.group(1)) * 60, int(m.group(2)) * 60)
                continue
            lab, _, ts = s.partition('|')
            panels.append((lab.strip(), [self.hm(x) for x in ts.split()]))
        t0, t1 = rng or (min(min(p[1]) for p in panels) - 60, max(max(p[1]) for p in panels) + 120)
        W, L, R, H, G = 440, 34, 10, 92, 30
        sx = lambda t: L + (t - t0) * (W - L - R) / (t1 - t0)
        svg, yb = [], 0
        for k, (lab, ts) in enumerate(panels):
            top = 8 + k * (H + G)
            sy = lambda p, top=top: top + 22 + (7 - p) * 66 / 2.7
            pts, below, t = [], 0, t0
            while t <= t1:
                p = max(4.3, 7 - sum(self.drop(t - s) for s in ts))
                pts.append('%.1f,%.1f' % (sx(t), sy(p)))
                below += p < 5.5
                t += 1
            self.uid += 1
            cid, y55, yb = 'phc%d' % self.uid, sy(5.5), sy(4.3)
            svg += ['<clipPath id="%s"><rect x="%d" y="%.1f" width="%d" height="%.1f"/></clipPath>' % (cid, L, y55, W - L - R, yb - y55),
                    '<polygon class="phf" clip-path="url(#%s)" points="%.1f,%.1f %s %.1f,%.1f"/>' % (cid, sx(t0), top, ' '.join(pts), sx(t1), top),
                    '<line class="ax" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (L, yb, W - R, yb),
                    '<line class="d" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (L, y55, W - R, y55),
                    '<polyline class="phl" points="%s"/>' % ' '.join(pts),
                    '<text x="%d" y="%.1f" text-anchor="end" class="s m">7</text>' % (L - 6, sy(7) + 4),
                    '<text x="%d" y="%.1f" text-anchor="end" class="s r">5,5</text>' % (L - 6, y55 + 4),
                    '<text x="%d" y="%d" class="s b">%s<tspan class="r"> · ≈ %d phút dưới pH 5,5</tspan></text>' % (
                        L, top + 12, html.escape(lab), below)]
            svg += ['<text x="%.1f" y="%.1f" text-anchor="middle" class="s m">▲</text>' % (sx(s), yb + 14) for s in ts]
        svg += ['<text x="%.1f" y="%.1f" text-anchor="middle" class="s m">%dh</text>' % (sx(h * 60), yb + 30, h)
                for h in range(t0 // 60, t1 // 60 + 1)]
        return '<figure><div class="sc"><svg class="dg" style="max-width:620px" viewBox="0 0 %d %d" role="img" aria-label="Biểu đồ pH mảng bám theo giờ ăn">%s</svg></div>%s</figure>' % (
            W, int(yb + 36), ''.join(svg), '<figcaption>%s</figcaption>' % self.inline(cap) if cap else '')

    # ---------- trắc nghiệm ----------
    def quiz(self, lines):
        out, i, n = [], 0, len(lines)
        while i < n:
            if lines[i].startswith('#### '):
                head, stem, opts, ex = lines[i][5:].strip(), [], [], []
                i += 1
                while i < n and not lines[i].startswith('#'):
                    l = lines[i]
                    i += 1
                    m = re.match(r'^\s*[-*]\s+\[([ xX])\]\s+(.*)$', l)
                    if m:
                        opts.append((m.group(1) != ' ', m.group(2).strip()))
                    elif l.strip().startswith('>'):
                        ex.append(re.sub(r'^\s*> ?', '', l))
                    elif l.strip():
                        (ex if opts else stem).append(l.strip())
                out.append(self.question(head, stem, opts, ex))
            else:
                j = i + 1
                while j < n and not lines[j].startswith('#### '):
                    j += 1
                out.append(self.blocks(lines[i:j]))
                i = j
        return '\n'.join(out)

    def question(self, head, stem, opts, ex):
        no, L = len(self.q) + 1, 'ABCDEFG'
        keys = [k for k, (ok, _) in enumerate(opts) if ok]
        if len(keys) != 1 or len(opts) < 2:
            print('  ! Câu %d: %d đáp án đúng / %d lựa chọn' % (no, len(keys), len(opts)))
        key = L[keys[0]] if keys else '?'
        self.q.append(key)
        tag = self.inline(head)
        ref = re.search(r'(\d+(?:\.\d+)*)\s*$', head)
        if ref:
            rid = 'm' + ref.group(1).replace('.', '-')
            self.links.append(rid)
            tag = '<a href="#%s">%s</a>' % (rid, self.inline(head[:ref.start()] + 'mục ' + ref.group(1)))
        opt_html = ''.join('<button class="opt" data-ok="%d"><b>%s.</b> %s</button>' % (ok, L[k], self.inline(t))
                           for k, (ok, t) in enumerate(opts))
        return ('<div class="q" id="cau-%d"><div class="qh"><b>Câu %d</b><span class="tag">%s</span></div>'
                '<div class="qs">%s</div><div class="opts">%s</div><div class="ex"><b>Đáp án %s.</b> %s</div></div>'
                % (no, no, tag, self.inline(' '.join(stem)), opt_html, key, '<br>'.join(self.inline(e) for e in ex)))

    def page(self, meta, body):
        toc = ''.join('<li class="t%d"><a href="#%s">%s</a></li>' % (lv, hid, html.escape(re.sub(r'[*=`]', '', t)))
                      for lv, hid, t in self.toc)
        return (TEMPLATE.replace('@@CSS@@', CSS).replace('@@JS@@', JS)
                .replace('@@SHORT@@', html.escape(meta.get('short') or meta.get('title', '')))
                .replace('@@TITLE@@', html.escape(meta.get('title', '')))
                .replace('@@SUB@@', self.inline(meta.get('sgk', '')))
                .replace('@@TOC@@', toc).replace('@@BODY@@', body))


TEMPLATE = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>@@SHORT@@</title>
<style>@@CSS@@</style></head>
<body id="top">
<header class="bar"><a class="home" href="#top">@@SHORT@@</a><span id="sc"></span>
<button data-act="cloze" title="Che các chữ tô vàng để tự nhớ lại; bấm vào ô bị che để xem">Che từ khoá</button>
<a href="#trac-nghiem">Trắc nghiệm ↓</a></header>
<main>
<p class="crumb"><a href="index.html">← Các bài Sâu Răng Học</a></p>
<h1>@@TITLE@@</h1><p class="sub">@@SUB@@</p>
<nav class="toc"><details><summary>Mục lục</summary><ol>@@TOC@@</ol></details></nav>
@@BODY@@
</main>
<script>@@JS@@</script>
</body></html>
'''

CSS = '''
:root{--bg:#fbfaf7;--fg:#1d2433;--mut:#5d6675;--line:#e2ddd2;--card:#fff;--h2:#b03010;--h3:#113366;--mark:#fde68a;--cloze:#d4d0c7;
--note:#2563eb;--note-b:#eef4ff;--tip:#15803d;--tip-b:#edf9f1;--imp:#7c3aed;--imp-b:#f4efff;--warn:#c2410c;--warn-b:#fff3ea;--cau:#be123c;--cau-b:#fff0f3;--why:#0f766e;--why-b:#e8f6f4;
--ok:#15803d;--ok-b:#e5f6ea;--bad:#dc2626;--bad-b:#fdecec;--en:#f4f1e6;--de:#f1dca8;--pu:#f3b2b2;--inf:#7a4517;--aff:#e5bd5c;--le:#cfc6b4;--phf:rgba(220,38,38,.35)}
@media (prefers-color-scheme:dark){:root{--bg:#15171c;--fg:#e4e6ea;--mut:#9aa3b2;--line:#30353e;--card:#1c1f26;--h2:#f08a6c;--h3:#8db4ff;--mark:#6b5313;--cloze:#3b4049;
--note:#6b9bff;--note-b:#16233b;--tip:#4ade80;--tip-b:#132a1c;--imp:#b794ff;--imp-b:#231a3a;--warn:#fb923c;--warn-b:#33200f;--cau:#fb7185;--cau-b:#361521;--why:#2dd4bf;--why-b:#10302c;
--ok:#4ade80;--ok-b:#12301d;--bad:#f87171;--bad-b:#3a1616;--en:#3d3b33;--de:#5c4b24;--pu:#713636;--inf:#c58a4e;--aff:#8a6d22;--le:#77705f;--phf:rgba(248,113,113,.35)}}
*{box-sizing:border-box}html{scroll-padding-top:58px}
body{margin:0;background:var(--bg);color:var(--fg);font:16.5px/1.65 "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-text-size-adjust:100%}
main{max-width:880px;margin:auto;padding:8px 16px 90px}
.bar{position:sticky;top:0;z-index:9;display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:7px 16px;background:var(--card);border-bottom:1px solid var(--line)}
.bar .home{font-weight:700;color:var(--h3);text-decoration:none;margin-right:auto}
#sc{font-size:13.5px;color:var(--mut)}
.bar button,.bar a:not(.home),.qbar button{font:inherit;font-size:14px;padding:4px 11px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);text-decoration:none;cursor:pointer}
button.on{background:var(--h3);border-color:var(--h3);color:#fff}
h1{font-size:1.55em;line-height:1.3;color:var(--h3);margin:.7em 0 .15em}.sub{color:var(--mut);margin:0 0 .8em}
.crumb{margin:.8em 0 0;font-size:.9em}.crumb a{text-decoration:none}.crumb+h1{margin-top:.2em}
h2{font-size:1.3em;line-height:1.35;color:var(--h2);border-bottom:2px solid var(--line);padding-bottom:4px;margin:2.2em 0 .6em}
h3{font-size:1.12em;color:var(--h3);margin:1.6em 0 .5em}h4{font-size:1.02em;margin:1.3em 0 .4em}
a{color:var(--note)}p,li{overflow-wrap:break-word}ul,ol{padding-left:1.4em}li{margin:.15em 0}
mark{background:linear-gradient(transparent 50%,var(--mark) 50%);color:inherit;padding:0 1px}
body.cloze mark{background:var(--cloze);color:transparent;border-radius:3px;cursor:pointer}
body.cloze mark.show{background:linear-gradient(transparent 50%,var(--mark) 50%);color:inherit}
.toc details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 14px}.toc summary{cursor:pointer;font-weight:600}
.toc ol{list-style:none;padding:4px 0 6px;margin:0;columns:2 280px}.toc li{margin:2px 0;break-inside:avoid}.toc .t3{padding-left:1.1em;font-size:.93em}.toc a{text-decoration:none}
.tw{overflow-x:auto;margin:.8em 0}table{border-collapse:collapse;width:100%;font-size:.95em;background:var(--card)}
th,td{border:1px solid var(--line);padding:6px 9px;vertical-align:top;text-align:left}th{background:var(--h2);color:#fff;font-weight:600}
tbody tr:nth-child(even){background:rgba(127,127,127,.06)}
.co{border-left:4px solid;border-radius:8px;padding:8px 14px;margin:1em 0}.co .ct{font-weight:700;margin-bottom:2px}
.co>:last-child{margin-bottom:.2em}.co p{margin:.4em 0}.co table{background:transparent}
.co.note{border-color:var(--note);background:var(--note-b)}.co.note .ct{color:var(--note)}
.co.tip{border-color:var(--tip);background:var(--tip-b)}.co.tip .ct{color:var(--tip)}
.co.imp{border-color:var(--imp);background:var(--imp-b)}.co.imp .ct{color:var(--imp)}
.co.warn{border-color:var(--warn);background:var(--warn-b)}.co.warn .ct{color:var(--warn)}
.co.cau{border-color:var(--cau);background:var(--cau-b)}.co.cau .ct{color:var(--cau)}
.co.why{border-color:var(--why);background:var(--why-b)}.co.why .ct{color:var(--why)}
.ls{list-style:none;padding:0;display:grid;gap:10px}.ls li{margin:0;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.ls a,.ls .off{display:block;padding:10px 14px;border-radius:12px;color:var(--fg);text-decoration:none}.ls a:hover{background:var(--note-b)}
.ls span{display:block;font-size:.88em;color:var(--mut)}.ls .off{color:var(--mut)}
blockquote{margin:1em 0;padding:2px 14px;border-left:4px solid var(--line);color:var(--mut)}
.flow{margin:1em 0;display:grid;gap:9px}.fr{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.nd{background:var(--card);border:1.5px solid var(--line);border-radius:10px;padding:4px 10px;font-size:.93em;line-height:1.45}
.nd.hot{border-color:var(--bad);background:var(--bad-b)}.nd.ok{border-color:var(--ok);background:var(--ok-b)}.ar{color:var(--mut);font-weight:700}
figure{margin:1.2em 0}figure img{display:block;max-width:100%;margin:auto;border-radius:8px}
figcaption{font-size:.88em;color:var(--mut);margin-top:6px}.miss{color:var(--bad)}
.sc{overflow-x:auto}svg.dg{display:block;width:100%;height:auto;margin:auto}
svg.dg text{fill:var(--fg);font-size:15px;font-family:inherit}svg.dg .s{font-size:13px}svg.dg .big{font-size:19px}svg.dg .b{font-weight:700}
svg.dg .m{fill:var(--mut)}svg.dg .r{fill:var(--bad)}.dg .mk{fill:var(--fg)}
.dg .k,.dg .ax{stroke:var(--fg);stroke-width:1.5;fill:none}.dg .d{stroke:var(--mut);stroke-width:1.3;stroke-dasharray:6 4;fill:none}
.dg .ld{stroke:var(--mut);stroke-width:1;fill:none}.dg .rl{stroke:var(--bad);stroke-width:2.5}
.dg .c1{fill:rgba(37,99,235,.16);stroke:#2563eb;stroke-width:2}.dg .c2{fill:rgba(234,88,12,.16);stroke:#ea580c;stroke-width:2}
.dg .c3{fill:rgba(22,163,74,.16);stroke:#16a34a;stroke-width:2}
.dg .en{fill:var(--en);stroke:var(--mut);stroke-width:1.2}.dg .de{fill:var(--de);stroke:var(--mut);stroke-width:1.2}
.dg .pu{fill:var(--pu);stroke:var(--mut);stroke-width:1.2}.dg .inf{fill:var(--inf)}.dg .aff{fill:var(--aff)}
.dg .le{fill:var(--le);stroke:var(--mut);stroke-width:1}.dg .phl{fill:none;stroke:var(--note);stroke-width:2}.dg .phf{fill:var(--phf)}
.qbar{display:flex;gap:8px;flex-wrap:wrap;margin:.4em 0 1em}
.q{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 14px;margin:14px 0}
.qh{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;font-size:.88em;color:var(--mut)}.qh b{color:var(--fg)}.qh a{text-decoration:none}
.qs{margin:5px 0 9px;font-weight:600}.opts{display:grid;gap:6px}
.opt{font:inherit;text-align:left;padding:7px 12px;border:1.5px solid var(--line);border-radius:10px;background:var(--bg);color:var(--fg);cursor:pointer;line-height:1.5}
.opt:hover{border-color:var(--note)}.opt.ok,body.all .opt[data-ok="1"]{border-color:var(--ok);background:var(--ok-b)}.opt.bad{border-color:var(--bad);background:var(--bad-b)}
.ex{display:none;margin-top:10px;padding:8px 12px;border-radius:8px;background:var(--note-b);font-size:.95em}
.q[data-done] .ex,body.all .ex{display:block}body.wrong .q:not(.wrong){display:none}
@media (max-width:600px){body{font-size:16px}main{padding:6px 14px 80px}.bar{padding:6px 12px}#sc{order:9;width:100%}}
@media print{.bar,.qbar,.toc,.crumb{display:none}body{background:#fff;color:#000}.ex{display:block}.opt[data-ok="1"]{border-color:#15803d}
.q,.co,figure,tr{break-inside:avoid}mark{background:linear-gradient(transparent 50%,#fde68a 50%);color:#000}}
'''

JS = '''
(()=>{const B=document.body,Q=[...document.querySelectorAll('.q')],sc=document.getElementById('sc');let ok=0,dn=0;
const up=()=>{sc.textContent=Q.length?`Trắc nghiệm: ${ok}/${dn} đúng · ${Q.length} câu`:''};
Q.forEach(q=>q.querySelectorAll('.opt').forEach(b=>b.addEventListener('click',()=>{if(q.dataset.done)return;q.dataset.done=1;dn++;
const r=b.dataset.ok==='1';if(r)ok++;q.classList.add(r?'right':'wrong');b.classList.add(r?'ok':'bad');
q.querySelector('.opt[data-ok="1"]').classList.add('ok');up()})));
const act={cloze:()=>{B.classList.toggle('cloze');document.querySelectorAll('mark.show').forEach(m=>m.classList.remove('show'))},
all:()=>B.classList.toggle('all'),wrong:()=>B.classList.toggle('wrong'),
reset:()=>{Q.forEach(q=>{delete q.dataset.done;q.classList.remove('right','wrong');q.querySelectorAll('.opt').forEach(o=>o.classList.remove('ok','bad'))});
ok=dn=0;B.classList.remove('wrong','all');document.querySelectorAll('button.on').forEach(b=>{if(b.dataset.act!=='cloze')b.classList.remove('on')});up()}};
document.addEventListener('click',e=>{const a=e.target.closest('[data-act]');
if(a){act[a.dataset.act]();if(a.dataset.act!=='reset')a.classList.toggle('on',B.classList.contains(a.dataset.act))}
else if(e.target.tagName==='MARK'&&B.classList.contains('cloze'))e.target.classList.toggle('show')});up()})();
'''


INDEX = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SRH · Sâu Răng Học theo SGK</title>
<style>@@CSS@@</style></head>
<body>
<header class="bar"><a class="home" href="index.html">SRH CH SGK</a></header>
<main>
<h1>Sâu Răng Học – học theo SGK</h1>
<p class="sub">Giáo trình Sâu Răng Học, Trường ĐH Y Dược Cần Thơ · mỗi bài một trang, học 1 bài/ngày</p>
<div class="co imp"><div class="ct">📌 Cách học mỗi bài</div><ol>
<li>Đọc từng mục theo đúng số mục SGK: 💡 Hiểu nhanh → 📖 SGK ghi → 🔍 Vì sao…? → 🧠 Mẹo nhớ → ⚠️ Đề hay gài.</li>
<li>Bấm <b>Che từ khoá</b> rồi đọc lại; gặp ô bị che thì tự nói ra trước, rồi bấm vào ô để kiểm tra.</li>
<li>Làm trắc nghiệm cuối bài; câu sai thì bấm nhãn "mục …" để quay về đúng đoạn cần đọc.</li>
<li>Sáng hôm sau: mở lại bài, bật Che từ khoá, đọc phần <b>Ôn 5 phút</b> rồi làm lại các câu sai.</li>
</ol></div>
<h2 id="cac-bai">Các bài</h2>
<ol class="ls">
@@LIST@@
</ol>
</main>
</body></html>
'''


def read(md_path):
    """Tách phần đầu '---' (title, short, sgk, out) khỏi nội dung."""
    text = open(md_path, encoding='utf-8').read().replace('\r\n', '\n')
    meta = {}
    if text.startswith('---\n'):
        end = text.index('\n---', 4)
        for ln in text[4:end].splitlines():
            k, _, v = ln.partition(':')
            if k.strip():
                meta[k.strip()] = v.strip()
        text = text[end + 4:]
    return meta, text


def build(md_path):
    meta, text = read(md_path)
    d = Doc(md_path)
    body = d.blocks(text.split('\n'))
    out = os.path.join(OUT_DIR, meta.get('out') or os.path.splitext(os.path.basename(md_path))[0] + '.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(d.page(meta, body))
    bad = sorted(set(l for l in d.links if l not in d.ids))
    print('%s -> %s | %d KB | %d câu, đáp án %s%s' % (
        os.path.basename(md_path), os.path.basename(out), os.path.getsize(out) // 1024, len(d.q),
        {k: d.q.count(k) for k in 'ABCD'}, (' | ! link hỏng: ' + ', '.join(bad)) if bad else ''))


def build_index():
    """index.html = trang chủ web: đủ 10 bài; bài đã dựng thì có link, còn lại ghi "chưa soạn"."""
    items, done = [], 0
    for n, name, pages in BAI:
        md = os.path.join(HERE, 'Bài %d.md' % n)
        meta, text = read(md) if os.path.exists(md) else ({}, '')
        out = meta.get('out') or 'Bài %d.html' % n
        if meta and os.path.exists(os.path.join(OUT_DIR, out)):
            done += 1
            nq = len(re.findall(r'^\s*[-*]\s+\[[xX]\]', text, re.M))
            items.append('<li><a href="%s"><b>Bài %d.</b> %s<span>%s · %d câu trắc nghiệm</span></a></li>' % (
                urllib.parse.quote(out), n, html.escape(name), html.escape(re.sub(r'[*=`]', '', meta.get('sgk', ''))), nq))
        else:
            items.append('<li class="off"><b>Bài %d.</b> %s<span>SGK tr. %s · chưa soạn</span></li>' % (
                n, html.escape(name), pages))
    with open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(INDEX.replace('@@CSS@@', CSS).replace('@@LIST@@', '\n'.join(items)))
    print('index.html | %d/%d bài có trang' % (done, len(BAI)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for a in sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, 'Bài *.md'))):
        build(a if os.path.exists(a) else os.path.join(HERE, a))
    build_index()
