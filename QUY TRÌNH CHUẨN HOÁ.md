# QUY TRÌNH CHUẨN HOÁ KIẾN THỨC SÂU RĂNG HỌC (SGK)

> Đây là "công thức" để làm Bài 1 → Bài 10 giống hệt nhau.
> **Mở phiên mới chỉ cần gõ: `soạn bài N srh`** (ví dụ `soạn bài 2 srh`, trong phiên mở ở thư mục `SRH CH SGK`) → Claude đọc file này rồi làm đúng các bước ở mục 5, không cần giải thích lại.

## 1. Hướng đã chọn và vì sao

- Sâu Răng Học RHM thi **trên máy, khả năng cao là đề mới** → không học tủ theo đề các khoá. Phải **phủ hết ý trong SGK** và **hiểu** để đọc đề là tự suy ra đáp án.
- **Ưu tiên số 1 là phần kiến thức để hiểu** (dồn khoảng 80% công sức vào đây): giải thích được **vì sao** (cơ chế, nối các ý với nhau), vừa để thi vừa để làm nghề sau này. Trắc nghiệm chỉ là công cụ tự kiểm tra, **không phải đề dự đoán**, vì chưa chắc câu nào sẽ ra trong đề máy.
- Hướng làm: **Hiểu → Nhớ → Tự kiểm tra**. Không tóm tắt cụt, cũng không chép lại nguyên sách.
  1. **Hiểu**: mỗi mục SGK có hộp 💡 *Hiểu nhanh* bằng lời thường, ví dụ đời thường, sơ đồ, và các hộp 🔍 *Vì sao…?* giải thích cơ chế đằng sau ý của sách.
  2. **Nhớ**: phần **📖 SGK ghi** giữ **đủ ý, đúng chữ SGK** (đề máy hay lấy nguyên câu sách rồi đổi một chữ); từ khoá và con số được ==tô vàng==; có 🧠 mẹo nhớ, bảng con số, bảng cặp dễ nhầm.
  3. **Tự kiểm tra**: nút **"Che từ khoá"** (che chữ tô vàng để tự nhớ lại) và **trắc nghiệm bấm được** ở cuối bài (biết đúng/sai ngay, có giải thích, có đường dẫn về đúng mục SGK).
- Mỗi bài học khoảng 75–90 phút, vừa nhịp **1 bài/ngày**.

## 2. Định dạng đầu ra và vì sao chọn HTML

- Mỗi bài = **1 file `.html` tự chứa**: hình, sơ đồ, trắc nghiệm nằm sẵn trong file. Mở bằng trình duyệt trên máy tính hoặc điện thoại (gửi file qua Zalo rồi mở), **không cần mạng**.
- **Trang web** (GitHub Pages, nhánh `main`, thư mục gốc): https://hungarara.github.io/SRH-CH-SGK/. Trang chủ `index.html` liệt kê đủ 10 bài; push lên `main` thì web tự cập nhật sau khoảng 1 phút.
- Muốn bản PDF: mở file → Ctrl+P → "Lưu dưới dạng PDF" (bản in tự hiện đáp án và giải thích).
- Nội dung viết bằng **Markdown** (`nguon/Bài N.md`), dựng bằng **một script chung** (`nguon/build.py`). Mỗi bài chỉ tốn công viết nội dung, không phải viết lại giao diện, nên **tốn ít token nhất**. Làm Word/PDF thì phải vẽ hình riêng, tốn hơn nhiều, và không làm được trắc nghiệm bấm.

## 3. Thư mục

```
Desktop/RHM 49/Kì 1 2026/SRH CH SGK/   (repo GitHub HungARARA/SRH-CH-SGK)
├── CLAUDE.md                      ← hướng dẫn cho Claude: lệnh tắt, sở thích, nguồn
├── QUY TRÌNH CHUẨN HOÁ.md        ← file này
├── index.html                     ← trang chủ web (build.py tự dựng lại, đừng sửa tay)
├── .nojekyll                      ← để GitHub Pages đưa file lên nguyên trạng
├── Bài N - <tên bài>.html         ← FILE ĐỂ HỌC (mở file này)
└── nguon/
    ├── build.py                   ← script dựng .md → .html (dùng chung mọi bài)
    ├── Bài N.md                   ← nội dung; sửa ở đây rồi dựng lại
    └── hinh/bN-h<số hình>.png     ← hình cắt từ SGK (có trong repo; được nhúng sẵn vào .html)
```

## 4. Nguồn tài liệu

Tài liệu gốc nằm **ngoài** thư mục này, trong kho học tập `C:/Users/1/Desktop/Local HỌC TẬP Y KHOA VÀ FILE/`; đường dẫn trong bảng tính từ đó (nếu bị đổi chỗ thì tìm trên Desktop theo tên file).

| Nguồn | Đường dẫn | Ghi chú |
|---|---|---|
| SGK bản chụp cả cuốn | `Sâu Răng Học/Giáo Trình Sâu Răng Học Bản Chụp Tay Scan.pdf` | Lớp chữ OCR **mất dấu**, chỉ dùng để dò trang. **Trang PDF = trang sách + 2.** Đọc chữ thật bằng cách xuất trang ra ảnh (fitz) rồi xem ảnh. |
| SGK từng bài | `Sâu Răng Học/Bài N.pdf` (Bài 2: `Sâu Răng Học/bài 2/Bài 2.pdf`) | ảnh chụp, không có chữ |
| Bài 1 dạng chữ | `Sâu Răng Học/Bài 1/Bài 1 SGK.docx` | chỉ Bài 1 có; 8 hình trong file theo đúng thứ tự Hình 1.1 → 1.8 |
| Câu hỏi lượng giá | trang cuối mỗi bài trong SGK | **đáp án ở SGK tr. 198** (PDF tr. 200) |
| Đề cũ RHM K40–K48 | `Đề thi Sâu Răng Học RHM/nguon/*.txt` | **chỉ xem để biết đề hỏi sâu tới đâu**, không bám theo khoá |
| Câu lâm sàng | `SRH Tình Huống RHM Thi.docx` | công thức làm câu tình huống (đã làm riêng) |

**Bảng bài** (trang sách):

| Bài | Tên | Trang | Trạng thái |
|---|---|---|---|
| 1 | Quan niệm mới trong chẩn đoán và điều trị bệnh sâu răng | 1–16 | ✅ xong (66 câu, 25 hộp 🔍) |
| 2 | Quá trình mất khoáng và tái khoáng mô cứng | 17–31 | ⏳ |
| 3 | Chẩn đoán bệnh sâu răng | 32–47 | ⏳ |
| 4 | Điều trị và phòng ngừa bệnh sâu răng | 48–92 | ⏳ (dài, nên chia 2 ngày) |
| 5 | Phân loại xoang sâu răng | 94–108 | ⏳ |
| 6 | Các yếu tố sinh học trong sửa soạn xoang | 109–113 | ⏳ |
| 7 | Nguyên tắc tạo xoang và trám bằng xi măng glass ionomer (GIC) | 114–122 | ⏳ |
| 8 | Nguyên tắc tạo xoang và trám bằng vật liệu composite | 123–170 | ⏳ (dài, nên chia 2 ngày) |
| 9 | Che tủy | 171–187 | ⏳ |
| 10 | Mòn răng | 188–197 | ⏳ |

## 5. Các bước làm một bài

1. **Đọc hết SGK bài N**: xuất từng trang ra ảnh và đọc, kể cả chú thích hình, bảng, câu lượng giá cuối bài.
   ```bash
   "C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I -c "import fitz; d=fitz.open(r'C:/Users/1/Desktop/Local HỌC TẬP Y KHOA VÀ FILE/Sâu Răng Học/Giáo Trình Sâu Răng Học Bản Chụp Tay Scan.pdf'); p=d[TRANG_SACH+1]; p.get_pixmap(matrix=fitz.Matrix(1000/p.rect.width,1000/p.rect.width)).save('trang.png')"
   ```
   (`d[...]` đếm từ 0, nên trang sách S nằm ở `d[S+1]`.)
2. **Lập danh sách "ý thi được"**: mọi định nghĩa, con số, danh sách (đếm đủ số ý), so sánh, cơ chế, chỉ định – chống chỉ định, thứ tự các bước, chú thích hình. Mỗi ý phải có trong bài viết **và** có ít nhất 1 câu trắc nghiệm.
3. **Xem nhanh đề cũ** (tìm theo từ khoá trong `Đề thi Sâu Răng Học RHM/nguon/`) chỉ để biết độ sâu câu hỏi. **Không** ghi "khoá nào đã ra" vào bài.
4. **Cắt hình SGK** cần dùng vào `nguon/hinh/` (ảnh lâm sàng, hình minh hoạ kỹ thuật). Sơ đồ khái niệm thì tự vẽ (SVG) cho rõ hơn ảnh chụp sách.
5. **Viết `nguon/Bài N.md`** theo khung ở mục 6 và quy tắc ở mục 7–8.
6. **Dựng file** (chạy trong thư mục `SRH CH SGK`):
   ```bash
   "C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I nguon/build.py "Bài N.md"
   ```
   Script in ra: dung lượng, số câu, phân bố đáp án A/B/C/D, link hỏng, hình thiếu, câu thiếu/thừa đáp án.
7. **Kiểm tra** theo mục 10, rồi cập nhật cột "Trạng thái" ở bảng bài (mục 4).
8. **Hỏi người dùng** có commit + push không. Push lên `main` thì trang web tự cập nhật.

## 6. Khung chuẩn của mỗi bài (giữ đúng thứ tự)

| # | Phần | Nội dung |
|---|---|---|
| 0 | Đầu bài | hộp 📌 "Cách học bài này (4 bước)" + **Mục tiêu SGK** (đề bám mục tiêu) |
| 1 | Bức tranh 1 phút | 5–7 câu kể cả bài như một câu chuyện + sơ đồ dòng chảy; nếu hợp thì thêm bảng so sánh lớn của bài |
| 2 | Từng mục SGK | **giữ đúng số mục SGK** (1.1, 1.2.1…) và ghi trang để mở sách đối chiếu. Mỗi mục theo thứ tự: 💡 Hiểu nhanh (lời thường + ví dụ đời thường) → 📖 SGK ghi (đủ ý, đúng chữ, từ khoá ==tô vàng==) → 🔍 Vì sao…? (cơ chế đằng sau các ý vừa đọc, mục 7) → sơ đồ/hình nếu giúp hiểu → 🧠 Mẹo nhớ → ⚠️ Đề hay gài → ⚖️ Hai cách hiểu (chỉ khi SGK khác khuyến cáo hiện nay) |
| 3 | Bảng con số phải thuộc | mọi con số trong bài: con số (tô vàng) – nghĩa – mục |
| 4 | Cặp dễ nhầm | các cặp đề hay tráo cho nhau |
| 5 | Trắc nghiệm tự kiểm tra | chia nhóm theo mục SGK (Phần A, B, C…) |
| 6 | Ôn 5 phút trước khi thi | 12–20 câu chốt có tô vàng, để đọc ở chế độ "Che từ khoá" |

## 7. Quy tắc viết

- Giọng **cầm tay chỉ việc**: câu ngắn, nói như giảng cho bạn cùng lớp. Thuật ngữ khó giải nghĩa ngay lần đầu gặp (ví dụ: *mất khoáng = acid rút calcium, phosphate ra khỏi men*).
- Mỗi khái niệm trừu tượng đi kèm một ví dụ đời thường (quả táo dập, bức tường gạch, căn phòng kín…).
- **Không bịa.** Ý nào không có trong SGK thì ghi rõ *(ngoài SGK)*. Con số giữ đúng SGK, kể cả khi khác tài liệu khác; khi đó dùng hộp ⚖️ *Hai cách hiểu*: bảng SGK ↔ hiện nay, ghi rõ **"Thi chọn SGK"** và chữ nào trong đề cho biết người ra đề theo hướng nào.
- Hộp 🔍 **Vì sao…?**: tiêu đề chính là câu hỏi "vì sao" gắn với một ý SGK (con số, danh sách, chỉ định, bẫy đề). Trả lời bằng cơ chế + hình ảnh đời thường, 2–6 dòng. Ý nào quan trọng mà có cơ chế để giải thích thì có một hộp (Bài 1 có 25 hộp). Không tô vàng trong hộp này vì đây không phải chữ để thuộc. Phần không có trong SGK ghi *(ngoài SGK)*; cơ chế lấy từ bài khác của SGK thì ghi bài và trang. Không dùng ý ngoài SGK làm đáp án trắc nghiệm.
- Không nhắc "khoá Kxx đã ra" trong bài (đề máy là đề mới).
- Tô vàng vừa đủ: chỉ những chữ mà nếu bị đổi thì câu thành sai (con số, tên vi khuẩn, chiều hướng, "không / chỉ / bắt buộc", tên các ý trong danh sách).

## 8. Quy tắc trắc nghiệm

- Trắc nghiệm là **phần phụ**, làm sau khi phần kiến thức đã xong và đủ. Mục đích: tự kiểm tra đã hiểu, đã nhớ từng ý chưa.
- 4 lựa chọn, 1 đáp án đúng. Mỗi mục SGK có ít nhất 1–2 câu; con số quan trọng có câu hỏi.
- Số câu: **30–50 câu/bài** (bài dài như Bài 4, Bài 8 tối đa khoảng 70). Bài 1 là bản đầu nên có 66 câu.
- Mức độ: ưu tiên câu kiểm tra **hiểu** – khoảng 40% **Nhớ** (đúng chữ SGK), 40% **Hiểu** (vì sao, so sánh), 20% **Vận dụng** (tình huống 2–3 dòng).
- Câu lượng giá cuối bài SGK đưa vào nguyên thứ tự lựa chọn gốc, nhãn `Lượng giá SGK câu n`, đáp án lấy theo SGK tr. 198.
- Lựa chọn sai lấy từ **cặp dễ nhầm**: tráo con số, tráo tên vi khuẩn, đảo chiều, đổi "cần" thành "đủ", lấy ý của nhóm khác (ví dụ yếu tố người lớn ↔ người trẻ). Các lựa chọn dài tương đương nhau. Có vài câu "chọn câu SAI" / "NGOẠI TRỪ".
- Đáp án đúng rải đều A/B/C/D (script in ra phân bố; lệch quá 3 câu thì đảo lại thứ tự lựa chọn).
- Giải thích 1–3 dòng: vì sao đúng + ý SGK liên quan. Không viết kiểu "A sai vì…" theo chữ cái.

## 9. Cú pháp nguồn (`build.py` hiểu được)

| Viết trong `.md` | Ra trong `.html` |
|---|---|
| đầu file `---` với `title:` `short:` `sgk:` `out:` `---` | tiêu đề trang, dòng phụ, tên file `.html` |
| `## 1. Tên mục`, `### 1.2. …`, `#### 1.2.1. …` | mục có id theo số mục: `1.2.1` → `#m1-2-1` (dùng để link) |
| `==từ khoá==` | tô vàng; bật "Che từ khoá" thì bị che, bấm để hiện |
| `**đậm**`, `*nghiêng*`, `[chữ](#m6-2)` | in đậm, in nghiêng, link về mục |
| `> [!NOTE]` / `[!TIP]` / `[!IMPORTANT]` / `[!WARNING]` / `[!CAUTION]` / `[!WHY]` | hộp 💡 Hiểu nhanh / 🧠 Mẹo nhớ / 📌 Lưu ý / ⚠️ Đề hay gài / ⚖️ Hai cách hiểu / 🔍 Vì sao. Chữ viết sau `]` thay cho tiêu đề mặc định (hộp 🔍 thì viết luôn câu hỏi, ví dụ `> [!WHY] Vì sao tủy viêm lại dễ chết?`). Nội dung hộp viết ở các dòng `>` tiếp theo (có thể có bảng, danh sách). |
| khối ` ```flow `: mỗi dòng `A -> B -> C`; ô bắt đầu bằng `!` = đỏ, `+` = xanh | sơ đồ ô – mũi tên, tự xuống dòng trên điện thoại |
| khối ` ```ph `: dòng `6-14` (giờ), mỗi dòng `Nhãn \| 7:00 12:00`, dòng `caption: …` | biểu đồ pH mảng bám theo giờ ăn, tự tính số phút dưới pH 5,5 |
| `<figure>` … `<svg class="dg" style="max-width:520px" viewBox="0 0 440 …">` … `</figure>` | sơ đồ vẽ tay. Rộng viewBox khoảng 440–450 để chữ đọc được trên điện thoại. Lớp màu có sẵn: `c1 c2 c3` (vòng tròn xanh dương / cam / xanh lá), `en de pu` (men / ngà / tủy), `inf aff le` (ngà nhiễm trùng / ngà bị ảnh hưởng / sang thương men), `k d ld rl` (nét thường / nét chấm / đường dẫn / vạch đỏ), chữ `b m r s big` (đậm / mờ / đỏ / nhỏ / to) |
| `![chú thích](hinh/bN-h1-2.png)` | hình nhúng thẳng vào `.html` (tự thu nhỏ, nén JPEG) |
| `## Trắc nghiệm …` rồi mỗi câu: `#### Nhớ · 1.2` + dòng đề + 4 dòng `- [ ]` / `- [x]` + dòng `> giải thích` | câu bấm được, tự đánh số, nhãn link về mục 1.2 |
| *(tự động)* | mỗi lần chạy, `build.py` dựng lại `index.html` (trang chủ web): đủ 10 bài, bài đã có `.html` thì có link và số câu. Tên và trang của 10 bài nằm ở danh sách `BAI` trong `build.py`. |

## 10. Kiểm tra trước khi giao

- [ ] Script không báo lỗi: link hỏng, hình thiếu, câu thiếu/thừa đáp án; phân bố A/B/C/D đều.
- [ ] Đối chiếu lại SGK: danh sách "ý thi được" ở bước 2 đều có mặt trong bài và trong trắc nghiệm.
- [ ] Mở `.html`: sơ đồ đọc được; bấm thử đáp án, "Che từ khoá", "Chỉ xem câu sai", "Làm lại"; xem ở bề ngang điện thoại (khoảng 375px) không vỡ khung.
- [ ] Mở `index.html`: bài mới đã có link. Sau khi push, mở trang web kiểm tra lại.
- [ ] Cập nhật bảng bài ở mục 4.

## 11. Cách dùng file mỗi ngày

- **Ngày học bài**: làm đúng 4 bước trong hộp 📌 ở đầu bài (khoảng 80–90 phút). Trên điện thoại thì mở trang web rồi chọn bài (cần mạng); không có mạng thì mở file `.html` đã tải về.
- **Sáng hôm sau** (10 phút): mở lại bài hôm trước → bật "Che từ khoá" → đọc phần **Ôn 5 phút** → làm lại các câu sai.
- **Cuối tuần**: mỗi bài làm lại toàn bộ trắc nghiệm một lượt (bấm "Làm lại").
