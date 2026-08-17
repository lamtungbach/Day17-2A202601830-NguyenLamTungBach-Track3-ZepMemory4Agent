# Huong dan doc hieu va su dung du an Lab 17

Tai lieu nay giai thich du an theo cach de tu hoc: **bai toan la gi, du lieu di qua
nhung dau, bon loai memory khac nhau the nao, cach chay, cach doc ket qua va cach
chup bang chung nop bai**.

## 1. Du an nay giai quyet bai toan gi?

Chatbot thong thuong chi nhin thay noi dung nam trong prompt hien tai. Khi doi sang
conversation/thread moi, no co the quen preference, deadline, kinh nghiem debug va
tri thuc domain da noi truoc do.

Du an xay mot agent co bon lop memory:

| Lop memory | Nho dieu gi? | Scope | Vi du trong lab |
| --- | --- | --- | --- |
| Short-term | Noi dung gan nhat cua thread hien tai | `thread_id` | Ten ORCHID-27 vua duoc nhac |
| Long-term | Fact, preference, open loop qua nhieu session | `user_id` | Minh thich Python, deadline 16:00 |
| Episodic | Mot trai nghiem, trajectory va outcome cu the | `user_id` | Tang timeout that bai; ClientSession moi fix duoc |
| Semantic | Tri thuc domain dung chung, khong thuoc user | `graph_id` | Quy tac retry payment voi Idempotency-Key |

Muc tieu chinh khong phai la lam chatbot "noi hay", ma la **retrieve dung evidence**.
Evaluator chi cho PASS neu chuoi marker trong ground truth that su xuat hien trong
retrieved context.

## 2. Kien truc tong quan

```text
data/sessions.json
       |
       | seed
       v
+----------------------+       +--------------------------+
| Zep user graph       |       | Zep standalone graph     |
| user facts + episode |       | shared domain knowledge  |
+----------+-----------+       +------------+-------------+
           |                                |
           +---------------+----------------+
                           |
Query -> route/chon layer -> retrieve tung layer
                           |
                  ContextBudgetManager
                    10% / 4% / 3% / 3%
                           |
                     merged context
                           |
                  evaluator hoac demo UI
```

Redis va Qdrant trong lab la **local baseline/de mo so sanh**, khong thay the backend
memory chinh. Memory chinh cua bai thuc hanh duoc retrieve tu Zep Cloud V3.

## 3. Luong hoat dong tu dau den cuoi

### Buoc 1 - Nap du lieu (`src.seed`)

`python -m src.seed` thuc hien:

1. Doc `data/sessions.json` va `data/knowledge.jsonl`.
2. Reset hai synthetic user `minh-lab17` va `lan-lab17`.
3. Tao cac thread va ingest message theo tung stage.
4. Tao standalone semantic graph tu domain knowledge.
5. Poll cho den khi cac marker nhu `PAYMENT-RULE-3` searchable.

Zep index bat dong bo, vi vay seed co the mat 1-3 phut. Day khong phai loi neu terminal
dang cho ma chua in exception.

### Buoc 2 - Evaluator doc tung test case

Moi case trong `data/sessions.json` co dang:

```json
{
  "id": "E04",
  "expected_layer": "episodic",
  "query": "Lan truoc Minh fix async HTTP timeout bang cach nao?",
  "must_contain_all": ["ClientSession", "concurrency=20", "ASYNC-FIX-20"]
}
```

Evaluator nhin `expected_layer`, goi dung ham retrieval, sau do kiem tra:

- moi chuoi trong `must_contain_all` phai co;
- moi chuoi trong `must_not_contain` phai khong co;
- retrieval bi exception cung tinh la FAIL.

### Buoc 3 - Retrieve memory

Bon ham chinh nam trong `src/memory_student.py`.

#### `retrieve_long_term`

1. `prime_eval_thread` tao evaluation thread moi cua dung user.
2. `thread.get_user_context` lay Context Block lien quan.
3. Search them user-scoped edges de co fact, timestamp va validity/provenance.
4. Return **string**, khong return object SDK.

Vi moi call deu co `user_id`, query cua Lan khong duoc lay memory cua Minh. Day la ly
do E09 kiem tra ca marker dung (`LOTUS-88`) va marker cam (`ORCHID-27`).

#### `retrieve_episodic`

Search Zep bang:

```python
client.graph.search(
    user_id=user_id,
    query=cap_query(query),
    scope="episodes",
    limit=5,
)
```

`user_id` bao ve isolation. `scope="episodes"` lay raw source, giu du cac marker cua
trajectory. Moi episode duoc gioi han ky tu de mot episode dai khong chiem het budget.

#### `retrieve_semantic`

Semantic memory dung `graph_id`, khong dung `user_id`:

```python
client.graph.search(
    graph_id=semantic_graph_id,
    query=cap_query(query),
    scope="episodes",
    limit=8,
)
```

`episodes` giu nguyen literal marker trong document. Neu search episodes loi/rong, code
fallback sang `nodes`. Khong dung `scope="auto"` cho benchmark nay vi fact extraction
co the lam mat ma nhu `PAYMENT-RULE-3`.

#### `assemble_context`

Tat ca evidence duoc truyen vao `ContextBudgetManager` theo thu tu:

1. short-term: 10% context window;
2. long-term: 4%;
3. episodic: 3%;
4. semantic: 3%.

Voi context 8.000 token, gioi han tuong ung la 800, 320, 240 va 240 token. Phan con
lai cua context window danh cho system prompt, task, tool output, policy va answer.

### Buoc 4 - Cham evidence va tao report

`src.evaluate` tao:

- `reports/benchmark.json`: ket qua may doc;
- `reports/benchmark.md`: bang va evidence de con nguoi doc;
- `reports/benchmark_no_memory.*`: baseline;
- `reports/comparison.md`: so sanh hai cach.

## 4. Hieu short-term memory va compaction

`src/short_term.py` co ba strategy:

| Strategy | Hanh vi | Van de/loi ich |
| --- | --- | --- |
| Buffer | Giu tat ca message | Day du nhung token tang mai |
| Summary | Nen message cu, giu vai message moi | Gon nhung co the mat chi tiet |
| Sliding | Summary + durable notes + K message moi | Can bang tot nhat cho lab |

Khi message cu bi day khoi sliding window, `extract_durable_notes` tim TODO, deadline,
constraint, decision, preference va marker viet hoa. Vi vay E10 van giu:

```text
REVIEW-DEADLINE-1600
Friday
16:00
```

Compaction tot khong phai tom tat moi cau deu nhau. No phai uu tien **state, decision,
TODO va constraint**.

## 5. Recency, scope va conflict

E08 co hai preference tuong nhu mau thuan:

- ORCHID-27: demo ca nhan uu tien Python;
- BLUEBIRD-42: project cong ty bat buoc TypeScript + NestJS.

Quy tac dung la **recency + scope**, khong phai "fact moi xoa sach fact cu". Preference
Python van dung cho ORCHID-27, con constraint moi hon chi override trong BLUEBIRD-42.

Mot durable record tot nen co:

```text
scope, type, content, source, timestamp, confidence, ttl, validity
```

Cac truong nay giup audit, xu ly conflict, expiry va right-to-be-forgotten.

## 6. Baseline 2/11 co anh huong khong?

**Khong. Day la ket qua dung va duoc mong doi.**

`no_memory` co chu dich khong retrieve long-term, episodic hay semantic memory. No chi
PASS E01 va E10 vi evidence cua hai case nay nam trong short-term local. Chin case con
lai phai FAIL de chung minh agent khong co memory khong the recall cross-session/domain.

Ket qua can dung de cham bai cua ban la:

```text
student:   11/11 = 100%
baseline:   2/11 = 18,2%
delta:     +9 case = +81,8 diem phan tram
```

Baseline 2/11 **khong tru diem**. Neu baseline cung 11/11 thi phep so sanh moi dang ngo,
vi co the evaluator dang leak ground truth hoac "no-memory" van doc durable memory.

No-memory co token reduction cao 81,8% vi no retrieve gan nhu rong. Do khong phai toi
uu tot: bo het evidence rat re nhung answer khong co co so.

## 7. Ban do cac file quan trong

| File/thu muc | Nen doc de hieu gi? |
| --- | --- |
| `README.md` | Quick start va dau ra tong quat |
| `LAB.md` | De bai, rubric va 13 task |
| `CHECKPOINTS.md` | Tien trinh da thuc hien trong repo |
| `data/sessions.json` | User, session va 11 evaluation case |
| `data/knowledge.jsonl` | Shared semantic knowledge |
| `src/memory_student.py` | Bon ham ban phai hieu/giai thich |
| `src/zep_common.py` | Tao user/thread, ingest, poll va render search |
| `src/short_term.py` | Buffer, summary, sliding va compaction |
| `src/context_budget.py` | Budget 10/4/3/3 va priority |
| `src/evaluate.py` | Cach route case, score va ghi report |
| `src/demo_ui.py` | UI xem evidence va chat tiep |
| `control_plane/*.md` | Persona, rule, schema, task va policy context |
| `reports/benchmark.md` | Ket qua student 11/11 |
| `reports/comparison.md` | Ly do memory tot hon baseline |

Thu tu doc de de hieu nhat:

```text
HUONG_DAN nay
 -> data/sessions.json
 -> src/memory_student.py
 -> src/zep_common.py
 -> src/context_budget.py + src/short_term.py
 -> src/evaluate.py
 -> reports/benchmark.md
```

## 8. Cach chay du an

### Lan dau hoac sau khi thay doi `.env`

```powershell
docker compose build
docker compose up -d redis qdrant
docker compose run --rm app python -m src.smoke
docker compose run --rm app python -m src.seed
```

Smoke thanh cong phai co:

```text
[OK] Redis reachable
[OK] Qdrant reachable
[OK] sessions.json valid: 11 evaluations
[OK] ZEP_API_KEY is present
```

### Chay test khong ton Zep call

```powershell
docker compose run --rm app pytest -q
```

Golden chua duoc phat thi `1 skipped` la binh thuong.

### Chay benchmark chinh

```powershell
docker compose run --rm app python -m src.evaluate --impl no_memory
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded
docker compose run --rm app python -m src.compare_reports
```

`--reuse-seeded` nghia la dung data da seed, khong reset/ingest lai moi lan.

### Chay rieng mot layer de debug

```powershell
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --only-layer long_term
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --only-layer episodic
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --only-layer semantic
```

Luu y: moi lenh tren ghi lai `reports/benchmark.*` bang chi layer duoc chon. Sau khi debug,
hay chay lai full student benchmark de report cuoi co du 11 case.

### Chay UI

```powershell
docker compose run --rm --service-ports app streamlit run src/demo_ui.py --server.address 0.0.0.0 --server.port 8501
```

Mo trinh duyet tai `http://localhost:8501`. UI cho phep:

1. chon E01-E11;
2. xem user, thread, query va expected layer;
3. run retrieval, xem evidence tung layer va merged context;
4. chat tiep tren cung user/thread.

`GEMINI_API_KEY` chi can de sinh chat reply. Benchmark retrieval van chay neu khong co
Gemini key.

## 9. Cach doc `reports/benchmark.md`

Hay doc theo ba cap:

1. **Summary:** `Passed`, `Evidence hit rate`, latency va token reduction.
2. **Bang case:** case nao PASS/FAIL, missing marker nao.
3. **Evidence excerpts:** backend that su tra ve noi dung gi.

Neu case FAIL:

- `missing=...`: retrieval khong chua du marker;
- `forbidden=...`: leak fact khong duoc phep, thuong la sai user scope;
- `error=...`: SDK/network/parameter bi loi;
- semantic mat marker: kiem tra `graph_id` va `scope="episodes"`;
- episodic ra sai user: kiem tra `user_id`;
- mixed thieu mot nua: kiem tra ca long-term, semantic va budget trim.

## 10. Cach chup ba anh retrieval

May cua ban co trinh duyet, vi vay co the chup tu HTML report da tao san.

### Anh 1 - Long-term

1. Mo file `reports/benchmark.html` bang Chrome/Edge (double-click file).
2. Nhan `Ctrl+F`, tim `E02` (hoac E03/E08).
3. Dam bao vung man hinh co case ID, layer `long_term`, chu `PASS` va evidence.
4. Nhan `Windows + Shift + S`.
5. Chon **Rectangular snip**, keo bao quanh vung evidence.
6. Mo thong bao screenshot, bam Save.
7. Luu thanh `submission/long_term.png`.

### Anh 2 - Episodic

Lam tuong tu, tim `E04` hoac `E05`, chup PASS + evidence va luu:

```text
submission/episodic.png
```

Anh E04 nen nhin thay `ClientSession`, `concurrency=20`, `ASYNC-FIX-20`.

### Anh 3 - Semantic

Tim `E06` hoac `E11`, chup PASS + evidence va luu:

```text
submission/semantic.png
```

Anh E06 nen nhin thay `Idempotency-Key`, `max-3-retries`, `exponential-backoff`.

## 11. Cach chup anh privacy

Privacy la thao tac xoa user-scoped memory. Chi chay sau khi `reports/benchmark.md` da
duoc luu.

1. Mo PowerShell tai thu muc du an.
2. Chay:

```powershell
docker compose run --rm app python -m src.forget --user-id minh-lab17
docker compose run --rm app python -m src.forget --user-id minh-lab17 --verify-only
```

3. Terminal phai hien:

```text
Zep user absent: True
Redis user keys remaining: 0
```

4. Nhan `Windows + Shift + S`, chup ca hai lenh va hai dong ket qua.
5. Luu thanh `submission/privacy.png`.
6. Seed lai de UI/golden co user:

```powershell
docker compose run --rm app python -m src.seed
```

Repo hien da tung chay privacy thanh cong va co transcript tai
`submission/privacy.log`. Neu giang vien chap nhan log, co the nop file do; neu rubric
bat buoc PNG, hay chup lai theo cac buoc tren.

## 12. Privacy va memory-poisoning guardrail

Du an ap dung cac y tuong:

- chi ingest durable memory khi consent `memory_opt_in=true`;
- redact email/phone truoc khi persist;
- user data dung user-scoped namespace;
- shared domain knowledge dung graph rieng, khong tron PII;
- preference/task anh huong cao can review truoc durable write;
- heartbeat khong duoc tu tao quyen hay instruction moi;
- deletion phai verify tren moi user-scoped store;
- evidence can source, timestamp, confidence va validity.

Trong production can bo sung authentication/authorization, encryption, audit log, data
retention, rate limit, prompt-injection filtering va human approval cho durable writes.

## 13. Golden va diem cong

`data/golden_eval.json` khong co san trong repo. Khi giang vien cung cap, copy vao dung
path va chay:

```powershell
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --golden
```

Golden chi co diem neu **20/20** va `summary.perfect == true`. Khong sua file golden va
khong commit file nay.

UI la diem cong rieng. Golden/UI khong phai dieu kien de dat lab co ban.

## 14. Checklist tu kiem tra truoc khi nop

- [ ] `pytest`: 11 pass; golden test skip neu chua co file.
- [ ] `reports/benchmark.md`: 11/11 PASS.
- [ ] `reports/benchmark.json`: implementation la `student`, `perfect=true`.
- [ ] `reports/comparison.md` ton tai.
- [ ] `README_submission.md` khong qua 400 tu.
- [ ] Co `long_term.png`, `episodic.png`, `semantic.png`, `privacy.png`.
- [ ] `.env` khong nam trong Git.
- [ ] `data/golden_eval.json` khong nam trong Git.
- [ ] Khong con `NotImplementedError` trong hai ham student/UI.

## 15. Nam cau hoi de tu kiem tra muc do hieu

1. Tai sao episodic search dung `user_id`, con semantic search dung `graph_id`?
2. Tai sao `scope="episodes"` phu hop hon `scope="auto"` trong bo benchmark nay?
3. Tai sao baseline token reduction cao nhung retrieval lai kem?
4. E08 ap dung recency + scope nhu the nao?
5. Neu E07 co `Python` nhung thieu `Idempotency-Key`, ban se debug ham nao truoc?

Neu tu tra loi duoc nam cau nay va giai thich duoc bon ham trong
`src/memory_student.py`, ban da nam du kien thuc chinh cua du an.
