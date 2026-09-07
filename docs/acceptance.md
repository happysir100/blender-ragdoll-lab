# Acceptance criteria — first development task

Status: proposed for user review. No generator exists yet and none of these behavior checks have passed. Criteria must be agreed before grading an implementation attempt.

## Task and scope

Implement Generate Ragdoll for the selected Quaternius rig in a Blender sidebar. The button generates a physics setup that drives the visible character, with keyable simulation control on the rig. Bake simulation is a separate required development task and is not automatically invoked by generation.

Success belongs to the tool: reproduce the result from the recorded input using the tool. A scene manually repaired after generation does not demonstrate that the generator passed.

## Reproducible scenario

Before the first attempt, record the exact starting scene hash, Blender version, initial pose/action, scale, gravity, collision floor, simulation settings, frame rate, frame range, and control keyframes. Any floor setup is an explicit test fixture, not an implied responsibility of the generator.

Proposed first scenario: the character begins in the agreed pose above a floor, physics takes over at an agreed frame, and the character falls and settles. An existing-animation-to-physics scenario checks preservation and transfer separately. The user selected continuous blending as the default control. Use 0 for animation, 1 for full ragdoll, and intermediate values for mixed influence. The initial value, detailed frame schedule, and interpolation remain to be defined.

The first concrete development fixture is now [scenario-001](../dataset/tasks/task-0001/scenario.md): Idle animation at 24 fps, blend 0 through frame 24, a linear transition to 1 at frame 48, and observation through frame 240. These are test-scenario settings, not default keyframes automatically added by the product. Candidate numerical limits are documented there for review before the first generator run.

## Proposed checks

| ID | Expected outcome | Evidence |
| --- | --- | --- |
| GEN-01 | The sidebar exposes Generate Ragdoll, operating on the selected supported rig without an execution error. | Recorded steps, UI capture, and tool output. |
| GEN-02 | Physics covers the whole body: pelvis, torso, neck/head, both arms/hands, and both legs/feet. Fingers and toes follow the simulated body. No body region remains unintentionally driven only by animation at full ragdoll influence. Separate articulation of fingers/toes remains to be agreed; helper and end bones do not automatically require separate rigid bodies. | Document the bone-to-body mapping for the entire rig, including bones that follow a simulated parent, and verify coverage against generated bodies/joints and full-ragdoll playback. |
| GEN-03 | Simulated bodies drive the intended bones and visible mesh; no body part remains unintentionally fixed or detached. | Evaluated bone/body transforms and recorded playback. |
| GEN-04 | The rig's keyable blend preserves animation at 0, follows ragdoll physics at 1, and produces a continuous transition at intermediate values without an unintended pose jump. | Compare endpoint poses with animation and physics outputs, sample intermediate blend values, and review playback across the transition. Agree tolerances and keyframe schedule before grading. |
| GEN-05 | In the agreed floor scenario, the character falls, makes contact, and settles without sustained jitter, joint separation, non-finite transforms, or unexplained explosive motion. | Full-window playback and measured motion/joint/contact checks. Numerical tolerances remain to be agreed. |
| GEN-06 | The character's mesh, weights, existing action data, and unrelated scene objects remain intact; intended rig modifications are documented. | Before/after inventory and comparison, plus existing-animation playback with physics disabled. |
| GEN-07 | Generated bodies and joints are named and organized so the user can inspect and adjust them. | User review against recorded naming/organization preferences. |
| GEN-08 | Generating does not bake or overwrite an animation action. | Before/after action inventory and content comparison. |

Invalid selections and repeated Generate Ragdoll presses need explicit behavior before implementation: agree whether to reject, replace, or update an existing setup. These should become additional cases rather than hidden assumptions.

## Human review and grading

The user judges whether the fall, limb motion, and editing experience meet the desired style. Record concrete feedback such as an elbow bending the wrong way or persistent foot sliding, rather than only good/bad labels.

Checks have pass, fail, or not-run status with evidence. Missing evidence cannot be counted as a pass. The first task is accepted only when agreed required checks pass and the user approves the motion/workflow. Record code-workflow compliance (including approval scope) separately from tool behavior.

Do not require pixel-identical videos or identical code to a reference implementation. Before grading, define joint-separation, penetration, and settling tolerances relative to the agreed character scale and observation window. Do not loosen checks after seeing a failure just to pass it.

## Separate bake task

Define Bake simulation later with an agreed frame range, action naming/overwrite behavior, bake sampling, and export format. Its central checks will be independent playback with physics disabled, motion matching within agreed tolerances, preservation of source animation, and export/reimport fidelity. Passing generation alone does not complete the overall tool.
