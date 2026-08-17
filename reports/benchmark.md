# Lab 17 Benchmark Report

- Implementation: `student`
- Kind: `practice`
- Cases: **11**
- Passed: **11/11**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **726.5 ms**
- Average token reduction vs full source context: **11.4%**

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| E01 | short_term | PASS | 0.0 | 133 | 0.0% |  |
| E06 | semantic | PASS | 352.1 | 202 | 56.0% |  |
| E09 | long_term | PASS | 1509.2 | 779 | 0.0% |  |
| E10 | short_term | PASS | 0.2 | 195 | 0.0% |  |
| E02 | long_term | PASS | 1262.7 | 1444 | 0.0% |  |
| E03 | long_term | PASS | 1251.6 | 1447 | 0.0% |  |
| E04 | episodic | PASS | 243.6 | 1613 | 0.0% |  |
| E05 | episodic | PASS | 265.6 | 1576 | 0.0% |  |
| E07 | mixed | PASS | 1510.5 | 538 | 4.8% |  |
| E11 | semantic | PASS | 275.5 | 198 | 65.0% |  |
| E08 | long_term | PASS | 1320.0 | 1458 | 0.0% |  |

## Evidence excerpts

### E01 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### E06 - semantic

`EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata= EPISODE: {"id":"kb-payment-retry","entity":"Payment API Retry Policy","summary":"For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Mar`

### E09 - long_term

`<USER_SUMMARY> Lan is working on a project titled LOTUS-88.  Lan prefers using Java and Spring Boot for backend development.  The user has instructed that Python should not be used in backend examples. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va `

### E10 - short_term

`<SESSION_SUMMARY> user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. | assistant: Acknowledged review constraint. | user: Filler turn 1 about UI spacing. | assistant: Filler answer 1. | user: Filler turn 2 about naming. | assistant: Filler answer 2. | user: Filler turn 3 about logging. | assistant: Filler answer 3. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. - assistant: Acknowledged review constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler turn 4 about tests. assistant: Filler answer 4. user: Filler turn 5 about docs. assistant: Filler answe`

### E02 - long_term

`<USER_SUMMARY> Minh is working on a personal project named ORCHID-27, for which he prefers Python. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, not Python. He has a deadline to complete a benchmark report for LAB-REPORT-1600 before Friday at 16:00. He recently debugged async HTTP, increasing the timeout to 60s, but it still failed. He is also addressing a concurrency issue related to connection churn in ASYNC-FIX-20 by reusing an aiohttp ClientSession with concurrency set to 20.  Minh prefers Python and dislikes Java. He wants a demo of his personal project ORCHID-27. He is learning async/await and often confuses coroutines with Tasks. He wants explanatio`

### E03 - long_term

`<USER_SUMMARY> Minh is working on a personal project named ORCHID-27, for which he prefers Python. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, not Python. He has a deadline to complete a benchmark report for LAB-REPORT-1600 before Friday at 16:00. He recently debugged async HTTP, increasing the timeout to 60s, but it still failed. He is also addressing a concurrency issue related to connection churn in ASYNC-FIX-20 by reusing an aiohttp ClientSession with concurrency set to 20.  Minh prefers Python and dislikes Java. He wants a demo of his personal project ORCHID-27. He is learning async/await and often confuses coroutines with Tasks. He wants explanatio`

### E04 - episodic

`EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. EPISODE: Cong ty yeu cau chinh context window cho agent tren dung backend du an cong ty. Minh can biet stack bat buoc cua BLUEBIRD va ty le budget bon tang nho trong lab de cau hinh cho dung, khong dung so thich project rieng. EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Cap nhat moi: voi du an cong ty BLUEBIRD-42, backend bat buo`

### E05 - episodic

`EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: Cong ty yeu cau chinh context window cho agent tren dung backend du an cong ty. Minh can biet stack bat buoc cua BLUEBIRD va ty le budget bon tang nho trong lab de cau hinh cho dung, khong dung so thich project rieng. EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Cap nhat moi: voi du an cong ty BLUEBIRD-42, backend bat buoc dung TypeScript voi NestJS; khong dung Python cho backend du an nay. Preference Python van dung cho `

### E07 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh is working on a personal project named ORCHID-27, for which he prefers Python. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, not Python. He has a deadline to complete a benchmark report for LAB-REPORT-1600 before Friday at 16:00. He recently debugged async HTTP, increasing the timeout to 60s, but it still failed. He is also addressing a concurrency issue related to connection churn in ASYNC-FIX-20 by reusing an aiohttp ClientSession with concurrency set to 20.  Minh prefers Python and dislikes Java. He wants a demo of his personal project ORCHID-27. He is learning async/await and often confuses coroutines with Tasks. He want`

### E11 - semantic

`EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST. EPISODE: {"id":"kb-async-http","entity":"Async HTTP Incident Playbook","summary":"When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST.","source":"incident-playbook-2026","updated_at":"2026-08-11T00:00:00Z"} metadata= EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing ti`

### E08 - long_term

`<USER_SUMMARY> Minh is working on a personal project named ORCHID-27, for which he prefers Python. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, not Python. He has a deadline to complete a benchmark report for LAB-REPORT-1600 before Friday at 16:00. He recently debugged async HTTP, increasing the timeout to 60s, but it still failed. He is also addressing a concurrency issue related to connection churn in ASYNC-FIX-20 by reusing an aiohttp ClientSession with concurrency set to 20.  Minh prefers Python and dislikes Java. He wants a demo of his personal project ORCHID-27. He is learning async/await and often confuses coroutines with Tasks. He wants explanatio`
