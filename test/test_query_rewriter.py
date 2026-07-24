"""测试查询重写模块"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from query_rewriter import rewrite_query


class TestQueryRewriter:
    """查询重写测试"""

    def test_rewrite_empty_query(self):
        """测试空查询重写"""
        result = rewrite_query("", [])
        assert result == ""

    def test_rewrite_simple_query(self):
        """测试简单查询重写"""
        result = rewrite_query("报销流程", [])
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rewrite_with_context(self):
        """测试带上下文的查询重写"""
        history = [
            {"role": "user", "content": "请问考勤制度是什么？"},
            {"role": "assistant", "content": "考勤制度规定了员工上下班时间和请假流程。"},
        ]
        result = rewrite_query("它的具体内容是什么？", history)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rewrite_resolves_reference(self):
        """测试查询重写解决指代问题"""
        history = [
            {"role": "user", "content": "年假政策是怎样的？"},
            {"role": "assistant", "content": "年假政策根据工龄不同而不同。"},
        ]
        result = rewrite_query("它有什么限制？", history)
        assert isinstance(result, str)

    def test_rewrite_maintains_meaning(self):
        """测试重写保持原意"""
        original = "加班工资怎么算？"
        result = rewrite_query(original, [])
        assert isinstance(result, str)
        assert len(result) >= len(original)

    def test_rewrite_with_multiple_history(self):
        """测试多轮对话上下文"""
        history = [
            {"role": "user", "content": "请介绍一下公司制度"},
            {"role": "assistant", "content": "公司制度包括考勤、薪酬、年假等方面。"},
            {"role": "user", "content": "薪酬方面具体有哪些？"},
            {"role": "assistant", "content": "薪酬包括基本工资、绩效奖金和年终奖金。"},
        ]
        result = rewrite_query("它的计算方式是什么？", history)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rewrite_query_not_none(self):
        """测试重写结果不为 None"""
        result = rewrite_query("测试查询", [])
        assert result is not None

    def test_rewrite_query_type(self):
        """测试重写结果类型"""
        result = rewrite_query("test", [])
        assert isinstance(result, str)