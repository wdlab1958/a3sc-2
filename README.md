# a3sc-2 · AI 플랫폼 화면(6종)과 플랫폼 상세 화면

작성일: Nov. 25, 2026 · 갱신: Nov. 26, 2026 (플랫폼 구현 결과 반영)

에이쓰리시큐리티 사이트의 「AI 플랫폼」 화면(`/a3sc/ISMA3SC003M4.do`)을 플랫폼 6종 기준으로 다시 만든 것과,
카드의 「자세히 보기」로 이어지는 여섯 상세 화면이다. 구조는 `~/ai_project/a3sc`(One Cycle Dev. Framework)와 같다.

## 화면과 폴더

| 화면 | 폴더 | 운영 주소(제안값) | 본문 |
|---|---|---|---|
| AI 플랫폼 (6종) | `./` | `/a3sc/ISMA3SC003M4.do` (기존 화면 교체) | `fragment/ISMA3SC003M4_main.html` |
| 01 AIMES | `AIMES/` | `/a3sc/ISMA3SC003M11.do` | `AIMES/fragment/ISMA3SC003M11_main.html` |
| 02 TruthLens | `TruthLens/` | `/a3sc/ISMA3SC003M12.do` | `TruthLens/fragment/ISMA3SC003M12_main.html` |
| 03 A3 AutoFlow | `A3-AutoFlow/` | `/a3sc/ISMA3SC003M13.do` | `A3-AutoFlow/fragment/ISMA3SC003M13_main.html` |
| 04 NexusAI | `NexusAI/` | `/a3sc/ISMA3SC003M14.do` | `NexusAI/fragment/ISMA3SC003M14_main.html` |
| 05 Cluster-Master | `Cluster-Master/` | `/a3sc/ISMA3SC003M15.do` | `Cluster-Master/fragment/ISMA3SC003M15_main.html` |
| 06 PokerFace Pro | `PokerFace-Pro/` | `/a3sc/ISMA3SC003M16.do` | `PokerFace-Pro/fragment/ISMA3SC003M16_main.html` |

One Cycle Dev. Framework 화면은 `/a3sc/ISMA3SC003M5.do`(M5~M10 사용 중)이므로 상세 화면은 M11부터 잡았다. 주소는 제안값이다.

## 폴더 구성 (루트와 여섯 하위 폴더가 같은 모양)

```
fragment/<화면ID>_main.html   본문. 운영 레이아웃의 <main> … </main> 안에 넣는 부분
build_preview.py              머리글·바닥글을 붙여 미리보기를 만든다
<화면ID>.html                 운영 경로(/resources, /a3sc/…) 그대로인 미리보기
index.html                    폴더째 열어 보는 미리보기 (상대 경로, 검색 노출 차단)
reference/ISMA3SC003M4.html   기존 화면 사본 (머리글·바닥글의 출처)
resources/                    b.css, 글꼴, 로고 사본 + 추가 스타일
```

추가 스타일은 두 개다.

- `resources/css/A3/renewal/onecycle_product.css` (`.pd-`): One Cycle 상세 화면과 같은 파일. 일곱 화면 모두 쓴다.
- `resources/css/A3/renewal/aiplatform.css` (`.ap-`): AI 플랫폼 화면의 6종 카드. 루트에만 있다.

## 미리보기

```
cd ~/ai_project/a3sc-2 && python3 -m http.server 8931 --bind 127.0.0.1
# http://127.0.0.1:8931/  →  카드의 「자세히 보기」로 ./AIMES/ 등 이동
```

본문을 고친 뒤에는 그 폴더에서 `python3 build_preview.py` 를 다시 실행한다.

## 기존 화면에서 달라지는 것

- 상단 메뉴: 「정보센터」 뒤에 「One Cycle Dev. Framework」 추가 (`build_preview.py` 가 미리보기에 반영. 운영에서는 공통 레이아웃에서 추가)
- 전체 메뉴·바닥글: 「플랫폼 9종」 → 「플랫폼 6종」, One Cycle Framework 항목 추가
- 머리말·강점 문구: 여섯 플랫폼에서 확인된 사실에 맞춰 수정 (외부 전송 「원천 차단」, 「전 구간 암호화」 같은 일괄 표현 삭제)
- 본문: 9종 목록과 분류 버튼 → 6종 카드(자세히 보기), 「고르는 법」 표, One Cycle 연결 배너 (기존 A3 AI 포털 배너 자리)

## 내용 출처와 확인할 점

상세 화면의 수치와 기능은 각 프로젝트 폴더의 사용자 가이드·README·코드에서 확인한 것만 실었다. 원본 프로젝트와 `~/ai_project/webpage*` 폴더는 고치지 않았다.

| 플랫폼 | 출처 폴더 | 공개 전에 정할 것 |
|---|---|---|
| AIMES | `AIMES-AgriProcess`, `AIMES-Eleven` | 2026-11-26 반영: 이중 출고 결함 수정(CASE를 FIXED로), 예측을 「참고 지표」로, 도메인 상태를 「서비스 시험 통과 3 · 부분 구현 8」 기준으로 고침. 남음: 현장 데이터 학습 전까지 예측 표현 유지 |
| TruthLens | `TruthLens` | 2026-11-26 반영: 「데모」 화면 → 「모델 미설치 — 판정 불가」, 섞인 결과 문제 수정. 정확도 수치는 계속 싣지 않음(탐지 모델 · 데이터셋 미확보) |
| A3 AutoFlow | `04_AutoFlow` | 2026-11-26 반영: 계정 · 부서 권한, 승인함, 승인 결함 5건 수정, 구글 연동 기본 꺼짐. 남은 한계: 서버 한 대 구성, SSO · 다단계 인증 없음 |
| NexusAI | `NexusAI` | 2026-11-26 반영: 실행 확인된 프레임워크는 2종(CrewAI · LangGraph), 로컬 전용이 기본, 명령 실행 격리, Google 연결 사용자별 · 기본 꺼짐 |
| Cluster-Master | `Cluster-Master` | 2026-11-26 반영: 하트비트 결함 수정(CASE를 FIXED로), 격리 실행, 재배정, 시뮬레이션 표시. 남은 한계: 실제 여러 대의 PC 검증 없음 |
| PokerFace Pro | `PokerFace` | 2026-11-26 반영: 영상 연결 로그인 확인, 저장 암호화, 분석 전 별도 동의, 본인 기록만 삭제. 화면에 적지 않은 것: 기본 언어 모델(EXAONE 3.5)의 비상업 라이선스 — 결정 후 반영 |
