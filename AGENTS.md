# HobbyshopGoblin Agent Instructions

## Work log provides durable project continuity

Before beginning a material project action—planning implementation, editing files, delegating work, changing priorities, or recommending a substantial next step—read `WORKLOG.md`.

`WORKLOG.md` compensates for context loss across compaction, agent handoffs, interrupted sessions, and parallel work. It is a curated project memory and coordination surface describing:

- where the project has been;
- where it is now;
- where it is going;
- which workstreams are active;
- which goals remain unmet;
- why consequential decisions were made;
- which failures or rejected approaches should not be repeated.

Do not reconstruct the project solely from recent chat, isolated commits, agent summaries, or old plans when the work log and canonical project documents are available.

### Authority and source-of-truth order

`WORKLOG.md` is derived coordination state, not the highest authority. When sources disagree, use this order:

1. Current explicit user direction.
2. Canonical product, design, and architecture documents.
3. Accepted implementation and observed validation evidence.
4. The project’s canonical task tracker or backlog.
5. `WORKLOG.md`.
6. Historical chat, delegated-agent summaries, and superseded plans.

If `WORKLOG.md` conflicts with higher-authority evidence or current repository state, ask if conflict is intentional change of direction and if so, reconcile and repair the log. Do not follow stale log content blindly.

Do not duplicate canonical systems unnecessarily. When the project already has a task tracker, design document, or architecture reference, summarize only the information needed for continuity and link to the canonical source.

### Interpret new steering carefully

Preserve nonconflicting project goals, but let the user’s current request control immediate attention and priority.

Interpret new steering using these rules:

1. Explicit cancellation or replacement language—such as “stop,” “shelf,” “replace,” “do this instead,” or “don’t continue that”—changes the affected workstream.
2. A direct correction overrides only the conflicting decision. Preserve unaffected requirements and workstreams.
3. Supplemental requirements should be folded into the relevant workstream or canonical backlog without implicitly erasing existing goals.
4. A request for unrelated work may change immediate priority without permanently canceling the previous workstream.
5. Recency alone does not prove cancellation, but neither should existing work continue automatically when the current request clearly requires attention elsewhere.
6. If an interpretation would discard, overwrite, or materially deprioritize valuable work and the user’s intent is genuinely ambiguous, preserve the work and ask before canceling it.

When steering materially changes project state, ownership, scope, or priority, update `WORKLOG.md` before starting the affected implementation or delegation.

### Maintain a clear project narrative

`WORKLOG.md` should make the following sections immediately understandable.

#### Current milestone

Record:

- the current milestone or product objective;
- its acceptance bar;
- links to the canonical scope and architecture;
- important exclusions or explicitly deferred work.

#### Active workstreams

Track each genuinely active workstream independently. Include:

- objective and scope boundary;
- owner;
- status: `planned`, `active`, `blocked`, or `validating`;
- whether the lane is read-only or may edit;
- branch and worktree when relevant;
- last durable checkpoint;
- blockers or unresolved findings;
- next resumable action;
- unverified assumptions;
- resumable run or session ID only when it remains useful.

Do not let the newest task overwrite an unrelated active lane.

#### Decisions

Retain consequential decisions that affect upcoming work. Include:

- the accepted decision;
- the reason;
- the alternatives rejected;
- links to durable supporting documentation, commits, or review evidence;
- any condition under which the decision should be revisited.

Do not record every routine implementation choice.

#### Known failures and risks

Keep unresolved defects, failed approaches, and rejected experiments when another agent might otherwise repeat them.

For each important failure, record:

- what was attempted;
- the observed failure;
- why it failed or was rejected;
- the evidence;
- whether it still blocks progress.

Remove the entry after the failure is fixed, deliberately accepted, or no longer relevant—unless it remains an important architectural lesson.

#### Ordered next work

Maintain a short, dependency-aware sequence of the next useful actions. A fresh agent should be able to select the next task without reconstructing the roadmap.

Do not mirror the entire canonical backlog. Link to it and record only:

- immediate priorities;
- dependencies;
- blockers;
- parked decisions that must not be accidentally revived;
- the next acceptance checkpoint.

#### Integrated checkpoints

Retain a compact rolling history of meaningful accepted outcomes. A checkpoint should normally include:

- the outcome;
- the relevant commit or durable artifact;
- validation or review evidence;
- an important limitation, if any.

Do not preserve routine command history, raw output, or every completed subtask.

### Keep the work log curated

`WORKLOG.md` is not an append-only transcript.

- Remove stale run IDs, obsolete temporary paths, completed worktrees, resolved blockers, and low-value chronology.
- Collapse completed operational checklists into compact checkpoints.
- Prefer links to canonical documents, task trackers, commits, and retained evidence over copied material.
- Move detailed implementation notes and test results into the relevant subsystem documentation.
- Preserve enough history to explain the current architecture, rejected approaches, unresolved risks, and remaining goals.
- Prune when duplication or chronology makes the log harder to use, not merely because it crosses an arbitrary line count.
- Do not store secrets, credentials, private tokens, or unnecessary machine-specific absolute paths.
- Include a “last reconciled” timestamp so readers can judge freshness.

### Delegated and parallel work

Before starting delegated or parallel work, record its owner, scope, editing boundary, and expected deliverable.

When applicable, include:

- agent or tool type;
- branch and worktree;
- resumable run or session ID;
- editing ownership;
- expected evidence;
- integration status.

Delegated output is not automatically project truth. It must be reviewed, accepted, and integrated before being recorded as an accomplished project outcome.

To avoid concurrent edit conflicts, the primary coordinating agent owns final reconciliation of `WORKLOG.md`. Delegated agents should normally return a proposed work-log update with their result. If delegated agents are allowed to edit the log directly, each must modify only its assigned workstream entry.

When a delegated lane finishes:

1. Review the result.
2. Integrate, revise, or reject it explicitly.
3. Record the accepted outcome or unresolved failure.
4. Remove obsolete run, branch, worktree, and ownership details.
5. Preserve a compact checkpoint when the result remains relevant.

### End-of-turn synchronization

Before ending a material work turn, reconcile `WORKLOG.md` with observed reality.

Confirm that:

- active work is still marked active;
- completed work is not left in progress;
- new failures and blockers are recorded;
- current user steering is reflected without erasing unaffected goals;
- ownership and delegated-session information are accurate;
- ordered next work reflects current dependencies;
- accepted outcomes link to durable evidence;
- stale operational details have been removed.

If the log cannot be updated, report that explicitly rather than implying synchronization occurred.

The goal is for another agent to resume correctly even if no useful chat history survives.

## Git Workflow

- As work progresses, commit and push each completed, meaningful unit of authorized work to the current working branch; do not leave completed work only on the local machine until the end of a larger project. This is standing authorization for routine commits and pushes of that work without asking again.
- Give every commit a clear description of what changed and why. Include relevant validation results and any remaining limitations in the commit body when useful; avoid vague messages such as "updates".
- Include the associated documentation and reconciled WORKLOG.md in each checkpoint. Review the diff before committing, and do not include unrelated user edits, secrets, ignored local assets, or generated files.
- Push to the current branch's configured upstream, or establish an upstream with the same branch name on the intended remote when needed. Verify the push succeeded before reporting the work as pushed. If authentication, network access, or remote changes prevent a push, report the blocker and preserve the local commit; do not force-push or overwrite remote work.
- The incremental commit-and-push rule does not authorize merging into main. Continue to use a dedicated branch for each new feature as described below.
- Begin every new feature on its own dedicated branch before making implementation changes. Create the branch from the intended integration base, normally the latest accepted `main`, and use a name that identifies the feature clearly.
- Keep each feature branch limited to one cohesive feature. Changes directly required by that feature—such as its tests, documentation, fixes, and supporting refactors—belong on the same branch. Do not add an unrelated feature unless the user explicitly approves combining the work.
- Check the current branch and working-tree state before editing. Do not accidentally begin feature work on `main` or mix pre-existing uncommitted work into a new feature branch.
- Do not merge a feature branch into `main` unless the user explicitly requests the merge.
- Before merging into `main`, run the complete automated test suite on the final branch tip. Every test must pass.
- Any code, asset, package, project-setting, or test change made after the successful run invalidates that evidence. Run the complete suite again before merging.
- If any test fails, cannot run, is interrupted, or does not produce a conclusive result, do not merge. Report the failure or missing validation and keep the work on its feature branch.
- After merging, verify that `main` contains the intended commits, remains clean, and still matches its configured remote before reporting completion.

## Architecture

- Inspect the existing implementation and `Docs/Architecture.md` before changing system responsibilities or dependencies.
- Preserve the established architecture unless the user explicitly approves an architectural change.
- Give each class one clear responsibility and keep one primary class per source file.
- Keep scene construction and dependency wiring in the composition layer; do not place gameplay rules there.
- Prefer narrow interfaces between actors and systems over direct access to large manager classes.
- Do not create a duplicate service or system when the existing implementation can be extended cleanly.
- Update `Docs/Architecture.md` when responsibilities, ownership, or important system relationships materially change.

## Dependency Approval

- Ask for explicit confirmation before adding, upgrading, removing, or replacing a package, plugin, SDK, or other production dependency.
- Before requesting confirmation, explain why the dependency is needed, what existing options were considered, and its expected project impact.
- Prefer existing project dependencies when they satisfy the requirement cleanly.

## Verification

- Confirm the project builds without new errors after code changes.
- Run the relevant automated tests for the affected systems.
- Never claim that a test or validation passed unless it was actually run and its result was observed.
- If validation cannot be completed, clearly state what was not run and why.

## Definition of Done

A change is complete only when:

- The confirmed behavior and scope are implemented.
- Existing behavior outside that scope is preserved.
- Relevant tests and validation pass, or any unverified checks are explicitly reported.
- Files and classes are organized according to their responsibilities.
- Generated files, temporary artifacts, and secrets are excluded.
- Architecture documentation is updated when the architecture materially changes.
- The final response summarizes what changed, what was verified, and any remaining risks or limitations.
