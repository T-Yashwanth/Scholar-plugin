# Generating the .docx

## Command

    python "${CLAUDE_PLUGIN_ROOT}/scripts/generate-docx.py" \
      --title "Paper Title in Title Case" \
      --author "Full Name" \
      --school "School of Business, Belhaven University" \
      --course "BUS 700: Orientation Seminar" \
      --instructor "Dr. Instructor Name" \
      --date "September 20, 2026" \
      --body "<path to body file>" \
      --references "<path to references file>" \
      --output "<course>_<assignment>_v<N>.docx"

Use `python`, not `python3` and not `py`. On Windows `python3` is often a
Microsoft Store stub that is not a working interpreter, and `py` may resolve
to a different installation than the one the SessionStart hook installed
python-docx into.

All flags except `--references` are required.

## Body file format

Plain text or light markdown. Write it to a scratch path, not the project root.

- Blank line between paragraphs. Every blank-line-separated block becomes one
  properly indented, double-spaced paragraph.
- `# Heading` becomes APA Level 1 (centered, bold).
- `## Heading` becomes APA Level 2 (left, bold).
- `### Heading` becomes APA Level 3 (left, bold italic).
- Omit headings entirely unless the assignment calls for them.
- Do not put the title in the body. The title page already has it.

## References file format

One entry per line. Blank lines are ignored. Entries must already be in APA 7
order and format, since the script applies the hanging indent but does not
reorder or reformat them.

## What the script guarantees

US Letter, 1 inch margins, Times New Roman 12pt, double spaced with no extra
paragraph spacing, 0.5 inch first-line body indent, page number top right via
a PAGE field, references on a new page with 0.5 inch hanging indents.

## Failure handling

Exit code 2 means python-docx is missing for that interpreter. Exit code 1
means something else failed.

Do not discard the drafted text. The essay is the expensive part and the
conversion is cheap and retryable. On any failure:

1. Write the verified body and references to a `.md` file beside the intended
   `.docx` output path so nothing is lost.
2. Tell the user the content is complete and verified, and that only the .docx
   conversion failed.
3. Give them the exact fix: `python -m pip install python-docx`
4. Offer to retry the conversion once they have run it.
