# Kế hoạch thực hiện Lab 19

## Phạm vi và baseline

Đọc README, rubric, VIBE-CODING, hai bản bonus, reflection, các notebook và
`.env`/`.env.example`. Hoàn thành NB1–NB8 và bằng chứng nộp bài; bonus là
bài tự nguyện riêng. Không thay đổi golden set để ép kết quả. Không push,
đổi visibility hoặc nộp LMS trước khi người dùng xác nhận.

Baseline: Python 3.14.7, 41 tests pass, `make verify-lite` pass. Có tám
notebook `.ipynb` chưa được Git theo dõi từ trước; giữ lại và cập nhật bằng
Jupytext, chỉ commit sau khi thực thi thành công.

## Thiết kế

Chọn cấu hình hiện có trong `.env`: fastembed bge-small 384 chiều, Qdrant
in-memory, Feast SQLite online và Parquet offline. Corpus nhỏ 1000 tài liệu
nên Lite đủ để kiểm chứng thuật toán, không cần Docker hay dịch vụ trả phí.
Model tiếng Anh là baseline có hạn chế với paraphrase tiếng Việt; báo cáo
kết quả đo thật trước khi cân nhắc model nặng hơn.

Luồng search: title + text → BM25 và embedding → Qdrant cosine → top-50
của mỗi retriever → RRF với k=60, rank bắt đầu từ 1 → top-10. API tái sử
dụng Searcher đã dựng lúc startup, đo riêng thời gian server bằng perf_counter.
Benchmark warm-up trước khi lấy mẫu; không cache câu trả lời để làm đẹp latency.

Luồng feature: ba nguồn Parquet → Feast registry → materialize → SQLite →
online lookup. TTL profile 30 ngày, popularity 24 giờ, velocity 1 giờ theo
definitions hiện có. Historical join dùng timestamp của entity để không đọc
feature tương lai. NB8 dùng registry riêng cho on-demand feature view.

Khối nâng cao kiểm chứng filter bằng exact cosine trong subset; so agent ở
cùng ngân sách 16 tài liệu; cache đo cả tiết kiệm và false hit, TTL và tenant;
feature engineering đo leakage sau khi split và so PIT với latest join.

## Checkpoints — mỗi mục một commit

1. **Thiết kế và baseline:** lưu kế hoạch, xác nhận môi trường và tests.
2. **NB1–NB2:** chạy index 1000 vector, top-5 và paraphrase, bảng Precision@10
   tổng thể và theo slice, lưu output. Giải thích trường hợp không đạt rubric.
3. **NB3:** API response, warm-up, 100 calls/mode, P50/P95/P99 server-side;
   kiểm tra ngưỡng hybrid P99 < 50 ms và lỗi HTTP rõ ràng.
4. **NB4:** apply/list đủ 3 views, materialize, online result và 100-call
   latency, PIT join 3 dòng; lưu output và bằng chứng.
5. **NB5–NB8 và hồ sơ:** chạy bốn notebook nâng cao, bổ sung diễn giải theo số
   thực đo, screenshots output, reflection ≤200 từ, báo cáo tiêu chí đạt/chưa
   đạt; chạy tests/smoke và benchmark tích hợp.

## Quy tắc kiểm chứng

`.py` là source, `.ipynb` giữ execution outputs để chấm. Mỗi checkpoint
review diff và lỗi notebook trước commit. Generated corpus/registry/model
không commit. Thông tin tên học viên còn thiếu sẽ để ghi rõ chưa cung cấp.
Kết quả latency là đơn luồng trên máy hiện tại, không suy ra SLA production.

## Trạng thái hoàn thành

Cả 5 checkpoint hoàn thành tại máy local. NB1–NB8 đã chạy, 47 tests và
smoke Lite pass, benchmark 5000 calls/mode pass. Mỗi notebook có PNG/HTML
output evidence. Reflection 169 từ đã điền tên Nguyễn Ngọc Tuyền và mã
2A202603010. Xem `RESULTS.md` để biết hạn chế paraphrase và phạm vi chưa chạy.
