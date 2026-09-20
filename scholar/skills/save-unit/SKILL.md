---
name: save-unit
description: >
  Save unit readings and materials to the course knowledge base for future
  reference. Extracts key concepts, author positions, and usable citations.
  Use to pre-load material or when not drafting an assignment.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---

# Save unit material to the knowledge base

The drafting skills auto-save when they detect new material. Use this skill to
bulk-load readings when you are not drafting anything yet.

## 1. Identify the course

Data root is `${CLAUDE_PROJECT_DIR}/scholar-data/`. If it does not exist,
create it with `courses.md` from `${CLAUDE_PLUGIN_ROOT}/templates/courses.md`.

Read `courses.md`. One active course: use it. Several: ask which. None: run the
`setup-course` interview inline first.

## 2. Read the existing knowledge base

Read `scholar-data/{course}/knowledge.md`. Note which units are already there
so the new entry gets the right number and nothing is duplicated.

## 3. Extract

From the supplied material, pull out:

- Key concepts and definitions, each with its author attribution
- Author positions and arguments, including where authors disagree
- Usable citations in the form `Author (Year) - key claim`
- Connections to concepts already saved from earlier units

Record only what the material actually says. Do not infer a citation, a year,
or a page number that is not there. If the material lacks full citation
details, save what exists and mark the entry `[incomplete citation]` so a
later draft does not present it as verified.

## 4. Append

Append under a `## Unit N: {topic}` header. Ask for the unit number and topic
if they are not obvious from the material.

Do not rewrite or reorder existing entries. Append only.

## 5. Confirm

State what was saved: the unit header, the count of concepts, and the count of
usable citations. List the citations so the user can spot a bad one early.
