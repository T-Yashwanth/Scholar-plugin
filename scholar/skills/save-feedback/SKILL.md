---
name: save-feedback
description: >
  Save instructor feedback to the course feedback log. Extracts the lesson
  (what went wrong, what to do differently) so future drafts avoid the same
  mistake. Use after receiving graded work back.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---

# Save instructor feedback

Every drafting skill reads this log and treats each entry as a hard constraint.
An entry saved here changes all future drafts for the course.

## 1. Identify the course

Data root is `${CLAUDE_PROJECT_DIR}/scholar-data/`. If it does not exist,
create it with `courses.md` from `${CLAUDE_PLUGIN_ROOT}/templates/courses.md`.

Read `courses.md`. One active course: use it. Several: ask which.

## 2. Read the existing log

Read `scholar-data/{course}/feedback.md`. If this feedback repeats an entry
already there, say so and strengthen the existing entry rather than adding a
near duplicate.

## 3. Extract the lesson

From the feedback, determine:

- What was the mistake or deduction?
- What should be done differently next time, stated as an action?
- Which assignment type was it: essay, post, or reply?
- How many points were lost, if mentioned?

Write the fix as something a drafter can act on. "Be more analytical" is not
actionable. "Tie each source to the research question instead of summarizing
it" is.

If the feedback is vague, ask the user what they think the grader wanted rather
than guessing.

## 4. Append

    ## Unit N - {assignment type}
    - Issue: {what was wrong}
    - Fix: {what to do instead}
    - Points lost: {if mentioned}

Append only. Do not edit or remove earlier entries.

## 5. Confirm

Read back the entry as written, and state that future drafts for this course
will treat it as a constraint.
