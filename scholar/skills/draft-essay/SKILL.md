---
name: draft-essay
description: >
  Draft a writing assignment or paper as APA 7 formatted Word (.docx)
  files. Answers every part of the question, writes to the rubric, cites
  only the materials provided in the chat, and produces exactly the number
  of variants asked for, each with its own title page. Every variant is
  verified before and after the humanizer. Use for any assignment submitted
  as a Word document.
allowed-tools: Agent, Task, Skill, Bash, Write, Read, Glob, Grep
---

# Draft a writing assignment

**Do not show the user any draft until the verifier agent has returned
`RESULT: PASS` for it twice: once before the humanizer (Gate 1) and once
after it (Gate 2).** No previews, no "here is a first pass while I check."
The only exceptions are the cap rules in `shared/verification-protocol.md`.

## 1. Read the reference files

- `${CLAUDE_PLUGIN_ROOT}/shared/apa7-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/verification-protocol.md`
- [reference.md](reference.md), for the .docx step

If a path does not resolve, Glob for `**/shared/verification-protocol.md`.

## 2. Collect the inputs from the chat

Everything comes from this chat: earlier messages, pasted text, and uploaded
files all count.

- **Prompt:** the assignment question and every professor instruction.
- **Rubric:** use the rubric for this assignment if it is in the chat. A
  rubric from an earlier assignment in the chat does not count. If there is
  none, do not draft yet. Ask, in the same message as anything else that is
  missing:

  > I don't see a rubric for this assignment. Did you forget to add it, or
  > do you want to skip it? If you have one, please paste it here.

  Then wait for the answer.
  - **Rubric pasted:** use it.
  - **User says skip:** continue without one. Send the verifier the words
    "skipped by the user" as the rubric, and say in one line with the output
    that it was written without a rubric, at the user's request.
  - **Unclear answer:** ask again. Never decide to skip on your own.
- **Materials:** readings, transcripts, documents, and links for this
  assignment.
- **Variant count:** write exactly the number the user asked for. If they
  did not say, write one.
- **Title page details for each variant:** name, school, course,
  instructor. The user usually gives these at the start of the chat. If one
  person's details are given, every variant uses them. If several people's
  are given, match one person to each variant, and ask if the match is
  unclear.
- **Paper title and due date:** use the title the prompt gives, or propose
  one in title case and confirm it. Ask for the due date if it is not in
  the chat, and write it out in full, for example `September 20, 2026`.

Ask for everything missing in one message, then wait.

## 3. Analyze

Internal, not shown:

- Every question and sub-question, every required topic, example,
  comparison, and reading, and every professor instruction.
- Every rubric criterion and its highest performance level.
- The required length and structure from the prompt, including headings.
- Which provided sources support which point.

## 4. Draft each variant

- Answer every part of the question, written to the top rubric level.
- Follow the prompt's structure and length. Use APA heading levels if the
  paper uses headings.
- Cite only sources from the provided materials, in APA 7, with a
  references list. Never invent a source, quote, page number, or DOI. If
  the materials are not enough to answer a part, ask the user.
- Natural academic tone. No em dashes and no en dashes.
- **Variants 2 and later:** read the variants already written, then make
  this one clearly different: a different angle, thesis framing, opening,
  structure, and order of points, and different examples where the
  materials allow. It must read like another student wrote it, not like a
  reworded copy.

## 5. Verify, humanize, verify

Write every variant first, then follow `shared/verification-protocol.md`
exactly, with output type `essay`. All variants go to the verifier together
in one call per round, each labeled and with its own title page details.
Gate 1, then one humanizer pass over all passed variants, then the citation
compare, then Gate 2.

Do not show a before and after. Do not mention the humanizer, except when a
cap rule or an unavailable humanizer requires it.

## 6. Generate the .docx

Follow [reference.md](reference.md) for the command, the file formats, and
the failure handling.

One file per variant, named
`{writingassignment}_{assignment-short-name}_{last-name}.docx`, saved in the
current working folder. When two or more variants share a last name (for
example, every variant uses one person's details), add the variant number so
no file overwrites another: `{writingassignment}_{assignment-short-name}_{last-name}_v{N}.docx`.

`--author`, `--school`, `--course`, and `--instructor` come from that
variant's title page details, verbatim. `--title` and `--date` are the same
for every variant.

Report the full path of each file and which person it belongs to. Exactly
the number of variants requested.
