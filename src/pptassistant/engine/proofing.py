from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from lxml import etree

DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"


@dataclass(slots=True)
class ProofingStats:
    xml_parts: int = 0
    text_properties: int = 0
    removed_error_attributes: int = 0


def _is_presentation_xml(name: str) -> bool:
    return name.startswith("ppt/") and name.endswith(".xml")


def clean_pptx_xml(
    source: bytes,
    *,
    language: str = "ko-KR",
    disable_proofing: bool = True,
) -> tuple[bytes, ProofingStats]:
    stats = ProofingStats()
    source_buffer = BytesIO(source)
    output_buffer = BytesIO()

    with ZipFile(source_buffer, "r") as zin, ZipFile(output_buffer, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if _is_presentation_xml(item.filename):
                try:
                    root = etree.fromstring(data)
                except etree.XMLSyntaxError:
                    root = None

                if root is not None:
                    changed = False
                    for element in root.iter():
                        local_name = etree.QName(element).localname
                        if local_name in {"rPr", "defRPr", "endParaRPr"}:
                            element.set("lang", language)
                            element.set(f"{{{XML_NS}}}lang", language)
                            if disable_proofing:
                                element.set("noProof", "1")
                            if "err" in element.attrib:
                                del element.attrib["err"]
                                stats.removed_error_attributes += 1
                            stats.text_properties += 1
                            changed = True
                    if changed:
                        data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
                        stats.xml_parts += 1

            info = ZipInfo(item.filename, date_time=item.date_time)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = item.external_attr
            info.comment = item.comment
            info.create_system = item.create_system
            zout.writestr(info, data)

    return output_buffer.getvalue(), stats
