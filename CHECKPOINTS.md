# Checkpoint thuc hien Lab 17

File nay la bang theo doi tien trinh dua tren `README.md`, `LAB.md`, cac tai lieu
trong `control_plane/`, ma nguon, test va du lieu benchmark. Quy uoc trang thai:
`[ ]` chua lam, `[-]` dang lam, `[x]` da xac minh, `[!]` bi chan boi dieu kien ben ngoai.

## Muc tieu bat buoc

- Practice benchmark dat it nhat **9/11 PASS** va diem nen it nhat **56/80**.
- Hoan thanh dung 4 ham trong `src/memory_student.py`.
- Co `reports/benchmark.md`, `reports/benchmark.json`, `reports/comparison.md`.
- Co `README_submission.md` khong qua 400 tu va 4 anh minh chung.
- Hoan thanh privacy drill, khong commit `.env`, API key hoac golden dataset.

## CP0 - Hieu de bai va hien trang

- [x] Doc `README.md`, toan bo 712 dong `LAB.md`, `VALIDATION.md` va cac README phu.
- [x] Doc 6 file control plane: rules, context layers, persona, memory schema va tasks.
- [x] Doi chieu 11 case E01-E11 voi marker bat buoc/cam trong `data/sessions.json`.
- [x] Xac dinh pham vi code bat buoc chi gom 4 ham trong `src/memory_student.py`.
- [x] Xac dinh `reports/benchmark_no_memory.*` da co san trong working tree va se duoc bao toan.

Tieu chi hoan thanh: moi yeu cau nop bai co checkpoint tuong ung va khong sua file starter
ngoai pham vi neu khong can thiet.

## CP1 - Moi truong va smoke test

- [x] Xac minh Docker/Compose, Python va dependency.
- [x] Khoi dong Redis + Qdrant.
- [x] Chay `python -m src.smoke` va xac minh 4 dong `[OK]`.
- [x] Seed 2 synthetic user va standalone semantic graph mot lan.

Tieu chi hoan thanh: Redis, Qdrant, dataset, Zep key deu san sang; seed ket thuc khong loi.

## CP2 - Short-term memory va compaction

- [x] Chay demo 3 chien luoc buffer/summary/sliding voi cua so 6.
- [x] Chay bien the cua so 4 ma khong de lai thay doi tam trong starter kit.
- [x] Xac minh durable note van giu `REVIEW-DEADLINE-1600`, `Friday`, `16:00`.
- [x] Chay unit test short-term; ghi nhan giai thich E10 cho bai nop.

Tieu chi hoan thanh: E01/E10 co the PASS va hieu vi sao compaction can uu tien
state/decision/TODO/constraint.

## CP3 - Bon ham memory bat buoc

- [x] Long-term: prime evaluation thread, lay Zep Context Block va return string.
- [x] Episodic: user-scoped `scope="episodes"`, query <= 400 ky tu, render co provenance.
- [x] Semantic: shared `graph_id`, `scope="episodes"`, query <= 400 ky tu, fallback nodes.
- [x] Mixed context: assemble theo priority STM -> LT -> EP -> SEM va budget 10/4/3/3.
- [x] Khong con `NotImplementedError` trong `src/memory_student.py`.

Tieu chi hoan thanh: implementation dung scope, bao ve user isolation va dung contract cua
evaluator.

## CP4 - Test va practice benchmark

- [x] Chay toan bo `pytest` (starter kit mong doi 11/11 PASS; golden test co the skip).
- [x] Chay rieng long-term, episodic va semantic de chan doan theo layer.
- [x] Chay full student benchmark E01-E11.
- [x] Dat it nhat 9/11 PASS, E09 khong leak `ORCHID-27`, E07 co ca LT + semantic.
- [x] Tao `reports/comparison.md` tu memory-enabled va no-memory baseline.

Tieu chi hoan thanh: report student hop le, hit rate >= 80%, moi failure (neu co) duoc giai thich.

## CP5 - Control plane va cac mini-drill

- [x] Chay episodic maintenance va quan sat importance decay/LRU/consolidation.
- [x] Chay heartbeat dry-run, xac minh khong ghi durable memory hay tu cap quyen.
- [x] Chay compiled-KB demo va quan sat provenance/contradiction/freshness.

Tieu chi hoan thanh: co du co so de giai thich trade-off Zep vs local stores va guardrail
chong memory poisoning.

## CP6 - Artefact nop bai va privacy

- [x] Viet `README_submission.md` <= 400 tu, tra loi du 3 cau va 4 phan tich benchmark.
- [!] Luu anh `long_term.png`, `episodic.png`, `semantic.png`: browser backend khong kha dung.
- [x] Chi sau khi benchmark da luu: forget `minh-lab17`, verify Zep absent va Redis key = 0.
- [x] Luu `submission/privacy.log` voi delete + verify that; rubric chap nhan screenshot/log.
- [x] Seed lai synthetic data sau privacy de san sang cho UI/golden.
- [x] Ra soat `.gitignore`, Git status va khong de lo secret/golden dataset.

Tieu chi hoan thanh: du artefact cot loi va bang chung cham diem privacy.

## CP7 - Diem cong (khong chan dieu kien pass)

- [x] Hoan thien `retrieve_for_case` trong `src/demo_ui.py` va smoke-test UI.
- [x] Golden 20/20, `summary.perfect=true`, bonus 10/10; input van duoc gitignore.

Tieu chi hoan thanh UI: load case, hien metadata, retrieval tung layer + merged context,
va chat tiep cung user/thread. Golden chi dat diem khi `summary.perfect == true` va 20/20.

## Nhat ky ket qua

- CP0: hoan thanh. Phat hien Docker CLI/Compose co san; Docker daemon hien bi tu choi truy
  cap trong sandbox. `.env` co cac bien can thiet (gia tri da duoc an, khong ghi vao file nay).
- Baseline hien co: `no_memory` PASS 2/11 (18.2%), dung voi ky vong chi E01 va E10.
- CP1: hoan thanh. Docker image build thanh cong; Redis healthy, Qdrant running; smoke
  test 4/4 `[OK]`; Zep seed xong 2 user, 3 stage va standalone semantic graph.
- CP2: hoan thanh. Cua so 4 giu du 3 marker deadline sau 12 lan compact; test 2/2 PASS.
- CP3: hoan thanh phan code. Bon ham dung scope/budget; compile PASS; full unit test
  12 PASS sau khi golden duoc cung cap.
- CP4: hoan thanh. Long-term 4/4, episodic 2/2, semantic 2/2; full practice 11/11
  (100%). Baseline 2/11 (18.2%); `reports/comparison.md` da duoc tao.
- CP5: hoan thanh. Da quan sat importance decay/LRU/consolidation, heartbeat read-only
  voi 3 open loop, va compiled KB tra ve provenance/freshness/contradiction/decision.
- CP6: phan bat buoc chay du: README 292 tu; privacy delete + verify PASS; da seed lai;
  secret scan sach. Con 4 PNG can chup thu cong vi runtime khong co browser backend.
- CP7: UI da wire retrieval, mock-smoke E01/E04/E07 va Streamlit health `ok`. Golden
  da dat 20/20 hai lan lien tiep, ke ca re-run sau practice ma khong seed lai.
- Final: practice 11/11, golden 20/20, `perfect=True`, pytest 12 PASS; khong co API
  key ngoai `.env`, golden input khong bi Git track, khong con `NotImplementedError`.
- Golden fix: reseed user Minh sau privacy; semantic deduplicate JSON/summary de marker
  khong bi trim; episodic re-rank 20 candidate de evaluation thread khong lan source episode.
