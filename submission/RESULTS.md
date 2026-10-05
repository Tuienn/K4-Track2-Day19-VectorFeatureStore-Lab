# Kết quả Lab 19

**Học viên:** Nguyễn Ngọc Tuyền · **Mã học viên:** 2A202603010

## Cách tái chạy

```bash
bash setup-lite.sh
make test
make verify-lite
make notebooks
make benchmark
.venv/bin/python scripts/export_evidence.py
```

`.env` được app tự nạp, biến môi trường đã export có ưu tiên cao hơn.
Lần này dùng fastembed bge-small 384d, Qdrant memory, Feast SQLite/file.
ONNX dùng mặc định 4 worker (`EMBEDDING_THREADS`) để tránh oversubscription.
Đổi model thì chạy lại seed advanced và notebooks để index/golden vectors
cùng không gian embedding. Không so vector của hai model trực tiếp.

## Bằng chứng thực thi

Cả tám `.ipynb` giữ output, mọi code cell có execution count và không có
error output. 47 tests pass; smoke Lite pass. Runner cũng đã được kiểm tra
trả exit code thất bại khi notebook lỗi. Chưa thử bootstrap từ venv trống
trong lần thực hiện này; venv có sẵn được dùng và kiểm chứng.

- **NB1:** 1000 vector, top-5 keyword có 4 cloud; paraphrase có 5/5 cloud.
- **NB2:** Precision@10 BM25 77,8%, semantic 73,2%, hybrid 78,6%. Mixed:
  BM25 97%, semantic 98,5%, hybrid 100%. Exact: BM25/hybrid 96,7%.
- **NB3:** 10 warm-up queries/mode rồi 100 measured calls/mode; P50/P95/P99
  server-side (ms): keyword 1,9/2,8/3,4; semantic 10,1/13,7/15,0; hybrid
  13,4/17,7/20,7. Hybrid đạt ngưỡng <50 ms. HTTP wall-clock đo riêng.
- **NB4:** đủ ba feature views; materialize cả snapshot để chạy lặp lại
  không bị incremental watermark bỏ qua dữ liệu. User u_001 và item
  cloud_001 có feature hợp lệ. Online P99 0,81 ms qua 100 calls. PIT có
  ba dòng; probe trước event đầu tiên không nhận giá trị tương lai.
- **NB5:** filter acme + published≥2026 có selectivity 3,8%, post-filter
  recall 0, filtered search 1,00. Over-fetch 500/1000 doc mới đạt recall
  trung bình 1,00; local Qdrant không đo được lợi ích HNSW production.
- **NB6:** cùng budget 16 doc, single-shot recall/balance 0,526/0,08;
  agentic no-filter 0,906/0,93; agentic +filter 0,823/0,76. Filter suy đoán
  loại tài liệu thuộc topic lân cận; reflection nới filter khi thiếu bằng
  chứng. Context có cả Feast feature và doc_ids.
- **NB7:** 25 cached questions, 75 positive và 75 negative probes. Ngưỡng
  0,75 tiết kiệm 100% positives nhưng trả sai 36% negatives; chọn 0,85 vì
  vẫn tiết kiệm 100% và trả sai 0% trên bộ probe này. Chưa suy ra ngưỡng
  production. TTL hết hạn gây MISS; namespace chặn leak tenant.
- **NB8:** session target-naive gap AUC 0,477, in-fold -0,003. Latest join
  rò 98,2% rows, AUC 0,715 so với PIT 0,595. Cùng user u_000, amount
  100.000 và 15.000.000 tạo ratio 0,03 và 4,21, spike 0 và 1.

Benchmark tích hợp đầy đủ 5000 calls/mode được lưu tại `benchmark.txt`,
exit code 0. P99 keyword/semantic/hybrid lần lượt 2,1/13,3/17,7 ms;
hybrid vượt BM25 +0,8 điểm phần trăm và semantic +5,4 điểm phần trăm.
Ảnh PNG trong `screenshots/` là browser captures của output thật được xuất
thành HTML, không phải ảnh dựng lại số liệu; HTML đi kèm và notebook là
nguồn đối chiếu. Thông báo stderr được giữ trong notebook nhưng bỏ khỏi
HTML cho dễ đọc.

## Tiêu chí chưa đạt hoặc chưa làm

Semantic chưa thắng slice paraphrase: 24% so với BM25 33,3%, hybrid 32%.
Đây là hạn chế baseline model tiếng Anh; không sửa golden set để ép thắng.
Chưa chạy model đa ngữ hay Docker; chưa làm bonus tự nguyện.
Latency là phép đo đơn luồng trên máy hiện tại, không phải SLA tải lớn.

Chưa push, chưa đổi visibility và chưa nộp LMS.
Trước khi nộp, kiểm tra tên trong reflection và xác nhận repo GitHub public.
