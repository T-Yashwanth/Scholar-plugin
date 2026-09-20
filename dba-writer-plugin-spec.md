# DBA Writer Plugin — Complete Build Specification

> **Purpose of this document:** This is a self-contained spec for a Claude Code plugin called `dba-writer`. Hand this file to Claude Code and say: "Build this plugin from this spec." Everything Claude Code needs to build every file is in here.

---

## 1. What this plugin does

`dba-writer` automates academic writing for a Doctor of Business Administration (DBA) program at Belhaven University. The user takes multiple courses across semesters. Each course has writing assignments, discussion posts, and peer reply requirements. All work follows APA 7th edition formatting.

The plugin handles three output types:

1. **Writing assignments** — multi-page essays/papers delivered as `.docx` files with APA 7 title pages. Multiple distinct variants per assignment (for different people, each with their own title page).
2. **Discussion posts** — 250-350 word essay-format responses. Multiple distinct versions per post. No title page.
3. **Peer replies** — 100-130 word replies to classmates' posts. 2 replies per classmate post. Multiple distinct reply sets.

Every output goes through:
- A strict verification loop (prompt completeness + rubric compliance + APA 7 check) that retries until PASS
- An invisible humanizer pass that strips AI writing patterns
- The user never sees a draft that failed verification

The plugin is **multi-course aware**. Each course has its own knowledge base, feedback log, and variant configurations. These accumulate over a semester and persist across sessions.

---

## 2. Plugin directory structure

Build exactly this structure:

```
dba-writer/
├── .claude-plugin/
│   └── plugin.json
│
├── skills/
│   ├── setup-course/
│   │   └── SKILL.md
│   ├── draft-essay/
│   │   ├── SKILL.md
│   │   └── reference.md
│   ├── draft-post/
│   │   └── SKILL.md
│   ├── reply/
│   │   └── SKILL.md
│   ├── save-unit/
│   │   └── SKILL.md
│   ├── save-feedback/
│   │   └── SKILL.md
│   └── humanize/
│       └── SKILL.md
│
├── agents/
│   └── verifier.md
│
├── shared/
│   ├── voice-profile.md
│   ├── humanizer-checklist.md
│   ├── verification-protocol.md
│   └── apa7-rules.md
│
├── hooks/
│   └── hooks.json
│
├── scripts/
│   └── generate-docx.py
│
└── README.md
```

The plugin also initializes a **data directory** in the user's project folder on first use:

```
dba-writer-data/
├── courses.md
├── BUS-700/
│   ├── variants.md
│   ├── knowledge.md
│   └── feedback.md
├── BUS-719/
│   ├── variants.md
│   ├── knowledge.md
│   └── feedback.md
└── BUS-729/
    ├── variants.md
    ├── knowledge.md
    └── feedback.md
```

---

## 3. Plugin manifest

File: `.claude-plugin/plugin.json`

```json
{
  "name": "dba-writer",
  "displayName": "DBA Academic Writer",
  "version": "1.0.0",
  "description": "Academic writing assistant for DBA coursework: essays, discussion posts, peer replies. APA 7, multi-course, multi-variant, with strict verification and AI-pattern removal.",
  "author": {
    "name": "Yashwanth"
  },
  "keywords": ["academic", "apa", "dba", "writing", "coursework"]
}
```

---

## 4. Skills — detailed specifications

### 4.1 `/dba-writer:setup-course`

**Trigger:** User starting a new course for the semester.

**Behavior:**

1. Ask: "Course code?" (e.g., BUS 741)
2. Ask: "Course name?" (e.g., Strategic Leadership)
3. Ask: "How many variants (people submitting)?"
4. For each variant, ask: "Full name, school line, course line, instructor name?"
5. Create `dba-writer-data/{COURSE-CODE}/` directory
6. Create `variants.md` inside it with all title page configs
7. Create empty `knowledge.md` with a header: `# {COURSE-CODE} Course Knowledge Base`
8. Create empty `feedback.md` with a header: `# {COURSE-CODE} Instructor Feedback Log`
9. Add the course to `dba-writer-data/courses.md` under "Active courses"
10. Confirm: "{COURSE-CODE} is set up with N variants. Ready."

**Frontmatter:**
```yaml
---
name: setup-course
description: >
  Initialize a new course for the semester. Creates the course data directory
  with variant configs, empty knowledge base, and empty feedback log.
  Use at the start of each new course.
allowed-tools: Bash, Write, Read
---
```

---

### 4.2 `/dba-writer:draft-essay`

**Trigger:** User has a writing assignment that requires a .docx submission.

**Input the user provides:** Assignment prompt, grading rubric, unit readings/materials.

**Behavior:**

1. **Identify course:**
   - Read `dba-writer-data/courses.md`
   - If one active course: use it
   - If multiple: display list, ask "Which course?"

2. **Load course context:**
   - Read `{course}/knowledge.md` for accumulated prior knowledge
   - Read `{course}/feedback.md` for past instructor feedback to avoid

3. **Auto-save new knowledge:**
   - Compare pasted readings against `knowledge.md`
   - If new concepts/material found, extract and append to `knowledge.md` under the current unit header before proceeding

4. **Variant selection:**
   - Read `{course}/variants.md`
   - Display candidate names with numbers
   - Ask: "Which variants? (e.g., '1 and 3' or 'all')"

5. **Assignment analysis (internal, not shown to user):**
   - List every question and sub-question in the prompt
   - List every rubric criterion and its highest performance level
   - Map which parts of the response address which requirements
   - Note any word count, page count, source count, or formatting requirements

6. **Draft N distinct versions:**
   - Each version uses a genuinely different angle, analogy, and argument structure
   - Apply the voice profile (see shared/voice-profile.md)
   - Apply APA 7 rules throughout (see shared/apa7-rules.md)
   - Use knowledge from knowledge.md where relevant (including cross-course if clearly connected)
   - Avoid mistakes logged in feedback.md
   - Each version is independently written, not a rephrased copy of another

7. **Verification loop (per version) — HARD GATE:**
   - Delegate draft + original prompt + rubric to the verifier agent
   - If RESULT: FAIL → read every issue, revise the draft, resubmit to verifier
   - Keep looping until RESULT: PASS
   - Maximum 5 iterations; if still failing, output with remaining issues listed
   - **Do NOT show any draft to the user that has not passed verification**

8. **Humanizer pass (invisible, per version):**
   - Apply all rules from shared/humanizer-checklist.md
   - Do not show before/after
   - Do not mention the humanizer ran

9. **Generate .docx (per version):**
   - Use scripts/generate-docx.py
   - APA 7 student paper format: Times New Roman 12pt, double-spaced, 1-inch margins
   - Title page with correct variant's name, school, course, instructor
   - Page numbers top right
   - Body text with proper APA headings where the assignment calls for them
   - Reference list on new page
   - Output files named: `{course}_{assignment-short-name}_v{N}.docx`

**Frontmatter:**
```yaml
---
name: draft-essay
description: >
  Draft a writing assignment as APA 7 formatted .docx files. Produces multiple
  distinct variants with different title pages. Each version passes strict
  verification (prompt, rubric, APA) before humanizer and .docx generation.
  Use for any assignment submitted as a Word document.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---
```

---

### 4.3 `/dba-writer:draft-post`

**Trigger:** User has a discussion post assignment.

**Input:** Discussion prompt, readings, rubric.

**Behavior:**

Same as draft-essay steps 1-3 (course identification, context loading, auto-save), then:

4. **Version count:**
   - Ask: "How many distinct versions?"

5. **Assignment analysis:** (same as draft-essay step 5)

6. **Draft N distinct versions:**
   - 250-350 words body text each
   - Essay format, no title page, no headings (unless prompt requires them)
   - Each version: different analogy/hook, different angle on the argument, different structure
   - Voice profile applied
   - APA 7 in-text citations + reference list at the end
   - No "In today's world" or "In conclusion" bookends

7. **Verification loop:** (same as draft-essay step 7 — HARD GATE)

8. **Humanizer pass:** (same as draft-essay step 8 — invisible)

9. **Output as formatted text in chat** (no .docx for discussion posts — user pastes into LMS)

**Frontmatter:**
```yaml
---
name: draft-post
description: >
  Draft a discussion post in APA 7 format. 250-350 words, essay format,
  no title page. Multiple distinct versions. Strict verification loop
  and invisible humanizer. Use for any discussion board assignment.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---
```

---

### 4.4 `/dba-writer:reply`

**Trigger:** User needs to write peer replies for a discussion post.

**Input:** The classmate's post(s) to reply to.

**Behavior:**

1. **Identify course** (same as others)
2. **Load feedback.md** (knowledge less relevant for replies)
3. **User pastes classmate post(s)**
4. **Ask version count:** "How many distinct reply sets?" (if user didn't specify)
5. **Draft N distinct reply sets:**
   - For each classmate post: one reply per set
   - 100-130 words each
   - Each reply must:
     - Engage the classmate's SPECIFIC argument (not generic praise)
     - Reference at least one source (from the unit readings or relevant prior knowledge)
     - End with a genuine question that advances the discussion
   - Each version set takes a different angle on the classmate's points
   - Different versions should not repeat the same compliment, source, or question
6. **Verification loop (per reply):**
   - Does it actually engage the classmate's specific argument?
   - Does it meet word count (100-130)?
   - Is the source reference accurate?
   - Is the closing question genuine and substantive?
   - HARD GATE: retry until PASS
7. **Humanizer pass** (invisible)
8. **Output as formatted text in chat**

**Frontmatter:**
```yaml
---
name: reply
description: >
  Write peer replies for discussion posts. 100-130 words each, engaging
  the classmate's specific argument with a source and a closing question.
  Multiple distinct reply sets. Strict verification and invisible humanizer.
allowed-tools: Bash, Read, Glob, Grep
---
```

---

### 4.5 `/dba-writer:save-unit`

**Trigger:** User wants to explicitly save unit readings/materials for future use.

**Input:** Unit readings, materials, or key takeaways.

**Behavior:**

1. Identify course
2. Read existing `{course}/knowledge.md`
3. Extract from new material:
   - Key concepts and definitions (with author attributions)
   - Author positions and arguments
   - Usable citations formatted as: Author (Year) — key claim
   - Connections to previously saved concepts from other units
4. Append under a `## Unit N: {topic}` header in knowledge.md
5. Confirm what was saved

Note: The drafting skills also auto-save when they detect new material. This skill is for bulk-loading readings when you're not drafting anything yet.

**Frontmatter:**
```yaml
---
name: save-unit
description: >
  Save unit readings and materials to the course knowledge base for future
  reference. Extracts key concepts, author positions, and usable citations.
  Use to pre-load material or when not drafting an assignment.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---
```

---

### 4.6 `/dba-writer:save-feedback`

**Trigger:** User received instructor feedback or grade comments.

**Input:** The feedback text (pasted or described).

**Behavior:**

1. Identify course
2. Read existing `{course}/feedback.md`
3. Extract the lesson:
   - What was the mistake or deduction?
   - What should be done differently?
   - Which assignment type was it (essay/post/reply)?
4. Append as a rule entry:
   ```
   ## Unit N — {assignment type}
   - Issue: {what was wrong}
   - Fix: {what to do instead}
   - Points lost: {if mentioned}
   ```
5. Confirm what was saved

All drafting skills read this file and treat each entry as a hard constraint to avoid.

**Frontmatter:**
```yaml
---
name: save-feedback
description: >
  Save instructor feedback to the course feedback log. Extracts the lesson
  (what went wrong, what to do differently) so future drafts avoid the same
  mistake. Use after receiving graded work back.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---
```

---

### 4.7 `/dba-writer:humanize`

**Trigger:** User wants to manually clean up any text for AI patterns.

**Input:** Any text.

**Behavior:**

1. Read shared/humanizer-checklist.md
2. Scan input for all 33 AI writing patterns
3. Rewrite to remove them while preserving meaning, length, and tone
4. Final check: scan rewrite for em dashes, en dashes, rule-of-three, copula avoidance, and other patterns. If any remain, fix them.
5. Output clean version

This is the standalone version. The other skills apply this automatically and invisibly.

**Frontmatter:**
```yaml
---
name: humanize
description: >
  Strip AI writing patterns from any text. Standalone version of the
  humanizer that runs automatically inside the drafting skills. Use when
  you want to manually clean up text written outside the plugin workflow.
allowed-tools: Read
---
```

---

## 5. Verifier agent

File: `agents/verifier.md`

This is a subagent that acts as a strict quality gate. It is called by the drafting skills in a retry loop. It returns PASS or FAIL with zero ambiguity.

```markdown
---
name: verifier
description: >
  Strict quality gate for academic writing. Returns PASS or FAIL with zero
  ambiguity. A single failed check means the entire draft is rejected and
  must be revised. Called by drafting skills in a mandatory retry loop.
model: sonnet
effort: high
maxTurns: 5
disallowedTools: Write, Edit
---

You are a strict academic writing gatekeeper. You receive three inputs:
1. The draft to evaluate
2. The original assignment prompt (with all questions and sub-questions)
3. The grading rubric

You return exactly one outcome: PASS or FAIL.
There is no "pass with suggestions." There is no "minor issues." Any problem is a FAIL.

Run three checks in order. Stop at the first FAIL.

CHECK 1 — PROMPT COMPLETENESS
List every question and sub-question from the prompt, numbered.
For each one, quote the specific sentence(s) from the draft that answer it.
If you cannot find a direct answer for ANY sub-question: FAIL.
  Output:
  - Every unanswered sub-question
  - What content is needed
  - Where in the draft it should go

CHECK 2 — RUBRIC ALIGNMENT
List every rubric criterion and its highest performance level descriptor.
For each, identify what in the draft satisfies it AT that highest level.
If any criterion is not met at the highest level: FAIL.
  Output:
  - Every underserved criterion
  - The rubric's highest-level descriptor (what "full marks" requires)
  - What specifically the draft is missing or doing insufficiently

CHECK 3 — APA 7 CORRECTNESS
For every in-text citation: verify a matching reference entry exists.
For every reference entry: verify at least one in-text citation exists.
Check citation format: author names, year, page numbers for direct quotes,
  narrative vs parenthetical format used correctly.
Check reference format: hanging indent instruction, capitalization, italics,
  DOI/URL format, alphabetical ordering.
Check: no fabricated citations, no invented page numbers, no made-up DOIs.
If any APA error exists: FAIL.
  Output:
  - Every error with the exact fix

PASS condition: all three checks pass with zero issues.

Output format on FAIL:
  RESULT: FAIL
  FAILED CHECK: [1, 2, or 3]
  ISSUES:
  - [specific problem]: [specific fix]
  - [specific problem]: [specific fix]

Output format on PASS:
  RESULT: PASS
  All sub-questions answered. All rubric criteria met at highest level.
  All APA 7 formatting correct.
```

---

## 6. Shared reference files

### 6.1 `shared/voice-profile.md`

This defines the user's established academic writing voice, extracted from their actual submissions across BUS 700, 719, and 729.

```markdown
# Writing Voice Profile

This is the target voice for all academic outputs from this plugin.
Extracted from actual submitted work across multiple DBA courses.

## Opening pattern
- Open with a concrete analogy that does real argumentative work.
- The analogy should connect a non-academic domain to the assignment's topic.
- Examples of analogies used: railroad gauge standardization, Malcolm McLean's
  shipping containers, factory electrification, building wiring codes.
- The analogy sets up the thesis. It is not decorative.

## Source integration
- Weave citations into the argument as they become relevant.
- Do NOT front-load all citations in one paragraph.
- Do NOT dump citations at the end of a paragraph as afterthoughts.
- A citation should arrive at the point where it strengthens the argument.
- Use a mix of narrative citations ("Mullaney and Rea (2022) argue that...")
  and parenthetical citations ("...since the thing being credited is the
  idea, not the phrasing (Excelsior Online Writing Lab, n.d.)").

## Workplace observation
- Include one personal workplace observation from AI/ML engineering work.
- Make it specific: the RAG platform, a model review process, an
  undocumented data lineage issue, a production incident. Not generic.
- This observation should connect to the academic argument, not be tacked on.
- Pattern: "I see this in my own work. On the retrieval platform I support..."
  or "At my firm, leadership handed generative AI tools to existing teams..."

## Closing pattern
- End with a hard declarative line that makes a concrete claim.
- No generic upbeat closings ("the future looks bright").
- No restating the thesis in different words.
- No "time will tell" or "only time will tell."
- The closer should land as a judgment, not a summary.
- Examples: "Fluency was never the thing being checked."
  "APA holds writers to the same bar." "The old process was the problem."

## Sentence structure
- Vary sentence length deliberately.
- Short sentences for emphasis. Longer ones for argument development.
- No uniform mid-length cadence (that reads as AI).
- Lists of examples should run to four, five, or six items naturally,
  not always exactly three (rule-of-three is an AI tell).

## What to avoid
- No title on discussion posts (unless the prompt requires one).
- No section headings on discussion posts (unless the prompt requires them).
- No "In today's world," "In today's academic landscape," or similar.
- No "In conclusion," "To sum up," or similar closing signposts.
- No "This is significant because..." or "This is important because..."
- No em dashes or en dashes anywhere.
- No generic praise of the topic's importance.
```

---

### 6.2 `shared/humanizer-checklist.md`

This is a condensed version of the full humanizer skill (622 lines), focused on the patterns that actually fire in academic writing. The full humanizer skill file is available at the path `/mnt/skills/user/humanizer/SKILL.md` if the complete version is needed.

Build this file by condensing the 33 patterns from the humanizer SKILL.md into a checklist format optimized for quick scanning during the invisible pass. For each pattern, include:
- The pattern number and name
- 3-5 trigger words/phrases to scan for
- The one-line fix

Key patterns that fire most often in academic writing (prioritize these):
- Pattern 1: Significance inflation (serves as, testament, pivotal, crucial)
- Pattern 3: Superficial -ing analyses (highlighting, ensuring, reflecting)
- Pattern 4: Promotional language (vibrant, rich, profound, nestled)
- Pattern 7: AI vocabulary (additionally, delve, enhance, foster, landscape, tapestry, underscore)
- Pattern 8: Copula avoidance (serves as, stands as, features, boasts)
- Pattern 9: Negative parallelisms (not just X, it's Y)
- Pattern 10: Rule of three
- Pattern 14: Em dashes and en dashes (HARD ZERO — none allowed in final output)
- Pattern 22: Sycophantic tone (Great question! Excellent point!)
- Pattern 23: Filler phrases (In order to, Due to the fact that)
- Pattern 25: Generic positive conclusions
- Pattern 27: Persuasive authority tropes (The real question is, at its core)
- Pattern 28: Signposting (Let's dive in, here's what you need to know)
- Pattern 31: Manufactured punchlines / staccato drama
- Pattern 33: Conversational rhetorical openers (Honestly? Look, Here's the thing)

Final scan rule: after all rewrites, scan the entire output for `—` and `–`. If any em or en dash remains, the humanizer pass is not complete.

---

### 6.3 `shared/verification-protocol.md`

```markdown
# Verification Protocol

This protocol defines what the verifier agent checks. Every drafting skill
delegates to the verifier agent using this protocol. The verifier runs in
a retry loop: FAIL means revise and resubmit. PASS means proceed to humanizer.

## The retry loop (enforced by each drafting skill)

1. Draft the output.
2. Delegate draft + prompt + rubric to verifier agent.
3. If FAIL: read every issue. Revise the draft to fix ALL of them. Go to step 2.
4. If PASS: proceed to humanizer pass.
5. Maximum 5 iterations. If still failing after 5, output with remaining issues
   listed so user can address manually. This should be rare.

CRITICAL: Do NOT show the user any draft that has not passed verification.
CRITICAL: Do NOT skip verification to save time or tokens.
CRITICAL: Do NOT self-assess ("I checked and it looks good"). Delegate to the
verifier agent. The separation matters because the verifier is adversarial.

## What the verifier checks

### Check 1: Prompt completeness
Every question in the assignment prompt gets answered. Every sub-question
gets answered. Every explicit instruction gets followed. No part of the
prompt is missed. The verifier lists each sub-question and maps it to
specific sentences in the draft.

### Check 2: Rubric alignment
Every rubric criterion receives sufficient attention at the HIGHEST
performance level. The verifier reads the rubric's top-level descriptor
for each criterion and verifies the draft meets it. "Adequate" is not
enough; the goal is maximum points.

### Check 3: APA 7 correctness
All in-text citations match reference entries. All references have at
least one in-text citation. Citation and reference formatting follows
APA 7. No fabricated citations. No invented page numbers or DOIs.

## Additional checks by output type

### Writing assignments (.docx)
- Word/page count within specified limits
- APA heading levels used correctly (if required by prompt)
- Title page information matches the selected variant exactly

### Discussion posts
- Body word count: 250-350 words (not counting references)
- Essay format (no bullet lists, no numbered lists, unless prompt requires)
- Reference list present and APA-formatted

### Peer replies
- Word count: 100-130 words each
- Reply engages the classmate's SPECIFIC argument (not generic)
- At least one source referenced
- Ends with a genuine question (not rhetorical)
```

---

### 6.4 `shared/apa7-rules.md`

```markdown
# APA 7th Edition — Student Paper Quick Reference

This file covers the APA 7 rules relevant to DBA coursework.
Student paper format only (not professional manuscript).

## Title page (student paper)
- Page 1, centered in upper half:
  - Paper title (bold, title case)
  - Blank line
  - Author name
  - Department/school, University name
  - Course number and name
  - Instructor name
  - Due date
- Page number: top right, starting at 1
- No running head (student papers don't require one in APA 7)

## General formatting
- Font: Times New Roman 12pt
- Spacing: Double-spaced throughout (including references)
- Margins: 1 inch all sides
- Paragraph indent: 0.5 inch first line
- Page numbers: top right, flush right
- Alignment: left-aligned (no full justification)

## Headings (when required)
- Level 1: Centered, bold, title case
- Level 2: Left-aligned, bold, title case
- Level 3: Left-aligned, bold italic, title case
- Level 4: Indented, bold, title case, period. Text continues.
- Level 5: Indented, bold italic, title case, period. Text continues.

## In-text citations
- Parenthetical: (Author, Year) or (Author, Year, p. X) for direct quotes
- Narrative: Author (Year) states that...
- Two authors: (Author & Author, Year) — use "&" in parenthetical, "and" in narrative
- Three or more: (First Author et al., Year) from the first citation
- No author: ("Title of Work," Year) — title in quotes if article, italics if book
- Multiple citations in one parenthetical: alphabetical, semicolons between

## Direct quotations
- Under 40 words: in quotes within the text, with page number
- 40+ words: block quote (new paragraph, 0.5" indent, no quotes), with page number
- Page number required for ALL direct quotes: (Author, Year, p. X)

## Paraphrasing
- Page number encouraged but not required
- Still requires (Author, Year) citation
- Must be genuinely reworded, not minor word swaps

## Reference list
- New page, "References" centered bold at top
- Hanging indent: 0.5" for lines after the first
- Double-spaced
- Alphabetical by first author's last name
- Author format: Last, F. M.
- Year in parentheses after author
- Article titles: sentence case, not italic
- Journal names: title case, italic
- Book titles: sentence case, italic
- DOI as https://doi.org/xxxxx (preferred over URL when available)
- URL: Retrieved Month Day, Year, from https://... (only for content that changes)
- No period after DOI or URL

## Common errors to catch
- Citation in text with no matching reference (or vice versa)
- Using "et al." on first citation of a two-author source (wrong — use both names)
- Missing page numbers on direct quotes
- Reference list not alphabetical
- Inconsistent date formats
- Fabricated DOIs or page numbers (NEVER fabricate anything)
- Using "&" in narrative citations (should be "and")
- Using "and" in parenthetical citations (should be "&")
```

---

## 7. Hooks

File: `hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "pip install python-docx --quiet --break-system-packages 2>/dev/null; echo 'dba-writer: python-docx ready'"
          }
        ]
      }
    ]
  }
}
```

This runs once at session start. If python-docx is already installed, it finishes instantly. The `--quiet` flag suppresses output.

---

## 8. Scripts

### `scripts/generate-docx.py`

Build a Python script using `python-docx` that:

**Accepts arguments:**
- `--title` — paper title
- `--author` — author full name
- `--school` — school/department line
- `--course` — course code and name
- `--instructor` — instructor name
- `--date` — due date
- `--body` — path to a markdown or text file containing the essay body
- `--references` — path to a text file containing the reference list
- `--output` — output .docx file path

**Produces:**
- Page 1: APA 7 student title page (centered, upper half of page)
- Page 2+: body text with 0.5" first-line indent, double-spaced
- Handles APA heading levels (Level 1-3) if markdown headers present
- Final page(s): Reference list with "References" centered bold header, hanging indent
- Times New Roman 12pt throughout
- 1-inch margins (US Letter)
- Page numbers top right starting at 1

**Important .docx generation notes (from the docx skill):**
- Page size defaults to A4 — explicitly set to US Letter: `width: 12240, height: 15840` (DXA)
- Never use `\n` — use separate Paragraph elements
- Use `numbering` config for bullet lists, never literal `•`
- PageBreak must be inside a Paragraph

---

## 9. Data files — initial content

### `dba-writer-data/courses.md`

```markdown
# DBA Course Registry

## Active courses
(none yet — use /dba-writer:setup-course to add)

## Completed courses
(none yet — move courses here when the semester ends)
```

### `dba-writer-data/{COURSE}/variants.md` (example for BUS 700)

```markdown
# BUS 700 — Orientation Seminar: Variants

## Variant 1
- Name: Chandrika Miryala
- School: School of Business, Belhaven University
- Course: BUS 700: Orientation Seminar
- Instructor: Dr. D Lance Revenaugh

## Variant 2
- Name: Keerthan Tumuganti
- School: Belhaven University
- Course: BUS 700: Orientation Seminar
- Instructor: Dr. Kimberly Strickland

## Variant 3
- Name: Bhavana Ganji
- School: School of Business, Belhaven University
- Course: BUS 700: Orientation Seminar
- Instructor: Dr. Michael Brizek
```

### `dba-writer-data/{COURSE}/knowledge.md` (starts empty)

```markdown
# BUS 700 Course Knowledge Base

(Accumulated unit readings, concepts, and usable citations)
```

### `dba-writer-data/{COURSE}/feedback.md` (starts empty)

```markdown
# BUS 700 Instructor Feedback Log

(Lessons from graded work — each entry is a mistake to avoid in future drafts)
```

---

## 10. Cross-course knowledge rules

The skill instructions for draft-essay, draft-post, and reply should include this rule:

> Load the active course's knowledge.md as the primary source. If the assignment topic has a clear connection to a concept from a completed or different active course, you may check that course's knowledge.md too. Do not force connections. Only pull cross-course material when it genuinely strengthens the argument and is relevant to the current prompt.

---

## 11. README.md

Build a README that covers:

### Overview
- What the plugin does (one paragraph)
- Who it's for (DBA students managing multiple courses with multiple variants)

### Quick start
1. Install: `claude --plugin-dir ./dba-writer` (for dev) or marketplace install
2. Set up your first course: `/dba-writer:setup-course`
3. Draft your first assignment: `/dba-writer:draft-essay` or `/dba-writer:draft-post`

### Skills reference
For each of the 7 skills, document:
- Invocation: `/dba-writer:{name}`
- What it does (one sentence)
- What input it expects
- What output it produces
- Example usage

### Workflow: typical assignment cycle
1. Start of semester: `/dba-writer:setup-course` for each course
2. Each unit: paste readings + prompt → `/dba-writer:draft-essay` or `/dba-writer:draft-post`
3. After classmates post: paste their posts → `/dba-writer:reply`
4. After grades come back: paste feedback → `/dba-writer:save-feedback`
5. Between assignments (optional): `/dba-writer:save-unit` to bulk-load readings

### Verification system
Explain the strict verification loop:
- Every output is checked against the full prompt, rubric, and APA 7 rules
- Failed verification triggers automatic revision and recheck
- Maximum 5 retry attempts
- User never sees an unverified draft

### Humanizer system
Explain the invisible AI-pattern removal:
- Runs automatically on all outputs after verification passes
- Based on Wikipedia's "Signs of AI Writing" (33 patterns)
- `/dba-writer:humanize` available for standalone manual use

### Data directory structure
Explain `dba-writer-data/` and what each file does:
- `courses.md` — course registry
- `{COURSE}/variants.md` — title page configs
- `{COURSE}/knowledge.md` — accumulated unit knowledge
- `{COURSE}/feedback.md` — instructor feedback log

### Architecture
- Component summary table (7 skills, 1 agent, 1 hook, 1 script)
- File tree showing the complete plugin structure

---

## 12. Implementation notes for Claude Code

When building this plugin:

1. **Build order:** manifest → shared references → agent → skills → hooks → scripts → data templates → README
2. **Test with:** `claude --plugin-dir ./dba-writer` — no marketplace needed during development
3. **Validate with:** `claude plugin validate ./dba-writer`
4. **The humanizer checklist** should be condensed from the full humanizer SKILL.md at `/mnt/skills/user/humanizer/SKILL.md` (622 lines, 33 patterns). Condense to a scannable checklist format, keeping all 33 pattern names and their trigger words but removing the verbose before/after examples.
5. **The generate-docx.py script** must handle the edge cases from the docx skill: US Letter page size (not A4), proper paragraph elements (no `\n`), hanging indent for references.
6. **Every SKILL.md** should include the verification loop instructions and humanizer invocation as the final steps, since these apply to all drafting skills.
7. **The voice profile** is extracted from actual submitted work (examples provided in this spec under the voice-profile section). Do not invent a different voice.

---

## 13. Pre-loaded course data

Build these courses as part of the initial data setup:

### BUS 700 — Orientation Seminar (completed)
Variants: Chandrika Miryala / Dr. D Lance Revenaugh, Keerthan Tumuganti / Dr. Kimberly Strickland, Bhavana Ganji / Dr. Michael Brizek

### BUS 719 — Issues in Management (need variant details from user)

### BUS 729 — AI Foundations for Executives (need variant details from user)

For BUS 719 and BUS 729, create the directory structure with placeholder variants.md files that say "(variants not yet configured — run /dba-writer:setup-course or edit this file)".

---

End of specification.
