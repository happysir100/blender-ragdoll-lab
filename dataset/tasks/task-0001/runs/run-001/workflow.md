# Run 001 — first generator attempt

Status: implementation checkpoint on codex/generate-ragdoll. Accepted scenario failed; higher-accuracy diagnostic passes automated checks but is not accepted. Human review is pending.

## Request and input

Task: implement the approved Generate Ragdoll scope. The task requirements are in ../../request.md and the frozen scenario input is identified by ../../input/manifest.json.

The user accepted the scene and scenario instructions on 2026-09-06: "Ok I've reviewed them, looks good". This covers the baseline and documented initial measurement limits. It does not authorize an unspecified code implementation.

## Proposal

See [docs/generator-plan.md](../../../../../docs/generator-plan.md) for the file-level scope, 20-body mapping, built-in Blender systems, constraints-based binding, proposed controls, and validation plan.

## Code approval

User explicitly replied "approved" on 2026-09-06 to the file-level scope in docs/generator-plan.md.

## Starting code and environment

- Full implementation starting revision: 159e06245954dfa560c9ffca144054e1f2a68524.
- Scenario preparation checkpoint: d7114245013234d83f98e9d3eb672efdaf056e5a.
- Blender: 5.1.2.
- Input: scenario-001, SHA-256 5a01b42be88a50998a66753a0e0d2eb63f30509cbbd6f94a4f38a0ad234e1851.
- No additional add-ons or production dependencies proposed.

## Changes, feedback, and results

Initial implementation created the 20 bodies, 19 joints, and 41 pose targets. The first 240-frame run passed source preservation and pose endpoint checks but failed the release schedule: bodies remained kinematic throughout the same authoring session, so it did not demonstrate a ragdoll fall. Settling also failed because the animation kept moving. A fresh load evaluates the kinematic driver correctly; investigating animation dependency/cache invalidation before changing physics tuning. Initial evidence: initial-result.json. This result is a failed attempt checkpoint, not a verified generator.

Release correction: create an editable output action copy with an empty blend channel before authoring its dependent drivers. This resolved same-session keyframe release without frame handlers or save/reload workarounds; original actions remain untouched. The next full run produced a real fall but exceeded joint separation, endpoint-position, and settling limits (release-fixed-result.json). Volume-based masses gave a tiny neck proxy about 0.18 kg supporting a 12 kg head. Explicit balanced segment masses and fitted convex hulls improved the result. Local joint solver overrides were explored but could worsen contact; they are disabled in the final checkpoint. Accepted world settings and grading thresholds remain unchanged.

## Final checkpoint evidence

- [result.json](result.json): all 240 accepted-scenario frames measured; physics endpoint, floor penetration and settling fail. Blender exited 1 as expected for failed assertions.
- [diagnostic-result.json](diagnostic-result.json): same production code, 30 substeps/100 iterations, all 240 frames and all automated checks pass; explicitly diagnostic-only. Blender exited 0. Original input remains unchanged.
- [fresh-load.json](fresh-load.json): both saved scenes replayed all 240 frames without loading the add-on; body positions and kinematic release matched exactly. Six packaged source files passed Python syntax compilation.
- [artifacts.json](artifacts.json): source/input/code-adjacent review artifact hashes and local paths, including generated scenes, seven stills per run and complete MP4 recordings. Binary artifacts remain local/ignored.
- [findings](../../../../../docs/solver-resolution-findings.md): comparison, reproduction steps and concrete proposed solver-setting revision. It requires review before replacing the accepted fixture.

Validation includes operator registration/generation, invalid selection, duplicate generation, injected failure after binding and full rollback, content-based source preservation, body/bone coverage, endpoint poses, release timing, joint separation, collider contact and final-window speeds. The test harness corrected quaternion sign ambiguity using shortest-angle rotation distance and checks actual convex-hull vertices for floor contact; these are measurement corrections, not changed thresholds. Blender 5.1 video rendering required setting media_type to VIDEO before selecting FFMPEG; complete recordings were subsequently generated successfully.

Assistant inspected original frames 36/240 and diagnostic frames 36/48/240. Feet intersect the floor during the blend, including diagnostic frame 36. Mesh contact, pose plausibility, blend continuity and workflow acceptance remain unresolved human-review items. UI installation and undo were not tested. This checkpoint is useful negative/development data, not an approved reference example. Bake/export remains deferred.
