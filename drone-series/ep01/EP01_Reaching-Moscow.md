# EP01 — "Reaching Moscow": How Ukraine's Long-Range Drones Work

> Series: **Drone War Decoded: How Ukraine Rewrote Modern Warfare**
> Runtime target: **9:45** · Narration: ~1,350 words @ 140 wpm · Language: English
> Higgsfield budget: **≈ 505 credits** incl. retakes (balance 918.8 → ~410 left)

---

## 0. 제작 메모 (Production notes)

- **[FACT-CHECK]** 표시된 수치·사건은 업로드 전 최신 공개자료(RUSI, ISW, CSIS, Oryx, Reuters, 각 제조사 발표)로 반드시 재확인.
- 제원은 화면에 출처 등급 태그를 붙인다: `REPORTED` (언론 보도) / `MANUFACTURER CLAIM` (제조사 주장) / `ESTIMATE` (분석가 추정).
- AI로 만든 사실적 장면에는 화면 좌하단에 `AI VISUALIZATION` 워터마크 + 유튜브 업로드 시 "변경/합성 콘텐츠" 체크.
- 기술 도해(단면도, 그래프, 지도)는 **AI 생성 금지** → After Effects / DaVinci Fusion / Blender로 제작.
- 무기 제조·개조 수준의 디테일은 넣지 않는다. 원리·개념 수준까지만.
- 실존 인물 얼굴, 실제 기업 로고 생성 금지.

### 소스 유형 범례
| 코드 | 의미 | 비용 |
|---|---|---|
| **HF** | Midjourney 키프레임 → Higgsfield image-to-video (Kling 3.0, std, 5s, sound off) | ~5 cr/회 (추정) |
| **HF★** | 히어로 샷: 1080p / pro 모드 | ~12–15 cr/회 (추정) |
| **MJ** | Midjourney 스틸 + 편집툴에서 Ken Burns(줌·팬) | Higgsfield 0 cr |
| **MG** | 모션그래픽 도해·그래프·텍스트 | 0 cr |
| **MAP** | 지도 애니메이션 | 0 cr |
| **PUB** | 공개 자료 화면(정부·제조사 공개 영상, CC 라이선스) — 라이선스 확인 필수 | 0 cr |

> 크레딧 단가는 추정치. Higgsfield 생성 화면에 표시되는 실제 크레딧을 확인하고 진행.

---

## 1. SCRIPT (Narration)

### [0:00–0:45] COLD OPEN

> Night. Somewhere south of Moscow, a radar operator watches a cluster of slow-moving dots crawl across the screen.
>
> They're not fast. Roughly the speed of a car on a highway. They've been in the air for hours.
>
> And they took off from Ukraine — more than five hundred kilometres away.
>
> Over the past few years, Moscow has gone from a city that felt untouchable to one where airports shut down and air-defence crews sit on rooftops. **[FACT-CHECK: airport closures, rooftop Pantsir reports]**
>
> Not because of ballistic missiles. Not because of an air force.
>
> Because of something that looks a lot like a small private aircraft — with nobody inside.
>
> This is how Ukraine's long-range drones actually work.

**[TITLE CARD: DRONE WAR DECODED — EP01: REACHING MOSCOW]**

### [0:45–1:45] CONTEXT — Why build a drone instead of a missile?

> In 2022, Ukraine had a problem. Russia could strike any Ukrainian city with cruise and ballistic missiles. Ukraine could not strike back deep inside Russia.
>
> Western partners supplied long-range weapons, but in limited numbers, and often with restrictions on where they could be used. **[FACT-CHECK: timeline of restrictions]**
>
> So Ukraine went looking for a weapon it could build itself, in large numbers, at a fraction of the cost of a missile.
>
> The answer was the long-range one-way attack drone — sometimes called a "kamikaze drone," though the engineering is closer to a light aircraft than a toy.
>
> Today, dozens of Ukrainian manufacturers produce them. Names like **Liutyi**, **UJ-22 Airborne**, **Bober**, and **FP-1**. Their targets: oil refineries, airbases, ammunition depots, and command sites — hundreds, sometimes more than a thousand kilometres from the front. **[FACT-CHECK: list of confirmed types and ranges]**
>
> To understand why they look the way they do, you have to start with one brutal engineering triangle.

### [1:45–3:15] SEGMENT 1 — The Airframe

> Every long-range drone designer is fighting three demands at once: **fly far, carry enough, cost little.** Improve one, and the other two get worse.
>
> The first answer is the wing.
>
> Look at a Liutyi: long, slender wings — what engineers call a **high aspect ratio**. That's the ratio of wingspan to wing width. Gliders use the same trick.
>
> Here's why. A wing creates lift by pushing air downward, but at the wingtips, high-pressure air from underneath curls around to the top, forming a vortex. That vortex is pure waste — it's called **induced drag**. A longer, thinner wing spreads lift across a wider span and weakens those tip vortices. Less drag means less fuel burned per kilometre.
>
> The second answer is where the propeller goes. Most of these drones use a **pusher** layout — the propeller at the back.
>
> That keeps the nose free for the payload and sensors, and it means the wing sees clean, undisturbed air instead of the turbulent wash from a propeller in front.
>
> The third answer is material. Instead of aerospace aluminium, many airframes use **composites, foam cores and simple tubing** — cheap, light, and quick to manufacture. A non-metallic body also reflects radar less strongly than a metal one. The engine, fuel system and payload are still metal, so these drones are not "stealthy" — just harder to see than their size suggests.
>
> Finally, balance. The heaviest items — fuel and payload — sit close to the **centre of gravity**, so the aircraft stays stable as fuel burns off over a long flight.

### [3:15–4:45] SEGMENT 2 — Propulsion and the Physics of Range

> Why a piston engine, and not a jet?
>
> Because at these speeds — roughly 150 to 200 kilometres per hour — a propeller driven by a small piston engine is far more fuel-efficient than a jet. Jets shine at high speed. At low speed, they drink fuel. **[FACT-CHECK: cruise speed range — REPORTED]**
>
> Aircraft designers have an equation for this, the **Breguet range equation**. Stripped down, it says range depends on three things:
>
> One — how efficiently the engine and propeller turn fuel into thrust.
> Two — how aerodynamically efficient the aircraft is: its **lift-to-drag ratio**.
> Three — how much of the take-off weight is fuel.
>
> That last part is the trap. Range depends on the *logarithm* of the weight ratio — meaning every extra litre of fuel buys you a little less range than the one before. And every kilogram of fuel is a kilogram you can't use for payload.
>
> That's the trade-off you see across the Ukrainian fleet. Some designs carry a small warhead a very long way. Others carry more over a shorter distance. Published figures for different types range from roughly **20 to more than 70 kilograms** of payload, and from **several hundred to over 1,500 kilometres** of range. **[FACT-CHECK: per-type figures, tag as REPORTED/MANUFACTURER CLAIM]**
>
> At highway speed, a thousand-kilometre mission takes **five to seven hours**. That long flight time shapes everything — especially navigation.

### [4:45–6:15] SEGMENT 3 — Navigation: Flying Blind for Six Hours

> Here's a problem most people never think about. Over a thousand kilometres, nobody can fly this drone by remote control.
>
> Radio needs line of sight, and because the Earth is curved, a low-flying aircraft disappears below the radio horizon within a few dozen kilometres. So for most of the mission, the drone is on its own.
>
> Its first tool is the **inertial navigation system** — accelerometers and gyroscopes that measure every turn and change of speed, and calculate position from them. It can't be jammed, because it doesn't listen to anything. But small errors add up. Every hour, the estimated position drifts further from reality.
>
> So the drone corrects itself with **satellite navigation** — GPS, Galileo, and others.
>
> And that's exactly what Russia attacks. Electronic warfare systems either drown the satellite signal in noise — **jamming** — or broadcast fake signals that make the drone think it's somewhere else — **spoofing**.
>
> Both sides have responded with **anti-jam antenna arrays**, sometimes called CRPA. Several antenna elements work together, detect the direction the jamming comes from, and electronically "turn a deaf ear" to it while still listening to the satellites.
>
> And when satellites fail completely, some systems are reported to use a third layer: **cameras that compare the ground below with stored maps** — a modern version of terrain matching, a technique first developed for cruise missiles. **[FACT-CHECK: which types reportedly use visual navigation]**
>
> Three layers — inertial, satellite, visual. Each one covers the others' weaknesses.

### [6:15–7:30] SEGMENT 4 — Getting Through the Air Defence

> Building the drone is half the job. The other half is planning a route through one of the densest air-defence networks in the world.
>
> Mission planners use intelligence on radar and missile positions to route drones through gaps — around known sites, along valleys, at **low altitude** where the Earth's curvature hides them from ground radar until the last moment.
>
> Then there's **saturation**. An air-defence battery can only track and engage so many targets at once. Launch enough drones on converging routes — mixed with cheap decoys — and some get through. **[FACT-CHECK: decoy use reported]**
>
> And then there's the math that matters most. An air-defence interceptor can cost several times more than the drone it destroys. **[FACT-CHECK: unit cost comparisons — ESTIMATE]** Even when the defender wins every engagement, it is spending more than the attacker. And every launcher guarding a refinery near Moscow is one launcher not protecting troops at the front.

### [7:30–8:30] IN THE FIELD

> The results are visible in public reporting.
>
> A sustained campaign against Russian **oil refineries** has, at times, taken a significant share of refining capacity offline. **[FACT-CHECK: % capacity figures & dates]**
>
> Strikes on **airbases** have reached aircraft hundreds of kilometres from the border.
>
> And the attacks on the Moscow region — most of them intercepted — have still repeatedly forced airports to suspend flights, and pushed Russia to put air-defence systems on buildings in and around the capital. **[FACT-CHECK]**
>
> The drone doesn't need to get through every time. It only needs to make the defender pay — everywhere, all the time.

### [8:30–9:20] LIMITS & COUNTER

> But these drones have real weaknesses.
>
> They're **slow**, giving defenders time to react. They're **loud** — the piston engine can be heard from the ground. They show up on radar. And their warheads are small compared with a cruise missile.
>
> Russia has adapted: **mobile fire teams** with machine guns and autocannons, short-range missile systems on rooftops, layered electronic warfare, and its own interceptor drones. **[FACT-CHECK]**
>
> Which raises the obvious question.
>
> If being slow is the weakness… what happens when you make it fast?

### [9:20–9:45] OUTRO

> In the next episode, we look at the new generation: **jet-powered missile-drones** — Palianytsia, Peklo, and the Flamingo — weapons that blur the line between a drone and a cruise missile.
>
> If you want to understand how a war is reshaping the future of air power, subscribe — and tell us in the comments which system you want us to break down next.

**[END CARD: EP02 — FASTER THAN DEFENSE]**

---

## 2. CUT LIST

> 총 51컷 · HF 14컷 · HF★ 4컷 · 나머지 MG / MAP / PUB (Higgsfield 미사용)
> MJ 공통 파라미터: `--ar 16:9 --style raw --v 7` (색감 통일: *cold teal night, desaturated, cinematic documentary*)
> HF 공통: Kling 3.0, std, 5s, **sound off**, 16:9 / 히어로는 1080p 또는 pro

### A. COLD OPEN (0:00–0:45)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 (MJ 키프레임 / HF 모션) | 예상 cr |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:05 | "Night." | 어두운 레이더 화면, 녹색 스윕 | MG | 레이더 UI 직접 제작 (점 6–8개 천천히 이동) | 0 |
| 2 | 0:05–0:10 | "radar operator…" | 어두운 지휘 벙커, 모니터 불빛, 얼굴 없는 실루엣 | HF | MJ: `dim military air-defense control room at night, operator seen from behind as silhouette, glowing green radar screens, cinematic documentary, cold teal light` / HF: `slow dolly-in toward the radar screen, subtle screen flicker` | 5 |
| 3 | 0:10–0:15 | "They're not fast…" | 저공 비행하는 무인기 실루엣, 밤하늘, 숲 위 | **HF★** | MJ: `small unmanned propeller aircraft with long slender wings and rear pusher propeller, flying low over dark pine forest at night, moonlight rim light, no markings, cinematic wide shot` / HF: `camera tracks alongside the aircraft, trees passing below, gentle motion blur` | 15 |
| 4 | 0:15–0:20 | "in the air for hours" | 지도: 우크라이나→모스크바 궤적 선 | MAP | 거리 라벨 "500+ km" | 0 |
| 5 | 0:20–0:28 | "Moscow… untouchable" | 밤의 대도시 스카이라인 원경, 탐조등 | HF | MJ: `distant night skyline of a large European capital, generic, searchlights in sky, haze, telephoto` / HF: `slow pan right, searchlights sweeping` | 5 |
| 6 | 0:28–0:35 | "airports shut down…" | 출발 안내판 'SUSPENDED' 연속 표시 | MG | 가상 공항 보드 (실제 공항명 X) | 0 |
| 7 | 0:35–0:45 | "nobody inside." + 타이틀 | 3번 기체가 화면을 지나가며 타이틀 등장 | HF | 3번 MJ 재사용 / HF: `aircraft flies away from camera into darkness` | 5 |

### B. CONTEXT (0:45–1:45)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 8 | 0:45–0:55 | "Ukraine had a problem" | 지도: 러시아 미사일 사거리 원 vs 우크라이나 | MAP | — | 0 |
| 9 | 0:55–1:05 | "Western partners…" | 사거리 제한 영역 시각화 | MAP | — | 0 |
| 10 | 1:05–1:15 | "build itself" | 작업장 조립 라인, 날개 부품, 작업자 손만 | HF | MJ: `small workshop assembling unmanned aircraft wings, composite panels on workbenches, workers' hands only, warm industrial light, documentary` / HF: `slow lateral slide along the workbench` | 5 |
| 11 | 1:15–1:25 | "closer to a light aircraft" | 비교 그래픽: 경비행기 vs 드론 실루엣 | MG | — | 0 |
| 12 | 1:25–1:35 | "Liutyi, UJ-22, Bober, FP-1" | 4개 기체 카드 (공개 사진 + 출처 태그) | PUB/MG | 공개 사진 라이선스 확인 / 없으면 실루엣 드로잉 | 0 |
| 13 | 1:35–1:45 | "refineries, airbases…" | 지도: 표적 유형 아이콘 확산 | MAP | — | 0 |

### C. SEGMENT 1 — Airframe (1:45–3:15)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 14 | 1:45–1:55 | "fly far, carry enough, cost little" | 삼각형 트레이드오프 도해 | MG | — | 0 |
| 15 | 1:55–2:05 | "Look at a Liutyi" | 기체 360° 회전 (스튜디오 배경) | **HF★** | MJ: `generic unmanned aircraft, high aspect ratio straight wings, slim fuselage, rear pusher propeller, twin tail booms, matte grey, studio dark background, product shot, 3/4 view` / HF: `slow orbit around the aircraft, studio lighting` | 15 |
| 16 | 2:05–2:20 | "aspect ratio… gliders" | 날개폭/익현 비율 도해 + 글라이더 비교 | MG | — | 0 |
| 17 | 2:20–2:40 | "induced drag… vortex" | 날개 끝 와류 애니메이션 (짧은 날개 vs 긴 날개) | MG | Blender 연기 시뮬 or AE 파티클 | 0 |
| 18 | 2:40–2:45 | (B-roll) | 비행 중 날개 끝 근접, 응결 와류 | HF | MJ: `close-up of a long thin aircraft wingtip in flight, faint wingtip vortex in humid air, dusk sky` / HF: `steady chase-cam, vortex trailing` | 5 |
| 19 | 2:45–2:55 | "pusher layout" | 후방 프로펠러 클로즈업 | HF | MJ: `rear pusher propeller of a small unmanned aircraft, spinning, close-up, overcast daylight` / HF: `propeller spinning, slight camera drift` | 5 |
| 20 | 2:55–3:00 | "clean air…" | 기류 도해: 트랙터 vs 푸셔 | MG | — | 0 |
| 21 | 3:00–3:08 | "composites, foam…" | 재질 분해도 (exploded view) | MG | 단순화된 개념도 (실제 설계도 X) | 0 |
| 22 | 3:08–3:15 | "centre of gravity" | 무게중심 마커 + 연료/탑재물 블록 | MG | — | 0 |

### D. SEGMENT 2 — Propulsion & Range (3:15–4:45)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 23 | 3:15–3:25 | "piston… not a jet" | 소형 피스톤 엔진 매크로 | HF | MJ: `macro shot of a small air-cooled two-cylinder aircraft engine on a test stand, cooling fins, workshop light` / HF: `slow push-in, subtle vibration` | 5 |
| 24 | 3:25–3:40 | "fuel-efficient… drink fuel" | 그래프: 속도 vs 연료효율 (프롭 vs 제트) | MG | 개념 곡선 (정량값 표기 X) | 0 |
| 25 | 3:40–4:00 | "Breguet range equation" | 수식 등장 → 3개 항 하이라이트 | MG | R = (η/c)·(L/D)·ln(W₀/W₁) | 0 |
| 26 | 4:00–4:15 | "logarithm… trap" | 로그 곡선: 연료 비율↑ 항속거리 증가 둔화 | MG | — | 0 |
| 27 | 4:15–4:30 | "20 to 70 kg… 1,500 km" | 기체별 탑재량-거리 산점도 (출처 태그) | MG | dataviz 규칙 적용 | 0 |
| 28 | 4:30–4:45 | "five to seven hours" | 시계 타임랩스 + 비행 궤적 | HF | MJ: `small unmanned aircraft silhouette crossing a vast landscape at dawn, long shadow, aerial wide shot` / HF: `time-lapse feel, light shifting from night to dawn` | 5 |

### E. SEGMENT 3 — Navigation (4:45–6:15)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 29 | 4:45–5:00 | "radio horizon" | 지구 곡률 단면 + 전파선 차단 도해 | MG | — | 0 |
| 30 | 5:00–5:15 | "inertial navigation" | 자이로·가속도계 개념 애니메이션 | MG | 3축 화살표 | 0 |
| 31 | 5:15–5:25 | "errors add up" | 예상 궤적 vs 실제 궤적 벌어짐 | MAP | 오차 원 확대 | 0 |
| 32 | 5:25–5:32 | "satellite navigation" | 궤도의 위성들, 신호선 | HF | MJ: `navigation satellites orbiting Earth, thin signal lines to the surface, dark space, realistic` / HF: `slow orbital drift` | 5 |
| 33 | 5:32–5:45 | "jamming… spoofing" | 신호 노이즈 vs 가짜 위치 점프 도해 | MG | 좌: 노이즈, 우: 위치 순간이동 | 0 |
| 34 | 5:45–5:50 | (B-roll) | 들판 위 트럭형 전자전 장비 실루엣 (일반형) | HF | MJ: `generic military truck with antenna masts in a snowy field at dusk, silhouette, no insignia` / HF: `slow push-in, antenna slight sway` | 5 |
| 35 | 5:50–6:00 | "anti-jam antenna arrays" | 다중 안테나 → 재밍 방향 '널' 빔 패턴 | MG | 빔 패턴 꽃잎 그래픽 | 0 |
| 36 | 6:00–6:10 | "cameras… stored maps" | 지상 영상 위 특징점 매칭 오버레이 | HF + MG | MJ: `top-down aerial view of farmland, roads and a river from 1,000 m altitude, overcast` / HF: `slow forward drift`, 위에 특징점 오버레이 합성 | 5 |
| 37 | 6:10–6:15 | "Three layers" | INS / GNSS / Visual 3층 아이콘 | MG | — | 0 |

### F. SEGMENT 4 — Air Defence (6:15–7:30)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 38 | 6:15–6:35 | "route… gaps" | 지도: 방공 원들 사이 경로 | MAP | 가상 배치 (실제 위치 X) | 0 |
| 39 | 6:35–6:45 | "low altitude… curvature" | 레이더 사각지대 단면도 | MG | — | 0 |
| 40 | 6:45–6:52 | (B-roll) | 강 계곡을 따라 저공 비행 | **HF★** | MJ: `small unmanned aircraft flying very low along a misty river valley at dawn, hills on both sides, cinematic aerial` / HF: `chase camera following low over water` | 15 |
| 41 | 6:52–7:10 | "saturation… decoys" | 레이더 화면 표적 수 증가 → 추적 한계 표시 | MG | — | 0 |
| 42 | 7:10–7:30 | "the math…" | 비용 비교 바 차트 (ESTIMATE 태그) | MG | — | 0 |

### G. IN THE FIELD (7:30–8:30)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 43 | 7:30–7:50 | "oil refineries" | 원경 정유시설, 연기 기둥 (폭발 묘사 X) | HF | MJ: `distant oil refinery at night with a large column of dark smoke and orange glow on horizon, telephoto, documentary` / HF: `static camera, smoke drifting slowly` | 5 |
| 44 | 7:50–8:05 | "airbases" | 지도: 공개 보도된 타격 지점 (출처 명시) | MAP/PUB | 공개 위성사진 사용 시 라이선스 확인 | 0 |
| 45 | 8:05–8:30 | "Moscow region… airports" | 6번 공항 보드 재사용 + 지도 | MG/MAP | — | 0 |

### H. LIMITS & OUTRO (8:30–9:45)

| # | 시간 | 내레이션 큐 | 화면 | 유형 | 프롬프트 | 예상 cr |
|---|---|---|---|---|---|---|
| 46 | 8:30–8:45 | "slow, loud, radar" | 약점 4개 아이콘 체크리스트 | MG | — | 0 |
| 47 | 8:45–9:00 | "mobile fire teams" | 야간 들판, 픽업트럭 위 대공 화기 실루엣, 탐조등 | HF | MJ: `night field, pickup truck with mounted anti-aircraft machine gun silhouette, searchlight beam into sky, soldiers as distant silhouettes, no faces` / HF: `searchlight beam sweeping slowly` | 5 |
| 48 | 9:00–9:10 | "rooftops" | 도시 옥상 위 방공 장비 실루엣 (일반형) | HF | MJ: `generic air-defense vehicle silhouette on top of a tall city building at night, city lights below, telephoto` / HF: `slow tilt up` | 5 |
| 49 | 9:10–9:20 | "make it fast?" | 화면 정지 → 하얀 섬광 컷 | MG | — | 0 |
| 50 | 9:20–9:35 | EP2 티저 | 제트 추진 기체가 매우 빠르게 지나감 | **HF★** | MJ: `sleek small jet-powered unmanned aircraft with short wings, flying fast at low altitude over steppe at dusk, motion blur, cinematic` / HF: `fast fly-by past camera, strong motion blur` | 15 |
| 51 | 9:35–9:45 | 구독 + 엔드카드 | 엔드카드 템플릿 | MG | — | 0 |

---

## 3. HIGGSFIELD 크레딧 예산

| 구분 | 컷 수 | 회당 cr (추정) | 시도 횟수 | 소계 |
|---|---|---|---|---|
| HF (std 720p, 5s, sound off) | 14 | ~5 | ×2.5 | ~175 |
| HF★ (히어로, 1080p/pro) | 4 | ~15 | ×3 | ~180 |
| 예비 (실패·거부 재시도) | — | — | — | ~150 |
| **합계** | | | | **≈ 505 cr** |
| **잔액 918.8 기준 남는 크레딧** | | | | **≈ 410 cr** |

**절약 팁**
1. **MJ 키프레임을 먼저 완성**하고, 마음에 드는 이미지에만 HF 영상 생성 → 영상 재시도 횟수가 크게 줄어듦.
2. 소리는 후반에 효과음으로 넣으므로 **sound off** 고정.
3. 프롬프트 검열 회피: `explosion`, `strike`, `missile hit`, `kamikaze` 같은 단어 대신 `smoke column`, `aftermath`, `glow on horizon`, `unmanned aircraft` 사용.
4. 3번 컷처럼 **같은 키프레임을 여러 컷에 재사용**(7번)해 일관성과 비용 둘 다 확보.

---

## 4. 사운드 & 그래픽 가이드

- **음악:** 저음 드론 앰비언트(0:00–1:45) → 미니멀 펄스(기술 세그먼트) → 긴장감 상승(6:15~) → 9:10 정적 → EP2 티저 업템포.
- **SFX:** 레이더 핑, 피스톤 엔진 웅웅거림(라이브러리), 바람, 무전 노이즈. 폭발음 남용 금지.
- **폰트:** 제목 — 산세리프 콘덴스드(예: Barlow Condensed), 본문 — Inter. 출처 태그는 모노스페이스.
- **컬러:** 배경 #0B1215, 강조 #3FD0C9(우크라이나 측 데이터), 경고 #E8A33D(러시아 측/방공), 텍스트 #E6EDF0.

---

## 5. 업로드 전 체크리스트

- [ ] 모든 `[FACT-CHECK]` 항목 출처 확인 후 태그 제거
- [ ] 제원 화면마다 REPORTED / MANUFACTURER CLAIM / ESTIMATE 태그
- [ ] AI 장면 `AI VISUALIZATION` 워터마크 + 유튜브 합성 콘텐츠 공개 체크
- [ ] PUB 소스 라이선스 및 크레딧 표기
- [ ] 설명란에 출처 목록 + 타임스탬프 챕터
- [ ] 썸네일: 3번 히어로 샷 + 텍스트 "1,000 KM. NO PILOT."
