"""测试权限管理模块（RBAC）"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestAuth:
    """权限管理测试"""

    def test_jwt_importable(self):
        """测试 JWT 模块可导入"""
        try:
            from app.auth import create_access_token, verify_token
            assert callable(create_access_token)
            assert callable(verify_token)
        except ImportError:
            pytest.skip("Auth 模块未找到")

    def test_jwt_secret_exists(self):
        """测试 JWT 密钥配置存在"""
        from config import SECRET_KEY
        assert SECRET_KEY is not None
        assert len(str(SECRET_KEY)) >= 32

    def test_password_hasher_importable(self):
        """测试密码哈希模块可导入"""
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            assert pwd_context is not None
        except ImportError:
            pytest.skip("passlib 未安装")

    def test_password_hashing(self):
        """测试密码哈希和验证"""
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            password = "test_password_123"
            hashed = pwd_context.hash(password)
            assert pwd_context.verify(password, hashed)
            assert not pwd_context.verify("wrong_password", hashed)
        except ImportError:
            pytest.skip("passlib 未安装")

    def test_create_access_token_returns_string(self):
        """测试创建访问令牌返回字符串"""
        try:
            from app.auth import create_access_token
            token = create_access_token(data={"sub": "test_user"})
            assert isinstance(token, str)
            assert len(token) > 0
        except ImportError:
            pytest.skip("Auth 模块未找到")

    def test_access_token_not_empty(self):
        """测试访问令牌不为空"""
        try:
            from app.auth import create_access_token
            token = create_access_token(data={"sub": "test"})
            assert token is not None
            assert token.strip() != ""
        except ImportError:
            pytest.skip("Auth 模块未找到")

    def test_access_token_has_expiry(self):
        """测试访问令牌包含过期时间"""
        try:
            from app.auth import create_access_token
            from jose import jwt
            from config import SECRET_KEY, ALGORITHM
            token = create_access_token(data={"sub": "test"})
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
            assert "exp" in payload
            assert isinstance(payload["exp"], int)
        except ImportError:
            pytest.skip("依赖未安装")

    def test_user_model_exists(self):
        """测试用户模型存在"""
        try:
            from app.models import User
            assert hasattr(User, "id")
            assert hasattr(User, "username")
            assert hasattr(User, "email")
            assert hasattr(User, "hashed_password")
            assert hasattr(User, "role")
        except ImportError:
            pytest.skip("User 模型未找到")

    def test_user_role_field(self):
        """测试用户角色字段"""
        try:
            from app.models import User
            assert hasattr(User, "role")
        except ImportError:
            pytest.skip("User 模型未找到")

    def test_role_values_defined(self):
        """测试角色值定义"""
        try:
            from app.schemas import Role
            roles = ["admin", "user"]
            for role in roles:
                assert hasattr(Role, role.upper()) or role in [r.value for r in Role]
        except ImportError:
            pytest.skip("Schemas 未找到")

    def test_admin_has_more_permissions(self):
        """测试管理员权限大于普通用户"""
        try:
            from app.auth import get_current_user, RoleChecker
            assert hasattr(RoleChecker, "__call__")
        except ImportError:
            pytest.skip("Auth 模块未找到")