# EP01 asset manifest (test build, 2026-10-10)

All AI assets live in the Higgsfield account library. The IDs below are Higgsfield **job IDs**;
use them to re-fetch results (e.g. Higgsfield `show_generation_by_ids` / `jobs_wait` return the result URL).
Download URLs are deliberately not stored here because they contain the account identifier.

Final test video (uploaded media): `bfb063b9-1c69-4eb2-a103-731fecd1369a` — `ep01_reaching_moscow_test_720p.mp4` (9:15, 720p, 38 MB)

## Credit usage (measured)

| Item | Model / settings | Unit cost | Count | Credits |
|---|---|---|---|---|
| Narration | `seed_audio`, preset voice **Arthur** (`30fc8796-ceb6-4a66-b3a7-4a145ef7f346`) | ~3.7 per 100 words | 9 sections | ~50 |
| Keyframes | `gpt_image_2_5`, 16:9 | 0.25 | 16 (+1 blocked) | ~4 |
| Motion clips | `kling3_0`, mode `std`, 5 s, sound off | 7.5 | 4 | 30 |
| Graphics / edit / pad | local (Pillow, ffmpeg, sox in Higgsfield sandbox) | 0 | — | 0 |
| **Total** | balance 918.8 → 830.9 | | | **~88** |

Other preflight prices seen: `nano_banana` image 1.0 · `seedance_2_5` 480p 5 s 15 · `grok_video_v15` 480p 5 s 12.5 · `minimax_h3_max` 768p 5 s 12.5.

## Narration (`audio/voN.wav`)

| File | Section | Job ID | Length |
|---|---|---|---|
| vo0 | Cold open | 87b64723-e1d9-4676-aab7-bc8db2760c16 | 50.3 s |
| vo1 | Context | 23d8d867-782a-4024-b669-7b818409bed0 | 75.3 s |
| vo2 | Airframe | 23ff7caf-d41a-4bd3-9104-492fcf66ebb1 | 95.6 s |
| vo3 | Propulsion & range | ce242c37-a37e-4098-82bf-109cf90b6055 | 82.3 s |
| vo4 | Navigation | ca8eeb9d-5d87-4783-bb12-3896e85392e8 | 85.7 s |
| vo5 | Air defence | b36132f1-688a-43e6-af0c-e9ae0e743bfa | 50.7 s |
| vo6 | In the field | 12b38148-f830-4937-9912-fef72e02e3e2 | 35.9 s |
| vo7 | Limits & counter | d81a9954-cbf0-42ad-bb3a-37ce96e7a00a | 48.2 s |
| vo8 | Outro | 1996f176-2e66-42c8-a5e1-2c43bcd64622 | 24.3 s |

Text sent per section: `narration.json` (minor punctuation tweaks for TTS pacing).

## Keyframes (`img/NN.png`, gpt_image_2_5, 16:9)

| NN | Job ID | Prompt (abridged) |
|---|---|---|
| 01 | c10cace6-17a8-4dbf-b6f3-05b443e610f8 | Dim air-defense control room at night, operator silhouette from behind, green radar screens |
| 02 | e67f1a91-4421-48c9-b4b4-28777824cb48 | Small pusher-prop UAV, long slender wings, low over dark pine forest at night, moonlight |
| 03 | 4bcb3015-bc04-4063-8b1e-b9132c917ddb | Distant night skyline of a generic European capital, searchlights in haze |
| 04 | c41115e7-f4eb-4930-a267-d08560e61326 | Workshop assembling UAV wings, gloved hands only, warm industrial light |
| 05 | 40ff2903-9c5a-4327-98c9-6cac468d06f4 | Generic UAV product shot, high-AR wings, twin booms, pusher prop, dark studio |
| 06 | 05ce4a4d-6f84-4025-86a1-77b838cdd924 | Long thin wingtip in flight at dusk, faint wingtip vortex |
| 07 | 1c7dfb97-ad8a-4a5e-ad87-dfcbc5e0c414 | Rear pusher propeller close-up, overcast daylight |
| 08 | 2a12de02-ce55-42dd-9a7d-741b35434b0c | Macro of small air-cooled two-cylinder piston engine on test stand |
| 09 | 49451227-00a8-4eaf-a628-ba538c7cb159 | Tiny UAV silhouette crossing vast landscape at dawn, mist |
| 10 | 42390089-6599-4942-8595-a8969896108a | Navigation satellites over Earth at night, signal lines |
| 11 | bb2203b6-32d7-4aef-a058-dd0a2dd5e1dc | Generic truck with antenna masts in snowy field at dusk, no insignia |
| 12 | aef52e0e-1d40-4dba-b694-97c13991688e | Top-down farmland, roads, river from 1000 m |
| 13 | ef0d766e-f5e5-431d-8648-a1f310c38684 | UAV flying low along misty river valley at dawn |
| 14 | a0793ce4-df0d-4e36-8dd3-8d02640e2168 | Distant refinery at night, smoke column, orange glow |
| 15 | 4811824e-6ed1-4690-82ce-1793519dfc84 | (blocked by moderation: pickup with mounted machine gun) — not used |
| 16 | ed6577ea-d069-45a2-a2e7-6dbf46b3af64 | Generic air-defense vehicle silhouette on city rooftop at night |
| 17 | cbb5931d-a7c1-4acc-85f9-8e649117a782 | Sleek small jet-powered UAV low over steppe at dusk, motion blur |

## Motion clips (`vid/NN.mp4`, kling3_0 std 5 s, start_image = keyframe NN)

| NN | Job ID | Motion prompt |
|---|---|---|
| 02 | cfec6b86-7849-4481-8862-17420bed038f | Tracking alongside aircraft over forest at night (declined auto-preset "IN THE DARK") |
| 05 | ce34b05c-11f5-477c-9403-4f5885b6ba2b | Slow studio orbit, rim light sliding over wings |
| 13 | 1d4e2f71-fbec-4f47-8213-b4ab049c8914 | Chase shot along misty river valley |
| 17 | fd9e8446-95d3-46c2-bd03-77960f3fc260 | Fast low fly-by over steppe (EP02 teaser) |

## Lessons for next episodes

- `gpt_image_2_5` rate-limits batches above ~8 → submit in groups of ≤ 6.
- Weapon-mounted vehicles trip image moderation; use generic "vehicle silhouette" wording.
- `generate_video` may return a preset recommendation instead of a job; resubmit with `declined_preset_id`.
- This Claude environment cannot download Higgsfield CDN files (network policy), so editing runs in the Higgsfield sandbox.
