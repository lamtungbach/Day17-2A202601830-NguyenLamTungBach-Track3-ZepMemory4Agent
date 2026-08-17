# Lab 17 - Submission

## Ba cau hoi bat buoc

**Layer quan trong nhat trong bo test.** Long-term co tac dong lon nhat ve diem va do
phu: no quyet dinh E02, E03, E08, E09 va la mot nua cua E07. Context Block nho duoc
preference/open loop qua session, tach user o E09, va ap dung scope + recency de E08
giu ca ORCHID-27/Python lan BLUEBIRD-42/TypeScript/NestJS ma khong danh dong hai du an.

**Zep Context Block so voi Redis + Qdrant.** Zep giam phan ingestion, entity/fact
extraction, temporal conflict, cross-thread recall va provenance; doi lai phu thuoc dich
vu cloud, co latency/chi phi va it quyen kiem soat ranking. Redis + Qdrant re hon, de
self-host va tuy bien TTL/schema, nhung nhom phai tu xay extraction, namespace, recency,
consolidation, deletion va danh gia chat luong retrieval.

**Guardrail chong memory poisoning.** Chi durable-write khi user da opt-in; redact PII;
allowlist loai memory va scope; luu source, timestamp, confidence, validity; yeu cau review
cho preference/task anh huong cao. Heartbeat la read-only, khong duoc tu cap quyen. Khi
recall, uu tien evidence moi dung scope va giu provenance de audit/rollback.

## Phan tich benchmark

- Khong co layer thap nhat: tat ca layer dat 100%; toan bai **11/11**, baseline **2/11**.
- O lan benchmark cuoi, E04 retrieve nhieu nhat: **1.613 token**.
- E07 can long-term (`Python`) + semantic (`Idempotency-Key`), sau do trim 10/4/3/3.
- Memory-enabled giam trung binh **11,4%** token, no-memory giam **81,8%** nhung chi
  dat 18,2% hit rate: retrieval rong rat re nhung khong co evidence.

E10 cho thay buffer tang vo han; sliding compaction van giu durable constraint
`REVIEW-DEADLINE-1600`, Friday, 16:00 sau khi raw turn bi evict. E08 cho thay "recency
wins" phai ket hop scope: cap nhat cong ty khong xoa preference demo ca nhan.

## Bang chung

- [Long-term](submission/long_term.png)
- [Episodic](submission/episodic.png)
- [Semantic](submission/semantic.png)
- [Privacy delete + verify log](submission/privacy.log)
