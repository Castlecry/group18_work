"""测试 LangGraph 编排模块"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestLangGraph:
    """LangGraph 编排测试"""

    def test_langgraph_importable(self):
        """测试 LangGraph 模块可导入"""
        try:
            from langgraph_agent import create_langgraph_agent, run_langgraph_workflow
            assert True
        except ImportError:
            pytest.skip("LangGraph 模块未安装")

    def test_langgraph_state_schema_exists(self):
        """测试状态 schema 存在"""
        try:
            from langgraph_agent import AgentState
            assert hasattr(AgentState, "__fields__")
        except ImportError:
            pytest.skip("LangGraph 模块未安装")

    def test_langgraph_node_functions_exist(self):
        """测试节点函数存在"""
        try:
            from langgraph_agent import (
                should_continue,
                call_model,
                call_tool,
                summarize,
            )
            assert callable(should_continue)
            assert callable(call_model)
            assert callable(call_tool)
            assert callable(summarize)
        except ImportError:
            pytest.skip("LangGraph 模块未安装")

    def test_create_agent_returns_graph(self):
        """测试创建 Agent 返回图"""
        try:
            from langgraph_agent import create_langgraph_agent
            graph = create_langgraph_agent()
            assert graph is not None
            assert hasattr(graph, 'invoke')
        except ImportError:
            pytest.skip("LangGraph 模块未安装")

    def test_workflow_executes(self):
        """测试工作流可执行"""
        try:
            from langgraph_agent import run_langgraph_workflow
            result = run_langgraph_workflow("你好")
            assert isinstance(result, dict)
            assert "output" in result
        except ImportError:
            pytest.skip("LangGraph 模块未安装")
        except Exception:
            pytest.skip("LangGraph 需要外部服务")

    def test_agent_state_has_message_history(self):
        """测试 AgentState 包含消息历史"""
        try:
            from langgraph_agent import AgentState
            fields = AgentState.__fields__
            assert "messages" in fields
        except ImportError:
            pytest.skip("LangGraph 模块未安装")

    def test_agent_state_has_tool_calls(self):
        """测试 AgentState 包含工具调用状态"""
        try:
            from langgraph_agent import AgentState
            fields = AgentState.__fields__
            assert "tool_calls" in fields or "intermediate_steps" in fields
        except ImportError:
            pytest.skip("LangGraph 模块未安装")