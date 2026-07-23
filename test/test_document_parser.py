"""测试文档解析模块"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_parser import IMAGE_EXTENSIONS, MIME_MAP


class TestDocumentParser:
    """文档解析测试"""

    def test_image_extensions_set(self):
        """测试图片扩展名集合"""
        assert ".png" in IMAGE_EXTENSIONS
        assert ".jpg" in IMAGE_EXTENSIONS
        assert ".jpeg" in IMAGE_EXTENSIONS
        assert ".bmp" in IMAGE_EXTENSIONS
        assert ".tiff" in IMAGE_EXTENSIONS
        assert ".tif" in IMAGE_EXTENSIONS

    def test_mime_map_pdf(self):
        """测试 PDF MIME 类型"""
        assert MIME_MAP[".pdf"] == "application/pdf"

    def test_mime_map_docx(self):
        """测试 DOCX MIME 类型"""
        assert MIME_MAP[".docx"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    def test_mime_map_xlsx(self):
        """测试 XLSX MIME 类型"""
        assert MIME_MAP[".xlsx"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def test_mime_map_markdown(self):
        """测试 Markdown MIME 类型"""
        assert MIME_MAP[".md"] == "text/markdown"

    def test_mime_map_text(self):
        """测试纯文本 MIME 类型"""
        assert MIME_MAP[".txt"] == "text/plain"

    def test_mime_map_html(self):
        """测试 HTML MIME 类型"""
        assert MIME_MAP[".html"] == "text/html"
        assert MIME_MAP[".htm"] == "text/html"

    def test_mime_map_image(self):
        """测试图片 MIME 类型"""
        assert MIME_MAP[".png"] == "image/png"
        assert MIME_MAP[".jpg"] == "image/jpeg"
        assert MIME_MAP[".jpeg"] == "image/jpeg"

    def test_mime_map_epub(self):
        """测试 EPUB MIME 类型"""
        assert MIME_MAP[".epub"] == "application/epub+zip"

    def test_mime_map_mobi(self):
        """测试 MOBI MIME 类型"""
        assert MIME_MAP[".mobi"] == "application/x-mobipocket-ebook"

    def test_mime_map_ppt(self):
        """测试 PPT MIME 类型"""
        assert MIME_MAP[".ppt"] == "application/vnd.ms-powerpoint"
        assert MIME_MAP[".pptx"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"

    def test_mime_map_xls(self):
        """测试 XLS MIME 类型"""
        assert MIME_MAP[".xls"] == "application/vnd.ms-excel"

    def test_mime_map_doc(self):
        """测试 DOC MIME 类型"""
        assert MIME_MAP[".doc"] == "application/msword"

    def test_mime_map_tiff(self):
        """测试 TIFF MIME 类型"""
        assert MIME_MAP[".tiff"] == "image/tiff"
        assert MIME_MAP[".tif"] == "image/tiff"

    def test_mime_map_bmp(self):
        """测试 BMP MIME 类型"""
        assert MIME_MAP[".bmp"] == "image/bmp"

    def test_mime_map_size(self):
        """测试 MIME 映射表大小"""
        assert len(MIME_MAP) >= 20

    def test_image_extensions_size(self):
        """测试图片扩展名集合大小"""
        assert len(IMAGE_EXTENSIONS) == 6