"""测试文档生成模块（Word/PDF）"""

import pytest
import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_generator import generate_word, generate_pdf, _register_file, DOCS_DIR


class TestDocumentGenerator:
    """文档生成测试"""

    def test_docs_dir_exists(self):
        """测试文档输出目录存在"""
        assert DOCS_DIR.exists()
        assert DOCS_DIR.is_dir()

    def test_generate_word_returns_file_id(self):
        """测试生成 Word 文档返回 file_id"""
        markdown = "# 测试文档\n\n这是一段测试内容。"
        file_id = generate_word(markdown, "test_document")
        assert isinstance(file_id, str)
        assert len(file_id) == 32  # UUID hex

    def test_generate_word_file_exists(self):
        """测试生成的 Word 文件存在"""
        markdown = "# 测试文档\n\n内容测试。"
        file_id = generate_word(markdown, "test_word")
        assert file_id is not None

    def test_generate_pdf_returns_file_id(self):
        """测试生成 PDF 文档返回 file_id"""
        markdown = "# PDF 测试\n\n这是 PDF 测试内容。"
        file_id = generate_pdf(markdown, "test_pdf")
        assert isinstance(file_id, str)
        assert len(file_id) == 32

    def test_generate_pdf_file_exists(self):
        """测试生成的 PDF 文件存在"""
        markdown = "# PDF 测试\n\n内容测试。"
        file_id = generate_pdf(markdown, "test_pdf_file")
        assert file_id is not None

    def test_generate_word_with_table(self):
        """测试生成带表格的 Word 文档"""
        markdown = """# 测试表格

| 姓名 | 部门 |
|------|------|
| 张三 | 技术部 |
| 李四 | 产品部 |"""
        file_id = generate_word(markdown, "test_table")
        assert file_id is not None

    def test_generate_word_with_list(self):
        """测试生成带列表的 Word 文档"""
        markdown = """# 测试列表

1. 第一项
2. 第二项
3. 第三项

- 无序列表 A
- 无序列表 B"""
        file_id = generate_word(markdown, "test_list")
        assert file_id is not None

    def test_generate_word_with_code(self):
        """测试生成带代码块的 Word 文档"""
        markdown = """# 测试代码

```python
def hello():
    print('hello')
```"""
        file_id = generate_word(markdown, "test_code")
        assert file_id is not None

    def test_generate_pdf_with_markdown_elements(self):
        """测试 PDF 生成支持多种 Markdown 元素"""
        markdown = """# 标题

## 子标题

**加粗文本**

*斜体文本*

> 引用文本

1. 有序列表
2. 第二项"""
        file_id = generate_pdf(markdown, "test_pdf_elements")
        assert file_id is not None

    def test_generate_word_empty_content(self):
        """测试生成空内容的 Word"""
        markdown = ""
        file_id = generate_word(markdown, "empty_doc")
        assert file_id is not None

    def test_generate_pdf_empty_content(self):
        """测试生成空内容的 PDF"""
        markdown = ""
        file_id = generate_pdf(markdown, "empty_pdf")
        assert file_id is not None

    def test_generate_word_special_chars(self):
        """测试生成含特殊字符的 Word"""
        markdown = "# 特殊字符测试\n\n包含中文：你好世界\n包含符号：@#$%^&*()\n包含表情：😊🎉"
        file_id = generate_word(markdown, "special_chars")
        assert file_id is not None

    def test_generate_pdf_special_chars(self):
        """测试生成含特殊字符的 PDF"""
        markdown = "# PDF 特殊字符\n\n中文测试：你好\n符号：@#$%"
        file_id = generate_pdf(markdown, "pdf_special_chars")
        assert file_id is not None