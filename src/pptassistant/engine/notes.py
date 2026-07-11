from __future__ import annotations

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def remove_notes_parts(source: bytes) -> tuple[bytes, int]:
    output = BytesIO()
    removed = 0
    with ZipFile(BytesIO(source), "r") as zin, ZipFile(output, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            name = item.filename
            if name.startswith("ppt/notesSlides/") or name.startswith("ppt/notesMasters/"):
                removed += 1
                continue
            data = zin.read(name)
            info = ZipInfo(name, date_time=item.date_time)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = item.external_attr
            info.comment = item.comment
            info.create_system = item.create_system
            zout.writestr(info, data)
    return output.getvalue(), removed
