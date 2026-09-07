Create a tool in blender.
The tool should be a sidebar tab.

What it needs to be:
- Two buttons
 - Generate Ragdoll
    - The user will select a rig and press this button
    - Physics must cover the whole body: torso, pelvis, neck/head, both arms and hands, and both legs and feet. Fingers and toes must move with the simulated body; whether they need individually articulated physics bodies remains a design detail to agree. Whole-body coverage does not mean creating a separate rigid body for every helper or end bone.
    - The tool will create a ragdoll physics mesh based on the rig heirarchy that the bones will be parented to so when physics are simulated the character will act as a ragdoll
    - This needs to be a keyable attribute on the rig
    - Use a continuous blend between animation and ragdoll physics by default. A blend of 0 means animation, 1 means full ragdoll, and intermediate values mix their influence. The initial value and default transition duration remain to be defined.
 - Bake simulation
    - This will bake the simulation onto the bones to be exported as an animation

First development rig: Animated Human Low Poly by Quaternius (selected by the user). See [rig-source.md](rig-source.md) for provenance, license, and inspection status. Support for other rigs remains to be defined.
