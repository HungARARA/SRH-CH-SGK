# -*- coding: utf-8 -*-
"""SRH CH SGK - cắt hình từ SGK bản chụp vào nguon/hinh/ (.jpg rộng tối đa 1000 px).

Chạy bằng Python313 (có fitz, PIL, numpy):
  "C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I nguon/cat_hinh.py b2-h2-3 b2-h2-4
  (bỏ trống đối số = cắt lại mọi hình khai trong HINH)
  ... cat_hinh.py --luoi 23 40 370 420 590 [ra.png]
  = ảnh trang sách 23 có lưới toạ độ (ô 10, vạch đỏ mỗi 50) để dò khung cắt.

Toạ độ: trang đã xoay thẳng, quy về bề ngang 480 (x0, y0 = góc trên trái; x1, y1 = góc dưới phải).
Trang ảnh chụp nghiêng nên script tự xoay thẳng trước khi cắt.
"""
import io, os, sys, tempfile

import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = 'C:/Users/1/Desktop/Local HỌC TẬP Y KHOA VÀ FILE/Sâu Răng Học/Giáo Trình Sâu Răng Học Bản Chụp Tay Scan.pdf'

# tên file: (trang sách, x0, y0, x1, y1, kiểu[, vùng tô trắng])
# kiểu 'l' = hình vẽ, biểu đồ: đẩy nền trắng mạnh, xoá chữ trang sau in thấm qua
# kiểu 'p' = ảnh chụp, hình có chữ trên nền màu: làm trắng nhẹ tay
# kiểu 's' = sơ đồ khối màu trên nền giấy: như 'l', thêm xoá mọi vệt xám nhạt (chữ trang sau in thấm), giữ nét đậm và màu
# vùng tô trắng = danh sách (x0, y0, x1, y1) cùng hệ toạ độ trang, để xoá chữ in thấm ở khoảng trống giữa các ảnh
HINH = {
    'b2-h2-3': (23, 60, 385, 396, 566, 'l'),
    'b2-h2-4': (24, 137, 433, 359, 575, 'p'),
    'b2-h2-5': (25, 125, 287, 352, 556, 'p'),
    'b2-h2-6': (26, 115, 62, 415, 228, 'p'),
    'b2-h2-8': (27, 113, 302, 362, 564, 'l'),
    'b2-h2-9a': (28, 88, 70, 250, 198, 'l'),
    'b2-h2-9b': (28, 258, 88, 442, 192, 'l'),
    'b2-h2-9c': (28, 150, 198, 380, 400, 'l'),
    'b2-h2-10': (30, 165, 70, 372, 195, 'l'),
    'b3-h3-1': (38, 66, 248, 451, 370, 'p'),
    'b3-h3-2': (39, 60, 248, 405, 467, 'p'),
    'b3-h3-3': (42, 133, 66, 396, 232, 'p', [(262, 66, 396, 138.5)]),
    'b3-h3-4': (43, 80, 68, 387, 168, 'p'),
    'b3-h3-5': (43, 117, 378, 347, 552, 'p'),
    'b3-h3-6': (44, 86, 188, 441, 412, 'p'),
    'b4-h4-2': (50, 100, 222, 402, 400, 'l'),
    'b4-h4-3': (51, 88, 62, 376, 226, 'p'),
    'b4-h4-4': (51, 88, 374, 378, 528, 's'),
    'b4-h4-6': (54, 96, 58, 410, 246, 'p'),
    'b4-h4-7': (55, 58, 62, 398, 500, 'p', [(238, 390, 398, 500)]),
    'b4-h4-8': (56, 106, 55, 422, 228, 'p'),
    'b4-h4-9': (56, 143, 444, 394, 571, 'p'),
    'b4-h4-10': (57, 80, 64, 376, 200, 'p'),
    'b4-h4-11': (57, 67, 492, 398, 600, 'p'),
    'b4-h4-12': (58, 155, 55, 374, 201, 'p'),
    'b4-h4-18': (76, 160, 62, 403, 468, 'p'),
    'b4-h4-22': (80, 74, 60, 435, 343, 'p'),
    'b4-h4-23': (81, 52, 230, 420, 410, 'l'),
}


def nghieng(im):
    """Góc xoay (độ) làm các dòng chữ nằm ngang: góc cho tổng mực theo hàng biến thiên nhiều nhất."""
    g = np.asarray(im.convert('L').resize((im.width // 4, im.height // 4)), dtype=np.float32)
    chu = Image.fromarray(((g < g.mean() - 40) * 255).astype(np.uint8))
    tot = max(np.arange(-3, 3.01, 0.1), key=lambda a: np.asarray(
        chu.rotate(a, resample=Image.BILINEAR), dtype=np.float32).sum(axis=1).var())
    return round(float(tot), 1)


def trang(sach):
    """Ảnh gốc của trang sách (PDF đếm từ 0 nên trang sách S nằm ở d[S + 1]), đã xoay thẳng."""
    p = fitz.open(PDF)[sach + 1]
    im = Image.open(io.BytesIO(p.parent.extract_image(p.get_images(full=True)[0][0])['image'])).convert('RGB')
    a = nghieng(im)
    if abs(a) >= 0.2:
        nen = tuple(int(v) for v in np.median(np.asarray(im).reshape(-1, 3), axis=0))
        im = im.rotate(a, resample=Image.BICUBIC, fillcolor=nen)
    return im


def cat(ten, cache={}):
    sach, x0, y0, x1, y1, kieu, *xoa = HINH[ten]
    if sach not in cache:
        cache[sach] = np.asarray(trang(sach)).astype(np.float32)
    a = cache[sach]
    s = a.shape[1] / 480
    X0, Y0, X1, Y1 = round(x0 * s), round(y0 * s), round(x1 * s), round(y1 * s)
    # màu giấy = phân vị 80 của vòng giấy rộng 40 px quanh khung
    m = 40
    vong = np.concatenate([
        a[max(Y0 - m, 0):Y0, X0:X1].reshape(-1, 3), a[Y1:Y1 + m, X0:X1].reshape(-1, 3),
        a[Y0:Y1, max(X0 - m, 0):X0].reshape(-1, 3), a[Y0:Y1, X1:X1 + m].reshape(-1, 3)])
    giay = np.percentile(vong, 80, axis=0)
    c = a[Y0:Y1, X0:X1]
    trang_ = giay * (0.98 if kieu == 'p' else 0.90)
    den = np.percentile(c.reshape(-1, 3), 0.5, axis=0) * 0.85
    c = np.clip((c - den) / (trang_ - den), 0, 1) ** (1.05 if kieu == 'p' else 1.0)
    if kieu == 's':
        xam = (c.max(axis=2) - c.min(axis=2) < 0.12) & (c.mean(axis=2) > 0.55)
        c[xam] = 1.0
    for a0, b0, a1, b1 in (xoa[0] if xoa else []):
        c[max(round(b0 * s) - Y0, 0):round(b1 * s) - Y0, max(round(a0 * s) - X0, 0):round(a1 * s) - X0] = 1.0
    im = Image.fromarray((c * 255 + 0.5).astype(np.uint8))
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if im.width > 1000:
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
    ra = os.path.join(HERE, 'hinh', ten + '.jpg')
    im.save(ra, 'JPEG', quality=90, optimize=True)
    print('  %s.jpg  %dx%d  %d KB' % (ten, im.width, im.height, os.path.getsize(ra) // 1024))


def luoi(sach, x0, y0, x1, y1, ra=None):
    im = trang(sach)
    s = im.width / 480
    k = 2  # 2 px ảnh cho mỗi đơn vị toạ độ
    c = im.crop((round(x0 * s), round(y0 * s), round(x1 * s), round(y1 * s)))
    c = c.resize(((x1 - x0) * k, (y1 - y0) * k), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    for v in range((x0 // 10 + 1) * 10, x1, 10):
        d.line([((v - x0) * k, 0), ((v - x0) * k, c.height)], fill=(255, 0, 0) if v % 50 == 0 else (0, 200, 255))
        if v % 50 == 0:
            d.text(((v - x0) * k + 2, 2), str(v), fill=(255, 0, 0))
    for v in range((y0 // 10 + 1) * 10, y1, 10):
        d.line([(0, (v - y0) * k), (c.width, (v - y0) * k)], fill=(255, 0, 0) if v % 50 == 0 else (0, 200, 255))
        if v % 50 == 0:
            d.text((2, (v - y0) * k + 2), str(v), fill=(255, 0, 0))
    ra = ra or os.path.join(tempfile.gettempdir(), 'luoi_tr%d.png' % sach)
    c.save(ra)
    print('  lưới:', ra)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    if arg[:1] == ['--luoi']:
        luoi(*map(int, arg[1:6]), *arg[6:7])
    else:
        for ten in arg or HINH:
            cat(ten)
