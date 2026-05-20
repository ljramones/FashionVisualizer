# Hero-Still Prompt Tuning Results

Run ID: `20260520T010854Z`
Run timestamp: `2026-05-20T01:09:18.823754+00:00`
Profile: `sdxl_turbo_preview`
Image size: `512x768`
Steps: `2`
Seeds: `42, 43`
Contact sheet: `assets/outputs/prompt_tuning/20260520T010854Z/contact_sheet.png`

Manual review columns are intentionally blank for human scoring.

Initial visual review note: all six generated stills produced an unwanted handbag or purse-like accessory. The hotel lobby setting and editorial model framing are usable, but the hand/product area is not yet clean enough for product-locked compositing. Next tuning should strengthen no-bag constraints, test the `studio_safe_pose_v1` variant, or simplify the action away from walking.

| variant | seed | status | output | hand area usable? | no unwanted bag? | model/action believable? | scene matches? | recommended? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| editorial_empty_hand_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T010854Z/editorial_empty_hand_v1/8cd895924b6cbff4/hero_still.png` |  |  |  |  |  |
| editorial_empty_hand_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T010854Z/editorial_empty_hand_v1/5661c35bc901b205/hero_still.png` |  |  |  |  |  |
| natural_side_carry_space_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T010854Z/natural_side_carry_space_v1/8cd895924b6cbff4/hero_still.png` |  |  |  |  |  |
| natural_side_carry_space_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T010854Z/natural_side_carry_space_v1/5661c35bc901b205/hero_still.png` |  |  |  |  |  |
| minimal_accessory_free_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T010854Z/minimal_accessory_free_v1/8cd895924b6cbff4/hero_still.png` |  |  |  |  |  |
| minimal_accessory_free_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T010854Z/minimal_accessory_free_v1/5661c35bc901b205/hero_still.png` |  |  |  |  |  |
