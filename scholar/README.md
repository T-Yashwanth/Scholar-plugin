# Scholar

Academic writing assistant for DBA coursework. Drafts APA 7 essays as .docx,
discussion posts, and peer replies. Every output passes an adversarial verifier
before you see it.

Built for a student carrying several courses at once, where each course has its
own readings, its own instructor feedback, and several people submitting their
own copy with their own title page. Scholar keeps that state per course and
reuses it across sessions.

## Requirements

- Python 3 on PATH as `python`. The plugin installs `python-docx` on first
  session start.
- The [`humanizer`](https://github.com/blader/humanizer) plugin. Scholar
  delegates its AI-pattern cleanup to it rather than shipping a second copy.
  Without it the drafting skills still work, and they will tell you the
  humanizer pass was skipped.

## Quick start

The [Scholar-plugin](https://github.com/T-Yashwanth/Scholar-plugin) repo is
itself a marketplace named `scholar-plugin`. Add it straight from GitHub:

    /plugin marketplace add T-Yashwanth/Scholar-plugin
    /plugin install scholar@scholar-plugin

For development, add your local clone instead, so edits apply on reload:

    /plugin marketplace add <path to your Scholar-plugin clone>

Then reload the window and use:

    /scholar:setup-course                # once per course
    /scholar:draft-post                  # paste prompt, rubric, readings

## Skills

| Skill | Use it for | Input | Output |
|---|---|---|---|
| `/scholar:setup-course` | Starting a course | Course code, name, variant details | `scholar-data/{COURSE}/` with 3 files |
| `/scholar:draft-essay` | Assignments submitted as Word files | Prompt, rubric, readings | One .docx per variant, APA 7 title page |
| `/scholar:draft-post` | Discussion board posts | Prompt, rubric, readings | 250 to 350 word posts as chat text |
| `/scholar:reply` | Peer replies | Classmate posts | 100 to 130 word replies as chat text |
| `/scholar:save-unit` | Pre-loading readings | Unit material | Appended to `knowledge.md` |
| `/scholar:save-feedback` | Graded work returned | Instructor comments | Appended to `feedback.md` |

Standalone AI-pattern cleanup is `/humanizer`, from the humanizer plugin.

## Typical semester

1. Start of term: `/scholar:setup-course` for each course.
2. Each unit: paste readings, prompt, and rubric, then `/scholar:draft-essay`
   or `/scholar:draft-post`.
3. After classmates post: paste their posts, then `/scholar:reply`.
4. When grades return: paste the feedback, then `/scholar:save-feedback`.
   Every later draft for that course treats it as a constraint.
5. Between assignments: `/scholar:save-unit` to bulk-load readings.

## Verification

Each draft goes to the `verifier` subagent, which returns `PASS` or `FAIL` with
no middle option. It runs four checks:

1. **Prompt completeness.** Every question and sub-question is answered, and
   every explicit instruction followed.
2. **Rubric alignment.** Every criterion is met at its *highest* performance
   level, not merely adequately.
3. **APA 7 correctness.** Citations match references both ways, formatting is
   right, and nothing is fabricated.
4. **Output type rules.** Word counts, essay format, title page accuracy, and
   for replies, that it engages the classmate's actual argument.

Every version passes the verifier twice:

    draft -> Gate 1 -> humanizer -> scan -> Gate 2 -> output

**Gate 1** checks the content. A `FAIL` sends the draft back for revision
and another check, up to 5 attempts. **Gate 2** runs the same four checks
on the humanized text, so the rewrite cannot quietly cost rubric points,
drop a sub-question, or break a citation. A Gate 2 `FAIL` gets small
targeted fixes, not another humanizer pass, up to 3 attempts.

You are not shown text that has not passed Gate 2. If a draft hits the
Gate 1 cap, you get it with a warning header listing what is still
unresolved. If it hits the Gate 2 cap, you get the Gate 1 version instead,
which passed every check, with a one-line note that the humanizer pass was
dropped for it. Nothing is lost and nothing is passed off as finished.

One honest limit: these gates are instruction-level, not mechanically
enforced. Chat text is not a tool call that a hook could intercept, so the
protocol is reinforced in several places rather than being technically
impossible to skip.

## AI-pattern cleanup

Between the gates, the text goes through the `humanizer` plugin in its
embedded mode, which returns only the finished text. It runs under three
constraints Scholar adds: em dashes and en dashes are banned outright by
the voice profile; no citation, author, year, page number, or DOI may be
added or changed; and every point that answers the prompt or meets a
rubric criterion must survive. Gate 2 then confirms all of it held.

## Your data

Course data lives in your project, not in the plugin:

    scholar-data/
    ├── courses.md              # course registry
    └── {COURSE}/
        ├── variants.md         # title page configs, one block per person
        ├── knowledge.md        # accumulated readings and usable citations
        └── feedback.md         # instructor feedback, as hard constraints

**Add `scholar-data/` to your `.gitignore`.** It holds real names, instructor
names, and coursework. The plugin ships placeholder templates only, so nothing
personal travels with it.

## Architecture

| Component | Count | Location |
|---|---|---|
| Skills | 6 | `skills/*/SKILL.md` |
| Agent | 1 | `agents/verifier.md` |
| Shared references | 3 | `shared/*.md` |
| Data templates | 4 | `templates/*.md` |
| Hook | 1 | `hooks/hooks.json` |
| Scripts | 2 | `scripts/*.py` |

    scholar/
    ├── .claude-plugin/plugin.json
    ├── agents/verifier.md
    ├── hooks/hooks.json
    ├── scripts/
    │   ├── ensure-deps.py          # installs python-docx into this interpreter
    │   └── generate-docx.py        # APA 7 .docx writer
    ├── shared/
    │   ├── apa7-rules.md
    │   ├── verification-protocol.md
    │   └── voice-profile.md
    ├── skills/
    │   ├── draft-essay/{SKILL.md,reference.md}
    │   ├── draft-post/SKILL.md
    │   ├── reply/SKILL.md
    │   ├── save-feedback/SKILL.md
    │   ├── save-unit/SKILL.md
    │   └── setup-course/SKILL.md
    ├── templates/{courses,feedback,knowledge,variants}.md
    └── README.md

The four checks live only in `agents/verifier.md`, the one place they execute.
`shared/verification-protocol.md` owns the retry loop and restates no check
content, so the two cannot drift apart.

## Notes on portability

`python`, not `python3` or `py`. On Windows `python3` is often a Microsoft Store
stub, and `py` can resolve to a different installation than the one holding
`python-docx`. `ensure-deps.py` installs into `sys.executable` so the package
lands in the interpreter that actually runs the docx script.

The SessionStart hook passes the interpreter and script path in a single
`command` string, the form Claude Code's hook schema supports, and quotes the
`${CLAUDE_PLUGIN_ROOT}` path so it survives spaces on Windows.
