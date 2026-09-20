---
name: setup-course
description: >
  Initialize a new course for the semester. Creates the course data directory
  with variant configs, empty knowledge base, and empty feedback log.
  Use at the start of each new course.
allowed-tools: Bash, Write, Read
---

# Set up a course

Create the per-course data files that every drafting skill reads.

## 1. Locate the data directory

The data root is `${CLAUDE_PROJECT_DIR}/scholar-data/`.

If it does not exist, create it and copy `${CLAUDE_PLUGIN_ROOT}/templates/courses.md`
to `scholar-data/courses.md`. Never fail because the directory is absent.

## 2. Interview

Ask these in order. Ask the variant questions once per variant.

1. Course code? (for example BUS 741)
2. Course name? (for example Strategic Leadership)
3. How many variants (people submitting)?
4. For each variant: full name, school line, course line, instructor name?

Normalize the course code for the directory name by replacing the space with
a hyphen: `BUS 741` becomes `BUS-741`. Keep the spaced form for display and
for title pages.

## 3. Write the files

Create `scholar-data/{COURSE-CODE}/` and write three files. Use the templates
in `${CLAUDE_PLUGIN_ROOT}/templates/` as the starting shape, substituting the
real values and deleting placeholder blocks that were not filled.

- `variants.md` from `templates/variants.md`, one block per variant, numbered
  from 1. Every field the user gave goes in verbatim. Do not invent a school
  line or an instructor.
- `knowledge.md` from `templates/knowledge.md`, header only.
- `feedback.md` from `templates/feedback.md`, header only.

## 4. Register the course

Add the course under `## Active courses` in `scholar-data/courses.md` as:

    - {COURSE-CODE}: {COURSE-NAME} ({N} variants)

Remove the `(none yet ...)` placeholder line if it is still there.

## 5. Confirm

State: `{COURSE-CODE} is set up with {N} variants. Ready.`

List the paths written so the user can check them.

## Notes

- If the course directory already exists, say so and ask whether to add
  variants to the existing `variants.md` or leave it alone. Do not overwrite
  a `knowledge.md` or `feedback.md` that has content in it.
- This data is personal. It stays in the user's project, never in the plugin.
  Remind the user once, on first setup, to add `scholar-data/` to `.gitignore`.
