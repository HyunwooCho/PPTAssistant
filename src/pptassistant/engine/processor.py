from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .fonts import normalize_fonts
from .notes import remove_notes_parts
from .proofing import clean_pptx_xml


@dataclass(slots=True)
class ProcessingOptions:
    remove_proofing: bool = True
    language: str = "ko-KR"
    normalize_font: bool = False
    font_name: str = "Aptos"
    remove_notes: bool = False
    output_suffix: str = "_fixed"


@dataclass(slots=True)
class ProcessingResult:
    source: Path
    output: Path
    messages: list[str] = field(default_factory=list)


def process_presentation(source: Path, options: ProcessingOptions) -> ProcessingResult:
    source = source.resolve()
    if source.suffix.lower() not in {".pptx", ".potx"}:
        raise ValueError(f"Unsupported file type: {source.suffix}")
    if not source.exists():
        raise FileNotFoundError(source)

    data = source.read_bytes()
    messages: list[str] = []

    if options.remove_proofing:
        data, stats = clean_pptx_xml(data, language=options.language, disable_proofing=True)
        messages.append(
            f"Proofing: {stats.text_properties} text properties, "
            f"{stats.removed_error_attributes} error markers removed"
        )

    if options.normalize_font:
        data, count = normalize_fonts(data, options.font_name)
        messages.append(f"Fonts: {count} font references changed to {options.font_name}")

    if options.remove_notes:
        data, count = remove_notes_parts(data)
        messages.append(f"Notes: {count} note-related parts removed")

    output = source.with_name(f"{source.stem}{options.output_suffix}{source.suffix}")
    output.write_bytes(data)
    messages.append(f"Saved: {output.name}")
    return ProcessingResult(source=source, output=output, messages=messages)
