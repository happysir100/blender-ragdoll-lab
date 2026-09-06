# Working agreement

## Approval before code changes

Before implementing code or changing existing code, you must:

1. Restate your understanding of the user's request, including the intended outcome and relevant scope or constraints.
2. Explain the specific changes you propose to make. Identify the affected files or components when known, and describe the resulting behavior in plain language.
3. Explain why those changes are needed and how they address the request. Mention material tradeoffs or risks when relevant.
4. Explicitly ask the user to approve the proposed changes.
5. Wait for explicit approval before editing or creating code.

A request to implement or fix something is not, by itself, approval of a proposal that has not yet been explained. Do not implement first and ask for approval afterward. Silence or elapsed time is not approval.

Read-only investigation is allowed before approval so the proposal can be concrete. This includes inspecting files, reviewing relevant documentation, and running checks that do not modify project files. Do not use investigation as a reason to make unapproved code changes.

Approval covers only the explained scope. If implementation requires materially different or additional changes, stop, restate your updated understanding, explain the additional changes and why they are necessary, and ask for approval again. Do not repeatedly request approval for changes already approved within the same scope.

Apply this rule to source code, scripts, tests, dependencies, and configuration that changes tool behavior. Do not bypass it by generating code indirectly or delegating work to another agent.

## Suggested approval message

- **My understanding:** What the user wants and the intended outcome.
- **Proposed changes:** What will change and where.
- **Why:** How the changes fulfill the request and any material tradeoffs.
- **Approval:** "Do you approve these changes?"

After completing approved work, summarize what changed, how it was verified, and any remaining limitations.
