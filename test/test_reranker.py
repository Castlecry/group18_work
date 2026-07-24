"""测试 Rerank 结果重排模块"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reranker import rerank_documents


class TestReranker:
    """结果重排测试"""

    def test_rerank_empty_documents(self):
        """测试空文档列表重排"""
        query = "测试查询"
        documents = []
        result = rerank_documents(query, documents)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_rerank_single_document(self):
        """测试单文档重排"""
        query = "考勤制度"
        documents = [
            {"text": "考勤制度规定了上下班时间", "metadata": {"source": "doc1"}}
        ]
        result = rerank_documents(query, documents)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_rerank_multiple_documents(self):
        """测试多文档重排"""
        query = "年假政策"
        documents = [
            {"text": "请假制度说明", "metadata": {"source": "doc1"}},
            {"text": "年假政策规定了员工年假天数", "metadata": {"source": "doc2"}},
            {"text": "薪酬管理制度", "metadata": {"source": "doc3"}},
        ]
        result = rerank_documents(query, documents)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_rerank_preserves_metadata(self):
        """测试重排保留元数据"""
        query = "测试"
        documents = [
            {"text": "内容1", "metadata": {"source": "doc1", "page": 1}}
        ]
        result = rerank_documents(query, documents)
        assert "metadata" in result[0]
        assert result[0]["metadata"]["source"] == "doc1"
        assert result[0]["metadata"]["page"] == 1

    def test_rerank_returns_list(self):
        """测试重排返回列表"""
        query = "测试"
        documents = [{"text": "内容"}]
        result = rerank_documents(query, documents)
        assert isinstance(result, list)

    def test_rerank_with_different_content(self):
        """测试不同内容的文档重排"""
        query = "报销流程"
        documents = [
            {"text": "考勤制度", "metadata": {"source": "doc1"}},
            {"text": "报销流程说明：填写报销单并提交审批", "metadata": {"source": "doc2"}},
            {"text": "年假政策", "metadata": {"source": "doc3"}},
            {"text": "报销流程的具体步骤和注意事项", "metadata": {"source": "doc4"}},
        ]
        result = rerank_documents(query, documents)
        assert isinstance(result, list)
        assert len(result) == 4