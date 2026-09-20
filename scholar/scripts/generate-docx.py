#!/usr/bin/env python
"""Generate an APA 7 student paper as .docx.

Usage:
  python generate-docx.py --title "..." --author "..." --school "..." \
      --course "..." --instructor "..." --date "..." \
      --body body.md [--references refs.txt] --output out.docx

Body file: plain text or light markdown. Blank lines separate paragraphs.
Leading '#', '##', '###' become APA heading levels 1, 2, 3.
References file: one entry per line (blank lines ignored).

Exits non-zero with a clear message if python-docx is missing, so the caller
can fall back to markdown rather than losing the drafted content.
"""

import argparse
import os
import sys

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt
except ImportError:
    sys.stderr.write(
        "generate-docx: python-docx is not installed for this interpreter.\n"
        "Fix: python -m pip install python-docx\n"
    )
    sys.exit(2)

FONT = "Times New Roman"


def set_base_style(doc):
    """APA body defaults: Times New Roman 12pt, double spaced, no extra gap.

    The font goes on the Normal style rather than each run, so every
    paragraph inherits it. w:eastAsia must be set explicitly or Word may
    substitute a different font for some characters.
    """
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(12)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), FONT)
    rfonts.set(qn("w:hAnsi"), FONT)
    rfonts.set(qn("w:eastAsia"), FONT)
    pf = style.paragraph_format
    pf.line_spacing = 2.0
    # python-docx leaves a default space_after that breaks true double spacing.
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)


def set_page(section):
    """US Letter with 1 inch margins. python-docx defaults to A4."""
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    for side in ("left", "right", "top", "bottom"):
        setattr(section, "%s_margin" % side, Inches(1))


def add_page_number(section):
    """Page number, top right, via a raw PAGE field.

    python-docx has no API for field codes, so the w:fldSimple element is
    built by hand and appended to the header paragraph.
    """
    para = section.header.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    text = OxmlElement("w:t")
    text.text = "1"
    run.append(text)
    fld.append(run)
    para._p.append(fld)


def add_para(doc, text, indent=True, align=None, bold=False, italic=False):
    para = doc.add_paragraph()
    if align is not None:
        para.alignment = align
    if indent:
        para.paragraph_format.first_line_indent = Inches(0.5)
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    return para


def build_title_page(doc, args):
    """APA 7 student title page: centered, upper half, no running head."""
    center = WD_ALIGN_PARAGRAPH.CENTER
    for _ in range(4):
        add_para(doc, "", indent=False)
    add_para(doc, args.title, indent=False, align=center, bold=True)
    add_para(doc, "", indent=False)
    for line in (args.author, args.school, args.course,
                 args.instructor, args.date):
        add_para(doc, line, indent=False, align=center)


def page_break(doc):
    """A page break must live inside a paragraph run."""
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def add_body(doc, path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()

    # One add_paragraph per paragraph. A newline inside add_paragraph does
    # NOT start a new paragraph, so indent and line spacing would silently
    # fail for everything after the first line.
    for block in raw.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("### "):
            add_para(doc, block[4:].strip(), indent=False,
                     bold=True, italic=True)
        elif block.startswith("## "):
            add_para(doc, block[3:].strip(), indent=False, bold=True)
        elif block.startswith("# "):
            add_para(doc, block[2:].strip(), indent=False,
                     align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
        else:
            add_para(doc, " ".join(block.split()), indent=True)


def add_references(doc, path):
    with open(path, encoding="utf-8") as fh:
        entries = [ln.strip() for ln in fh if ln.strip()]
    if not entries:
        return
    page_break(doc)
    add_para(doc, "References", indent=False,
             align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    for entry in entries:
        para = doc.add_paragraph()
        pf = para.paragraph_format
        # Hanging indent: text block in 0.5", first line pulled back out.
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.5)
        para.add_run(entry)


def main():
    ap = argparse.ArgumentParser()
    for flag in ("title", "author", "school", "course", "instructor",
                 "date", "body", "output"):
        ap.add_argument("--%s" % flag, required=True)
    ap.add_argument("--references")
    args = ap.parse_args()

    # Check inputs up front so a bad path fails with a clear message rather
    # than a traceback. The caller falls back to markdown on any failure, and
    # needs to know which file was wrong.
    for flag, path in (("--body", args.body), ("--references", args.references)):
        if path and not os.path.isfile(path):
            sys.stderr.write("generate-docx: %s file not found: %s\n" % (flag, path))
            return 1

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.isdir(out_dir):
        sys.stderr.write("generate-docx: output directory does not exist: %s\n" % out_dir)
        return 1

    doc = Document()
    set_base_style(doc)
    section = doc.sections[0]
    set_page(section)
    add_page_number(section)

    build_title_page(doc, args)
    page_break(doc)
    add_body(doc, args.body)
    if args.references:
        add_references(doc, args.references)

    try:
        doc.save(args.output)
    except OSError as exc:
        sys.stderr.write("generate-docx: could not write %s (%s)\n"
                         % (args.output, exc))
        return 1
    print("generate-docx: wrote %s" % args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
