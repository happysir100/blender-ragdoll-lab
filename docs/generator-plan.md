# Generate Ragdoll — first implementation proposal

Status: awaiting explicit code-scope approval. The user has accepted scenario-001, not this implementation. No Python files in this plan exist yet.

## Intended behavior

Select the supported Human Armature and press Generate Ragdoll in a Ragdoll Lab sidebar tab. Create editable whole-body physics, preserving the original mesh, weights, and action data. Expose a keyable rig property named Ragdoll Blend, initially 0: 0 displays source animation, 1 follows physics, and intermediate values blend the poses. Do not insert scenario-specific keyframes automatically.

Bake simulation remains a separate task. In this first increment the sidebar may show it disabled with an explicit not-yet-implemented explanation; it must not pretend to bake. Invalid selections and repeated generation on a rig already owning a setup should report a clear message without modifying the scene. Generation should support undo and remove partially created owned data if it fails.

## Inspected input

Blender 5.1.2, scenario-001: 41 bones, no existing pose-bone constraints, an active Idle action, source action stashes, and a uniformly scaled fixture parent. Hips, hands, Spine2, and end bones have short bone lengths; bone length alone is insufficient for their collider dimensions. Use the associated mesh regions and anatomical neighbors when fitting bodies. The original input remains frozen.

## Proposed physics mapping

20 physical bodies and 19 parent-child joints:

- Hips, Spine, Spine1, Spine2, Neck, Head.
- LeftShoulder, LeftArm, LeftForeArm, LeftHand.
- RightShoulder, RightArm, RightForeArm, RightHand.
- LeftUpLeg, LeftLeg, LeftFoot.
- RightUpLeg, RightLeg, RightFoot.

The remaining 21 bones are finger/thumb segments, toe segments/end bones, and HeadTop_End. They follow their nearest physical ancestor with appropriate offsets; no independently simulated fingers/toes are proposed in this increment. At full ragdoll they must not continue independent source animation. This mapping needs approval as part of the implementation scope.

## Use Blender's existing systems

Generate mesh collision proxies with built-in active rigid bodies and Generic joint constraints, locking joint translation and limiting angular movement. Fit simple collision shapes to the associated mesh regions, disable collisions between connected bodies, and retain inspectable mass, damping, shape, and joint settings. Preserve the accepted floor/world settings while running the scenario; do not alter them merely to meet the tolerances.

Use an owned animation-reference armature to evaluate source action/NLA poses independently of physics. Physics bodies follow it while the blend is zero and release from the current animated pose when the blend becomes positive. Drive output bones through pose constraints and generated offset targets with the blend as influence. Preserve source actions rather than baking them as a substitute for the requested setup.

The custom layer orchestrates authoring, mapping, ownership, and the blend; Blender performs the rigid-body simulation and constraint evaluation. No new dependency or custom physics solver is proposed. Blender 5.1.2 runtime introspection confirms the kinematic property supports animation control and constraints expose influence. The Copy Transforms reference is https://docs.blender.org/manual/en/4.5/animation/constraints/transform/copy_transforms.html; runtime validation on 5.1.2 remains required.

This replaces the spec's informal wording about parenting bones directly to physics meshes with a proposed constraint-based binding. It is an architectural proposal for approval, not a silently accepted change to the spec.

## File-level scope

No existing Python scripts will be edited. Create:

| Path | Primary responsibility |
| --- | --- |
| addon/ragdoll_lab/__init__.py | Add-on metadata and registration/unregistration; no primary class. |
| addon/ragdoll_lab/panel.py | RAGDOLL_PT_panel: sidebar, generation control, keyable blend, and truthful disabled bake placeholder. |
| addon/ragdoll_lab/generate.py | RAGDOLL_OT_generate: selection validation, generation orchestration, undo, duplicate rejection, failure cleanup. |
| addon/ragdoll_lab/mapping.py | Supported rig mapping, mesh-region assignment, body fitting data, and validation; functions/data only. |
| addon/ragdoll_lab/physics.py | Author editable collision bodies, mass/damping, joint frames/limits, owned collection and tags; functions only. |
| addon/ragdoll_lab/binding.py | Animation-reference rig, bone targets, rig blend property and drivers, independent animation/physics pose binding; functions only. |
| evaluation/checks/scenario_001.py | Blender test runner: load fresh input, invoke the operator, apply the accepted test keys, advance all frames, collect evidence and assertions; no production behavior. |

Documentation and records to edit: docs/first-tool.md (approved binding wording and supported first scope), docs/acceptance.md (link validation evidence without weakening checks), dataset/tasks/task-0001/task.json, dataset/tasks/task-0001/runs/run-001/workflow.md, and WORKLOG.md. Create docs/architecture.md to document approved ownership/dependencies and lifecycle, plus run-001/result.json and artifact manifests when outputs exist. Do not mark the architecture accepted until code-scope approval arrives.

Generated Blender outputs go to a new ignored work/runs/task-0001/run-001/ directory. Do not change the frozen work/scenarios/scenario-001/start.blend or user-cleaned work/rig-001. No dependency changes, merges, export implementation, or broader rig claims are included.

## Validation

Run registration and operator checks, invalid/repeated selection checks, source preservation comparisons, and the complete accepted 240-frame scenario. Capture all 41 bone mappings, 20 bodies/19 joints, blend endpoint and transition measurements, joint separation, floor penetration, settling, finite values, and playback evidence. Compare source action/mesh/weight content, not just datablock names.

Blender's dependency ordering, connected-bone transforms, kinematic release, and pose blending need observed validation; the plan is not proof these work. Investigate failures without weakening accepted limits. If the approach requires materially different rig modifications or responsibilities, present a revised scope before implementing them. User motion review remains part of acceptance.

## Git and run capture

Keep the accepted scenario checkpoint on codex/first-test-scenario. After explicit implementation approval, create a dedicated generator branch from that reviewed checkpoint so its input/docs are available; do not mix generator code into the scenario branch or merge either into main without instruction. Record the full generator starting revision in run-001 when the branch exists. Commit and push meaningful implementation checkpoints with results and limitations.
