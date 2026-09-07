# Project Work Log

Last reconciled: 2026-09-06 (America/New_York).

## Current milestone

The primary objective is to create training and validation data that captures effective workflows, the user's working preferences, and reviewed examples useful to the wider game-development community. Developing a Blender tool supplies the tasks and evidence for the dataset. The intended training mechanism remains unspecified; collecting examples does not itself retrain a model.

The user-provided prior conversation confirms the first tool is a Blender-only ragdoll generator, consistent with [README.md](README.md). The repository is in its initial planning stage and contains no working add-on or training dataset.

Confirmed tool workflow: the user selects an existing rig, adds a ragdoll physics simulation, keys its control over time, and bakes the simulation back onto the rig to produce exportable ragdoll animations. Creating a rig from an unrigged mesh is not part of the stated workflow.

Baking must be triggered by its own button, separate from adding the ragdoll simulation. The user can set up and adjust the simulation before explicitly baking its motion onto the rig.

The user-authored spec now requires a Blender sidebar tab with two buttons: Generate Ragdoll and Bake simulation. Generation uses the selected rig hierarchy to create a physics mesh that drives the bones and character; the spec describes parenting bones to that mesh. This is recorded as requested behavior/structure, not a technically validated implementation. Simulation control must be a keyable attribute on the rig.

Supported rig types, the meaning of keyable simulation control (switching versus blending), export format, and concrete acceptance criteria remain to be defined. Reproducible starting states and observed validation outcomes are required for reviewed workflows. The tool remains Blender-only; exportable baked animation is explicitly required, while integration with another application has not been requested.

Canonical references:

- [README.md](README.md): project objective, goals, and data handling.
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution and example quality requirements.
- [docs/first-tool.md](docs/first-tool.md): user-authored tool specification, including sidebar placement, generation, keyable rig control, and separate baking.
- [docs/acceptance.md](docs/acceptance.md): proposed first-task success criteria, evidence requirements, and outstanding decisions; not yet approved or executed.
- [templates/workflow.md](templates/workflow.md): intended demonstration template; currently empty.
- [AGENTS.md](AGENTS.md): agent workflow instructions.
- [docs/dataset-structure.md](docs/dataset-structure.md): proposed repository layout, record contents, pilot size, review process, and held-out evaluation boundaries.

## Active workstreams

- Rig preparation — owner: primary assistant; status: planned; editing boundary: source/provenance and local asset preparation, no add-on code. User selected Quaternius Animated Human Low Poly. User cleaned work/rig-001 to Animated Human.blend and Textures/. The scene now includes the user texture fix; the current hash and inspection are recorded in docs/rig-source.md. The original archive, license file, and preview are no longer in this folder; provenance remains in docs/rig-source.md. A neutral rest-pose preview was previously inspected in Blender 5.1.2. Evidence and archive hash: [docs/rig-source.md](docs/rig-source.md). Next action: check animated deformation and establish the canonical task input. The material texture resolves; one older image datablock remains unresolved. Legacy conversion warnings occurred. No binary assets were added to Git and no source scene was saved.
- Goal and dataset definition — owner: primary assistant with user; status: active; editing boundary: continuity documentation only during discussion, no implementation. Branch: `main`. Latest checkpoint: user specified selected-rig input, keyable ragdoll simulation, and baking onto the rig for animation export. Next action: review docs/acceptance.md and clarify keyable control for the selected rig. Unverified assumptions: training mechanism, supported rig types, switching versus blending, and export requirements. No delegated work is active.

Planning documentation and agent instructions were committed as 11d7ee6 and successfully pushed to origin/main. The checkpoint includes the accumulated specification, dataset plan, rig provenance, and work log. Binary assets under work/ remain local and ignored.

## Decisions

- User requested incremental commits and pushes to the current branch, with descriptions of completed work. AGENTS.md now records this standing workflow authorization, while retaining dedicated feature branches and explicit merge approval. The initial checkpoint covers the accumulated project planning/specification, rig provenance, work log, and instruction edits; ignored work/ assets remain local.
- User selected Quaternius Animated Human Low Poly as the first development rig. Respect the user-cleaned layout under ignored work/rig-001: Animated Human.blend and Textures/. Keep provenance in docs/rig-source.md while binary distribution/storage remains undecided; do not restore the removed archive hierarchy or preview. Inspect without saving over the source; this selection does not authorize add-on code changes.
- Prioritize dataset design and use the confirmed Blender-only ragdoll generator as the first tool. Do not infer supported rigs, physics behavior, or an interface before design establishes them.
- The supplied prior conversation includes the user's general code-change approval preference: restate the request, explain proposed changes and why, and obtain explicit approval before implementation or code changes. The current AGENTS.md lost the explicit gate when its Unity-specific section was removed; preserve the general preference during this discussion and reconcile its wording before code work.
- A manually authored, user-reviewed reference ragdoll, paired starting/result files, a simulation recording, and an acceptance checklist were proposed in the prior conversation. These remain proposals, not approved implementation scope. The user has now specified starting from an existing rig.
- Baking the simulated motion onto the selected rig for export is part of the required outcome. A simulation-only demonstration is insufficient; exact animation-control and export criteria still need agreement.
- User interface requirement: a sidebar tab with Generate Ragdoll and Bake simulation buttons, as specified in docs/first-tool.md. Generation must not automatically bake the animation.
- At the user's request, remove Unity-specific instructions from `AGENTS.md` while retaining general project continuity, Git, architecture, dependency, and verification rules. This instruction cleanup does not replace the project goals in the README.
- Use this file as curated coordination state; canonical documents and observed evidence remain authoritative as specified in `AGENTS.md`.

## Known failures and risks

- User corrected the material texture path; read-only inspection confirmed it resolves. One older dark-skin image datablock remains unresolved but is not used by the inspected material. Current scene hash and evidence are recorded in docs/rig-source.md; previous unchanged-source hash is historical. Animated deformation remains unchecked.

- The tool scope document now contains the user's requirements. The demonstration template remains empty, and detailed acceptance criteria are still pending.
- `AGENTS.md` references `Docs/Architecture.md`, but no architecture document currently exists. Establish the relevant design before changing system responsibilities.
- Code and dataset licensing remain undecided; follow the contribution restrictions in the README and CONTRIBUTING document before external contributions or asset distribution.

## Ordered next work

Immediate proposed checkpoint: review docs/acceptance.md for the first code-development task (Generate Ragdoll on the selected rig), freeze the user-corrected input, and agree observable success checks before implementation. Clarify whether keyable control means an on/off switch, blending, or both. Baking remains required as a separate subsequent development task. Prepare the input and capture record before starting the first attempt; obtain approval for a concrete file-level code plan.

1. Review [docs/dataset-structure.md](docs/dataset-structure.md), now containing the proposed repository layout and capture process. Start with one complete example; the proposed next pilot is six independent rig families split 3/2/1 across training/validation/test. These counts and folders are proposals, not approved implementation or evidence of reliability. Reference construction can be collaborative; held-out solutions must be outside the evaluated workspace.
2. Clarify keyable simulation control and define successful simulation and baked-animation outcomes using the selected Quaternius rig; distinguish technical requirements, personal preferences, and project constraints.
3. Reconcile the README and scope document with the agreed dataset-first objective; define the smallest tool workflow and acceptance checks.
4. Fill `templates/workflow.md` with the reproducibility and validation fields, including starting inputs, instructions, reviewed outcomes, corrections, and evidence. Include task IDs, asset-family IDs, exact environment and code revision, review status, and links to evidence. Record code-development examples as well as resulting Blender scenes.
5. Complete and independently reproduce one pilot example before expanding the collection. Proposed pilot: add a ragdoll to one agreed rig, exercise the agreed keyable control, explicitly bake through the separate button, and verify independent animation playback and the agreed export result.
6. After scope is established, begin implementation on a dedicated feature branch and retain observed validation evidence.

These are pending planning steps, not authorization to start implementation.

## Integrated checkpoints

- Rig sourcing: found and downloaded a CC0 humanoid Blender source from its creator, checked its included license, and observed a successful read-only load/data inventory in Blender 5.1.2. See docs/rig-source.md for provenance, limitations, and pending visual checks.
- Instruction cleanup: removed Unity-specific sections and references from `AGENTS.md`; a text search found no remaining Unity references. General project rules were retained.
- Initial continuity record: created this work log from the current README, contribution guidance, repository inventory, and observed working-tree state. Confirmed that the scope document and workflow template are empty. Documentation-only work; no build or behavioral tests were run.
- Prior-chat reconciliation: confirmed the user's dataset/community objective, Blender-only ragdoll tool choice, and general code-approval preference. Retained earlier assistant suggestions as proposals rather than accepted requirements.
- User spec review: read the additions to docs/first-tool.md and synchronized this log. Confirmed sidebar placement and the two named buttons. No specification or implementation files were changed during the review.
