"""测试配置模块"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfig:
    """配置模块测试"""

    def test_config_exists(self):
        """测试配置文件存在"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "config.py")
        assert os.path.exists(config_path)

    def test_config_importable(self):
        """测试配置模块可导入"""
        from config import (
            DEEPSEEK_API_KEY,
            DEEPSEEK_BASE_URL,
            LLM_MODEL,
            TOP_K,
            CHUNK_SIZE,
            CHUNK_OVERLAP,
        )
        assert True

    def test_top_k_is_positive(self):
        """测试 TOP_K 为正数"""
        from config import TOP_K
        assert TOP_K > 0

    def test_chunk_size_is_positive(self):
        """测试 CHUNK_SIZE 为正数"""
        from config import CHUNK_SIZE
        assert CHUNK_SIZE > 0

    def test_chunk_overlap_non_negative(self):
        """测试 CHUNK_OVERLAP 非负"""
        from config import CHUNK_OVERLAP
        assert CHUNK_OVERLAP >= 0

    def test_chunk_overlap_less_than_chunk_size(self):
        """测试 CHUNK_OVERLAP 小于 CHUNK_SIZE"""
        from config import CHUNK_SIZE, CHUNK_OVERLAP
        assert CHUNK_OVERLAP < CHUNK_SIZE

    def test_base_url_exists(self):
        """测试 BASE_URL 非空"""
        from config import DEEPSEEK_BASE_URL
        assert DEEPSEEK_BASE_URL is not None
        assert len(str(DEEPSEEK_BASE_URL)) > 0

    def test_model_exists(self):
        """测试 LLM_MODEL 非空"""
        from config import LLM_MODEL
        assert LLM_MODEL is not None
        assert len(str(LLM_MODEL)) > 0