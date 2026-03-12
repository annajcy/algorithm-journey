#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
}


@dataclass
class Paragraph:
    text: str
    level: int = 0
    is_title: bool = False
    is_subtitle: bool = False


@dataclass
class TableData:
    rows: list[list[str]]


@dataclass
class ImageData:
    target_member: str
    name: str
    description: str
    extracted_path: str = ""


@dataclass
class ShapeContent:
    kind: str
    top: int
    left: int
    paragraphs: list[Paragraph] = field(default_factory=list)
    table: TableData | None = None
    image: ImageData | None = None


@dataclass
class SlideContent:
    number: int
    title: str
    contents: list[ShapeContent]
    notes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PowerPoint (.pptx/.ppt) into structured Markdown."
    )
    parser.add_argument("input", type=Path, help="Input .pptx or .ppt file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output markdown path. Defaults to <input>.md",
    )
    parser.add_argument(
        "--title-from-first-slide",
        action="store_true",
        help="Use the first slide title as the document title when available.",
    )
    parser.add_argument(
        "--include-notes",
        action="store_true",
        help="Include speaker notes if present.",
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Directory for extracted slide images. Defaults to <output>_assets.",
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def xml_root_from_zip(pptx_path: Path, member: str) -> ET.Element:
    with zipfile.ZipFile(pptx_path) as zf:
        with zf.open(member) as fp:
            return ET.fromstring(fp.read())


def target_to_member(base_member: str, target: str) -> str:
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    base_dir = Path(base_member).parent
    resolved = (base_dir / target).as_posix()
    return posixpath.normpath(resolved)


def convert_ppt_to_pptx(input_path: Path) -> Path:
    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError(
            "Legacy .ppt is not supported directly. Install LibreOffice or convert to .pptx first."
        )
    temp_dir = Path(tempfile.mkdtemp(prefix="ppt_to_md_"))
    cmd = [
        soffice,
        "--headless",
        "--convert-to",
        "pptx",
        "--outdir",
        str(temp_dir),
        str(input_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    converted = temp_dir / f"{input_path.stem}.pptx"
    if not converted.exists():
        raise RuntimeError("LibreOffice did not produce the expected .pptx output.")
    return converted


def presentation_slide_members(pptx_path: Path) -> list[str]:
    rels_root = xml_root_from_zip(pptx_path, "ppt/_rels/presentation.xml.rels")
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels_root.findall("pr:Relationship", NS)
    }
    pres_root = xml_root_from_zip(pptx_path, "ppt/presentation.xml")
    members: list[str] = []
    for slide_id in pres_root.findall("p:sldIdLst/p:sldId", NS):
        rel_id = slide_id.attrib.get(f"{{{NS['r']}}}id")
        if not rel_id or rel_id not in rel_map:
            continue
        members.append(target_to_member("ppt/presentation.xml", rel_map[rel_id]))
    return members


def core_properties_title(pptx_path: Path) -> str:
    try:
        root = xml_root_from_zip(pptx_path, "docProps/core.xml")
    except KeyError:
        return ""
    title = root.findtext("dc:title", default="", namespaces=NS)
    return normalize_text(title or "")


def shape_position(sp: ET.Element) -> tuple[int, int]:
    off = sp.find("p:spPr/a:xfrm/a:off", NS)
    if off is None:
        return (10**12, 10**12)
    x = int(off.attrib.get("x", "0"))
    y = int(off.attrib.get("y", "0"))
    return (y, x)


def placeholder_type(sp: ET.Element) -> str:
    ph = sp.find("p:nvSpPr/p:nvPr/p:ph", NS)
    if ph is None:
        return ""
    return ph.attrib.get("type", "")


def paragraph_runs_text(p: ET.Element) -> str:
    parts: list[str] = []
    for node in p:
        tag = node.tag.rsplit("}", 1)[-1]
        if tag == "r":
            text = node.findtext("a:t", default="", namespaces=NS)
            if text:
                parts.append(text)
        elif tag == "br":
            parts.append("\n")
        elif tag == "fld":
            text = node.findtext("a:t", default="", namespaces=NS)
            if text:
                parts.append(text)
    return normalize_text("".join(parts))


def shape_paragraphs(sp: ET.Element) -> list[Paragraph]:
    ph_type = placeholder_type(sp)
    is_title = ph_type in {"title", "ctrTitle"}
    is_subtitle = ph_type == "subTitle"
    paragraphs: list[Paragraph] = []
    for p in sp.findall(".//a:p", NS):
        text = paragraph_runs_text(p)
        if not text:
            continue
        p_pr = p.find("a:pPr", NS)
        level = int(p_pr.attrib.get("lvl", "0")) if p_pr is not None else 0
        paragraphs.append(
            Paragraph(
                text=text,
                level=level,
                is_title=is_title,
                is_subtitle=is_subtitle,
            )
        )
    return paragraphs


def extract_table(graphic_frame: ET.Element) -> TableData | None:
    tbl = graphic_frame.find(".//a:tbl", NS)
    if tbl is None:
        return None
    rows: list[list[str]] = []
    for tr in tbl.findall("a:tr", NS):
        row: list[str] = []
        for tc in tr.findall("a:tc", NS):
            cell_lines = [paragraph_runs_text(p) for p in tc.findall(".//a:p", NS)]
            cell_text = normalize_text("\n".join(line for line in cell_lines if line))
            row.append(cell_text)
        if any(cell.strip() for cell in row):
            rows.append(row)
    return TableData(rows=rows) if rows else None


def graphic_frame_position(frame: ET.Element) -> tuple[int, int]:
    off = frame.find("p:xfrm/a:off", NS)
    if off is None:
        return (10**12, 10**12)
    x = int(off.attrib.get("x", "0"))
    y = int(off.attrib.get("y", "0"))
    return (y, x)


def slide_notes(pptx_path: Path, slide_member: str) -> list[str]:
    rels_member = f"{Path(slide_member).parent}/_rels/{Path(slide_member).name}.rels"
    try:
        rels_root = xml_root_from_zip(pptx_path, rels_member)
    except KeyError:
        return []
    notes_member = ""
    for rel in rels_root.findall("pr:Relationship", NS):
        if rel.attrib.get("Type", "").endswith("/notesSlide"):
            notes_member = target_to_member(slide_member, rel.attrib["Target"])
            break
    if not notes_member:
        return []
    notes_root = xml_root_from_zip(pptx_path, notes_member)
    lines: list[str] = []
    for p in notes_root.findall(".//a:p", NS):
        text = paragraph_runs_text(p)
        if text:
            lines.append(text)
    return lines


def slide_relationships(pptx_path: Path, slide_member: str) -> dict[str, str]:
    rels_member = f"{Path(slide_member).parent}/_rels/{Path(slide_member).name}.rels"
    try:
        rels_root = xml_root_from_zip(pptx_path, rels_member)
    except KeyError:
        return {}
    rels: dict[str, str] = {}
    for rel in rels_root.findall("pr:Relationship", NS):
        target = rel.attrib.get("Target")
        rel_id = rel.attrib.get("Id")
        if not target or not rel_id:
            continue
        rels[rel_id] = target_to_member(slide_member, target)
    return rels


def picture_position(pic: ET.Element) -> tuple[int, int]:
    off = pic.find("p:spPr/a:xfrm/a:off", NS)
    if off is None:
        return (10**12, 10**12)
    x = int(off.attrib.get("x", "0"))
    y = int(off.attrib.get("y", "0"))
    return (y, x)


def extract_picture(pic: ET.Element, rel_map: dict[str, str]) -> ImageData | None:
    blip = pic.find(".//a:blip", NS)
    if blip is None:
        return None
    rel_id = blip.attrib.get(f"{{{NS['r']}}}embed")
    if not rel_id or rel_id not in rel_map:
        return None
    c_nv_pr = pic.find("p:nvPicPr/p:cNvPr", NS)
    name = ""
    description = ""
    if c_nv_pr is not None:
        name = normalize_text(c_nv_pr.attrib.get("name", ""))
        description = normalize_text(c_nv_pr.attrib.get("descr", ""))
    return ImageData(
        target_member=rel_map[rel_id],
        name=name,
        description=description,
    )


def parse_slide(pptx_path: Path, slide_member: str, slide_number: int) -> SlideContent:
    root = xml_root_from_zip(pptx_path, slide_member)
    contents: list[ShapeContent] = []
    title = ""
    rel_map = slide_relationships(pptx_path, slide_member)

    for sp in root.findall(".//p:sp", NS):
        paragraphs = shape_paragraphs(sp)
        if not paragraphs:
            continue
        top, left = shape_position(sp)
        if not title:
            for para in paragraphs:
                if para.is_title:
                    title = para.text
                    break
        contents.append(
            ShapeContent(
                kind="text",
                top=top,
                left=left,
                paragraphs=paragraphs,
            )
        )

    for frame in root.findall(".//p:graphicFrame", NS):
        table = extract_table(frame)
        if table is None:
            continue
        top, left = graphic_frame_position(frame)
        contents.append(
            ShapeContent(kind="table", top=top, left=left, table=table)
        )

    for pic in root.findall(".//p:pic", NS):
        image = extract_picture(pic, rel_map)
        if image is None:
            continue
        top, left = picture_position(pic)
        contents.append(
            ShapeContent(kind="image", top=top, left=left, image=image)
        )

    contents.sort(key=lambda item: (item.top, item.left))
    notes = slide_notes(pptx_path, slide_member)
    title = normalize_text(title) or f"Slide {slide_number}"
    return SlideContent(number=slide_number, title=title, contents=contents, notes=notes)


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|")


def render_table(table: TableData) -> list[str]:
    if not table.rows:
        return []
    width = max(len(row) for row in table.rows)
    rows = [row + [""] * (width - len(row)) for row in table.rows]
    header = rows[0]
    lines = [
        "| " + " | ".join(markdown_escape(cell) for cell in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(markdown_escape(cell) for cell in row) + " |")
    return lines


def render_slide(slide: SlideContent, include_notes: bool) -> str:
    lines = [f"## Slide {slide.number}: {slide.title}", ""]
    seen_title = False
    for content in slide.contents:
        if content.kind == "text":
            for para in content.paragraphs:
                if para.is_title and not seen_title and para.text == slide.title:
                    seen_title = True
                    continue
                if para.is_subtitle:
                    lines.append(f"> {para.text}")
                    continue
                indent = "  " * max(para.level, 0)
                lines.append(f"{indent}- {para.text}")
            if lines and lines[-1] != "":
                lines.append("")
        elif content.kind == "table" and content.table:
            lines.extend(render_table(content.table))
            lines.append("")
        elif content.kind == "image" and content.image and content.image.extracted_path:
            alt = content.image.description or content.image.name or f"slide-{slide.number}-image"
            lines.append(f"![{alt}]({content.image.extracted_path})")
            lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    if include_notes and slide.notes:
        lines.extend(["", "### Notes", ""])
        for note in slide.notes:
            lines.append(f"- {note}")
    return "\n".join(lines)


def derive_doc_title(
    pptx_path: Path, slides: list[SlideContent], title_from_first_slide: bool
) -> str:
    if title_from_first_slide and slides:
        return slides[0].title
    return core_properties_title(pptx_path) or (slides[0].title if slides else pptx_path.stem)


def convert_presentation(
    input_path: Path,
    output_path: Path,
    include_notes: bool,
    title_from_first_slide: bool,
    image_dir: Path | None,
) -> None:
    working_path = input_path
    temp_pptx: Path | None = None
    if input_path.suffix.lower() == ".ppt":
        temp_pptx = convert_ppt_to_pptx(input_path)
        working_path = temp_pptx
    elif input_path.suffix.lower() != ".pptx":
        raise ValueError("Only .pptx is supported directly. Use .ppt only when LibreOffice is installed.")

    slide_members = presentation_slide_members(working_path)
    slides = [
        parse_slide(working_path, slide_member, index + 1)
        for index, slide_member in enumerate(slide_members)
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image_output_dir = image_dir or output_path.parent / f"{output_path.stem}_assets"
    image_output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(working_path) as zf:
        for slide in slides:
            image_index = 1
            for content in slide.contents:
                if content.kind != "image" or not content.image:
                    continue
                target_member = content.image.target_member
                suffix = Path(target_member).suffix or ".bin"
                file_name = f"slide-{slide.number:03d}-image-{image_index:02d}{suffix}"
                image_index += 1
                destination = image_output_dir / file_name
                destination.write_bytes(zf.read(target_member))
                content.image.extracted_path = os.path.relpath(destination, output_path.parent)

    doc_title = derive_doc_title(working_path, slides, title_from_first_slide)
    parts = [f"# {doc_title}", ""]
    for slide in slides:
        parts.append(render_slide(slide, include_notes))
        parts.append("")
    markdown = "\n".join(parts).rstrip() + "\n"
    output_path.write_text(markdown, encoding="utf-8")

    if temp_pptx:
        shutil.rmtree(temp_pptx.parent, ignore_errors=True)


def main() -> int:
    args = parse_args()
    input_path = args.input.expanduser().resolve()
    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else input_path.with_suffix(".md")
    )

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        convert_presentation(
            input_path=input_path,
            output_path=output_path,
            include_notes=args.include_notes,
            title_from_first_slide=args.title_from_first_slide,
            image_dir=args.image_dir,
        )
    except Exception as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1

    print(f"Written markdown to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
