# Solver resolution findings — run-001

Status: development result awaiting review, not an accepted training example.

The user approved implementation on 2026-09-06. The generator creates 20 rigid bodies, 19 joints and 41 bone targets, with a keyable animation/physics blend. Both runs below use the same production code and 240-frame schedule in Blender 5.1.2. No source file or frozen input was overwritten.

| Measurement | Accepted limit | Original: 10 substeps / 20 iterations | Diagnostic: 30 / 100 |
| --- | --- | --- | --- |
| Animation position error | 1 mm | 0.00048 mm | 0.00048 mm |
| Physics bone position error | 1 mm | **4.704 mm — fail** | 0.777 mm |
| Joint anchor separation | 10 mm | 4.943 mm | 0.749 mm |
| Collider floor penetration | 10 mm | **12.389 mm — fail** | 0 mm |
| Maximum speed, frames 193–240 | 0.05 m/s | **0.1002 m/s — fail** | 0 m/s |
| Maximum angular speed, frames 193–240 | 0.1 rad/s | **1.1038 rad/s — fail** | 0 rad/s |

Generation, invalid/duplicate rejection, injected late-failure rollback, source action/mesh/weight/rest-bone preservation, unrelated scene preservation, whole-body coverage, finite transforms, blend schedule and kinematic release checks passed in both runs. Bone rotation errors were zero at the measured endpoints. Every frame was evaluated; both generated scenes reproduced all body positions and release states exactly after reopening in the same Blender build without loading add-on code. This is observed reproducibility, not a cross-platform determinism guarantee.

Reports: [original result](../dataset/tasks/task-0001/runs/run-001/result.json), [diagnostic result](../dataset/tasks/task-0001/runs/run-001/diagnostic-result.json), [fresh-load check](../dataset/tasks/task-0001/runs/run-001/fresh-load.json), [artifact manifest](../dataset/tasks/task-0001/runs/run-001/artifacts.json).

## Visual findings and remaining checks

Full 240-frame MP4 recordings and seven stills per run are retained locally. Assistant spot review of transition and final frames confirms a visible fall, but feet intersect the floor during the blended transition, including diagnostic frame 36. Numerical floor checks measure collision proxies, not the visible skinned mesh; a diagnostic numerical pass does not resolve this defect. The final pose and restrictive symmetric joint limits also need user review for anatomical plausibility. UI installation/interaction and undo have not been tested. Baking/export is deferred.

## Proposed next decision

Approve a distinct scenario input revision with **30 substeps per frame and 100 solver iterations**, retaining all existing tolerances and the original `start.blend`. The generated diagnostic scene and recording provide the concrete preview. The generator would continue preserving the scene's world settings. After approval, create/hash the revised input, update its manifest and scenario settings, and run it fresh as a new recorded attempt. Visual transition issues still need correction or explicit reviewed disposition before acceptance.

Approval is requested because [the approved plan](generator-plan.md) explicitly says: "Preserve the accepted floor/world settings while running the scenario; do not alter them merely to meet the tolerances." The diagnostic has not replaced the accepted test. The result suggests solver resolution contributes to the failures; it does not prove that tuning the generator could never pass the original settings.

## Reproduction and local review

From the repository root, run Blender 5.1.2 in background mode with `--factory-startup --disable-autoexec --python-exit-code 1 --python evaluation/checks/scenario_001.py -- --record`. The accepted test intentionally exits 1 when checks fail. Add `--diagnostic-high-accuracy` after `--` for the separate experiment; its report always says diagnostic-only.

Generated scenes and recordings are under `work/runs/task-0001/run-001/` and its `diagnostic-high-accuracy/` subfolder. Return to frame 1 and play sequentially when reviewing the saved setup. Restart/clear the simulation cache after edits. Render previews use a neutral material view, not texture-fidelity grading.

The local installable archive is `work/builds/ragdoll_lab-0.1.0.zip`. It contains the six add-on source modules, syntax checked by Blender's Python. It is a development build for the selected first rig. Use Generate Ragdoll at frame 1 in Object Mode, then key Ragdoll Blend in the Ragdoll Lab sidebar. Baking is visibly unavailable in this increment.
