# SRH CH SGK – hướng dẫn cho Claude

Thư mục này chuẩn hoá kiến thức **Sâu Răng Học** (giáo trình Trường ĐH Y Dược Cần Thơ, ngành Răng Hàm Mặt) cho một sinh viên RHM K49. Mỗi bài SGK làm thành **1 file `.html`** để học offline, đồng thời đưa lên trang web https://hungarara.github.io/SRH-CH-SGK/ (GitHub Pages). Nội dung được viết trong `nguon/Bài N.md`, rồi dựng thành `.html` bằng `nguon/build.py` (script dựng luôn trang chủ `index.html`).

## Lệnh tắt

- **`soạn bài N srh`** (ví dụ `soạn bài 2 srh`): soạn Bài N đúng theo `QUY TRÌNH CHUẨN HOÁ.md`. Đọc file đó trước rồi làm theo các bước ở mục 5. **Không hỏi lại** định dạng hay hướng làm, vì người dùng đã chốt.

## Người dùng muốn gì

- Môn Sâu Răng Học RHM thi **trắc nghiệm trên máy, khả năng cao là đề mới**. Vì vậy **ưu tiên số 1 là kiến thức để hiểu**: giải thích bằng lời thường, có "vì sao" (cơ chế), ví dụ đời thường và sơ đồ. Mục đích vừa để thi, vừa để làm nghề sau này.
- Trắc nghiệm chỉ là phần phụ để tự kiểm tra (30–50 câu/bài), **không phải đề dự đoán**. Không bám theo đề các khoá, không ghi "khoá Kxx đã ra".
- Người dùng học tốt, chỉ cần nhớ ý là đọc đề sẽ chọn được, nên không cần thuộc nguyên văn. Nhưng **chữ và con số phải đúng SGK**. Đừng tóm tắt quá cụt.
- Nhịp học 1 bài/ngày. Chỉ hỏi khi thật cần, còn lại tự chọn hướng tốt nhất. Tiết kiệm token. Trả lời bằng tiếng Việt.
- Khi SGK khác khuyến cáo hiện đại (ICCC, AAE, AAPD, WHO…): **ghi cả hai** trong hộp ⚖️ "Hai cách hiểu" và không tự chọn. Nhưng khi cần **một** đáp án duy nhất (đáp án trắc nghiệm) thì **chọn theo SGK**.

## Nguồn (nằm ngoài thư mục này)

Gốc: `C:/Users/1/Desktop/Local HỌC TẬP Y KHOA VÀ FILE/` (kho học tập cũ, repo `HungARARA/quiz`).

- `Sâu Răng Học/Giáo Trình Sâu Răng Học Bản Chụp Tay Scan.pdf`: SGK cả cuốn, 200 trang.
  - **Trang PDF = trang sách + 2.**
  - Lớp chữ OCR **mất hết dấu**, chỉ dùng để dò trang: tìm bằng regex, coi mỗi chữ có dấu là một ký tự bất kỳ.
  - Muốn đọc chữ thật thì xuất trang ra PNG bằng fitz rồi xem ảnh.
  - Đáp án câu hỏi lượng giá của mọi bài nằm ở **sách tr. 198**.
- `Sâu Răng Học/Bài N.pdf` (riêng Bài 2: `Sâu Răng Học/bài 2/Bài 2.pdf`): ảnh chụp từng bài, không có chữ.
- `Sâu Răng Học/Bài 1/Bài 1 SGK.docx`: chỉ Bài 1 có bản chữ, gồm 8 hình theo thứ tự Hình 1.1 → 1.8.
- `Đề thi Sâu Răng Học RHM/nguon/RHM K40…K48.txt`: đề các khoá trước.
  - Dấu `*` đánh dấu đáp án. Chỉ K48 có đáp án chính thức, các khoá khác là bài khoanh của sinh viên.
  - Chỉ xem để biết đề hỏi sâu tới đâu.
- `SRH Tình Huống RHM Thi.docx`: công thức làm câu lâm sàng, đã làm riêng.

Nếu các đường dẫn trên bị đổi thì tìm trên Desktop theo tên file.

## Công cụ

- Python: `C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe -I` (có `fitz`/PyMuPDF, `PIL`, `python-docx`). Lệnh `python` trên PATH là bản giả của Microsoft Store, không dùng được. Máy không có tesseract.
- Dựng trang (chạy trong thư mục này): `"C:/Users/1/AppData/Local/Programs/Python/Python313/python.exe" -I nguon/build.py "Bài N.md"`. Script in ra số câu, phân bố đáp án A/B/C/D, link hỏng và hình thiếu.
- Cú pháp Markdown mở rộng mà `build.py` hiểu được: xem `QUY TRÌNH CHUẨN HOÁ.md` mục 9.

## Trạng thái (28/10/2026)

- **Bài 1 xong**, có 25 hộp 🔍 "Vì sao…?". Có 66 câu vì đây là bản đầu, làm trước khi quy trình giảm xuống 30–50 câu.
- **Bài 2–10 chưa làm.** Trang sách của từng bài có trong `QUY TRÌNH CHUẨN HOÁ.md` mục 4.
- **Trang web chưa chạy:** `index.html` và `.nojekyll` đã có trên `main`, nhưng **GitHub Pages chưa bật**. Bật Pages là tạo trang công khai nên cần người dùng đồng ý. Nếu tài khoản GitHub là gói miễn phí thì repo cũng phải chuyển sang công khai. Bật xong thì link ở trên mới mở được.
- **Git:** repo `HungARARA/SRH-CH-SGK`, nhánh `main`. Soạn xong bài nào thì hỏi người dùng có muốn commit + push không. Push xong thì trang web tự cập nhật từ nhánh `main` (thư mục gốc).
