from io import BytesIO
from zipfile import ZipFile

from pptassistant.engine.proofing import clean_pptx_xml


def make_test_pptx() -> bytes:
    slide_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
           xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:r><a:rPr lang="en-US" err="1"/><a:t>Hello</a:t></a:r>
    </p:sld>'''
    output = BytesIO()
    with ZipFile(output, "w") as zf:
        zf.writestr("ppt/slides/slide1.xml", slide_xml)
    return output.getvalue()


def test_clean_pptx_xml_sets_korean_and_noproof() -> None:
    cleaned, stats = clean_pptx_xml(make_test_pptx())
    with ZipFile(BytesIO(cleaned), "r") as zf:
        xml = zf.read("ppt/slides/slide1.xml").decode("utf-8")
    assert 'lang="ko-KR"' in xml
    assert 'noProof="1"' in xml
    assert 'err="1"' not in xml
    assert stats.text_properties == 1
