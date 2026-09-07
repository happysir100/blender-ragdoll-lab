# Project Work Log

Last reconciled: 2026-09-06 (America/New_York).

## Current milestone

Build reviewed training/validation examples through development of a Blender ragdoll tool. Data collection does not itself retrain a model. Complete one reproducible, reviewed example before expanding to more rig families.

The user approved the first Generate Ragdoll implementation scope on 2026-09-06. The generator now exists, but the accepted 240-frame scenario fails three automated checks and the motion/workflow still needs human review. The full product also requires a separate Bake simulation button and exportable baked animation; baking/export is a subsequent task, not implemented in this increment.

Canonical references: [tool specification](docs/first-tool.md), [approved generator plan](docs/generator-plan.md), [architecture](docs/architecture.md), [acceptance](docs/acceptance.md), [scenario-001](dataset/tasks/task-0001/scenario.md), [dataset structure](docs/dataset-structure.md), [run-001](dataset/tasks/task-0001/runs/run-001/workflow.md).

## Active workstreams

- Generator implementation and validation — owner: primary assistant; status: validating; may edit the approved six add-on modules, scenario runner, supporting documentation and run evidence. Branch: `codex/generate-ragdoll`, based on accepted scenario checkpoint `159e06245954dfa560c9ffca144054e1f2a68524`. Implemented 20 bodies, 19 joints, 41 bone targets, keyable blend, duplicate/invalid-input rejection and failure rollback. Accepted fixture at 10 substeps/20 solver iterations fails tracking, penetration and settling. A separate 30/100 diagnostic passes measured limits; it is not an accepted-scenario pass. Next checkpoint: retain final reports/playback, review visual behavior, and request approval before revising frozen scenario settings. No agents are delegated; no merge or dependency change is authorized.
- Dataset capture — owner: primary assistant with user; status: active; may edit documentation and run records. Same branch. Preserve failed experiments, exact code/input hashes, and review outcomes. Next action: finish run-001 evidence and human feedback. Broader rig coverage, binary hosting, export format and licensing of contributed code/data remain open. The proposed six-family 3/2/1 split is a pilot proposal, not established evaluation coverage.

## Decisions

- User accepted scenario-001 and initial limits, then explicitly approved the file-level generator plan. Scope approval is not acceptance of generated motion. Keep the original scene and numerical tolerances intact; proposed setting changes need review because the approved plan requires preserving floor/world settings.
- Continuous blend is the default: 0 animation, 1 physics, initially 0 without generated keys. Scenario keys are test data. Native drivers, pose constraints and an independent animation reference implement the approved binding; no custom solver or frame handler.
- Whole-body coverage uses 20 physical bodies. The other 21 finger/toe/end bones follow their nearest physical ancestor; individual digit articulation is deferred. See the mapping and architecture for current joint restrictions.
- Original source action content, mesh, weights and rest structure remain intact. The visible rig gets an editable action copy and pose constraints. Baking remains separate and unavailable in this increment.
- User selected the CC0 Quaternius rig and cleaned `work/rig-001`. Do not restore removed archives or overwrite the user-fixed source. Frozen scenario binaries and generated artifacts remain local under ignored `work/`; hashes and reports are tracked.
- User requires incremental descriptive commits and pushes to the feature branch. No merge into main without explicit request. General code-scope approval preference remains applicable for future substantial changes; this generator scope is already approved.

## Known failures and risks

- Accepted 10/20 settings fail the full run: maximum physics tracking error 4.704 mm (limit 1 mm), collider floor penetration 12.389 mm (limit 10 mm), final-window linear speed 0.1002 m/s (limit 0.05), angular speed 1.1038 rad/s (limit 0.1). See run-001/result.json. Higher-accuracy settings are a diagnostic, not permission to alter the accepted fixture.
- Initial same-session animated blend drivers left bodies kinematic. Declaring an empty blend FCurve in an output action copy before creating dependent drivers fixed release. Preserve this dependency-order lesson; initial-result.json retains negative evidence.
- Volume-based masses made short connector bodies too light to support the head. Balanced segment weights and fitted convex hulls improved behavior. Increasing local joint iteration overrides was not sufficient and could worsen contact; overrides are now disabled. Do not repeat blind local-iteration tuning.
- Spot review found feet intersecting the floor during the blend, including diagnostic frame 36. Human review must assess this defect, blend continuity and anatomical plausibility. Collider penetration checks do not measure skinned-mesh intersections. Symmetric first-rig joint limits are approximate; upper-leg rotation is currently restrictive. UI undo and installation were not tested. Both saved scenes reproduced all 240 body-position/release samples after reopening; the six-file archive passed syntax compilation.
- Bake/export, broader rigs, automatic removal/rebuild, and reverse-transition quality are not implemented/validated. Licensing and distribution decisions remain outstanding; see README/CONTRIBUTING.

## Ordered next work

1. Complete the implementation checkpoint with reports, generated scenes, playback and package; commit and push with validation failures disclosed.
2. Review the proposed 30-substep/100-iteration scenario revision and visual motion. Preserve the original input and thresholds; approval would authorize a distinct input revision, then a fresh accepted run. Do not label the diagnostic an accepted example.
3. Resolve generator failures and concrete human feedback within approved scope; obtain new scope approval for material changes. Finish one accepted generator example.
4. Define and implement the separate bake task with action naming, frame range, independent playback and export/reimport criteria.
5. Complete reproducibility/template and storage decisions before scaling the dataset. Keep related asset-family variants together and held-out solutions outside the evaluated assistant workspace.

## Integrated checkpoints

- Approved generator implementation scope on 2026-09-06; code and run evidence are on `codex/generate-ragdoll`. Generation/source-preservation/rollback/release checks pass, but the accepted simulation fails; this is a development checkpoint, not completed acceptance.
- Scenario accepted on 2026-09-06 at `159e062`: frozen input, procedure, baseline animation checks, packed textures and hashes; user reviewed the scene/instructions. Source and frozen input remain unchanged.
- Initial planning and rig provenance were committed/pushed as `11d7ee6`; the source is Quaternius Animated Human Low Poly (CC0). See docs/rig-source.md.
- AGENTS.md was cleaned of Unity-specific guidance and given durable work-log and incremental Git requirements. The project remains Blender-only.
