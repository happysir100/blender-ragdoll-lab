Create a tool in blender.
The tool should be a sidebar tab.

What it needs to be:
- Two buttons
 - Generate Ragdoll
    - The user will select a rig and press this button
    - Physics must cover the whole body: torso, pelvis, neck/head, both arms and hands, and both legs and feet. Fingers and toes must move with the simulated body; whether they need individually articulated physics bodies remains a design detail to agree. Whole-body coverage does not mean creating a separate rigid body for every helper or end bone.
    - The tool creates collision meshes and joints based on the supported rig hierarchy. Pose constraints bind the bones to physics targets, with a separate animation-reference rig preserving the source motion. This binding was approved in [generator-plan.md](generator-plan.md).
    - This needs to be a keyable attribute on the rig
    - Use a continuous blend between animation and ragdoll physics by default. A blend of 0 means animation, 1 means full ragdoll, and intermediate values mix their influence. Generation starts at 0 without inserting keyframes; the user chooses the transition duration.
 - Bake simulation
    - This will bake the simulation onto the bones to be exported as an animation

First development rig: Animated Human Low Poly by Quaternius (selected by the user). See [rig-source.md](rig-source.md) for provenance, license, and inspection status. Support for other rigs remains to be defined.

The first approved implementation generates 20 bodies and 19 joints; the remaining 21 bones follow their nearest simulated ancestor. Bake simulation is a separate subsequent increment and is currently shown as unavailable. See [architecture.md](architecture.md) for implementation boundaries and [solver-resolution-findings.md](solver-resolution-findings.md) for unresolved validation.
