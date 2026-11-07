# SRH CH SGK – hướng dẫn cho Claude

Thư mục này chuẩn hoá kiến thức **Sâu Răng Học** (giáo trình Trường ĐH Y Dược Cần Thơ, ngành Răng Hàm Mặt) cho một sinh viên RHM K49. Mỗi bài SGK làm thành **1 file `.html`** để học offline, đồng thời đưa lên trang web https://hungarara.github.io/SRH-CH-SGK/ (GitHub Pages). Nội dung được viết trong `nguon/Bài N.md`, rồi dựng thành `.html` bằng `nguon/build.py` (script dựng luôn trang chủ `index.html`).

## Lệnh tắt

- **`soạn bài N srh`** (ví dụ `soạn bài 2 srh`): soạn Bài N đúng theo `QUY TRÌNH CHUẨN HOÁ.md`. Đọc file đó trước rồi làm theo các bước ở mục 5. **Không hỏi lại** định dạng hay hướng làm, vì người dùng đã chốt. Làm xong thì **tự commit + push** lên `main`, không hỏi trước (xem mục Trạng thái).

## Người dùng muốn gì

- Môn Sâu Răng Học RHM thi **trắc nghiệm trên máy, khả năng cao là đề mới**. Vì vậy **ưu tiên số 1 là kiến thức để hiểu**: giải thích bằng lời thường, có "vì sao" (cơ chế), ví dụ đời thường và sơ đồ. Mục đích vừa để thi, vừa để làm nghề sau này.
- Trắc nghiệm chỉ là phần phụ để tự kiểm tra (30–50 câu/bài), **không phải đề dự đoán**. Riêng **Bài 7, 8** (GIC, composite) người dùng xem là hai bài cần học kỹ nên muốn **nhiều câu hơn** (ngày 07/11/2026). Không bám theo đề các khoá, không ghi "khoá Kxx đã ra".
- Câu trắc nghiệm viết **như đề thi thật**: đề và lựa chọn không ghi "Theo SGK", "theo Hình…", "(mục…)" (người dùng góp ý ngày 28/10/2026). Nguồn chỉ để ở nhãn câu và phần giải thích.
- **Hình**: đưa vào **mọi hình SGK thật sự giúp hiểu**, nhưng không lấy hình chỉ để cho đủ. Chỗ SGK có hình thì **ưu tiên hình** (hình SGK hoặc sơ đồ vẽ), không thay bằng bảng, flow hay biểu đồ mô phỏng (người dùng góp ý ngày 28/10/2026). Cách làm: `QUY TRÌNH CHUẨN HOÁ.md` mục 5 bước 4.
- Người dùng học tốt, chỉ cần nhớ ý là đọc đề sẽ chọn được, nên không cần thuộc nguyên văn. Nhưng **chữ và con số phải đúng SGK**. Đừng tóm tắt quá cụt.
- Người dùng học **ít nhất 8 tiếng/ngày**, nên thời gian không phải giới hạn: đừng cắt bớt ý cho vừa giờ. Con số "~90 phút" ghi trong bài chỉ là thời gian đọc hết bài một lượt. Dự định ban đầu là học 1 bài/ngày.
- Chỉ hỏi khi thật cần, còn lại tự chọn hướng tốt nhất. Tiết kiệm token. Trả lời bằng tiếng Việt.
- Khi SGK khác khuyến cáo hiện đại (ICCC, AAE, AAPD, WHO…): **ghi cả hai** trong hộp ⚖️ "Hai cách hiểu" và không tự chọn. Nhưng khi cần **một** đáp án duy nhất (đáp án trắc nghiệm) thì **chọn theo SGK**.

## Nguồn (nằm ngoài thư mục này)

Gốc: `C:/Users/1/Desktop/Local HỌC TẬP Y KHOA VÀ FILE/` (kho học tập cũ, repo `HungARARA/quiz`).

- `Sâu Răng Học/Giáo Trình Sâu Răng Học Bản Chụp Tay Scan.pdf`: SGK cả cuốn, 200 trang.
  - **Trang PDF = trang sách + 2.**
  - Lớp chữ OCR **mất hết dấu**, chỉ dùng để dò trang: tìm bằng regex, coi mỗi chữ có dấu là một ký tự bất kỳ.
  - Muốn đọc chữ thật thì xuất trang ra PNG bằng fitz rồi xem ảnh.
  - Đáp án câu hỏi lượng giá của mọi bài nằm ở **sách tr. 198**.
- `Sâu Răng Học/Bài N.pdf` (riêng Bài 2: `Sâu Răng Học/bài 2/Bài 2.pdf`): ảnh chụp từng bài, không có chữ. Bài 2.pdf có 16 trang: trang k = sách tr. 15 + k (trang 1 là câu lượng giá của Bài 1).
- `Sâu Răng Học/Bài 1/Bài 1 SGK.docx`: chỉ Bài 1 có bản chữ, gồm 8 hình theo thứ tự Hình 1.1 → 1.8.
- `Đề thi Sâu Răng Học RHM/nguon/RHM K40…K48.txt`: đề các khoá trước.
  - Dấu `*` đánh dấu đáp án. Chỉ K48 có đáp án chính thức, các khoá khác là bài khoanh của sinh viên.
  - Chỉ xem để biết đề hỏi sâu tới đâu.
- `SRH Tình Huống RHM Thi.docx`: công thức làm câu lâm sàng, đã làm riêng.

Nếu các đường dẫn trên bị đổi thì tìm trên Desktop theo tên file.

## Công cụ

- Python: `C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe -I` (có `fitz`/PyMuPDF, `PIL`, `python-docx`). Lệnh `python` trên PATH là bản giả của Microsoft Store, không dùng được. Máy không có tesseract.
- Dựng trang (chạy trong thư mục này): `"C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I nguon/build.py "Bài N.md"`. Script in ra số câu, phân bố đáp án A/B/C/D, link hỏng và hình thiếu.
- Cắt hình SGK: `nguon/cat_hinh.py` (khai khung cắt trong `HINH`; `--luoi` để dò khung). Script tự xoay thẳng trang ảnh chụp, làm trắng nền, lưu `nguon/hinh/<tên>.jpg`.
- Cú pháp Markdown mở rộng mà `build.py` hiểu được: xem `QUY TRÌNH CHUẨN HOÁ.md` mục 9. In nghiêng chỉ dùng `*…*`; `_…_` không được hiểu.

## Trạng thái (07/11/2026)

- **Bài 1 xong**, có 25 hộp 🔍 "Vì sao…?". Có 66 câu vì đây là bản đầu, làm trước khi quy trình giảm xuống 30–50 câu. Đề trắc nghiệm đã viết lại theo kiểu đề thi thật.
- **Bài 2 xong**: 50 câu, 34 hộp 🔍. Có 9 hình cắt từ SGK (2.3, 2.4, 2.5, 2.6, 2.8, 2.9A–C, 2.10). Hình 2.1, 2.2, 2.7b, 2.11 thì vẽ lại bằng SVG, vì ảnh SGK mờ hoặc khó đọc. Nội dung đã rà lại với SGK ngày 28/10/2026.
- **Bài 3 xong**: 50 câu, 48 hộp 🔍, 8 hộp ⚖️. Có 6 hình cắt từ SGK (3.1–3.6). Hình 3.7 (hai phim cánh cắn) quá mờ nên vẽ lại bằng SVG cơ chế góc chiếu. Bốn câu lượng giá Bài 3 hỏi cả ý nằm ở Bài 4 (tr. 59–63: FOTI, DIAGNOdent, QLF, ECM, trám kiểm soát); bài đã dẫn sang các trang đó.
- **Bài 4 xong**: 71 câu (bài dài nhất, chia 2 ngày học), 63 hộp 🔍, 10 hộp ⚖️. Có 13 hình cắt từ SGK (4.2–4.4, 4.6–4.12, 4.18, 4.22, 4.23). Hình 4.1 (cân bằng sâu răng) chữ quá nhỏ nên vẽ lại SVG; Hình 4.24–4.25 thay bằng SVG cơ chế trám bít hố rãnh; thêm SVG thang nồng độ fluor (log). Bỏ ảnh máy (4.13–4.15), ảnh hiển vi mờ (4.5), ảnh đen trắng mờ (4.16, 4.17, 4.19–4.21). Đã thêm dẫn chiếu sang Bài 4 ở Bài 1 (súc fluor 0,05/0,2%, chlorhexidine, xylitol, thứ tự điều trị) và Bài 3 (IgA).
- **Bài 5 xong**: 49 câu (có đủ 12 câu lượng giá), 33 hộp 🔍, 11 hộp ⚖️. Có 9 hình cắt từ SGK (5.1, 5.3, 5.4, Bảng 5.1, 5.5, 5.11, 5.12, Bảng 5.2, 5.14). Hình 5.13 (tảng băng Pitts) chữ nhỏ nên vẽ lại SVG; thêm SVG 4 mức độ sâu. Bỏ Hình 5.2 (ảnh mô học màu lệch, khó đọc) và Hình 5.6–5.10 (trùng Bảng 5.1). Đáp án tr. 198 của bốn câu lượng giá (2, 6, 10, 11) không khớp hẳn phần chữ SGK; mỗi câu có hộp riêng: gặp đúng câu lượng giá thì chọn theo đáp án sách, câu khác chọn theo chữ SGK. Các chỗ Bài 5 khác Bài 3 (Black, sâu ngà 2–4 mm, 5 vùng sâu ngà, thứ phát/tái phát, nhóm tuổi) đều có hộp ⚖️.
- **Bài 6 xong**: 49 câu (có đủ 4 câu lượng giá), 27 hộp 🔍, 4 hộp ⚖️. Không cắt hình SGK: Hình 6.1 là ảnh lát cắt răng không nhãn, mờ, dính chữ in thấm nên vẽ lại SVG có nhãn (kèm ba loại ngà); thêm 3 SVG: thuyết thủy động học, độ sâu xoang và mật độ ống ngà, trụ men và thành xoang. Đáp án tr. 198 của câu lượng giá 2 (A) ngược chữ SGK (theo chữ thì câu sai là B, lớp mùn ngà): có hộp 📌 riêng. Đã ghi "thuyết thủy động học, SGK Bài 6 tr. 110" vào Bài 1, 2, 3, 5; Bài 2 thêm dòng so tỉ lệ khoáng (trọng lượng khô ↔ tính cả nước).
- **Bài 7 xong**: 115 câu (bản đầu 50 câu; ngày 07/11/2026 thêm 65 câu, có Phần K tổng hợp, tình huống; có đủ 3 câu lượng giá; đáp án tr. 198 khớp chữ SGK), 46 hộp 🔍, 5 hộp ⚖️. Có 4 hình cắt từ SGK: sơ đồ phản ứng đông cứng tr. 116 (SGK không đánh số), Hình 7.1–7.3. Thêm 2 SVG: xoang amalgam (Black) ↔ xoang GIC (mục 4); đường hầm và lối vào từ mặt bên (mục 5.2). Hình 7.3 B in nhãn "Glass ionomer" phía trên lớp composite: chú thích đã nói rõ lớp nào là GIC. Đã thêm dẫn chiếu sang Bài 7 ở Bài 1 (GIC lót nền), Bài 3 (hộp ⚖️ trám kiểm soát: GIC IX trám tạm khoảng 4 tháng) và Bài 6 (GIC không tạo hình thể lưu; thổi khô quá thì GIC liên kết yếu).
- **Bài 8 xong**: 237 câu (bản đầu 70 câu; ngày 07/11/2026 thêm 167 câu, có Phần J tổng hợp, tình huống; bài dài thứ hai, chia 2 ngày: mục 0–3 và 4–6, trắc nghiệm Phần A–E và F–J), 55 hộp 🔍, 6 hộp ⚖️. Có 17 hình cắt từ SGK (8.1–8.7, 8.9, 8.11–8.19); bỏ Hình 8.8 (ảnh hiển vi mờ) và 8.10 (nhãn chồng chéo, trùng ý 8.7); chép Bảng 8.1–8.4 thành bảng chữ (ảnh nghiêng). Thêm 4 SVG: góc tiếp xúc, dán men (đuôi lớn – vi nối), trám từng lớp và chiếu đèn nhiều hướng, hệ số giãn nở nhiệt. Đáp án tr. 198: 1D · 2A · 3B · 4D; câu 1 (vừa cơ học vừa hóa học) và câu 3 (chọn màu "sau khi đánh bóng và làm sạch") không khớp hẳn chữ SGK: có hộp 📌. SGK Bài 8 có lỗi in: "pm" là µm (tr. 138–142); tr. 135 "độ nhớt sẽ giảm" bị dịch ngược (tr. 137, 140 ghi đúng); Hình 8.19 xếp hạng C vào cả GIC lẫn Ca(OH)₂: đều có hộp riêng. Đã cập nhật dẫn chiếu sang Bài 8 ở Bài 6 (composite: vi lưu cơ học, bảo tồn tối đa) và Bài 7 (acid phosphoric 35–37%, liên kết ngà kém bền, lót GIC dưới composite).
- **Bài 9 xong**: 50 câu (có đủ 4 câu lượng giá), 35 hộp 🔍, 11 hộp ⚖️. Có 7 hình cắt từ SGK (9.1–9.7); Bảng 9.1 chép thành bảng chữ. Thêm 9 SVG: gián tiếp ↔ trực tiếp, giữ tủy sống và đóng chóp, sáu vùng và việc phải làm, xoang sau khi nạo, bốn bước tạo cầu ngà, ngà phản ứng ↔ cầu ngà, nội tiêu ↔ ngoại tiêu, lộ ở sừng tủy ↔ cổ răng, các mức giữ tủy. Đáp án tr. 198: 1B · 2A · 3C · 4C; mỗi câu có hộp 📌, trong đó câu 1, 3, 4 dễ phân vân với phần chữ SGK. Chỗ SGK khác hướng dẫn hiện nay dẫn theo EFCD-ESE-ORCA 2026 và Cushley 2021. Biodentine *(ngoài SGK)* có hộp riêng vì đề cương ôn tập của người dùng có hỏi, nhưng không dùng làm đáp án trắc nghiệm. Đã thêm dẫn chiếu sang Bài 9 ở Bài 1, 2, 3, 4, 5, 7, 8; Bài 3, 5 có thêm ý sáu vùng sâu ngà đánh số từ ngoài vào.
- **Ghi chú cho bài sau**: Bài 7, Bài 8 đã nói trước vài ý của Bài 10, soạn tới thì dẫn ngược: xoang V, cổ răng: GIC hợp hơn composite, Fuji II LC: Bài 7 mục 2.2, 5.3; composite hạt độn nhỏ đàn hồi thấp hợp xoang V, cổ răng chịu uốn: Bài 8 mục 4 Hình 8.12, mục 5. Chữ "**xoi mòn**" ở Bài 8 là **acid etching** (bước trám), còn ở Bài 10 là **mòn răng do acid** (erosion): khi soạn Bài 10 nhớ có hộp phân biệt. `cat_hinh.py` có phần tử thứ 8 "vùng xoá xám" (QUY TRÌNH mục 5 bước 4). Trong SVG, đặt lớp chữ (`s`, `m`…) lên **từng thẻ `text`**: CSS đặt cỡ chữ, màu thẳng lên `text` nên lớp đặt trên `<g>` không có tác dụng với chữ. Xem trang bằng máy chủ `srh-web` trong `.claude/launch.json` (preview_start). Khung trình duyệt bị ẩn vẫn chụp được, nhưng hình nhúng chưa tải (lazy) và ảnh chụp có lúc là ảnh cũ: kiểm tra bằng JS (`img.decode()`, `getBBox()` của chữ SVG) rồi chụp lại. Nếu vẫn không chụp được (ảnh ra màu nền trơn) thì chạy `nguon/soat_svg.py "Bài N.md" <thư mục>`: script đổi class sang thuộc tính màu rồi dựng từng sơ đồ thành PNG bằng fitz để xem (không có đầu mũi tên). Trang có chế độ tối: đừng ép màu chữ tối lên nền `.pu`, `.de`, và soát sơ đồ ở cả sáng lẫn tối.
- **Bài 10 chưa làm.** Trang sách của từng bài có trong `QUY TRÌNH CHUẨN HOÁ.md` mục 4.
- **Trang web** ở link trên: chỉ cần push lên GitHub (repo `HungARARA/SRH-CH-SGK`, nhánh `main`) là trang tự cập nhật. Soạn xong bài nào (hay sửa xong bài nào) thì **tự commit thẳng vào `main` rồi push**, không hỏi trước (người dùng chốt ngày 29/10/2026). Chỉ dừng lại hỏi khi có vấn đề: script dựng báo lỗi, push bị từ chối, xung đột với bản trên GitHub, hay trang web không cập nhật.
