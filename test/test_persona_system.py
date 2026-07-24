"""测试 Persona 人设系统"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona_system import (
    ENTERPRISE_GLOSSARY,
    MODULE_PERSONAS,
    OUTPUT_FORMAT_RULES,
    SAMPLE_RESPONSES,
    build_persona_prompt,
)


class TestPersonaSystem:
    """人设系统测试"""

    def test_enterprise_glossary_not_empty(self):
        """测试企业术语词典不为空"""
        assert len(ENTERPRISE_GLOSSARY) > 0

    def test_glossary_contains_common_terms(self):
        """测试术语词典包含常见企业术语"""
        common_terms = ["OA", "HRBP", "OKR", "KPI", "JD", "API", "SDK", "CI/CD"]
        for term in common_terms:
            assert term in ENTERPRISE_GLOSSARY

    def test_glossary_values_are_descriptions(self):
        """测试术语值为描述性文本"""
        for term, desc in ENTERPRISE_GLOSSARY.items():
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_module_personas_exists(self):
        """测试模块人设映射存在"""
        assert "policy" in MODULE_PERSONAS
        assert "tech" in MODULE_PERSONAS
        assert "admin" in MODULE_PERSONAS
        assert "general" in MODULE_PERSONAS

    def test_module_persona_has_fields(self):
        """测试模块人设结构完整"""
        for module, persona in MODULE_PERSONAS.items():
            assert "role" in persona
            assert "tone" in persona
            assert "scope" in persona
            assert "forbidden" in persona

    def test_policy_persona_role(self):
        """测试规章制度模块人设角色"""
        persona = MODULE_PERSONAS["policy"]
        assert "规章制度" in persona["role"] or "HR" in persona["role"]

    def test_tech_persona_role(self):
        """测试产品技术模块人设角色"""
        persona = MODULE_PERSONAS["tech"]
        assert "技术" in persona["role"] or "工程师" in persona["role"]

    def test_output_format_rules_not_empty(self):
        """测试输出格式规范不为空"""
        assert len(OUTPUT_FORMAT_RULES) > 0

    def test_sample_responses_exists(self):
        """测试少样本示例存在"""
        assert len(SAMPLE_RESPONSES) > 0

    def test_build_persona_prompt_returns_string(self):
        """测试构建人设提示词返回字符串"""
        prompt = build_persona_prompt("policy")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_build_persona_prompt_contains_role(self):
        """测试提示词包含角色定义"""
        prompt = build_persona_prompt("policy")
        assert "角色" in prompt or "role" in prompt.lower()

    def test_build_persona_prompt_contains_rules(self):
        """测试提示词包含格式规范"""
        prompt = build_persona_prompt("policy")
        assert "格式" in prompt or "format" in prompt.lower()

    def test_build_persona_prompt_module_specific(self):
        """测试不同模块生成不同提示词"""
        policy_prompt = build_persona_prompt("policy")
        tech_prompt = build_persona_prompt("tech")
        assert policy_prompt != tech_prompt

    def test_build_persona_prompt_all_modules(self):
        """测试所有模块都能生成提示词"""
        modules = ["policy", "tech", "admin", "general"]
        for module in modules:
            prompt = build_persona_prompt(module)
            assert isinstance(prompt, str)
            assert len(prompt) > 100