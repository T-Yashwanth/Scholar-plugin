---
name: draft-essay
description: >
  Draft a writing assignment as APA 7 formatted .docx files. Produces multiple
  distinct variants with different title pages. Never shows a draft that has
  not passed the verifier agent. Use for any assignment submitted as a Word
  document.
allowed-tools: Agent, Task, Skill, Bash, Write, Read, Edit, Glob, Grep
---

# Draft a writing assignment

**Do not show the user any draft until the verifier agent has returned
`RESULT: PASS` for it twice: once before the humanizer (Gate 1, step 8)
and once after it (Gate 2, step 10).** No previews, no "here is a first
pass while I check." The only exceptions are the cap rules in
`shared/verification-protocol.md`, which either attach a warning header or
fall back to the Gate 1 text.

## 1. Read the reference files

Read all three before drafting. Do not work from memory of them.

- `${CLAUDE_PLUGIN_ROOT}/shared/voice-profile.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/apa7-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/verification-protocol.md`

If a path does not resolve, Glob for `**/shared/voice-profile.md` and read the
match. Do not proceed without the voice profile.

## 2. Identify the course

Data root is `${CLAUDE_PROJECT_DIR}/scholar-data/`. If it does not exist,
create it with `courses.md` from `${CLAUDE_PLUGIN_ROOT}/templates/courses.md`.

Read `courses.md`. One active course: use it. Several: list them, ask which.
No active course: run the `setup-course` interview inline, then continue here.
Do not send the user away to another command.

## 3. Load course context

- `scholar-data/{course}/knowledge.md` for accumulated prior knowledge
- `scholar-data/{course}/feedback.md` for past instructor feedback

Every entry in `feedback.md` is a hard constraint. Treat each one as a rule
the draft must not break.

Cross-course rule: the active course's `knowledge.md` is primary. If the topic
clearly connects to another course's material, read that `knowledge.md` too.
Do not force connections. Pull cross-course material only where it genuinely
strengthens the argument.

## 4. Auto-save new knowledge

Compare the pasted readings against `knowledge.md`. If there is new material,
append it under a `## Unit N: {topic}` header before drafting: key concepts
with author attributions, author positions, and usable citations in the form
`Author (Year) - key claim`.

## 5. Select variants

Read `scholar-data/{course}/variants.md`. Display the candidate names numbered.
Ask: "Which variants? (for example '1 and 3' or 'all')"

Then collect the two title page fields that belong to the assignment, not to
a variant, so they are the same for every version:

- **Paper title.** Use the title the prompt gives. If it gives none, propose
  one in title case and confirm it with the user.
- **Due date.** Ask for it, and write it out in full, for example
  `September 20, 2026`. Do not guess or default to today.

## 6. Analyze the assignment

Internal. Do not show this to the user.

- List every question and sub-question in the prompt.
- List every rubric criterion and its highest performance level.
- Map which part of the planned response addresses which requirement.
- Note every word count, page count, source count, and formatting requirement.

If the user did not supply a rubric, ask for it. The verifier cannot run
CHECK 2 without one.

## 7. Draft one version per selected variant

Before writing, assign each variant a **different analogy domain** from the
voice profile's list, and do not reuse one across variants in the same
assignment. The analogy drives the thesis in this voice, so different
analogies produce genuinely different papers rather than paraphrases.

Each version must differ in angle, analogy, and argument structure. Each is
written independently. A version that is another version with synonyms
swapped is a failure of this step.

Apply the voice profile throughout: analogy opening that does argumentative
work, citations woven in where they land, one specific AI/ML workplace
observation, hard declarative closer, varied sentence length. No em dashes,
no en dashes.

## 8. Gate 1: verify each version. Hard gate.

Follow `shared/verification-protocol.md` exactly. For each version, delegate
to the `scholar:verifier` agent with the draft, the complete prompt, the rubric, and output type
`essay`. On FAIL, fix every listed issue and resubmit. Log each attempt:

    v{N} gate1 attempt {i}: RESULT: <PASS|FAIL>

Self-assessment is not verification. Only an Agent (Task) call to the
`scholar:verifier` agent returning `RESULT: PASS` satisfies this step.

On PASS, keep an exact copy of the text. It is the verified fallback if
Gate 2 cannot pass. Cap at 5 attempts; at the cap, follow the protocol's
Gate 1 cap rule and skip steps 9 and 10.

## 9. Humanizer pass. Invisible.

Only after Gate 1 passes. Invoke the `humanizer:humanizer` skill in
**embedded mode**, which returns only the final text. Pass these
constraints with the text:

- Em dashes and en dashes are banned outright. The voice profile is the
  governing writing sample and it forbids them. Do not preserve them.
- Do not add or remove any citation, author name, year, page number, or DOI.
- Keep every point that answers the prompt and every point that meets a
  rubric criterion. Change how things are said, not what is said.

Then run the protocol's scan: zero U+2014, zero U+2013, every citation
identical to the Gate 1 text, and length still inside any word or page limit the prompt states.

If the `humanizer:humanizer` skill is unavailable, apply the voice profile's
"What to avoid" list yourself, tell the user the humanizer pass was
skipped, and still run step 10.

## 10. Gate 2: verify again after the humanizer. Hard gate.

The humanizer rewrote the text, so Gate 1's PASS no longer covers it. Send
the humanized text to the `scholar:verifier` agent with the same inputs as
step 8. Log each attempt:

    v{N} gate2 attempt {i}: RESULT: <PASS|FAIL>

On FAIL, make the smallest edits that fix every listed issue and keep the
humanized wording everywhere else. Do not run the humanizer again. Cap at 3
attempts; at the cap, follow the protocol's Gate 2 cap rule and output the
Gate 1 fallback instead.

Do not show a before and after. Do not mention the humanizer, except when
a cap rule or an unavailable humanizer requires it.

The dash ban covers everything you print, not only the body text. Labels,
headers, word counts, and any commentary around the output must also be
free of em and en dashes. Use a colon or a period instead.

## 11. Generate the .docx

See [reference.md](reference.md) for the command, the file formats, and the
failure handling.

One file per version, named `{course}_{assignment-short-name}_v{N}.docx`.
Title page fields: `--author`, `--school`, `--course`, and `--instructor`
come from the selected variant, verbatim. `--title` and `--date` come from
step 5 and are the same for every version.

Report the output paths. State which variant each file belongs to.
