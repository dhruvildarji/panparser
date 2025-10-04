"""
Tests for image extraction functionality in panparsex.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from panparsex.types import ImageMetadata, UnifiedDocument, Metadata, Section, Chunk
from panparsex.image_extractor import ImageExtractor, extract_images_from_pdf
from panparsex.parsers.pdf import PDFParser


class TestImageMetadata:
    """Test ImageMetadata class."""
    
    def test_image_metadata_creation(self):
        """Test creating ImageMetadata instance."""
        img = ImageMetadata(
            image_id="test_img_1",
            page_number=1,
            position={"x": 100, "y": 200, "width": 300, "height": 400},
            file_path="/path/to/image.png",
            dimensions={"width": 300, "height": 400},
            format="PNG",
            associated_text="This is a test image"
        )
        
        assert img.image_id == "test_img_1"
        assert img.page_number == 1
        assert img.position["x"] == 100
        assert img.dimensions["width"] == 300
        assert img.format == "PNG"
        assert img.associated_text == "This is a test image"


class TestImageExtractor:
    """Test ImageExtractor class."""
    
    def test_image_extractor_initialization(self):
        """Test ImageExtractor initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            extractor = ImageExtractor(output_dir=temp_dir, min_image_size=(50, 50))
            assert extractor.output_dir == Path(temp_dir)
            assert extractor.min_image_size == (50, 50)
    
    def test_image_extractor_default_initialization(self):
        """Test ImageExtractor with default parameters."""
        extractor = ImageExtractor()
        assert extractor.output_dir.name == "extracted_images"
        assert extractor.min_image_size == (50, 50)
    
    @patch('panparsex.image_extractor.fitz')
    def test_extract_with_pymupdf_success(self, mock_fitz):
        """Test successful image extraction with PyMuPDF."""
        # Mock PyMuPDF objects
        mock_doc = Mock()
        mock_page = Mock()
        mock_pix = Mock()
        
        mock_fitz.open.return_value = mock_doc
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_page.get_images.return_value = [(0, "test_image")]
        mock_doc.__getitem__.return_value = mock_page
        
        # Mock pixmap
        mock_pix.width = 100
        mock_pix.height = 100
        mock_pix.n = 3  # RGB
        mock_pix.alpha = 0
        mock_pix.colorspace.name = "RGB"
        mock_pix.tobytes.return_value = b"fake_image_data"
        
        mock_fitz.Pixmap.return_value = mock_pix
        mock_fitz.Rect.return_value = Mock(x0=0, y0=0, width=100, height=100)
        
        # Mock page text extraction
        mock_page.get_text.return_value = {"blocks": []}
        mock_page.get_image_rects.return_value = [Mock(x0=0, y0=0, x1=100, y1=100)]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            extractor = ImageExtractor(output_dir=temp_dir)
            
            # Create a dummy PDF file
            pdf_path = os.path.join(temp_dir, "test.pdf")
            with open(pdf_path, "wb") as f:
                f.write(b"dummy pdf content")
            
            images = extractor.extract_images_from_pdf(pdf_path, extract_images=True)
            
            assert len(images) == 1
            assert images[0].page_number == 1
            assert images[0].dimensions["width"] == 100
            assert images[0].dimensions["height"] == 100
        
        mock_doc.close.assert_called_once()
    
    @patch('panparsex.image_extractor.fitz')
    def test_extract_with_pymupdf_no_images(self, mock_fitz):
        """Test image extraction when no images are found."""
        mock_doc = Mock()
        mock_page = Mock()
        
        mock_fitz.open.return_value = mock_doc
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_page.get_images.return_value = []  # No images
        
        with tempfile.TemporaryDirectory() as temp_dir:
            extractor = ImageExtractor(output_dir=temp_dir)
            
            pdf_path = os.path.join(temp_dir, "test.pdf")
            with open(pdf_path, "wb") as f:
                f.write(b"dummy pdf content")
            
            images = extractor.extract_images_from_pdf(pdf_path, extract_images=True)
            
            assert len(images) == 0
        
        mock_doc.close.assert_called_once()
    
    @patch('panparsex.image_extractor.pypdf')
    def test_extract_with_pypdf_fallback(self, mock_pypdf):
        """Test image extraction fallback to pypdf."""
        # Mock pypdf objects
        mock_reader = Mock()
        mock_page = Mock()
        mock_image = Mock()
        
        mock_pypdf.PdfReader.return_value = mock_reader
        mock_reader.pages = [mock_page]
        mock_page.images = [mock_image]
        mock_image.data = b"fake_image_data"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            extractor = ImageExtractor(output_dir=temp_dir)
            
            pdf_path = os.path.join(temp_dir, "test.pdf")
            with open(pdf_path, "wb") as f:
                f.write(b"dummy pdf content")
            
            # Mock PIL Image for dimension detection
            with patch('panparsex.image_extractor.Image') as mock_pil:
                mock_img = Mock()
                mock_img.size = (100, 100)
                mock_pil.open.return_value = mock_img
                
                images = extractor.extract_images_from_pdf(pdf_path, extract_images=True)
                
                assert len(images) == 1
                assert images[0].page_number == 1


class TestPDFParserWithImages:
    """Test PDF parser with image extraction."""
    
    def test_pdf_parser_with_image_extraction(self):
        """Test PDF parser with image extraction enabled."""
        parser = PDFParser()
        
        # Create mock metadata
        meta = Metadata(source="test.pdf", content_type="application/pdf")
        
        # Mock the image extractor
        with patch('panparsex.parsers.pdf.ImageExtractor') as mock_extractor_class:
            mock_extractor = Mock()
            mock_extractor_class.return_value = mock_extractor
            
            # Mock extracted images
            mock_image = ImageMetadata(
                image_id="test_img_1",
                page_number=1,
                dimensions={"width": 100, "height": 100},
                format="PNG"
            )
            mock_extractor.extract_images_from_pdf.return_value = [mock_image]
            
            # Mock pypdf
            with patch('panparsex.parsers.pdf.pypdf') as mock_pypdf:
                mock_reader = Mock()
                mock_page = Mock()
                mock_pypdf.PdfReader.return_value = mock_reader
                mock_reader.pages = [mock_page]
                mock_page.extract_text.return_value = "Sample text content"
                
                # Create a temporary file
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                    temp_file.write(b"dummy pdf content")
                    temp_path = temp_file.name
                
                try:
                    doc = parser.parse(
                        temp_path, 
                        meta, 
                        extract_images=True,
                        image_output_dir="/tmp/test_images"
                    )
                    
                    assert len(doc.images) == 1
                    assert doc.images[0].image_id == "test_img_1"
                    assert len(doc.sections) == 1
                    assert len(doc.sections[0].images) == 1
                    
                finally:
                    os.unlink(temp_path)
    
    def test_pdf_parser_without_image_extraction(self):
        """Test PDF parser with image extraction disabled."""
        parser = PDFParser()
        meta = Metadata(source="test.pdf", content_type="application/pdf")
        
        with patch('panparsex.parsers.pdf.pypdf') as mock_pypdf:
            mock_reader = Mock()
            mock_page = Mock()
            mock_pypdf.PdfReader.return_value = mock_reader
            mock_reader.pages = [mock_page]
            mock_page.extract_text.return_value = "Sample text content"
            
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(b"dummy pdf content")
                temp_path = temp_file.name
            
            try:
                doc = parser.parse(temp_path, meta, extract_images=False)
                
                assert len(doc.images) == 0
                assert len(doc.sections) == 1
                assert len(doc.sections[0].images) == 0
                
            finally:
                os.unlink(temp_path)


class TestUnifiedDocumentWithImages:
    """Test UnifiedDocument with image functionality."""
    
    def test_add_image(self):
        """Test adding images to UnifiedDocument."""
        meta = Metadata(source="test.pdf", content_type="application/pdf")
        doc = UnifiedDocument(meta=meta)
        
        img = ImageMetadata(
            image_id="test_img_1",
            page_number=1,
            dimensions={"width": 100, "height": 100}
        )
        
        # Add image to document
        doc.add_image(img)
        
        assert len(doc.images) == 1
        assert doc.images[0].image_id == "test_img_1"
    
    def test_add_image_to_section(self):
        """Test adding images to specific sections."""
        meta = Metadata(source="test.pdf", content_type="application/pdf")
        doc = UnifiedDocument(meta=meta)
        
        # Add a section first
        doc.add_text("Sample text", "Test Section")
        
        img = ImageMetadata(
            image_id="test_img_1",
            page_number=1,
            dimensions={"width": 100, "height": 100}
        )
        
        # Add image to the first section
        doc.add_image(img, section_index=0)
        
        assert len(doc.images) == 1
        assert len(doc.sections[0].images) == 1
        assert doc.sections[0].images[0].image_id == "test_img_1"
    
    def test_get_images_by_page(self):
        """Test getting images by page number."""
        meta = Metadata(source="test.pdf", content_type="application/pdf")
        doc = UnifiedDocument(meta=meta)
        
        # Add images from different pages
        img1 = ImageMetadata(image_id="img1", page_number=1)
        img2 = ImageMetadata(image_id="img2", page_number=2)
        img3 = ImageMetadata(image_id="img3", page_number=1)
        
        doc.add_image(img1)
        doc.add_image(img2)
        doc.add_image(img3)
        
        page1_images = doc.get_images_by_page(1)
        page2_images = doc.get_images_by_page(2)
        
        assert len(page1_images) == 2
        assert len(page2_images) == 1
        assert page1_images[0].image_id == "img1"
        assert page1_images[1].image_id == "img3"
        assert page2_images[0].image_id == "img2"
    
    def test_get_images_by_section(self):
        """Test getting images by section index."""
        meta = Metadata(source="test.pdf", content_type="application/pdf")
        doc = UnifiedDocument(meta=meta)
        
        # Add sections
        doc.add_text("Text 1", "Section 1")
        doc.add_text("Text 2", "Section 2")
        
        # Add images to sections
        img1 = ImageMetadata(image_id="img1", page_number=1)
        img2 = ImageMetadata(image_id="img2", page_number=2)
        
        doc.add_image(img1, section_index=0)
        doc.add_image(img2, section_index=1)
        
        section0_images = doc.get_images_by_section(0)
        section1_images = doc.get_images_by_section(1)
        
        assert len(section0_images) == 1
        assert len(section1_images) == 1
        assert section0_images[0].image_id == "img1"
        assert section1_images[0].image_id == "img2"


def test_extract_images_from_pdf_convenience_function():
    """Test the convenience function for image extraction."""
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "test.pdf")
        with open(pdf_path, "wb") as f:
            f.write(b"dummy pdf content")
        
        with patch('panparsex.image_extractor.ImageExtractor') as mock_extractor_class:
            mock_extractor = Mock()
            mock_extractor_class.return_value = mock_extractor
            
            mock_image = ImageMetadata(
                image_id="test_img_1",
                page_number=1,
                dimensions={"width": 100, "height": 100}
            )
            mock_extractor.extract_images_from_pdf.return_value = [mock_image]
            
            images = extract_images_from_pdf(
                pdf_path,
                output_dir=temp_dir,
                extract_images=True,
                min_image_size=(50, 50)
            )
            
            assert len(images) == 1
            assert images[0].image_id == "test_img_1"
            mock_extractor_class.assert_called_once_with(
                output_dir=temp_dir,
                min_image_size=(50, 50)
            )


if __name__ == "__main__":
    pytest.main([__file__])
