# Scenario 001: Idle to full-body ragdoll

Status: starting fixture and scenario instructions reviewed and accepted by the user on 2026-09-06. Generator behavior is **not run** because no generator exists. This is development material, not a held-out test.

## Purpose

Evaluate the future Generate Ragdoll tool on rig-001 using continuous animation-to-physics blending. The tool must generate a whole-body setup from this input; manually fixing the generated scene does not count as passing.

The local starting file is `work/scenarios/scenario-001/start.blend`, relative to the repository root. It is a separate copy; `work/rig-001/Animated Human.blend` is unchanged. See [input/manifest.json](input/manifest.json) for hashes and storage status. The local scene is not distributed with this Git checkout yet.

## Fixed starting conditions

| Setting | Value |
| --- | --- |
| Blender | 5.1.2 |
| Rig / mesh | Human Armature / Human_Mesh; 41 bones |
| Animation | Existing Idle action, preserved with all other source actions |
| Units | Metric; 1 Blender unit = 1 meter |
| Character placement | 1.8 m evaluated mesh height at frame 1; lowest vertex 0.08 m above floor |
| Placement method | ScenarioPlacement parent, uniform scale 0.343518702904352; original rig local transforms retained |
| Floor | ScenarioFloor, 6 m by 6 m by 0.2 m; top at Z=0; passive box collider |
| Floor response | Friction 0.8; restitution 0; margin 0.001 m |
| Gravity | (0, 0, -9.81) m/s² |
| Rigid-body world | 10 substeps/frame; 20 solver iterations; cache frames 1–240 |
| Timeline | Frames 1–240 at 24 fps; nominal 10-second clip |
| Starting selection | Human Armature, Object Mode, frame 1 |
| Dependencies | Both image textures packed into the scene; no extra add-on needed to open input |

These are scenario settings, not global product defaults. The slight floor clearance gives the character room to drop; it is intentional and is not an initial penetration defect. Scene scale must be respected by the generator, including the placement parent.

## Blend schedule to apply after generation

| Frame | Blend | Meaning |
| --- | --- | --- |
| 1 | 0 | Existing animation |
| 24 | 0 | Last fully animated frame |
| 48 | 1 | Fully simulated ragdoll |
| 240 | 1 | Remain simulated through end of observation |

Set these keys to **linear interpolation**: frame 36 should have blend 0.5. The transition lasts one second. Physics must begin from the current animated state rather than reveal a body that already collapsed while its visible blend was zero. The implementation strategy for achieving this remains open.

The input has named timeline markers and an embedded SCENARIO_README text. They do not create a working blend property or keyframes. The generator must supply the actual control. Do not add a dummy control that makes the fixture appear to implement the tool.

## Run procedure

1. Record generator code revision, Blender version, and a new run ID. Start from a fresh copy of the hashed input, not a previous generated result.
2. Select Human Armature and press Generate Ragdoll once. Record errors, generated body/joint inventory, and bone-to-body mapping.
3. Key the generated rig blend using the schedule above. Record its exact property path and interpolation.
4. Clear any prior rigid-body cache, return to frame 1, and advance sequentially through every frame to 240. Do not grade a simulation by jumping directly to later frames without computing its history.
5. Record the whole clip. Inspect the transition at frames 24/36/48 and the final settling interval at frames 193–240. Include a view that exposes joint separation and floor contact.
6. Compare frames 1–24 against the untouched input animation and verify all body regions participate at full ragdoll. Review fingers/toes following their simulated parent; separate articulation is not yet a required design choice.
7. Check that source actions, weights, and unrelated scene objects remain intact and that generation did not bake animation. Save the generated output separately and complete the run report.

Do not press Bake simulation: baking/export has a separate task. The fixture has no generated physics bodies or joints; its only physics object is the passive floor.

## Grading and evidence

Use [the project acceptance criteria](../../../docs/acceptance.md), especially GEN-01 through GEN-08. Every check must have pass/fail/not-run status and supporting evidence. Fixture preparation results must not be counted as generator results.

Initial numerical limits accepted with the scenario review on 2026-09-06:

- No non-finite position, rotation, or velocity at any sampled frame.
- Before the blend begins, animated bone positions differ from baseline by at most 1 mm and rotations by at most 0.1 degrees.
- At full influence, mapped bones follow their configured physics-body offsets within 1 mm and 0.1 degrees.
- Connected joint anchors remain within 1 cm; collider penetration below the floor top remains within 1 cm. Visual mesh penetration is reviewed separately from collider penetration.
- Throughout frames 193–240, each physical body's linear speed is at most 0.05 m/s and angular speed at most 0.1 rad/s, or it is sleeping.

These are user-accepted initial tolerances, not evidence of a passing implementation. Do not relax them after a failure merely to pass it. User review must still assess motion quality, persistent jitter, implausible movement, and unintended pose jumps during the blend.

Required future run artifacts: complete playback recording, generated scene, tool output, body/joint mapping, frame-indexed measurements, source-preservation comparison, check statuses, and user feedback. Record incomplete evidence as not-run or incomplete, never a pass.

## What was actually verified

- [preparation.json](evidence/preparation.json): all 240 baseline frames evaluated with finite mesh positions; minimum baseline floor clearance about 0.0799 m; seven representative skeletal samples retained.
- [fresh-load.json](evidence/fresh-load.json): saved scene reopened with the expected settings, selection, packed textures, Idle action, no active physics bodies, and no ragdoll joints. Sampled poses differ over time.
- Neutral material previews of frames 1 and 120 were visually inspected. This was a spot check of baseline deformation, not a full human playback review or a material-fidelity test.
- The original user-edited rig hash is unchanged. No generator attempt has started.

## Manual reconstruction recipe

Start from the user-corrected source identified in the manifest. Select Idle, use frames 1–240 at 24 fps, and keep source actions and mesh weights. At frame 1, measure the evaluated mesh bounds; let H be its height. Parent the rig to a new ScenarioPlacement empty while preserving its transform. Uniformly scale the empty by 1.8/H, center the mesh bounds on world X/Y, and offset Z so the lowest vertex is 0.08 m. This scene used scale 0.343518702904352.

Relink each image by its name to the source Textures folder and pack both images. Add the floor and physics-world settings in the table. Add the timeline markers and review camera, select the rig at frame 1, then save a new compressed .blend. Do not overwrite the source. Rebuilding may produce a different binary hash; publish it as a distinct input revision rather than silently substituting it for the frozen artifact.
