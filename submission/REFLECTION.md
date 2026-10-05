# Reflection — Lab 19

**Tên:** Nguyễn Ngọc Tuyền
**Mã học viên:** 2A202603010
**Cohort:** A20-K4
**Path đã chạy:** Lite (fastembed bge-small 384d, Qdrant memory, Feast SQLite)

## Câu trả lời (≤200 từ)

Trên 50 golden queries, hybrid đạt Precision@10 78,6%, BM25 77,8%,
semantic 73,2%. Với exact, BM25 và hybrid cùng đạt 96,7%; semantic 88,7%.
Với mixed, hybrid đạt 100%, vượt semantic 98,5% và BM25 97%. RRF dùng
rank bắt đầu từ 1 và k=60, giúp kết hợp hai tín hiệu xếp hạng.

Paraphrase là hạn chế rõ: BM25 33,3%, hybrid 32%, semantic 24%. Model
bge-small tiếng Anh chưa đủ tốt cho diễn đạt lại tiếng Việt. Không thể kết
luận vector luôn thắng; cần thử model đa ngữ và index lại trước khi chọn
stack production. Query paraphrase riêng ở NB1 vẫn tìm đúng cả 5 tài liệu
cloud, nhưng không đại diện cho toàn golden set.

Tôi chọn BM25 cho mã định danh hoặc thuật ngữ exact khi lexical signal
đã đủ; chọn vector cho paraphrase sau khi kiểm chứng model đúng ngôn ngữ.
Hybrid phù hợp mixed, song tốn thêm latency. Bài đo dùng corpus tổng hợp
và chạy đơn luồng, nên không suy ra hiệu năng tải lớn.

## Điều rút ra từ khối nâng cao

Filter suy đoán có thể loại mất bằng chứng; cache phải đo cả false hit.
PIT join và split trước encoding quan trọng hơn chỉ số offline đẹp.

## Bonus challenge

- [ ] Chưa làm bonus tự nguyện; đã hoàn thành phạm vi NB1–NB8.
