"""测试 DSML 工具调用解析"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_tools import _parse_dsml_tool_calls


class TestDSMLParsing:
    """DSML 格式解析测试"""

    def test_parse_dsml_fullwidth_bars(self):
        """测试全角竖线 DSML 格式解析"""
        content = """找到文档了，开始搜索。
<｜｜DSML｜｜invoke name="search_knowledge_base">
<｜｜DSML｜｜parameter name="query" string="true">员工手册 考勤制度</｜｜DSML｜｜parameter>
</｜｜DSML｜｜invoke>
<｜｜DSML｜｜invoke name="web_search">
<｜｜DSML｜｜parameter name="query" string="true">2026年企业考勤制度对比</｜｜DSML｜｜parameter>
</｜｜DSML｜｜invoke>"""
        
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 2
        assert tools[0]["function"]["name"] == "search_knowledge_base"
        assert "员工手册 考勤制度" in tools[0]["function"]["arguments"]
        assert tools[1]["function"]["name"] == "web_search"
        assert "2026年企业考勤制度对比" in tools[1]["function"]["arguments"]

    def test_parse_dsml_halfwidth_bars(self):
        """测试半角竖线 DSML 格式解析"""
        content = """<||DSML||invoke name="search_knowledge_base">
<||DSML||parameter name="query" string="true">薪酬制度</||DSML||parameter>
</||DSML||invoke>"""
        
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 1
        assert tools[0]["function"]["name"] == "search_knowledge_base"
        assert "薪酬制度" in tools[0]["function"]["arguments"]

    def test_parse_dsml_with_extra_spaces(self):
        """测试带多余空格的 DSML 格式"""
        content = """<｜ ｜DSML ｜ ｜invoke  name="search_document_by_title"  >
<｜ ｜DSML ｜ ｜parameter  name="title"  string="true"> 员工手册  </｜ ｜DSML ｜ ｜parameter>
</｜ ｜DSML ｜ ｜invoke  >"""
        
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 1
        assert tools[0]["function"]["name"] == "search_document_by_title"
        assert "员工手册" in tools[0]["function"]["arguments"]

    def test_parse_dsml_multiple_parameters(self):
        """测试多参数的 DSML 格式"""
        content = """<｜｜DSML｜｜invoke name="search_knowledge_base">
<｜｜DSML｜｜parameter name="query" string="true">年假政策</｜｜DSML｜｜parameter>
<｜｜DSML｜｜parameter name="top_k" string="false">10</｜｜DSML｜｜parameter>
</｜｜DSML｜｜invoke>"""
        
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 1
        assert tools[0]["function"]["name"] == "search_knowledge_base"
        assert "年假政策" in tools[0]["function"]["arguments"]
        assert '"top_k": 10' in tools[0]["function"]["arguments"]

    def test_parse_dsml_empty_content(self):
        """测试空内容解析"""
        content = ""
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 0

    def test_parse_dsml_no_tool_calls(self):
        """测试无工具调用的内容"""
        content = "这是一段普通文本，没有任何工具调用。"
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 0

    def test_parse_dsml_single_tool(self):
        """测试单个工具调用"""
        content = '<｜｜DSML｜｜invoke name="get_current_date"></｜｜DSML｜｜invoke>'
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 1
        assert tools[0]["function"]["name"] == "get_current_date"

    def test_parse_dsml_no_parameters(self):
        """测试无参数的工具调用"""
        content = '<｜｜DSML｜｜invoke name="get_system_info"></｜｜DSML｜｜invoke>'
        tools = _parse_dsml_tool_calls(content)
        assert len(tools) == 1
        assert tools[0]["function"]["arguments"] == "{}"

    def test_tool_call_has_id(self):
        """测试工具调用包含 UUID"""
        content = '<｜｜DSML｜｜invoke name="get_current_date"></｜｜DSML｜｜invoke>'
        tools = _parse_dsml_tool_calls(content)
        assert "id" in tools[0]
        assert len(tools[0]["id"]) > 0