# -*- coding: utf-8 -*-
"""Markdown -> styled DOCX for resume documents."""
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ACCENT = RGBColor(0x1F, 0x38, 0x64)
ACCENT2 = RGBColor(0x2E, 0x54, 0x96)
GREY = RGBColor(0x44, 0x44, 0x44)
MUTED = RGBColor(0x77, 0x77, 0x77)
FONT = 'Calibri'
BODY = 10.2


def add_hyperlink(paragraph, url, text, size=None, color='2E5496'):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
        is_external=True,
    )
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), FONT)
    rFonts.set(qn('w:hAnsi'), FONT)
    rPr.append(rFonts)
    c = OxmlElement('w:color')
    c.set(qn('w:val'), color)
    rPr.append(c)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    if size:
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(int(size * 2)))
        rPr.append(sz)
    new_run.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_inline(paragraph, text, size=BODY, color=None, bold_all=False, italic_all=False):
    """Supports **bold**, *italic*, [text](url), `code`."""
    token = re.compile(r'(\*\*.+?\*\*|\*[^*\n]+?\*|\[[^\]]+\]\([^)]+\)|`[^`]+`)')
    pos = 0
    for m in token.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            r.font.size = Pt(size)
            r.font.name = FONT
            r.bold = bold_all
            r.italic = italic_all
            if color:
                r.font.color.rgb = color
        chunk = m.group(0)
        if chunk.startswith('**'):
            r = paragraph.add_run(chunk[2:-2])
            r.font.size = Pt(size)
            r.font.name = FONT
            r.bold = True
            r.italic = italic_all
            if color:
                r.font.color.rgb = color
        elif chunk.startswith('`'):
            r = paragraph.add_run(chunk[1:-1])
            r.font.size = Pt(size)
            r.font.name = FONT
            r.font.color.rgb = ACCENT2
            r.bold = bold_all
        elif chunk.startswith('['):
            label, url = re.match(r'\[([^\]]+)\]\(([^)]+)\)', chunk).groups()
            if url.startswith('http'):
                add_hyperlink(paragraph, url, label, size=size)
            else:
                r = paragraph.add_run(label)
                r.font.size = Pt(size)
                r.font.name = FONT
                r.bold = bold_all
        else:
            r = paragraph.add_run(chunk[1:-1])
            r.font.size = Pt(size)
            r.font.name = FONT
            r.italic = True
            if color:
                r.font.color.rgb = color
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        r.font.size = Pt(size)
        r.font.name = FONT
        r.bold = bold_all
        r.italic = italic_all
        if color:
            r.font.color.rgb = color


def bottom_border(paragraph, size=6, color='9DB2D6'):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def shade(paragraph, fill='F2F5FA'):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    pPr.append(shd)


def left_bar(paragraph, color='9DB2D6'):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '18')
    left.set(qn('w:space'), '6')
    left.set(qn('w:color'), color)
    pBdr.append(left)
    pPr.append(pBdr)


PHOTO_RE = re.compile(r'^<!--\s*photo:\s*(.+?)\s*-->$')


def no_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'none')
        el.set(qn('w:sz'), '0')
        borders.append(el)
    tblPr.append(borders)
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)


def render_header_with_photo(doc, block, photo_path, text_width=14.7, photo_width=2.9):
    """Header block as a borderless table: text on the left, photo on the right."""
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    no_table_borders(table)
    table.columns[0].width = Cm(text_width)
    table.columns[1].width = Cm(photo_width)
    text_cell, photo_cell = table.rows[0].cells
    text_cell.width = Cm(text_width)
    photo_cell.width = Cm(photo_width)
    text_cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    photo_cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP

    first = True
    for raw in block:
        line = raw.rstrip()
        if not line.strip():
            continue
        p = text_cell.paragraphs[0] if first else text_cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        if line.startswith('# '):
            r = p.add_run(line[2:].strip())
            r.bold = True
            r.font.size = Pt(18)
            r.font.name = FONT
            r.font.color.rgb = ACCENT
        elif line.startswith('**') and line.endswith('**'):
            r = p.add_run(line[2:-2])
            r.bold = True
            r.font.size = Pt(11)
            r.font.name = FONT
            r.font.color.rgb = ACCENT2
        else:
            add_inline(p, line, size=9.4, color=GREY)

    p = photo_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(photo_path, width=Cm(photo_width - 0.4))


def setup(doc, margin_lr=1.6, margin_tb=1.25):
    st = doc.styles['Normal']
    st.font.name = FONT
    st.font.size = Pt(BODY)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    pf = st.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.03
    sec = doc.sections[0]
    sec.page_width = Cm(21)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(margin_lr)
    sec.right_margin = Cm(margin_lr)
    sec.top_margin = Cm(margin_tb)
    sec.bottom_margin = Cm(margin_tb)


def build(md_path, docx_path):
    lines = open(md_path, encoding='utf-8').read().split('\n')
    doc = Document()
    setup(doc)
    lb = doc.styles['List Bullet']
    lb.font.name = FONT
    lb.font.size = Pt(BODY)
    lb.paragraph_format.left_indent = Cm(0.55)
    lb.paragraph_format.first_line_indent = Cm(-0.35)
    lb.paragraph_format.space_after = Pt(1.2)
    lb.paragraph_format.line_spacing = 1.0

    seen_h1 = False
    quote_buf = []

    photo = None
    for idx, raw in enumerate(lines):
        m = PHOTO_RE.match(raw.strip())
        if m:
            photo = m.group(1)
            del lines[idx]
            break

    i = 0
    if photo:
        end = next(
            (k for k, l in enumerate(lines) if l.startswith('## ') or l.strip() == '---'),
            len(lines),
        )
        render_header_with_photo(doc, lines[:end], photo)
        seen_h1 = True
        i = end

    def flush_quote():
        nonlocal quote_buf
        if not quote_buf:
            return
        cleaned = []
        for q in quote_buf:
            s = q.strip()
            if s.startswith('## '):
                cleaned.append(('head', s[3:]))
            elif s:
                cleaned.append(('line', s))
        for idx, (kind, txt) in enumerate(cleaned):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.45)
            p.paragraph_format.right_indent = Cm(0.2)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(7 if idx == len(cleaned) - 1 else 0)
            p.paragraph_format.line_spacing = 1.05
            if kind == 'head':
                add_inline(p, txt.upper(), size=9, color=ACCENT, bold_all=True)
            else:
                add_inline(p, txt, size=9.3, color=GREY)
            shade(p)
            left_bar(p)
        quote_buf = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        if line.startswith('>'):
            quote_buf.append(line[1:])
            i += 1
            continue
        flush_quote()

        if not line.strip():
            i += 1
            continue

        if line.startswith('# '):
            txt = line[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(0)
            r = p.add_run(txt)
            r.font.size = Pt(20)
            r.bold = True
            r.font.name = FONT
            r.font.color.rgb = ACCENT
            seen_h1 = True
            i += 1
            continue

        if line.startswith('## '):
            txt = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(11)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            add_inline(p, txt.upper(), size=10.5, color=ACCENT, bold_all=True)
            bottom_border(p)
            i += 1
            continue

        if line.startswith('### '):
            txt = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(9)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            if ' — ' in txt:
                head, tail = txt.split(' — ', 1)
                r = p.add_run(head)
                r.bold = True
                r.font.size = Pt(11)
                r.font.name = FONT
                r.font.color.rgb = ACCENT
                add_inline(p, '  ·  ' + tail, size=10, color=ACCENT2, bold_all=True)
            else:
                add_inline(p, txt, size=11, color=ACCENT, bold_all=True)
            i += 1
            continue

        if line.startswith('---'):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            bottom_border(p, size=6, color='DDDDDD')
            for r in p.runs:
                r.font.size = Pt(2)
            i += 1
            continue

        if re.match(r'^\s*[-*]\s+', line):
            txt = re.sub(r'^\s*[-*]\s+', '', line)
            p = doc.add_paragraph(style='List Bullet')
            add_inline(p, txt, size=BODY)
            i += 1
            continue

        if re.match(r'^\d+\.\s+', line):
            txt = re.sub(r'^\d+\.\s+', '', line)
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.left_indent = Cm(0.55)
            p.paragraph_format.first_line_indent = Cm(-0.35)
            p.paragraph_format.space_after = Pt(1.5)
            add_inline(p, txt, size=BODY)
            i += 1
            continue

        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        if line.startswith('**') and line.rstrip().endswith('**') and len(line) < 90 and seen_h1:
            add_inline(p, line, size=12, color=ACCENT2, bold_all=True)
        else:
            add_inline(p, line, size=BODY)
        i += 1

    flush_quote()

    doc.core_properties.author = 'Владимир Савин'
    doc.core_properties.title = 'Резюме — Владимир Савин'
    doc.save(docx_path)
    print('saved', docx_path)


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
