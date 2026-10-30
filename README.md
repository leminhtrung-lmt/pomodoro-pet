# 🍅 Pomodoro Pet (phiên bản 1.1)

Ứng dụng Pomodoro cho Windows có **thú cưng đồng hành**. Bạn tập trung làm việc, hết giờ thì một chú mèo, cún, cá hoặc chim **tự chạy nhảy trên màn hình**, phủ lên mọi cửa sổ (kể cả Word, Excel) để bạn nghỉ ngơi đúng giờ. Nhạc thư giãn chạy ở nền, và app tự so sánh với hôm qua để khen hoặc nhắc bạn.

Toàn bộ app nằm trong **một file duy nhất** (`pomodoro_pet.pyw`), không cần cài thư viện nào. Người dùng cuối chỉ cần nhận file `PomodoroPet.exe` rồi bấm đúp để chạy.

---

## ⬇ Tải về

**[Tải PomodoroPet.exe (bản mới nhất)](https://github.com/leminhtrung-lmt/pomodoro-pet/releases/latest/download/PomodoroPet.exe)**

Bấm đúp file vừa tải là chạy, không cần cài gì. Nếu Windows hiện "Windows protected your PC", bấm **More info → Run anyway**.

> Kho mã nguồn: [leminhtrung-lmt/pomodoro-pet](https://github.com/leminhtrung-lmt/pomodoro-pet).

---

## 1. Tính năng

| Nhóm | Chi tiết |
|---|---|
| **Hẹn giờ** | Tự đặt thời gian tập trung (1–120 phút) và nghỉ ngắn (1–30 phút) |
| **Thú cưng** | 4 bạn đồng hành: Mèo, Cún, Cá, Chim, có hoạt hình chớp mắt, vẫy đuôi, thè lưỡi, vỗ cánh... |
| **Màn hình nghỉ** | Lớp phủ mờ chặn thao tác xuống các cửa sổ bên dưới, trên mọi màn hình. Chỉ có thú cưng và một nút **Thoát** |
| **Thú cưng tự chạy nhảy** | Mèo và cún chạy qua lại, dừng nghỉ, thỉnh thoảng nhảy lên. Cá và chim bay lượn ngẫu nhiên. **Không phụ thuộc chuột**. Bấm vào thú cưng thì nó nhảy và bắn tim |
| **Nhạc nền** | Lo-fi, tiếng mưa, tiếng sóng biển (app tự tạo) hoặc file `.wav` của bạn, với 3 mức âm lượng. Phần chọn nhạc nằm trong thẻ Cài đặt |
| **Khen / nhắc nhở** | Sau mỗi phiên, so sánh với hôm qua rồi khen hoặc khuyên chú tâm hơn |
| **Thống kê** | Biểu đồ phút tập trung, đợt xao nhãng theo ngày và điểm theo phiên; xuất CSV mở bằng Excel |
| **Chế độ nghiêm** | Ẩn nút Thoát, bắt buộc nghỉ hết giờ |
| **Khay hệ thống** | Thu nhỏ thì app vào khay cạnh đồng hồ Windows, không chiếm taskbar |
| **Giao diện co giãn** | Kéo to nhỏ cửa sổ thoải mái, tự thích ứng độ phân giải màn hình |

---

## 2. Yêu cầu hệ thống

- Windows 10 hoặc Windows 11.
- Chạy từ file `.exe`: không cần cài thêm gì.
- Chạy từ mã nguồn `.pyw`: cần Python 3.9 trở lên (xem mục 7).

---

## 3. Hướng dẫn sử dụng

### Bắt đầu một phiên
1. Mở app, ở thẻ **Tập trung** bấm **Bắt đầu**.
2. Vòng tròn đếm ngược chạy dần. Trạng thái hiện bên dưới đồng hồ.
3. Hết giờ tập trung, app kêu một tiếng chuông và màn hình nghỉ hiện ra.
4. Hết giờ nghỉ, màn hình nghỉ tự biến mất, cửa sổ app nổi lên kèm lời khen hoặc nhắc nhở.

### Các nút ở thẻ Tập trung
- **Bắt đầu / Tạm dừng / Tiếp tục**: điều khiển đồng hồ. Thời gian tạm dừng không được tính là thời gian tập trung hay xao nhãng.
- **Đặt lại**: dừng và đưa đồng hồ về ban đầu.

### Thẻ Cài đặt
- **Thời gian**: bấm `−` và `+` để chỉnh (giữ chuột để tăng giảm nhanh).
- **Bạn đồng hành**: chọn Mèo, Cún, Cá hoặc Chim.
- **Nhạc khi nghỉ**: chọn Tắt, Lo-fi, Mưa, Sóng biển hoặc File .wav. Bấm vào để nghe thử khoảng 6 giây.
- **Âm lượng**: Nhỏ, Vừa, To.
- **Chế độ nghiêm**: Bật hoặc Tắt.
- **Tự đo xao nhãng**: bật/tắt phân tích cửa sổ đang dùng, thời gian không thao tác và tần suất chuyển cửa sổ.
- **Từ khóa xao nhãng / ngoại lệ**: tự điều chỉnh danh sách ứng dụng, trang web và nội dung được coi là tập trung.
- **Thử đo cửa sổ**: kiểm tra một tiêu đề cửa sổ có khớp danh sách xao nhãng hay ngoại lệ không.
- **Xem thử giờ nghỉ (12 giây)**: xem ngay thú cưng và màn hình nghỉ mà không cần đợi.

### Thống kê
- Mở thẻ **Thống kê** để xem 14 ngày gần nhất và điểm của 10 phiên gần đây.
- Bấm **Xuất CSV cho Excel** để lưu tổng hợp theo ngày và chi tiết từng phiên vào một file CSV UTF-8.

### Màn hình nghỉ
- Thú cưng tự đi lại trên màn hình, bạn không cần làm gì.
- Bấm vào thú cưng thì nó nhảy lên và bắn tim.
- Nút **Thoát** nằm ở góc trên bên phải. Phím **Esc** cũng thoát được.
- Nhạc nền phát suốt giờ nghỉ và tự tắt khi kết thúc.

### Thoát khẩn cấp
Nếu đang bật **Chế độ nghiêm** (không có nút Thoát), nhấn **Ctrl + Shift + X** để thoát màn hình nghỉ bất cứ lúc nào.

### Khay hệ thống
- Bấm nút thu nhỏ (−): cửa sổ biến mất khỏi taskbar, chỉ còn biểu tượng 🍅 cạnh đồng hồ Windows.
- Rê chuột vào biểu tượng để xem thời gian còn lại.
- Bấm (hoặc bấm đúp) biểu tượng để mở lại cửa sổ.
- Bấm chuột phải để ra menu: *Mở Pomodoro Pet*, *Tạm dừng / Bắt đầu / Tiếp tục*, *Thoát*. Trong giờ nghỉ, mục điều khiển hiển thị *Đang nghỉ* và bị khóa.
- Khi hết giờ nghỉ mà app đang nằm trong khay, Windows hiện một thông báo nhỏ kèm lời khen hoặc nhắc nhở.
- Bấm nút **X** của cửa sổ là **thoát hẳn** app.
- Windows 11 đôi khi giấu biểu tượng mới trong nhóm "^". Kéo biểu tượng ra ngoài một lần là nó ở đó luôn.

---

## 4. Cách app tính "xao nhãng" và đưa ra lời khen

Trong phiên tập trung, app tự lấy tiêu đề cửa sổ và tên chương trình đang ở trước, thời gian không có thao tác bàn phím/chuột, và tần suất đổi cửa sổ. Tiêu đề chỉ được xử lý trong bộ nhớ; app chỉ lưu các số liệu tổng hợp, không lưu hay gửi tiêu đề.

- Cửa sổ khớp danh sách từ khóa xao nhãng chỉ được tính sau 10 giây liên tục; danh sách ngoại lệ được ưu tiên.
- Không thao tác trên 90 giây được ghi nhận là rời máy. Chuyển cửa sổ ít nhất 8 lần trong 60 giây được ghi nhận là chuyển liên tục.
- Mỗi đợt được tính một lần xao nhãng; thời lượng theo nguyên nhân cũng được cộng vào thống kê. Tạm dừng không bị tính là xao nhãng.
- App không tính cửa sổ Pomodoro hoặc trạng thái không đọc được cửa sổ là thời gian tập trung tốt.
- Sau mỗi phiên, điểm tập trung trong ngày được so với hôm qua để đưa phản hồi. Bật/tắt tự đo trong Cài đặt; dữ liệu cũ không có chỉ số tự đo sẽ không được dùng để so sánh điểm.
- Chi tiết từng phiên chỉ được lưu từ phiên hoàn thành sau khi cài bản có tính năng thống kê; dữ liệu tổng ngày cũ vẫn được giữ.

---

## 5. Dữ liệu lưu ở đâu

| Dữ liệu | Vị trí |
|---|---|
| Cài đặt và thống kê từng ngày | `C:\Users\<tên bạn>\.pomodoro_pet.json` |
| Chi tiết từng phiên | Lưu cùng file `.pomodoro_pet.json` |
| File Excel-compatible | CSV do người dùng chủ động xuất từ thẻ **Thống kê** |
| Nhật ký lỗi (chỉ có khi app gặp lỗi) | `C:\Users\<tên bạn>\.pomodoro_pet.log` |
| File nhạc app tự tạo (cache) | Thư mục tạm của Windows (`%TEMP%`), tên dạng `pomopet_v2_*.wav` |

Mọi thứ chỉ nằm trên máy của bạn, app không gửi dữ liệu đi đâu. Muốn xóa lịch sử, hãy xóa file `.pomodoro_pet.json`.

---

## 6. Tạo file `PomodoroPet.exe` để gửi cho người khác

Người dùng cuối **không cần cài Python**. Việc tạo file `.exe` chỉ làm **một lần**, bởi người phân phối app. Mỗi khi sửa code, hãy build lại.

### Cách A: không cài gì lên máy bạn (dùng GitHub, miễn phí)
1. Tạo tài khoản tại github.com. Bấm dấu **+** → **New repository**, đặt tên `pomodoro-pet`, chọn **Public**, bấm **Create repository**.
2. Bấm **uploading an existing file**, kéo thả toàn bộ nội dung đã giải nén (gồm `pomodoro_pet.pyw`, `README.md`, `LICENSE` và thư mục `.github`) vào trang, rồi bấm **Commit changes**.
3. Ở cột phải, bấm **Releases → Create a new release**. Ô **Choose a tag** gõ `v1.1.0` rồi chọn **Create new tag**. Đặt tiêu đề (ví dụ "Pomodoro Pet 1.1.0"), viết ghi chú, bấm **Publish release**.
4. Vào tab **Actions**, đợi dấu tick xanh (khoảng 2–3 phút). File `PomodoroPet.exe` sẽ tự xuất hiện trong mục **Assets** của bản Release.
5. Gửi cho mọi người đường dẫn tải: `https://github.com/<tên-bạn>/pomodoro-pet/releases/latest`

Nếu GitHub không nhận thư mục `.github`: bấm **Add file → Create new file**, đặt tên `.github/workflows/build.yml` rồi dán nội dung file `build.yml` vào.

### Cách B: trên một máy có Python
1. Cài Python từ python.org (nhớ tick **Add Python to PATH**).
2. Bấm đúp file `build_exe.bat` và đợi 1–2 phút.
3. File `PomodoroPet.exe` nằm trong thư mục `dist`, cạnh `build_exe.bat`.

### Khi gửi file `.exe` cho người khác
- Lần đầu chạy, Windows có thể hiện **"Windows protected your PC"**. Bấm **More info → Run anyway**. Đây là do file chưa có chữ ký số (chữ ký số tốn phí hàng năm), không phải lỗi.
- Một số phần mềm diệt virus có thể báo nhầm file được đóng gói bằng PyInstaller. Nếu gặp, hãy thêm file vào danh sách cho phép.

---

## 7. Chạy trực tiếp từ mã nguồn (cho người có Python)

1. Cài Python 3.9 trở lên.
2. Bấm đúp `pomodoro_pet.pyw` (chạy không hiện cửa sổ đen), hoặc chạy `python pomodoro_pet.pyw`.

---

## 8. Câu hỏi thường gặp

**App bị đơ, lag, hoặc hiện "Not responding"?**
Bản 1.1 đã sửa các nguyên nhân chính (xem mục 9). Nếu vẫn gặp, hãy mở file `C:\Users\<tên bạn>\.pomodoro_pet.log` (nếu có) và gửi nội dung cho người phát triển. Trong lúc chờ, bạn có thể tắt app bằng Task Manager (**Ctrl + Shift + Esc**).

**Tôi bị kẹt ở màn hình nghỉ?**
Nhấn **Ctrl + Shift + X**. Nếu vẫn không được, mở Task Manager và tắt Pomodoro Pet.

**Tôi không thấy thư mục `dist`?**
Nó nằm cạnh file `build_exe.bat`, và chỉ xuất hiện sau khi build thành công. Hãy chắc chắn bạn đã giải nén file zip và đã cài Python. Nếu dùng cách A thì không có `dist`: tải file từ mục Artifacts.

**Sao nhạc chỉ nhận file `.wav`?**
Để app chạy được chỉ với một file và không cần cài thêm thư viện, app dùng bộ phát âm thanh có sẵn của Windows, mà bộ này chỉ phát `.wav`. Bạn có thể đổi `.mp3` sang `.wav` bằng bất kỳ công cụ chuyển đổi nào.

**Lần đầu chọn nhạc Lo-fi/Mưa/Sóng có hơi chậm?**
App tạo sẵn nhạc ở nền ngay khi mở, lần đầu mất khoảng vài giây. Từ lần sau nhạc được lưu lại và bật ngay.

**Có chạy trên Mac, Linux, điện thoại không?**
Bản này chỉ dành cho Windows, vì thú cưng đè lên các cửa sổ khác và khay hệ thống là tính năng riêng của Windows.

**Dùng nhiều màn hình thì sao?**
Lớp phủ mờ che tất cả màn hình. Thú cưng chạy trên màn hình chính.

**Thú cưng có chặn tôi làm việc thật không?**
Có. Trong giờ nghỉ, lớp phủ chặn thao tác chuột xuống các cửa sổ bên dưới. Nút Thoát và phím khẩn cấp luôn có để bạn không bao giờ bị kẹt.

---

## 9. Nhật ký thay đổi

### 1.1 (bản sửa lỗi lớn)
- **Sửa lỗi đơ, lag:**
  - Màn hình nghỉ trước đây là một cửa sổ trong suốt phủ cả màn hình, phải vẽ lại 30 lần mỗi giây, rất nặng ở màn hình độ phân giải cao. Nay tách thành ba cửa sổ nhẹ: lớp mờ đứng yên, một cửa sổ nhỏ chỉ chứa thú cưng và chỉ việc di chuyển, và nút Thoát.
  - Việc tạo nhạc nền trước đây có thể chiếm CPU và làm giao diện khựng. Nay nhạc được tạo nhẹ hơn, nhường CPU đều đặn, tạo sẵn ở nền ngay khi mở app, và lưu lại để lần sau dùng ngay.
  - Các vòng lặp cập nhật giao diện giờ được bảo vệ: nếu một khung hình gặp lỗi thì app vẫn tiếp tục chạy chứ không bị "đứng hình". Lỗi được ghi vào file log.
  - App ngừng vẽ màn hình chính khi đang ẩn trong khay hoặc đang có lớp phủ nghỉ, để tiết kiệm CPU.
  - Nút `+` / `−` khi giữ chuột không còn ghi file liên tục.
- **Thú cưng tự chạy nhảy:** không còn chạy theo con trỏ chuột. Mèo và cún chạy, nghỉ, nhảy lên ngẫu nhiên. Cá và chim bay lượn ngẫu nhiên.
- Cập nhật tài liệu.

### 1.0
- Bản đầu tiên: hẹn giờ, thú cưng, màn hình nghỉ, nhạc nền, giao diện co giãn, khay hệ thống.

---

## 10. Hướng phát triển

Các tính năng tự đo xao nhãng, phát hiện chuyển cửa sổ/không thao tác, điểm tập trung và danh sách từ khóa tùy chỉnh đã có trong phiên bản này. Hướng tiếp theo có thể gồm tự khởi động cùng Windows, biểu đồ thống kê theo tuần và thêm thú cưng mới.

---

## 11. Cấu trúc thư mục

```
PomodoroPet-build/
├─ pomodoro_pet.pyw        ← toàn bộ ứng dụng (một file duy nhất)
├─ build_exe.bat           ← bấm đúp để tạo PomodoroPet.exe trên máy có Python
├─ HUONG-DAN.txt           ← hướng dẫn tạo file exe, bản rút gọn
├─ README.md               ← file này
├─ LICENSE                 ← giấy phép MIT (nhớ điền tên bạn)
├─ .gitignore              ← danh sách file không đưa lên GitHub
└─ .github/
   ├─ workflows/build.yml  ← GitHub tự tạo file exe và đính kèm vào Release
   └─ ISSUE_TEMPLATE/      ← mẫu báo lỗi và đề xuất tính năng
```
