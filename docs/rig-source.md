# First development rig

Status: selected by the user for the first development example. Loading, data inventory, and a neutral rest-pose preview have been checked; animated deformation and canonical input preparation remain pending.

- Asset: Animated Human Low Poly / Animated Human by Quaternius.
- Creator and publisher: Quaternius.
- Source: https://opengameart.org/content/animated-human-low-poly
- Download: https://opengameart.org/sites/default/files/Animated%20Human%20by%20%40Quaternius_0.zip
- License: CC0 1.0 Universal, confirmed on the creator's listing and the archive's License.txt.
- Archive SHA-256: DCD72162B5E59495EFC629FB624D9E1DEB12124B68291AD4FA3CE66B4FC24DB3
- Original scene: Animated Human by @Quaternius/Blend/Animated Human.blend

## Observed inspection

Downloaded into temporary staging and opened without saving in Blender 5.1.2, with automatic script execution disabled. No add-on implementation or source scene changes were made.

- One armature, Human Armature, with 41 bones.
- One mesh, Human_Mesh.
- Named actions: Death, Idle, Jump, Punch, Run, Walk, Working; two additional ArmatureAction entries.
- Hierarchy includes hips, spine, neck/head, shoulders, arms/hands, legs/feet, and finger/toe bones.
- Blender opened the file and exited successfully but reported legacy UI/color-management conversion warnings.
- Two external image references were unresolved: //ClothedDarkSkin.png and //ClothedLightSkin2.png. The archive includes corresponding files under Blend/Textures. Relinking is pending.

This verifies file loading and data inventory only, not visual deformation, animation playback, physics suitability, or export fidelity. Included animations make it a promising candidate for later animation-to-ragdoll transition checks.

## Next checkpoint

User texture update, verified 2026-09-06: the material Texture references ClothedLightSkin.png at //Textures\\ClothedLightSkin.png, which resolves to an existing file. An additional ClothedDarkSkin.png image datablock still references a missing file, but is not referenced by the inspected material's image nodes. Current user-edited scene SHA-256: AD782EAB2D24F03E24A44415A958B3324C0E1442E90636B524361ABBCF615D08. The earlier unchanged-source hash below is historical, not the current scene hash. Playback remains unverified.

The user simplified the local folder to work/rig-001/Animated Human.blend and work/rig-001/Textures/. The original.zip, original/ hierarchy, license file, and preview are no longer present in this folder. Do not recreate that layout. Source URL, license identification, and original archive hash remain recorded above. Files under work/ remain ignored by Git pending a binary distribution decision. The current scene was hash-compared against the downloaded source and is unchanged: SHA-256 6FFDF7B8A269C7D214C7775C01808B2CD6E780C8FB44B8FA3A3ABB03858487F7.

A neutral, untextured rest-pose preview was previously rendered and visually inspected; that preview was removed during the user cleanup. The character is visible with an intact humanoid silhouette. Preview camera and display changes were made only in memory; the source .blend was not saved. This does not verify animation playback or physics behavior.

Next: inspect animated deformation and freeze the agreed starting scene for the first task. Treat this rig as development material, not a held-out test asset.

Alternative reviewed: Quaternius Universal Base Characters, https://quaternius.itch.io/universal-base-characters. The creator lists CC0; the native .blend files are in its paid Source edition ($19.99 at inspection). The free Standard edition is a different package. No purchase was made.
