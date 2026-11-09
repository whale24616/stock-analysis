# 해설 영상 제작 플레이북 (드론 전쟁 해부 10편 작업 방식 정리)

새 세션에서 다른 주제로 같은 방식의 영상을 만들 때, 이 파일 하나만 읽고 그대로 이어서 일할 수 있도록 정리한 문서입니다.
기준이 된 작업: `drone-series/` (「드론 전쟁 해부 / Drone War Decoded」 EP01–EP10, 2026년 10–11월 제작).

새 세션에 처음 할 말 예시:
> "`VIDEO_PLAYBOOK.md`를 읽고 그 방식 그대로 [새 주제] 시리즈를 만들자. 먼저 기획안부터 보여줘."

---

## 1. 무엇을 만드는가

- **형식:** 한국어 내레이션 교육용 해설 영상. 편당 약 8분, 1920×1080, 24fps.
- **화면:**
  - **연필 그림(P 장면):** AI 생성 흑백 연필화에 천천히 줌·팬 효과를 줍니다.
  - **선화 장면(L 장면):** 코드로 그린 도표, 지도, 아이콘 애니메이션. 어두운 배경에 흰색·주황·빨강 선을 씁니다.
- **글자:** 화면 라벨은 영어 대문자, 자막은 한국어(Gmarket Sans Bold).
- **출처 표시:** 사실이 나오는 장면마다 오른쪽 아래에 작은 글씨로 넣습니다. 예: `SOURCE: … · CLAIM`.
- **역할 분담:**
  - **사용자:** ElevenLabs로 내레이션을 녹음해 GitHub에 올립니다.
  - **Claude:** 나머지 전부를 맡습니다. 기획, 대본, 사실 확인, 그림, 장면, 렌더링, 업로드, 유튜브 제목·설명·섬네일.

---

## 2. 사용자의 고정 원칙 (반드시 지킬 것)

**돈과 개인정보**
1. **결제·구매·자동 충전·개인정보 연결은 절대 하지 않는다.** Higgsfield는 생성 용도로만 쓴다. 크레딧이 0이면 멈추고 알린 뒤, 기존 그림 재사용과 선화 장면으로 대체한다.
2. **크레딧을 쓰기 전에 예상 크레딧을 먼저 말한다.** 예: "그림 20장, 약 5크레딧".

**저장소**
3. **큰 파일(영상, zip)은 GitHub에 커밋하지 않는다.** 오디오 mp3는 괜찮다. 영상은 Higgsfield 라이브러리에 올리고 링크를 준다.

**사실과 출처**
4. **모든 사실은 확인하고 화면에 출처를 표시한다.**
   - 한쪽 발표: `CLAIM`
   - 독립 확인이 없는 보도: `REPORTED` 또는 `NOT VERIFIED`
   - 개발사 발표: `MAKER CLAIM`
   - 단순 계산: `CALCULATION · ILLUSTRATIVE`
   - 과장돼 보이는 숫자는 원출처까지 따져 보고, 빼거나 맥락을 단다.
5. **위험한 무기 세부 정보는 다루지 않는다.** 탄두 무게, 제작·설정·유도 방식, 주파수 등. 원리와 공개 보도("○○에 따르면")는 괜찮다.

**대본 구조**
6. **"이번 편이 마지막일 수 있다"는 기준으로 쓴다.**
   - 대본 중간에 다음 편 예고를 넣지 않는다.
   - 다음 편 소개는 마지막 문단 한 문장에만 넣고 "…함께 살펴 보시죠"로 끝낸다.
   - 구독 요청은 넣지 않는다.
   - 이전 편 언급("3편에서 본")은 괜찮다.
   - 이미 앞 편에서 쓴 인용·수치는 다시 쓰지 않는다.

**그림**
7. **인물과 장비를 정확히 그린다.**
   - 나라별 인물 모습을 맞춘다. 드론 시리즈에서는 우크라이나인을 동유럽인으로 그렸다.
   - 기체 모양이 정확해야 한다. 예: Tu-95는 터보프롭 4개, F-16은 엔진 1개·꼬리날개 1개.
   - 배경에 엉뚱한 나라 랜드마크가 들어가면 다시 만든다. 예: 키이우 장면에 모스크바식 고층 건물.

**오디오**
8. **녹음된 말 속도와 쉼(약 0.5초)을 그대로 둔다.**
   - 클릭음과 꼬리 잡음은 없앤다.
   - 실제 음절은 절대 자르지 않는다.

**자막**
9. **Gmarket Sans Bold, 한 줄 최대 26자.**
   - 한 글자 앞꾸밈말(한·두·세·새·첫·큰·약·서·더·잘 등)은 다음 줄로 넘긴다.
   - 의존명사(수·데·번·것·때·대·배 등)는 앞말과 붙인다.
   - 이름, 단위가 붙은 숫자, 붙어 다니는 말은 가르지 않는다.

**소통**
10. **GitHub에 올리면 링크를 준다.** 오디오를 올릴 업로드 링크도 매번 준다.
11. **"결과/의견을 먼저 보여줘"라고 하면, 고치기 전에 분석과 제안부터 보여준다.**
12. **완성된 편은 사용자가 요청할 때만 손댄다.** 드론 시리즈 때 "5편 영상 건들지 말고".

---

## 3. 저장소 구조 (드론 시리즈 기준, 새 주제도 같은 틀 권장)

```
<series>/
  SERIES_PLAN*.md, SERIES_TITLES.md     기획안, 확정된 편 제목
  narration_ko/EPNN_<Slug>_Narration_KO.txt   한국어 대본 (한 줄 = 한 문장, 빈 줄 = 단락)
  narration_en/EPNN_<Slug>_Narration_EN.txt   영어 1:1 대본 (문장 수 반드시 같게)
  epNN/sources.md                        출처표 (내용 | URL | 화면 표기), "넣지 않은 것"
  deliverables/                          사용자 오디오 업로드 위치, 대본 사본
  deliverables/youtube/EPNN_YouTube_KO.txt   제목·후보·섬네일 URL·설명·목차·출처·해시태그
  tools/make_thumbnails.py               섬네일 생성 (편별 설정 dict 추가)
  tools/audio_check.py                   클릭 검사, 문장 사이 잡음·속도 검사
  tools/scene_check.py                   선화 장면 미리보기 + 출처 글씨 겹침 검사
  ep01_v2/                               렌더 엔진
    render.py  align.py  gfx.py  scenes.py
    shots_epNN.py   scenes_epNN.py   images.json (그림 이름 → URL)
    timing_EPNN_audio.json   EPNN_audio.mp3 (클릭 제거본)
    fonts/  img/ (그림 캐시, 커밋 안 함)  out/ (커밋 안 함)
```

**새 주제를 시작할 때:**
- `drone-series/`의 `ep01_v2/`(엔진), `tools/`, 폴더 틀을 새 폴더(예: `<new-series>/`)로 복사한다.
- `render.py`의 대본 경로 규칙(`narration_ko/EP{NN}_*_Narration_KO.txt`)은 그대로 쓴다.
- `set_episode(ep)`는 첫 번째로 정렬되는 파일을 고른다. 같은 편 번호의 옛 대본은 `narration_ko/archive_v1/` 같은 하위 폴더로 옮긴다.
- 엔딩 카드와 제목 카드의 시리즈 이름은 `scenes.py`의 `title_card`·`end_card`에 들어 있다("DRONE WAR DECODED"). 새 시리즈 이름으로 바꾼다.
- `KEEP_TOGETHER`, `FORWARD_MODIFIERS`, `BOUND_NOUNS`(render.py)는 그대로 두고 필요한 말만 추가한다.

---

## 4. 한 편을 만드는 순서

### 4-1. 기획 (시리즈 처음 한 번)
- 편 목록(제목 KO/EN, 여는 장면, 내용, 주요 출처)을 `SERIES_PLAN.md`로 만든다. 사용자 확인을 받은 뒤 확정한다.
- 제목은 생동감 있고 현재 시점 기준으로 짓는다.

### 4-2. 대본 (KO)
- **조사:** WebSearch를 `extended` 모드로, 여러 검색을 한 번에 보낸다.
  - 최신 숫자와 날짜, 누가 말했는지까지 확인한다.
  - 원문 페이지가 안 열리면 검색 요약으로 확인하고, sources.md에 "업로드 전 원문 확인 필요"라고 적는다.
- **구성(약 8분 기준):** 90–100문장, 공백 제외 약 2,900자.
  - 길이 추정: 공백 제외 글자 수 × 0.1655초 + 12초(시작 3초 + 제목 카드 3.2초 + 끝 화면 4초 + 여유) ≈ 완성 영상 길이.
  - 실측 예: 2,944자 → 8분 08초, 3,231자 → 8분 39초.
- **단락 흐름:**
  1. 여는 장면 (구체적 날짜·장소·장면)
  2. "오늘은 … 쉽게 풀어 보겠습니다."
  3. 3–5개 본문 단락
  4. 한계와 반론 단락 ("다만 …은 확인되지 않았습니다")
  5. 정리
  6. 마지막 문장에 다음 편 소개
- **문체:** 쉬운 말과 짧은 문장. 주장에는 "○○는 …라고 밝혔습니다/보도가 나왔습니다"를 붙인다.
- **사실 확인을 마친 뒤:**
  - 불확실한 날짜는 빼거나 "그 뒤로는"처럼 바꾼다.
  - 추측으로 쓴 수식어("몇 주씩")는 근거가 없으면 지운다.
  - 같은 편에서 숫자 표현이 서로 어긋나지 않는지 확인한다.

### 4-3. 영어 대본, 출처표
- 영어는 1:1로 옮기고 문장 수가 같은지 확인한다: `diff <(grep -c . KO) <(grep -c . EN)`.
- `epNN/sources.md`에는 다음을 적는다:
  - 표: 대본 내용 | 출처 URL | 화면 표기
  - "넣지 않은 것": 위험 세부 정보, 다른 편과 겹치는 내용, 미확인 단일 출처
  - 표기 원칙
- 대본 사본을 `deliverables/EPNN_Narration_KO.txt`, `deliverables/EPNN_Narration_EN.txt`로 둔다.

### 4-4. 자막 줄바꿈 미리 확인
```bash
cd <series>/ep01_v2 && python3 -c "
import render; render.LANG='ko'
for s in [l.strip() for l in open('../narration_ko/EPNN_..._KO.txt') if l.strip()]:
    c=render.chunks(s)
    if len(c)>1: print(' | '.join(c))"
```
- 이상하게 갈린 곳을 찾는다. 예: "로봇 / 포탑", "시속 / 416킬로미터", "2천 / 대까지".
- 고치는 방법:
  - `KEEP_TOGETHER`에 그 구절을 추가한다.
  - 규칙이 필요하면 `_cut_ok`에 넣는다. 예: '시속' 뒤에서는 끊지 않는다.
- 다른 편이 여전히 불러와지는지 확인한다: `render.set_episode(n); len(render.sentences())`.

### 4-5. 이 시점에 사용자에게 보고
- 대본 링크, 구성 요약, 새로 넣은 사실, 뺀 것, 예상 길이를 알린다.
- 오디오 업로드 링크를 준다: `https://github.com/<owner>/<repo>/upload/<branch>/<series>/deliverables`
- 파일 이름은 `EPNN_audio.mp3`로 안내한다.
- 다음 작업(그림 장수와 예상 크레딧)을 물어본다.

### 4-6. 연필 그림 (Higgsfield)
- **크레딧 먼저 확인:** `balance`. 0이거나 free 플랜이면 생성이 막힌다("Requires basic plan or higher"). 결제하지 말고 알린다.
- **모델:** `gpt_image_2_5`, 16:9, 장당 0.25크레딧. `generate_image_batch`의 `requests: [{index, params:{model, aspect_ratio, prompt}}]`.
  - **한 번에 최대 8장, 배치는 하나씩 차례로 보낸다.** 동시에 보내면 429 rate limit.
  - 기다릴 때는 `jobs_wait`의 `jobs: [{index, job_id}]`, `timeout_seconds` 15를 쓴다.
- **프롬프트 끝에 항상 붙이는 문장:**
  > Monochrome graphite pencil and charcoal illustration on textured off-white paper, soft smudged shading, cinematic lighting, hand-drawn storybook documentary style, grayscale only, no color, no text, no letters, no logos, no flags.
- **사람:** "Eastern European …"처럼 인물 모습을 명시한다.
- **장비:** 정확한 특징을 적는다. 예: "single engine, single vertical tail".
- **nsfw로 거부될 때:** 무기·작업장·부상 표현을 순하게 바꿔 다시 보낸다. 예: "engineering classroom", "injured soldier resting on a cot".
- **결과 URL 기록:** `images.json`에 `"epNN_00_name": "<url>"`로 넣는다. 그림 이름은 `eN_NN_짧은설명`.
- **이전 편 그림 재사용**은 크레딧을 아끼는 데 아주 유용하다. 9·10편은 크레딧 0이라 재사용과 선화만으로 만들었다.
- **검토 (반드시 직접 본다):** 샌드박스에서 묶음 이미지를 만들어 `sandbox_exec`의 `image_paths`로 확인한다. 한 번에 512KB 이하.
  - 확인할 것: 인물 모습, 기체 정확도, 배경 랜드마크, 엉뚱한 장비(다연장 로켓처럼 보이는 것 등).
  - 문제가 있으면 다시 만든다(장당 0.25크레딧).
  - 확인용 묶음 이미지에 붙인 붉은 파일명은 영상에 들어가지 않는다. 사용자에게도 그렇게 설명한다.

### 4-7. 장면 배치 (`shots_epNN.py`)
```python
SOURCES = {"key": "SOURCE: OUTLET, MON YYYY · CLAIM", ...}
P, L = "P", "L"
SHOTS = [
  dict(at="문장 앞부분 그대로", kind=P, img="eN_00_name", move="in", fade_in=2.5),  # 첫 장면
  dict(at="…", kind=L, scene="eN_scene", ph=0, src="key"),
  dict(dur=3.2, kind=L, scene="eN_title"),          # 7번째 문장 뒤 제목 카드 (오디오에 3.2초 무음이 들어감)
  ...
  dict(dur=4.0, kind=L, scene="eN_endcard"),        # 끝 화면
]
```
- `at`은 문장 앞부분과 정확히 같아야 한다(공백 포함). 대본을 고치면 `at`도 같이 고친다.
- `move`: in / up / right / left. 같은 그림을 연달아 쓸 때는 move를 바꾼다.
- 출처가 필요한 장면에는 빠짐없이 `src`를 붙인다.
- 검증:
```bash
python3 -c "import render; render.set_episode(N); s=render.sentences(); render.estimate(s); sh=render.build_timeline(s); print(len(s), len(sh))"
```
- 빠진 장면, 그림, 출처 키가 없는지도 확인한다. 추정 길이는 실제보다 약 1.26배 길게 나온다.

### 4-8. 선화 장면 (`scenes_epNN.py`)
- **함수 형식:** `def eN_name(cv, s, T, ph=0)`. `s`는 장면 시작 후 초, `ph`는 같은 장면의 단계.
  - 파일 끝에 `SCENES = {k: v for k, v in globals().items() if k.startswith("eN_") and callable(v)}`.
- **그리기 도구(gfx.Canvas):**
  - `text(xy, s, size, col, anchor="mm", alpha)`, `rect(box, w, col, fill=, radius=)`, `line(pts, w, col)`
  - `circle(c, r, w, col, fill=)`, `arc(c, r, a0, a1, w, col)`(도 단위), `arrow(p0, p1, w, col, prog, head)`, `dot`, `tag`(테두리 글자)
- **보조 함수:**
  - `backdrop(cv, s, "grid"|"radar")`, `title_card`, `end_card`, `seg(s, start, dur)`(0→1), `ease`, `lerp`, `cross`, `check`
  - 앞 편 아이콘을 import해서 다시 쓴다. 예: `geran`, `quad_top`, `turret`, `ugv`, `person`, `shield`, `spear`, `photo_card`.
- **화면 규칙:**
  - 1920×1080 기준이다.
  - 자막이 들어가는 아래쪽(y 약 900 이상)은 비운다.
  - **오른쪽 아래 출처 글씨 자리(y 796–840, 출처 폭만큼)에는 아무것도 그리지 않는다.**
  - 영어 라벨은 대문자로 짧게 쓴다.
- **검사(필수):**
  ```bash
  cd ep01_v2 && python3 ../tools/scene_check.py N <scratch>/sheets
  ```
  - `ERROR`(그리기 오류)와 `OVERLAPS SOURCE LABEL`(출처 겹침)은 모두 고친다.
  - 묶음 이미지를 Read로 열어 한 장씩 본다. 확인할 것: 글자 겹침, 화면 밖으로 나간 그물·선, 지도 방향, 의미에 맞는 아이콘.

### 4-9. 섬네일
- `tools/make_thumbnails.py`의 `EPISODES`에 설정을 추가한다:
  ```python
  dict(ep=N, img=..., side="left|right", lines=["첫 줄","주황 둘째 줄"], sub="검은 띠 문구", tag="빨간 태그")
  ```
- 샌드박스에서 left와 right 두 버전을 만들어 직접 보고, 그림의 중요한 부분을 가리지 않는 쪽을 고른다.
- 업로드 순서: `media_upload`(jpg) → 샌드박스에서 `curl -X PUT -H "Content-Type: image/jpeg" -H "If-None-Match: *" --upload-file … '<url>'` → `media_confirm`.

### 4-10. 유튜브 텍스트 (`deliverables/youtube/EPNN_YouTube_KO.txt`)
- 이전 편 파일을 틀로 쓴다. 들어갈 항목:
  - `[제목]`: `[실전] 핵심 문구 | 2026 … | 시리즈명 EPNN`
  - `[다른 제목 후보]` 2개
  - `[섬네일]` URL
  - `[설명]` 3–4문장
  - `■ 목차`: `0:00 …`, 나머지는 `?:??`로 두었다가 오디오 뒤에 채운다.
  - `■ 시리즈` 소개
  - 안내문(※): AI 일러스트, AI 음성, CLAIM 표기, 교육용
  - `■ 출처 (YYYY년 M월 확인)`: `· 매체 날짜 (내용) URL`
  - 해시태그

---

## 5. 오디오가 올라온 뒤

### 5-1. 클릭 제거와 검사 (로컬)
```bash
git pull origin <branch>
ffmpeg -v error -y -i deliverables/EPNN_audio.mp3 \
  -af "adeclick=w=55:o=75:a=2:t=2,adeclick=w=55:o=75:a=2:t=2" -ac 1 -ar 44100 -b:a 128k <scratch>/epNN_dc.mp3
python3 tools/audio_check.py clicks deliverables/EPNN_audio.mp3 <scratch>/epNN_dc.mp3   # 처리본은 0이어야 함
cp <scratch>/epNN_dc.mp3 ep01_v2/EPNN_audio.mp3   # 커밋, 푸시
```

### 5-2. 문장 정렬 (Higgsfield 샌드박스)
- **샌드박스는 자주 새로 만들어진다.** `sandbox_created: true`가 보이면 다시 준비한다:
  ```bash
  cd /home/user && git clone -q --depth 1 -b <branch> https://github.com/<owner>/<repo>.git sa
  cd sa/<series>/ep01_v2 && curl -sfL -o fonts/GmarketSansTTFBold.ttf \
    https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansBold.woff
  python3 -c "import render; render.fetch_images()"   # 그림 전체 다운로드 (오래 걸리면 background)
  ```
  - Gmarket 글꼴이 없으면 자막이 다른 글꼴로 나온다. 반드시 받는다.
- 이미 있으면 `git checkout -- . && rm -f timing_epNN.json && git pull`.
- **정렬은 `background: true`로 실행한다(약 4–5분).** nohup이나 &는 쓰지 않는다.
  ```bash
  cd .../ep01_v2 && python3 align.py EPNN_audio.mp3 ko N > /home/user/alN.log 2>&1; echo END >> /home/user/alN.log
  ```
- 진행 확인은 `sleep 55; tail -1 log`로 한다. 명령 하나는 60초를 넘기면 끊긴다.
- 끝나면 `timing_epNN.json`을 출력해 로컬로 가져온다.
- **로컬 파일은 `[{"start":a,"end":b}, …]` 형식으로 저장한다.** 리스트 형식이면 render.py가 오류를 낸다.

### 5-3. 속도와 잡음 검사, 시점 보정
```bash
python3 tools/audio_check.py gaps ep01_v2/EPNN_audio.mp3 <timing.json> narration_ko/EPNN_..._KO.txt
```
- **문장 사이에 큰 소리가 잡히면** 30ms 단위 에너지를 출력해 판단한다.
  - 다음 문장이 일찍 시작한 경우가 대부분이다. 그 문장의 start를 소리가 시작되는 지점(-40dB를 넘는 곳)보다 조금 앞으로 옮긴다.
  - 진짜 꼬리 잡음이면 무음 처리한다: `volume='if(between(t,a,b),(b-t)/d,if(between(t,b,c),0,1))':eval=frame`. 페이드는 약 35ms. 음절 경계는 ZCR로 확인한다(ㅅ 같은 마찰음은 ZCR이 높다).
- **속도 경고**(8.6자/초 초과)는 짧은 문장이면 대부분 정상이다. 끝 시점만 소리가 끝나는 지점으로 맞춘다.
- **목차 시간 계산:** 그 장의 첫 문장 start + 3.0(시작 무음) + 3.2(제목 카드가 7번째 문장 뒤에 있으므로, 8번째 문장부터 더한다).
  - `?:??`를 차례로 채우고 커밋한다.

### 5-4. 렌더링과 업로드
1. 업로드 URL을 받는다: `media_upload`(mp4). URL을 샌드박스 `/home/user/up_epN.txt`에 저장한다.
   - **URL은 한 번만 쓸 수 있다**(`If-None-Match: *`). 다시 렌더링하면 새 URL을 받는다.
2. 렌더는 `background: true`, `size: "xl"`로 실행한다. 80–100컷이면 약 4–6분, 15분 제한 안에 끝난다.
   ```bash
   cd /home/user/sa && git checkout -- . && git pull -q origin <branch>; cd <series>/ep01_v2 && rm -rf out/seg out/epNN_ko.mp4 && \
   python3 render.py --ep N --jobs 8 --timing timing_EPNN_audio.json --audio EPNN_audio.mp3 --out out/epNN_ko.mp4 > /home/user/rN.log 2>&1 && \
   ffprobe -v error -show_entries format=duration -of csv=p=0 out/epNN_ko.mp4 >> /home/user/rN.log && \
   curl -sf -o /dev/null -w "HTTP %{http_code}\n" -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" \
     --upload-file out/epNN_ko.mp4 "$(cat /home/user/up_epN.txt)" >> /home/user/rN.log; echo END >> /home/user/rN.log
   ```
3. 진행 확인: `grep -c done /home/user/rN.log`. 끝나면 `HTTP 200`을 확인하고 `media_confirm`(type video)을 호출한다.
4. **완성 영상 점검:**
   - 무음 구간 확인: `silencedetect=n=-40dB:d=2`. 시작 약 3초, 제목 카드 3.2초, 끝 화면 외에는 없어야 한다.
   - 화면 6–8장을 뽑아 묶음 이미지로 직접 본다. 자막 글꼴, 출처, 겹침, 그림을 확인한다.
5. 문제가 있으면 고치고 새 URL로 다시 렌더링한다. 렌더 중에 멈춰야 하면 `pkill -f "render.py --ep N"`.

### 5-5. 완료 보고 (사용자에게)
- 영상 URL, 길이
- 오디오 처리 결과: 클릭 몇 곳, 잔음 여부, 시점 보정한 문장
- 직접 확인한 것과 고친 것
- 목차(붙여 넣기용 코드 블록 포함)와 유튜브 텍스트 링크, 섬네일 URL
- 쓴 크레딧
- 다음 편 제안

---

## 6. 보고와 소통 방식

- **사용자에게 쓰는 글은 한국어**, 짧은 단락과 목록으로 쓴다. 날짜와 숫자를 분명히 하고 출처 표기 방식을 함께 말한다.
- **깃허브 링크:**
  - 파일: `https://github.com/<owner>/<repo>/blob/<branch>/<path>`
  - 캐시 문제로 옛 내용이 보이면 커밋 해시 링크를 준다: `blob/<hash>/<path>`
- **작업이 길어질 때**("작업 중에 소식이 없다"는 알림이 오면) 지금 하는 일을 한 줄로 알린다.
- **하루를 마칠 때**("백그라운드 작업 있나?"):
  - 샌드박스 프로세스를 확인한다: `ps aux | grep -E "render.py|align.py|ffmpeg|curl"`
  - 커밋하지 않았거나 푸시하지 않은 것이 없는지 확인한 뒤 알린다.
- **커밋 메시지:** `EPNN: <무엇>` 형식에 attribution 줄을 붙인다. 지정된 브랜치에만 푸시한다.

---

## 7. 겪었던 문제와 해결 (같은 실수를 피하기 위해)

**자막**

| 증상 | 원인과 해결 |
|---|---|
| 자막이 "시 / 베이비", "디 / 인사이더", "1년 / 반"처럼 갈림 | `KEEP_TOGETHER`에 추가 |
| "줄지어 서 / 있습니다", "…할 / 때" | 앞꾸밈말·의존명사 목록에 추가 |

**오디오**

| 증상 | 원인과 해결 |
|---|---|
| 끝음절이 잘림 ("보겠습니다"에서 "니다"가 사라짐) | 자르는 위치를 음절 경계(ZCR) 뒤로 옮김. 실제 음절은 절대 자르지 않음 |

**렌더링·엔진**

| 증상 | 원인과 해결 |
|---|---|
| 렌더가 `list indices must be integers` 오류 | timing 파일이 리스트 형식. dict 형식으로 저장 |
| 엉뚱한 대본으로 렌더링됨 | 같은 편 번호의 옛 대본이 glob에 먼저 걸림. archive 폴더로 옮김 |
| 샌드박스에 옛 그림이 남아 바뀐 그림이 반영 안 됨 | `fetch_images()`는 이미 있는 파일을 건너뜀. images.json URL을 바꾸면 샌드박스의 `img/<name>.png`도 지우거나 새로 받음 |
| 장면이 그리다 죽음 (음수 너비 사각형 등) | 모든 장면을 여러 시점(s)으로 미리 그려 보기 (`scene_check.py`) |
| 선화가 출처 글씨와 겹침 | `scene_check.py`의 겹침 검사로 찾아 위로 옮김 |

**그림**

| 증상 | 원인과 해결 |
|---|---|
| Tu-95가 B-52처럼, 키이우 다리 그림에 모스크바식 건물 | 프롬프트를 구체적으로 써서 다시 생성. 그림은 반드시 직접 봄 |
| 그림 생성 거부 (nsfw) | 표현을 순하게 바꿔 재시도 |
| 그림 생성 거부 (429 rate limit) | 배치를 하나씩 차례로 |
| 그림 생성 거부 ("Requires basic plan") | 크레딧 0. 결제하지 말고 알린 뒤 재사용과 선화로 대체 |

**샌드박스·도구**

| 증상 | 원인과 해결 |
|---|---|
| 샌드박스 명령이 60초에 끊김 | 오래 걸리는 작업은 `background: true`, 확인은 `sleep ≤55` |
| 사용자가 깃허브에서 옛 목차(`?:??`)를 봄 | 캐시. 커밋 해시 링크를 주고, 목차를 메시지에도 붙여 줌 |
| WebFetch로 기사·이미지 도메인이 안 열림 | 검색 요약으로 확인하고, 업로드 전 원문 확인을 sources.md와 보고에 남김. 이미지 확인은 샌드박스 `image_paths`로 |

---

## 8. 새 시리즈 시작 체크리스트

- [ ] 주제, 편 수, 편당 길이(기본 8분), 시청자 수준을 사용자와 확인한다.
- [ ] 사용자 원칙(2장)이 그대로인지, 새 주제에 맞는 추가 원칙이 있는지 묻는다. 예: 인물 모습, 다루지 말아야 할 세부 정보.
- [ ] 엔진과 도구를 새 폴더로 복사하고, 시리즈 이름(제목 카드·끝 화면·유튜브 템플릿)을 바꾼다.
- [ ] 기획안 → 사용자 확정 → 1편 대본 → 사실 확인 → 영어·출처 → 자막 점검 → 보고(오디오 링크) → 그림·장면·섬네일·유튜브 텍스트 → 오디오 → 정렬·점검 → 렌더·업로드 → 목차 → 보고.
- [ ] Higgsfield 크레딧을 확인한다(`balance`). 그림이 많이 필요하면 예상 크레딧을 먼저 말한다.
- [ ] 편마다 커밋하고 푸시한다. 큰 파일은 커밋하지 않는다.
