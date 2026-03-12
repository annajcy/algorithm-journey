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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_DIR = PROJECT_ROOT / "ppt"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "md"
SUPPORTED_EXTENSIONS = {".pptx", ".ppt", ".pdf"}
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
HTML_IMG_RE = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")', re.IGNORECASE)


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


@dataclass
class ConversionResult:
    input_path: Path
    output_path: Path | None
    success: bool
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PowerPoint/PDF files or directories into structured Markdown."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Input file (.pptx/.ppt/.pdf) or a directory containing those files. Defaults to ./ppt",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output markdown path for a single file, or output directory for batch mode. Defaults to ./md in no-arg mode.",
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
        help="Asset directory for a single file, or asset root directory for batch mode.",
    )
    parser.add_argument(
        "--mineru-bin",
        default="mineru",
        help="MinerU executable name or path. Falls back to magic-pdf if unavailable.",
    )
    parser.add_argument(
        "--pdf-backend",
        default="pipeline",
        help="Optional MinerU backend, for example 'pipeline' for CPU-only parsing.",
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


def resolve_mineru_executable(preferred: str) -> str:
    candidates = [preferred]
    if preferred != "mineru":
        candidates.append("mineru")
    candidates.append("magic-pdf")
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise RuntimeError(
        "MinerU executable not found. Install it with `uv pip install -U \"mineru[all]\"`, "
        "ensure 'mineru' is in PATH, or pass --mineru-bin /path/to/mineru."
    )


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


def find_mineru_markdown(output_dir: Path, source_path: Path) -> Path:
    candidates = list(output_dir.rglob("*.md"))
    if not candidates:
        raise RuntimeError("MinerU finished but no markdown file was produced.")

    def score(path: Path) -> tuple[int, int]:
        rel = path.relative_to(output_dir).as_posix()
        value = 0
        if path.stem == source_path.stem:
            value += 100
        if source_path.stem in path.stem:
            value += 40
        if source_path.stem in rel:
            value += 20
        return (value, path.stat().st_size)

    return max(candidates, key=score)


def is_local_asset_reference(target: str) -> bool:
    lower = target.lower()
    return bool(target) and not (
        lower.startswith(("http://", "https://", "data:", "mailto:", "#"))
    )


def sanitize_asset_relative_path(target: str) -> Path:
    cleaned = target.split("#", 1)[0].split("?", 1)[0].strip()
    parts = [part for part in Path(cleaned).parts if part not in ("", ".", "..")]
    if not parts:
        return Path(Path(cleaned).name or "asset.bin")
    return Path(*parts)


def rewrite_and_copy_markdown_assets(
    markdown_text: str,
    markdown_source_dir: Path,
    output_path: Path,
    asset_dir: Path,
) -> str:
    replacements: dict[str, str] = {}
    used_targets: set[Path] = set()

    def copy_target(raw_target: str) -> str:
        if raw_target in replacements:
            return replacements[raw_target]
        if not is_local_asset_reference(raw_target):
            replacements[raw_target] = raw_target
            return raw_target

        source = (markdown_source_dir / raw_target).resolve()
        if not source.exists() or not source.is_file():
            replacements[raw_target] = raw_target
            return raw_target

        relative_target = sanitize_asset_relative_path(raw_target)
        destination = asset_dir / relative_target
        stem = destination.stem
        suffix = destination.suffix
        index = 1
        while destination in used_targets or destination.exists():
            destination = destination.with_name(f"{stem}-{index}{suffix}")
            index += 1
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        used_targets.add(destination)
        rewritten = os.path.relpath(destination, output_path.parent)
        replacements[raw_target] = rewritten
        return rewritten

    def markdown_sub(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        return f"{prefix}{copy_target(target)}{suffix}"

    def html_img_sub(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        return f"{prefix}{copy_target(target)}{suffix}"

    updated = MARKDOWN_LINK_RE.sub(markdown_sub, markdown_text)
    updated = HTML_IMG_RE.sub(html_img_sub, updated)
    return updated


def convert_pdf_with_mineru(
    input_path: Path,
    output_path: Path,
    asset_dir: Path | None,
    mineru_bin: str,
    pdf_backend: str | None,
) -> None:
    mineru_executable = resolve_mineru_executable(mineru_bin)
    temp_dir = Path(tempfile.mkdtemp(prefix="mineru_to_md_"))
    try:
        cmd = [mineru_executable, "-p", str(input_path), "-o", str(temp_dir)]
        if pdf_backend:
            cmd.extend(["-b", pdf_backend])
        completed = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode != 0:
            stderr = normalize_text(completed.stderr or completed.stdout)
            raise RuntimeError(stderr or f"MinerU exited with code {completed.returncode}.")

        markdown_source = find_mineru_markdown(temp_dir, input_path)
        markdown_text = markdown_source.read_text(encoding="utf-8")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if asset_dir is not None:
            asset_dir.mkdir(parents=True, exist_ok=True)
        rewritten = rewrite_and_copy_markdown_assets(
            markdown_text=markdown_text,
            markdown_source_dir=markdown_source.parent,
            output_path=output_path,
            asset_dir=asset_dir or (output_path.parent / f"{output_path.stem}_assets"),
        )
        output_path.write_text(rewritten, encoding="utf-8")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def convert_any_file(
    input_path: Path,
    output_path: Path,
    include_notes: bool,
    title_from_first_slide: bool,
    image_dir: Path | None,
    mineru_bin: str,
    pdf_backend: str | None,
) -> None:
    suffix = input_path.suffix.lower()
    if suffix in {".pptx", ".ppt"}:
        convert_presentation(
            input_path=input_path,
            output_path=output_path,
            include_notes=include_notes,
            title_from_first_slide=title_from_first_slide,
            image_dir=image_dir,
        )
        return
    if suffix == ".pdf":
        convert_pdf_with_mineru(
            input_path=input_path,
            output_path=output_path,
            asset_dir=image_dir,
            mineru_bin=mineru_bin,
            pdf_backend=pdf_backend,
        )
        return
    raise ValueError(f"Unsupported file type: {input_path.suffix}")


def discover_inputs(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def output_path_for_single_input(input_path: Path, output_arg: Path | None) -> Path:
    if output_arg is None:
        return input_path.with_suffix(".md")
    if output_arg.suffix.lower() == ".md":
        return output_arg
    return output_arg / f"{input_path.stem}.md"


def output_root_for_directory(input_path: Path, output_arg: Path | None) -> Path:
    if output_arg is not None:
        if output_arg.suffix.lower() == ".md":
            raise ValueError("Batch mode requires an output directory, not a .md file path.")
        return output_arg
    return input_path.parent / f"{input_path.name}_markdown"


def asset_dir_for_output(
    input_root: Path | None,
    input_path: Path,
    output_path: Path,
    image_dir_arg: Path | None,
) -> Path:
    if image_dir_arg is None:
        return output_path.parent / f"{output_path.stem}_assets"
    if input_root is None:
        return image_dir_arg
    relative_parent = input_path.relative_to(input_root).parent
    return image_dir_arg / relative_parent / f"{input_path.stem}_assets"


def resolved_input_from_args(args: argparse.Namespace) -> Path:
    input_arg = args.input if args.input is not None else DEFAULT_INPUT_DIR
    return input_arg.expanduser().resolve()


def process_single_input(args: argparse.Namespace) -> ConversionResult:
    input_path = resolved_input_from_args(args)
    output_path = output_path_for_single_input(
        input_path,
        args.output.expanduser().resolve() if args.output else None,
    )
    asset_dir = asset_dir_for_output(
        input_root=None,
        input_path=input_path,
        output_path=output_path,
        image_dir_arg=args.image_dir.expanduser().resolve() if args.image_dir else None,
    )
    convert_any_file(
        input_path=input_path,
        output_path=output_path,
        include_notes=args.include_notes,
        title_from_first_slide=args.title_from_first_slide,
        image_dir=asset_dir,
        mineru_bin=args.mineru_bin,
        pdf_backend=args.pdf_backend,
    )
    return ConversionResult(
        input_path=input_path,
        output_path=output_path,
        success=True,
        message="ok",
    )


def process_directory(args: argparse.Namespace) -> list[ConversionResult]:
    input_root = resolved_input_from_args(args)
    output_root = output_root_for_directory(
        input_root,
        args.output.expanduser().resolve() if args.output else None,
    )
    image_root = args.image_dir.expanduser().resolve() if args.image_dir else None
    results: list[ConversionResult] = []
    for source in discover_inputs(input_root):
        relative = source.relative_to(input_root)
        output_path = output_root / relative.with_suffix(".md")
        asset_dir = asset_dir_for_output(
            input_root=input_root,
            input_path=source,
            output_path=output_path,
            image_dir_arg=image_root,
        )
        try:
            convert_any_file(
                input_path=source,
                output_path=output_path,
                include_notes=args.include_notes,
                title_from_first_slide=args.title_from_first_slide,
                image_dir=asset_dir,
                mineru_bin=args.mineru_bin,
                pdf_backend=args.pdf_backend,
            )
            results.append(
                ConversionResult(source, output_path, True, "ok")
            )
        except Exception as exc:
            results.append(
                ConversionResult(source, output_path, False, str(exc))
            )
    return results


def main() -> int:
    args = parse_args()
    input_path = resolved_input_from_args(args)

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        if input_path.is_dir():
            if args.output is None and args.input is None:
                args.output = DEFAULT_OUTPUT_DIR
            results = process_directory(args)
            succeeded = sum(1 for item in results if item.success)
            failed = len(results) - succeeded
            for result in results:
                status = "OK" if result.success else "FAIL"
                output_repr = str(result.output_path) if result.output_path else "-"
                print(f"[{status}] {result.input_path} -> {output_repr}")
                if not result.success:
                    print(f"       {result.message}")
            print(f"Processed {len(results)} files: {succeeded} succeeded, {failed} failed.")
            return 0 if failed == 0 else 1

        result = process_single_input(args)
    except Exception as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1

    print(f"Written markdown to {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
