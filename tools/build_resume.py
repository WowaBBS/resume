# -*- coding: utf-8 -*-
"""Assemble one resume from its folder and build the DOCX.

A resume folder holds topic files (`NN_slug.md`) and one experience folder
(`NN_experience/`) whose files are prefixed with the job start date, so they
sort chronologically. Resumes list the newest job first: the experience files
are emitted in reverse name order.

Sources stay next to each other; everything generated goes to `build/<folder>/`
(`resume.md`, `resume.docx`) so the tree stays clean and `build/` can be
git-ignored.

Usage:
    build_resume.py <resume-folder> [--docx] [--readme <path>]
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md2docx import build as build_docx  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'build'
GENERATED = {'resume.md', 'resume.docx', 'resume.pdf'}

README_HEAD = {
    'en': '**English** · [Русский]({alt})',
    'ru': '**Русский** · [English]({alt})',
}

# Only the Russian page gets a portrait: the international page stays text-only.
# `align="right"` on <img> makes the text wrap around the picture; if GitHub ever
# strips it, the fallback is a plain left-aligned image above the name.
PHOTO_BLOCK = """
<img src="resume/photo.jpg" width="140" align="right" alt="Владимир Савин">
"""

PDF_RU = '[PDF](savin_vladimir_cv.pdf)'
PDF_EN = '[PDF](savin_vladimir_cv_en.pdf)'
DOCX_RU = '[DOCX](savin_vladimir_cv.docx)'
DOCX_EN = '[DOCX](savin_vladimir_cv_en.docx)'

README_FOOTER = """
---

_Sources: `resume/` (ru), `resume-en/` (en). PDF and DOCX are rebuilt automatically
whenever these files change._
"""


def readme_text(folder, lang, alt):
    text, _ = assemble(folder)
    # The photo directive carries a local absolute path — keep it out of README.
    text = '\n'.join(l for l in text.split('\n') if not l.strip().startswith('<!-- photo:'))
    # The floated portrait stays active while the header rule is drawn, and the
    # line would cut through the picture. Drop that rule from the web page only;
    # the DOCX/PDF keep it.
    head_text, sep, rest = text.partition('## ')
    if sep:
        head_lines = [l for l in head_text.split('\n') if l.strip() != '---']
        text = '\n'.join(head_lines).rstrip() + '\n\n## ' + rest
    # GitHub strips CSS, so a per-element "left here, right there" needs a table
    # (and its borders look heavy). A whole right-aligned line does work: `align`
    # on a paragraph is kept. Inside HTML the markdown is not parsed, so links are
    # plain <a> tags.
    if lang == 'ru':
        line = ('<p align="right">'
                '<b>Русский</b> · <a href="README.md">English</a> · '
                '<a href="savin_vladimir_cv.pdf">PDF</a> · '
                '<a href="savin_vladimir_cv.docx">DOCX</a></p>')
    else:
        line = ('<p align="right">'
                '<a href="README.ru.md">Русский</a> · <b>English</b> · '
                '<a href="savin_vladimir_cv_en.pdf">PDF</a> · '
                '<a href="savin_vladimir_cv_en.docx">DOCX</a></p>')
    head = line
    if lang == 'ru':
        # GitHub draws a border under every H1. Declare the float after the
        # heading so that border is painted first and the portrait is not cut.
        lines = text.split('\n')
        h1 = next((i for i, l in enumerate(lines) if l.startswith('# ')), None)
        if h1 is not None:
            lines[h1 + 1:h1 + 1] = ['', PHOTO_BLOCK.strip()]
            text = '\n'.join(lines)
        else:
            head += '\n' + PHOTO_BLOCK.strip()
    footer = README_FOOTER
    return head + '\n\n' + text.rstrip('\n') + '\n' + footer


def is_topic(name):
    return name.endswith('.md') and name not in GENERATED and not name.startswith('_')


def collect(folder):
    """Return [(relative name, path)] in document order."""
    parts = []
    for entry in sorted(os.listdir(folder)):
        path = folder / entry
        if path.is_dir() and re.match(r'^\d\d_', entry):
            kids = sorted(
                (k for k in os.listdir(path) if is_topic(k) and k != 'title.md'),
                reverse=True,  # newest first
            )
            if (path / 'title.md').is_file():
                parts.append((f'{entry}/title.md', path / 'title.md'))
            parts.extend((f'{entry}/{k}', path / k) for k in kids)
        elif path.is_file() and is_topic(entry):
            parts.append((entry, path))
    return parts


def assemble(folder):
    folder = Path(folder)
    parts = collect(folder)
    if not parts:
        raise SystemExit(f'no markdown sources in {folder}')
    chunks = [p.read_text(encoding='utf-8').strip('\n') for _, p in parts]
    text = '\n\n'.join(chunks) + '\n'
    # `<!-- photo: name.jpg -->` is relative to the resume folder; make it absolute
    # so the assembled copy can live in build/ and still find the picture.
    def absolute(m):
        candidate = Path(m.group(1).strip())
        if not candidate.is_absolute():
            candidate = (folder / candidate).resolve()
        return f'<!-- photo: {candidate} -->'

    text = re.sub(r'<!--\s*photo:\s*(.+?)\s*-->', absolute, text)
    return text, parts


def main(argv):
    if len(argv) < 2:
        raise SystemExit('usage: build_resume.py <resume-folder> [--docx] [--readme <path> --lang ru|en --alt <file>]')
    folder = Path(argv[1]).resolve()
    text, parts = assemble(folder)
    out_dir = BUILD / folder.name
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / 'resume.md'
    md_path.write_text(text, encoding='utf-8', newline='\n')
    print(f'{md_path}: {len(parts)} source files, {len(text)} chars')

    if '--readme' in argv:
        target = Path(argv[argv.index('--readme') + 1]).resolve()
        lang = argv[argv.index('--lang') + 1] if '--lang' in argv else 'ru'
        alt = argv[argv.index('--alt') + 1] if '--alt' in argv else 'README.md'
        target.write_text(readme_text(folder, lang, alt), encoding='utf-8', newline='\n')
        print(f'{target}: README generated ({lang})')

    if '--docx' in argv:
        docx_path = out_dir / 'resume.docx'
        build_docx(str(md_path), str(docx_path))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
