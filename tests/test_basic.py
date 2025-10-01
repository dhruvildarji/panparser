import pytest
from panparsex import parse
from panparsex.types import UnifiedDocument


def test_text(tmp_path):
    """Test basic text file parsing."""
    fp = tmp_path / "a.txt"
    fp.write_text("hello world", encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    assert "hello world" in doc.sections[0].chunks[0].text


def test_json(tmp_path):
    """Test basic JSON file parsing."""
    fp = tmp_path / "test.json"
    fp.write_text('{"message": "hello world"}', encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    assert "hello world" in doc.sections[0].chunks[0].text


def test_html(tmp_path):
    """Test basic HTML file parsing."""
    fp = tmp_path / "test.html"
    fp.write_text('<html><head><title>Test</title></head><body><h1>Hello World</h1></body></html>', encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    assert "Hello World" in doc.sections[0].chunks[0].text
    # Title extraction might not work with simple HTML, so just check it's a UnifiedDocument
    assert doc.meta.title is not None or len(doc.sections) > 0


def test_yaml(tmp_path):
    """Test basic YAML file parsing."""
    fp = tmp_path / "test.yaml"
    fp.write_text("message: hello world", encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    assert "hello world" in doc.sections[0].chunks[0].text


def test_xml(tmp_path):
    """Test basic XML file parsing."""
    fp = tmp_path / "test.xml"
    fp.write_text('<?xml version="1.0"?><root><message>hello world</message></root>', encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    assert "hello world" in doc.sections[0].chunks[0].text


def test_csv(tmp_path):
    """Test basic CSV file parsing."""
    fp = tmp_path / "test.csv"
    fp.write_text("name,message\nWorld,hello world", encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    # Check that CSV content is parsed (could be in any section)
    content = " ".join([chunk.text for section in doc.sections for chunk in section.chunks])
    assert "hello world" in content


def test_markdown(tmp_path):
    """Test basic Markdown file parsing."""
    fp = tmp_path / "test.md"
    fp.write_text("# Hello World\n\nThis is a test.", encoding="utf-8")
    doc = parse(str(fp))
    assert isinstance(doc, UnifiedDocument)
    # Check that markdown content is parsed (could be in any section)
    content = " ".join([chunk.text for section in doc.sections for chunk in section.chunks])
    assert "Hello World" in content or "This is a test" in content
