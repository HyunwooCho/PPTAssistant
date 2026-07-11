from __future__ import annotations

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from lxml import etree


def normalize_fonts(source: bytes, font_name: str) -> tuple[bytes, int]:
    output = BytesIO()
    modified = 0
    with ZipFile(BytesIO(source), "r") as zin, ZipFile(output, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("ppt/") and item.filename.endswith(".xml"):
                try:
                    root = etree.fromstring(data)
                except etree.XMLSyntaxError:
                    root = None
                if root is not None:
                    changed = False
                    for element in root.iter():
                        if etree.QName(element).localname in {"latin", "ea", "cs"}:
                            if element.get("typeface") != font_name:
                                element.set("typeface", font_name)
                                modified += 1
                                changed = True
                    if changed:
                        data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            info = ZipInfo(item.filename, date_time=item.date_time)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = item.external_attr
            info.comment = item.comment
            info.create_system = item.create_system
            zout.writestr(info, data)
    return output.getvalue(), modified
