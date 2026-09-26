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
      --output "<assignment>_<last-name>_v<N>.docx"

Use `python`, not `python3` and not `py`. On Windows `python3` is often a
Microsoft Store stub that is not a working interpreter, and `py` may resolve
to a different installation than the one that has python-docx.

All flags except `--references` are required.

## Body file format

Plain text or light markdown. Write it to a scratch path, not the project root.

- Blank line between paragraphs. Every blank-line-separated block becomes one
  properly indented, double-spaced paragraph.
- `# Heading` becomes APA Level 1 (centered, bold).
- `## Heading` becomes APA Level 2 (left, bold).
- `### Heading` becomes APA Level 3 (left, bold italic).
- `#### Heading` becomes APA Level 4 (indented, bold, ends with a period).
  The next paragraph continues on the same line, as APA requires.
- `##### Heading` becomes APA Level 5 (indented, bold italic, ends with a
  period), run in the same way.
- `**text**` becomes bold. Rarely needed in APA body text.
- `*text*` becomes italic. Use it for titles of books, reports, and other
  standalone works named in the text.
- Omit headings entirely unless the assignment calls for them.
- Do not put the title in the body file. The script prints it on the title
  page and again, centered and bold, at the top of the first body page, as
  APA 7 requires. Do not add an "Introduction" heading.

## References file format

One entry per line. Blank lines are ignored. Entries must already be in APA 7
order and format, since the script applies the hanging indent but does not
reorder or reformat them.

Mark every part APA requires in italics with `*...*`: journal name and
volume, book title, report title, webpage title, video title. For example:

    Smith, J. (2020). Leading change. *Journal of Management, 12*(3), 45-60. https://doi.org/10.1000/xyz

## What the script guarantees

US Letter, 1 inch margins, Times New Roman 12pt, double spaced with no extra
paragraph spacing, 0.5 inch first-line body indent, page number top right via
a PAGE field, references on a new page with 0.5 inch hanging indents.

## Failure handling

Exit code 3 means python-docx is missing for that interpreter. Exit code 2
means a required flag was missing, so fix the command rather than
installing anything. Exit code 1 means something else failed; the stderr
line says what.

Do not discard the drafted text. The essay is the expensive part and the
conversion is cheap and retryable. On any failure:

1. Write the verified body and references to a `.md` file beside the intended
   `.docx` output path so nothing is lost.
2. Tell the user the content is complete and verified, and that only the .docx
   conversion failed.
3. Give them the exact fix. For exit 3 that is
   `python -m pip install python-docx`.
4. Offer to retry the conversion once they have run it.
