Resume working on "{{TITLE}}".

Read first:
1. `state/next-session-prompt.md` (this file)
2. `state/project-map.md`
3. `state/plan.json`
4. `state/writing-plan.md`
5. `state/style-analysis.md` (if it exists)
6. `state/section-summaries.md`
7. `state/checkpoint.md`
8. the target section file in `sections/`
9. section-specific materials in `materials/[section-id]/`
10. `materials/shared/` if needed
11. adjacent sections only if needed for coherence

Target for this session:
- Section ID or task: TBD
- Workflow state expected on entry: TBD

Materials for this session:
- Read files in `materials/TBD/`
- Read `materials/shared/` only if this section needs cross-cutting context
- Do **not** read `materials/original/` during ordinary writing sessions

Goal:
- If a content section remains: write exactly one section only - TBD
- After the prose is stable, immediately create/update that section's planned figures/tables, compile, generate PNG snapshots, and refine layout if possible
- If all content sections are complete: do the whole-paper pass instead

Do not redo:
- already completed sections unless the next-session prompt explicitly says a coherence fix is needed
- do not change section order, section IDs, or manuscript structure unless the user explicitly asks

State safety:
- Treat `state/plan.json` as the canonical structural source.
- If `state/plan.json`, `state/checkpoint.md`, and this file disagree on the current target, reconcile the state before drafting.

Stop after:
- the target section plus its own figures/tables and layout check are complete, or
- the whole-paper pass is complete

After completing the work:
- Append a concise summary to `state/section-summaries.md`
- Update `state/checkpoint.md`
- Update this file for the next session
- Append one entry to `state/session-log.md`
- Do not claim layout was visually checked unless you actually reviewed the generated PNG snapshot(s)
