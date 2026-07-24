"""测试 RAG 链核心功能"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_chain import _truncate_text, MODULE_DESCRIPTIONS


class TestRAGChain:
    """RAG 链测试"""

    def test_truncate_text_no_truncation(self):
        """测试不需要截断的文本"""
        text = "这是一段短文本"
        result = _truncate_text(text, 100)
        assert result == text

    def test_truncate_text_exact_length(self):
        """测试刚好达到最大长度的文本"""
        text = "a" * 100
        result = _truncate_text(text, 100)
        assert result == text

    def test_truncate_text_needs_truncation(self):
        """测试需要截断的文本"""
        text = "a" * 105
        result = _truncate_text(text, 100)
        assert len(result) == 100
        assert result.endswith("...")
        assert result.startswith("a" * 97)

    def test_truncate_text_empty(self):
        """测试空文本"""
        text = ""
        result = _truncate_text(text, 100)
        assert result == ""

    def test_module_descriptions_exists(self):
        """测试模块描述映射存在"""
        assert "policy" in MODULE_DESCRIPTIONS
        assert "tech" in MODULE_DESCRIPTIONS
        assert "admin" in MODULE_DESCRIPTIONS
        assert "general" in MODULE_DESCRIPTIONS

    def test_module_descriptions_chinese(self):
        """测试模块描述为中文"""
        assert MODULE_DESCRIPTIONS["policy"] == "规章制度"
        assert MODULE_DESCRIPTIONS["tech"] == "产品技术"
        assert MODULE_DESCRIPTIONS["admin"] == "行政服务"
        assert MODULE_DESCRIPTIONS["general"] == "自由问答"