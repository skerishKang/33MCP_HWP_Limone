"""Conservative HWP/PDF -> native-text HTML conversion.

Inspired by local 35's two pipeline split; code is newly implemented with no
hardcoded evaluation results, optional PyMuPDF, and clear non-OCR limitations.
"""
from html import escape
import os
from pathlib import Path
import tempfile
from typing import Literal

from .workflow import isolated_hwp_session


class ConversionError(RuntimeError):
    """A conversion could not produce a verified output."""


def _paths(source: str, output_dir: str, suffix: str):
    src = Path(source).expanduser().resolve(strict=True)
    dest = Path(output_dir).expanduser().resolve()
    if not src.is_file() or src.suffix.lower() != suffix:
        raise ConversionError("Source must be an existing " + suffix + " file")
    if not dest.is_dir():
        raise ConversionError("Output directory does not exist")
    return src, dest


def _native_pages(pdf: Path):
    try:
        import fitz  # PyMuPDF optional extra; never imported at MCP startup
    except ImportError as exc:
        raise ConversionError("PyMuPDF is required: pip install PyMuPDF") from exc

    pages = []
    with fitz.open(str(pdf)) as document:
        for page in document:
            rect = page.rect
            blocks = []
            for item in page.get_text("dict").get("blocks", []):
                if item.get("type") != 0:
                    continue
                lines = []
                for line in item.get("lines", []):
                    lines.append("".join(span.get("text", "") for span in line.get("spans", [])))
                content = "\n".join(lines).strip()
                if content:
                    x0, y0, x1, y1 = item["bbox"]
                    blocks.append((content, (x0, y0, x1, y1)))
            pages.append((max(1.0, float(rect.width)), max(1.0, float(rect.height)), blocks))
    if not pages:
        raise ConversionError("PDF contains no pages")
    if not any(blocks for _, _, blocks in pages):
        raise ConversionError("No native PDF text detected; scanned-PDF OCR is not implemented")
    return pages


def _html(pages, mode: Literal["editable", "faithful"]):
    css = """body{font:16px/1.55 system-ui,sans-serif;background:#f5f5f5;color:#222}
    .page{background:white;margin:18px auto;padding:20px;max-width:1000px;box-shadow:0 1px 5px #bbb}
    .block{white-space:pre-wrap;overflow-wrap:anywhere}
    .faithful{position:relative;padding:0;overflow:hidden}
    .faithful .block{position:absolute;line-height:1.2;font-size:11px}"""
    parts = ['<!doctype html><html lang="ko"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Converted PDF text</title><style>', css, '</style></head><body>',
             '<p>Text-only conversion. Images, tables, precise fonts and OCR are not preserved.</p>']
    for width, height, blocks in pages:
        if mode == "faithful":
            parts.append(f'<section class="page faithful" style="width:{width:.2f}px;height:{height:.2f}px">')
        else:
            parts.append('<section class="page editable">')
        for content, (x0, y0, _x1, _y1) in blocks:
            safe = escape(content)
            if mode == "faithful":
                parts.append(f'<div class="block" style="left:{x0:.2f}px;top:{y0:.2f}px">{safe}</div>')
            else:
                parts.append(f'<p class="block">{safe}</p>')
        parts.append('</section>')
    parts.append('</body></html>')
    return "\n".join(parts)


def pdf_to_html(source: str, output_dir: str, mode: str = "editable") -> str:
    """Extract native text from PDF, escaping content, never overwriting HTML."""
    if mode not in ("editable", "faithful"):
        raise ConversionError("mode must be editable or faithful")
    src, dest = _paths(source, output_dir, ".pdf")
    output = dest / f"{src.stem}.{mode}.html"
    if output.exists():
        raise ConversionError("HTML output already exists; no overwrite")
    html = _html(_native_pages(src), mode)
    # x = exclusive create: a competing request cannot silently replace output.
    with output.open("x", encoding="utf-8") as target:
        target.write(html)
    if output.stat().st_size == 0:
        output.unlink(missing_ok=True)
        raise ConversionError("Empty HTML output")
    return str(output)


def hwp_to_html(source: str, output_dir: str, mode: str = "editable") -> str:
    """Use a job-owned Hangul COM session to export PDF, then native text HTML."""
    src, dest = _paths(source, output_dir, ".hwp")
    # Check output before expensive HWP COM initialization.
    if mode not in ("editable", "faithful"):
        raise ConversionError("mode must be editable or faithful")
    if (dest / f"{src.stem}.{mode}.html").exists():
        raise ConversionError("HTML output already exists; no overwrite")
    fd, tmp = tempfile.mkstemp(prefix="hwp_convert_", suffix=".pdf", dir=str(dest))
    os.close(fd)
    os.unlink(tmp)
    try:
        with isolated_hwp_session() as hwp:
            if not hwp.Open(str(src), "HWP", ""):
                raise ConversionError("Hangul could not open HWP source")
            if not hwp.SaveAs(tmp, "PDF", ""):
                raise ConversionError("Hangul PDF export failed")
        if not os.path.isfile(tmp) or os.path.getsize(tmp) < 4:
            raise ConversionError("No PDF was exported by Hangul")
        with open(tmp, "rb") as f:
            if f.read(4) != b"%PDF":
                raise ConversionError("Hangul output was not a PDF")
        # Output HTML keeps source HWP basename, not intermediate temp name.
        intermediate = Path(tmp)
        target = dest / f"{src.stem}.{mode}.html"
        with target.open("x", encoding="utf-8") as out:
            out.write(_html(_native_pages(intermediate), mode))
        return str(target)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
