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

README_FOOTER = """
---

PDF: [{cv}]({cv}) · [{cv_en}]({cv_en})

_Текст собран из `{ru}/` и `{en}/`; PDF пересобирается автоматически при каждом
изменении этих файлов._
"""


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
    return '\n\n'.join(chunks) + '\n', parts


def readme_text(ru_folder, en_folder):
    text, _ = assemble(ru_folder)
    footer = README_FOOTER.format(
        cv='savin_vladimir_cv.pdf',
        cv_en='savin_vladimir_cv_en.pdf',
        ru=ru_folder.name,
        en=en_folder.name,
    )
    return text.rstrip('\n') + '\n' + footer


def main(argv):
    if len(argv) < 2:
        raise SystemExit('usage: build_resume.py <resume-folder> [--docx] [--readme <path>]')
    folder = Path(argv[1]).resolve()
    text, parts = assemble(folder)
    out_dir = BUILD / folder.name
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / 'resume.md'
    md_path.write_text(text, encoding='utf-8')
    print(f'{md_path}: {len(parts)} source files, {len(text)} chars')

    if '--readme' in argv:
        target = Path(argv[argv.index('--readme') + 1]).resolve()
        en_folder = target.parent / 'resume-en'
        if not en_folder.is_dir():
            en_folder = folder
        target.write_text(readme_text(folder, en_folder), encoding='utf-8')
        print(f'{target}: README generated')

    if '--docx' in argv:
        docx_path = out_dir / 'resume.docx'
        build_docx(str(md_path), str(docx_path))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
