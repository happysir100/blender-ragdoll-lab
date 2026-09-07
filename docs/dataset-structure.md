# Proposed dataset structure

Status: proposal for review. No add-on, dataset schema, collection pipeline, or evaluation runner has been implemented.

## Purpose

Collect reviewed examples of developing a Blender ragdoll generator, including user preferences, approvals, corrections, and observed validation. Also retain Blender scenarios that test the resulting tool. Distinguish these two kinds of task in the dataset index.

The tool takes an existing rig, adds a keyable ragdoll simulation, and offers a separate button to bake motion onto the rig for animation export. The user selected continuous blending and whole-body coverage; rig-001 is the first development input. Broader rig support remains undecided.

## Repository layout

```text
README.md                         Entry point and reproduction quick start
AGENTS.md                         Agent conduct and code approval rules
WORKLOG.md                        Current coordination state
CONTRIBUTING.md                    Contribution and review requirements
docs/
  first-tool.md                   Canonical tool requirements and exclusions
  dataset-structure.md            This collection and storage plan
  acceptance.md                   Versioned checks and review rubric
  preferences.md                  Personal preferences, kept distinct from correctness
  architecture.md                 Tool responsibilities, once designed
templates/
  workflow.md                    Human-readable example record
  review.md                      Reviewer checklist and sign-off
addon/
  ragdoll_lab/                    Future Blender add-on source
dataset/
  README.md                      How to select, obtain, and replay examples
  schema.json                    Future machine-readable record validation
  index.jsonl                    One record per task with stable IDs
  splits.json                    Authoritative task/family split assignments
  assets/
    rig-001/
      asset.json                 Provenance, permissions, family ID, file hashes
      source.blend               Shared untouched rig, or manifest reference
  tasks/
    task-0001/
      task.json                  Task kind, input references, environment, base revision
      request.md                 Exact request and constraints
      input/
        start.blend              Exact task scene, or immutable artifact reference
      runs/
        run-001/
          workflow.md            Proposal, approval, actions, corrections, outcome
          events.jsonl           Ordered visible interaction/tool event records
          changes.patch          Code change relative to recorded base revision
          result.json            Structured observed checks and review status
          artifacts.json         Paths/URLs, sizes, hashes, and access requirements
          output/                Result scenes, baked actions, export artifacts
          evidence/              Reports, screenshots, optional recordings
evaluation/
  README.md                      Evaluation protocol and access boundaries
  checks/                        Future automated Blender and dataset checks
releases/
  README.md                      Versioning and separate distribution packages
```

The first-tool specification is populated; the workflow template remains to be filled. The folder tree is a target, not a request to create empty scaffolding. The first prepared scenario and metadata live under dataset/tasks/task-0001; see dataset/README.md for the actual current collection and its local-only binary storage limitation. Script creation requires the user's code-change approval workflow.

## Task and run records

Every task identifies its task type (code development or tool operation), rig family, requirements/rubric version, starting code revision, input artifacts, exact Blender version, dependencies, scene settings, starting selection/mode, and expected deliverables. Exact code starts require a clean reproducible revision or an additional starting patch.

Each run records the tools/model identifiers available to the recorder, visible requests and responses, proposed changes, approval scope, actions, corrections, output artifacts, validation results, and review status. Preserve useful tool errors and failed attempts, excluding credentials and unrelated private information. Record concise decision explanations, not hidden model reasoning. Mark missing capture explicitly; never reconstruct exact transcripts from memory.

The assistant maintains records during work; the user supplies goals, approves code scope, judges preferences and motion quality, and reviews the proposed accepted outcome. At each meaningful checkpoint, save the relevant artifacts and a run record. Do not equate the end of a chat with an accepted example.

Use status values such as draft, reviewed, and independently-reproduced. Record reviewer identity/date, check results, and unresolved limitations. An assistant's successful command alone is not human approval or independent reproduction.

## Reference outcomes

The user and assistant can build the reference together. It need not be authored entirely by the user or through manual clicks. Any authoring script must follow the code approval rule. Review its result against checks defined beforehand; do not approve the generator's own output solely because it generated it.

Reference packages contain an approved scene, motion evidence, a baked action (which may be stored in the scene), the agreed export, and a checklist with tolerances and review notes. Multiple valid solutions are allowed. If the evaluated assistant helped create a task's reference, that task is a development example for that evaluation, not an unseen test.

## Starting size and growth

Start with one rig family and one complete development example. Use it to refine capture and review before collecting more.

Next, a practical pilot target is six independent rig families: three for training/development, two for validation, and one for a final held-out test. This is a proposed workflow pilot, not evidence of broad reliability. Choose all rigs within the supported scope once defined. Different names, poses, or slight modifications of the same rig do not make independent families.

Each family can support several tasks: setup, keyable transition, bake, export, and a repair/invalid-input case. Only claim these as separate examples when each has its own reproducible start, request, and checks. Keep dependent development tasks, closely related solutions, and rig derivatives together across splits.

Expand in response to coverage gaps and observed failures, rather than treating a fixed count as sufficient. Code-development task splitting also needs review for shared solution leakage; rig separation alone does not guarantee independence.

## Evaluation boundaries

Training packages may include reviewed solutions, corrections, and preferences. Validation supports iteration; the final test remains untouched until assessment. Material used to improve the system is no longer untouched test material.

Store private validation/test reference scenes, solutions, and grader-only evidence outside the evaluated assistant's workspace and outside accessible Git history. A folder called hidden is not access control. Supply an input-only package and evaluate outputs separately. Public releases may distribute benchmark solutions, but those tasks cannot then be described as unseen to an assistant that accessed them.

Grade process and artifact quality separately. The add-on may pass a Blender scenario even if the development workflow violated approval requirements; conversely, a well-recorded development run may still fail behavior checks. Report both outcomes.

## Storage and releases

Keep documentation, metadata, code, small reports, and patches in ordinary Git. Before adding large binary files, agree on Git LFS or versioned external artifact storage. Do not change storage tooling as part of this proposal.

For externally stored files, retain immutable locations, hashes, sizes, format, and retrieval instructions in manifests. Avoid duplicating identical binary assets; preserve exact task scenes where differences matter. Record licenses and provenance per asset, and decide code/dataset licensing before distribution.

Keep the canonical collection independent of a particular model training format. Future exporters can derive training-ready records or evaluation input packages from reviewed records. Release a dataset version with its schema, split mapping, rubric version, artifact manifests, known limitations, and reproduction instructions.

## First acceptance checkpoint

One agreed rig, one task with a reproducible starting state, a collaboratively approved reference, one recorded development attempt with corrections, observed simulation/bake/export checks, and another person's successful reproduction. Export checks wait until format and expected fidelity are agreed.
