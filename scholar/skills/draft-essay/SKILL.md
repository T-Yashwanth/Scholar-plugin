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
- **Rubric:** required. If none is in the chat, ask for it and wait. Do not
  draft without it.
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

Follow `shared/verification-protocol.md` exactly, with output type `essay`.
Send the prompt, the rubric, the source materials, this variant's title
page details, and the other finished variants. Gate 1, then the humanizer,
then Gate 2.

Do not show a before and after. Do not mention the humanizer, except when a
cap rule or an unavailable humanizer requires it.

## 6. Generate the .docx

Follow [reference.md](reference.md) for the command, the file formats, and
the failure handling.

One file per variant, named `{assignment-short-name}_{last-name}_v{N}.docx`,
saved in the current working folder. `--author`, `--school`, `--course`, and
`--instructor` come from that variant's title page details, verbatim.
`--title` and `--date` are the same for every variant.

Report the full path of each file and which person it belongs to. Exactly
the number of variants requested.
