# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
Khi temperature = 0.0, model luôn trả về cùng một câu trả lời cố định, súc tích và mang tính sách vở. Khi tăng dần lên 0.5 và 1.0, phản hồi bắt đầu đa dạng hơn về cách diễn đạt và lựa chọn sự kiện. Ở temperature = 1.5, câu trả lời sáng tạo và bất ngờ hơn nhưng đôi khi lan man, kém tập trung và có thể kém chính xác hơn.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
Nên đặt temperature = 0.2, vì chatbot hỗ trợ khách hàng cần trả lời nhất quán, chính xác và đáng tin cậy. Độ sáng tạo cao không cần thiết và có thể gây ra thông tin sai lệch hoặc phản hồi không phù hợp với chính sách công ty.
---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
Tổng token mỗi ngày: 10.000 × 3 × 350 = 10.500.000 token (giả sử chia đều input/output: 175 token input + 175 token output).

Chi phí GPT-4o: (175 × $5 + 175 × $20) / 1.000.000 × 10.000 × 3 ≈ $131.25/ngày
Chi phí GPT-4o-mini: (175 × $0.15 + 175 × $0.60) / 1.000.000 × 10.000 × 3 ≈ $3.94/ngày
→ GPT-4o đắt hơn GPT-4o-mini khoảng 33 lần cho workload này.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
GPT-4o xứng đáng khi xây dựng công cụ phân tích hợp đồng pháp lý hoặc hỗ trợ chẩn đoán y tế — những tác vụ đòi hỏi lý luận phức tạp, độ chính xác cao và sai sót có thể gây hậu quả nghiêm trọng. Ngược lại, GPT-4o-mini là lựa chọn tốt hơn cho chatbot phân loại câu hỏi FAQ, tóm tắt email hay gán nhãn nội dung đơn giản — khối lượng lớn, yêu cầu không cao, tiết kiệm chi phí vận hành đáng kể.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
Streaming quan trọng nhất khi người dùng trực tiếp đọc output trong thời gian thực — chẳng hạn chatbot hội thoại, công cụ viết bài, hay giải thích code — vì chữ hiện ra ngay lập tức giúp trải nghiệm mượt mà, tránh cảm giác chờ đợi khó chịu dù response dài. Ngược lại, non-streaming phù hợp hơn khi toàn bộ output cần được xử lý trước khi thực hiện bước tiếp theo, ví dụ như phân tích sentiment, trích xuất dữ liệu JSON có cấu trúc, hay các pipeline batch processing tự động — trong những trường hợp này người dùng không đọc trực tiếp nên streaming không mang lại lợi ích gì mà còn làm phức tạp code xử lý kết quả.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
