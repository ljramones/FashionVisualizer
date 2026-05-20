# Hero-Still Prompt Tuning Results

Run ID: `20260520T014558Z`
Run timestamp: `2026-05-20T01:47:10.638612+00:00`
Profile: `sdxl_turbo_preview`
Image size: `512x768`
Steps: `2`
Seeds: `42, 43`
Actions: `standing_right_hand_visible, slow_walk_right_hand_visible`
Contact sheet: `assets/outputs/prompt_tuning/20260520T014558Z/contact_sheet.png`

Manual review columns are intentionally blank for human scoring.

Current tuning focus: separate final catalog action from hero-stage action so the image model produces empty visible hands and clean placement space instead of hallucinated accessories.

| action | variant | seed | status | output | hand area usable? | no unwanted accessory? | model/action believable? | scene matches? | recommended? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| standing_right_hand_visible | strict_empty_hand_no_accessory_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/standing_right_hand_visible/strict_empty_hand_no_accessory_v1/3ce543eea4d42043/hero_still.png` |  |  |  |  |  |
| standing_right_hand_visible | strict_empty_hand_no_accessory_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/standing_right_hand_visible/strict_empty_hand_no_accessory_v1/cdcd61a6fb6b89d7/hero_still.png` |  |  |  |  |  |
| standing_right_hand_visible | studio_safe_pose_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/standing_right_hand_visible/studio_safe_pose_v1/3ce543eea4d42043/hero_still.png` |  |  |  |  |  |
| standing_right_hand_visible | studio_safe_pose_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/standing_right_hand_visible/studio_safe_pose_v1/cdcd61a6fb6b89d7/hero_still.png` |  |  |  |  |  |
| standing_right_hand_visible | minimal_accessory_free_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/standing_right_hand_visible/minimal_accessory_free_v1/3ce543eea4d42043/hero_still.png` |  |  |  |  |  |
| standing_right_hand_visible | minimal_accessory_free_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/standing_right_hand_visible/minimal_accessory_free_v1/cdcd61a6fb6b89d7/hero_still.png` |  |  |  |  |  |
| slow_walk_right_hand_visible | strict_empty_hand_no_accessory_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/slow_walk_right_hand_visible/strict_empty_hand_no_accessory_v1/643ad669788b3ce3/hero_still.png` |  |  |  |  |  |
| slow_walk_right_hand_visible | strict_empty_hand_no_accessory_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/slow_walk_right_hand_visible/strict_empty_hand_no_accessory_v1/9a4078c350cb89f3/hero_still.png` |  |  |  |  |  |
| slow_walk_right_hand_visible | studio_safe_pose_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/slow_walk_right_hand_visible/studio_safe_pose_v1/643ad669788b3ce3/hero_still.png` |  |  |  |  |  |
| slow_walk_right_hand_visible | studio_safe_pose_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/slow_walk_right_hand_visible/studio_safe_pose_v1/9a4078c350cb89f3/hero_still.png` |  |  |  |  |  |
| slow_walk_right_hand_visible | minimal_accessory_free_v1 | 42 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/slow_walk_right_hand_visible/minimal_accessory_free_v1/643ad669788b3ce3/hero_still.png` |  |  |  |  |  |
| slow_walk_right_hand_visible | minimal_accessory_free_v1 | 43 | success_real_generation | `assets/outputs/prompt_tuning/20260520T014558Z/slow_walk_right_hand_visible/minimal_accessory_free_v1/9a4078c350cb89f3/hero_still.png` |  |  |  |  |  |

## Manual Review Notes

- The decoupled standing action improved the no-accessory result: several `standing_right_hand_visible` outputs have no obvious bag or purse.
- The slow-walk action still leaks handbag-like objects, especially around the relaxed hand. Keep it out of the product-compositing path for now.
- Best current review candidates are `standing_right_hand_visible` with `studio_safe_pose_v1` seed 42 and `minimal_accessory_free_v1` seed 43. Both need closer hand/placement inspection before product-lock work.
- Some standing outputs include small watermark-like text artifacts. The negative prompt already includes text and watermark terms, but this remains a review item.
- The prompt was shortened after earlier truncation warnings; SDXL Turbo may still trim the last token or two, but the empty-hand instructions now appear early in the prompt.
