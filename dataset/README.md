# Development dataset

The first prepared input is [task-0001 / scenario-001](tasks/task-0001/scenario.md): an Idle-to-ragdoll floor scenario for the future Generate Ragdoll tool.

This collection currently contains scenario documentation, metadata, and input-preparation evidence. It does not yet contain a completed generator attempt, training-ready solution, or passed ragdoll test.

The .blend input and preview images are stored locally under ignored `work/scenarios/scenario-001/`. The tracked manifest identifies their location and hashes. A fresh clone cannot retrieve the exact input until binary artifact distribution is agreed; no Git LFS or external storage has been configured.

All rig-001 derivatives belong to one development family. They must not also be counted as independent held-out validation/test examples. See [the structure proposal](../docs/dataset-structure.md) for future collection and release design.
