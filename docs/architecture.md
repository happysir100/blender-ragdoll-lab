# Ragdoll Lab architecture

The first implementation scope was approved on 2026-09-06; see [generator-plan.md](generator-plan.md). This document describes the code, not a claim that its behavior has passed validation.

## Ownership and responsibilities

- `addon/ragdoll_lab/__init__.py` registers the operator and sidebar. Unregistering removes UI classes, not saved scene content.
- `panel.py` presents generation and the rig's keyable blend. Baking remains visibly unavailable.
- `generate.py` validates before changing the scene, orchestrates authoring, supports Blender undo, and rolls back its own partial output on an exception.
- `mapping.py` explicitly supports the inspected humanoid naming/hierarchy and one deforming mesh, assigns weighted vertices to physical regions, and calculates world-space body fits. Uniform world scale and an active action are required; unsupported input produces an error rather than a guessed rig.
- `physics.py` creates 20 inspectable active rigid bodies and 19 Generic constraints. Joint translations are locked; rotation limits and collision settings remain editable Blender content. The scenario's existing floor and solver settings are preserved.
- `binding.py` owns the separate animation-reference rig, animated body targets, physical bone targets, output pose constraints, and native driver connections. Every output object is tracked through the generated collection and role metadata.
- `evaluation/checks/scenario_001.py` runs the accepted fixture independently of production code, measures outcomes across 240 frames, compares source content, and writes reports. It does not supply missing production behavior.

## Animation and physics

The source reference retains the original action and NLA data. The visible rig receives an editable action copy for the blend channel, leaving original action content intact. The control starts at zero and has no inserted keyframes. The new channel exists before dependent drivers are built so Blender can account for animated control dependencies.

While blend is zero, rigid bodies are kinematic and follow the reference through fitted bone-space targets. When blend is positive, native rigid bodies become dynamic. Pose constraints on the visible rig blend from animation toward body-relative targets. The 21 nonphysical bones follow body-relative offsets at full influence; this first scope does not simulate individual digits.

The setup uses built-in rigid-body physics, joints, parenting, pose constraints, and drivers. It does not require a custom solver, frame handler, or an installed third-party package. The saved scene remains an inspectable authoring artifact.

Collision proxies use convex hulls of fitted skin-weight regions, with small boxes for sparse regions. Explicit segment mass weights total 70 kg; proxy volume is unsuitable for short connector bones. Neck and shoulder connectors have locked rotation, with articulation at the adjacent head and arm joints. Current symmetric joint limits are a first-rig approximation, including restrictive upper-leg limits; anatomical quality needs human review. Joint solver overrides are disabled. The generator preserves world solver settings.

The separate `--diagnostic-high-accuracy` test option temporarily sets 30 substeps and 100 solver iterations in memory. It always labels its result diagnostic-only and never overwrites the accepted input or turns a changed fixture into an accepted pass.

## Lifecycle and boundaries

One generated collection owns one rig's setup. Duplicate generation is rejected. Undo is the supported way to discard a newly generated setup in this increment; a removal/rebuild feature is not yet implemented. Failure cleanup targets only newly created data and restores the original active action. Source .blend inputs are never overwritten.

Adding keys or changing physical settings requires restarting playback from the cache start and clearing stale simulation caches. Physics evaluation must advance sequentially. No automatic bake or export occurs.

This feature branch depends on the accepted first-scenario checkpoint. No merge to main is authorized. Binary scene outputs and previews remain under ignored `work/`; tracked run records state the exact tested code and input hashes.
