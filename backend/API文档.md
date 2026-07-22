# 智汇办公 AI 智能平台 - 后端 API 文档

> **Base URL**: `http://localhost:8888`  
> **认证方式**: JWT Bearer Token  
> **内容类型**: `application/json`（除特殊标注外）

---

## 一、认证与授权

所有需要认证的接口，请求头需携带：
```
Authorization: Bearer <access_token>
```

Token 通过 `/auth/login/json` 接口获取，有效期 30 分钟。

---

## 二、接口列表

### 2.1 系统接口

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/` | API 根路径，返回欢迎信息 | 否 |
| GET | `/health` | 健康检查 | 否 |
| GET | `/stats` | 仪表盘统计数据（Redis 缓存） | 否 |

#### GET `/stats`

返回仪表盘统计数据。

**响应示例**：
```json
{
  "total_knowledge_bases": 6,
  "total_documents": 10,
  "total_conversations": 128,
  "active_users": 4,
  "hot_questions": ["报销流程", "年假天数", "API认证"]
}
```

---

### 2.2 认证模块（`/auth`）

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| POST | `/auth/login` | 表单登录（Swagger 兼容） | 否 |
| POST | `/auth/login/json` | JSON 登录（前端使用） | 否 |
| GET | `/auth/me` | 获取当前用户信息 | 是 |
| POST | `/auth/register` | 用户注册 | 否 |
| DELETE | `/auth/deactivate` | 注销当前账户 | 是 |

#### POST `/auth/login/json`

JSON 格式登录，前端使用。

**请求体**：
```json
{
  "username": "admin",
  "password": "123456"
}
```

**响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### POST `/auth/register`

用户注册，新用户默认为普通用户角色。

**请求体**：
```json
{
  "username": "zhangsan",
  "email": "zhangsan@company.com",
  "password": "123456",
  "full_name": "张三",
  "department": "人力资源部"
}
```

**响应**：
```json
{
  "message": "User created successfully",
  "user_id": 2
}
```

#### GET `/auth/me`

获取当前登录用户信息。

**响应**：
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@company.com",
  "full_name": "系统管理员",
  "department": "技术部",
  "role_id": 1,
  "status": true,
  "avatar": null
}
```

#### DELETE `/auth/deactivate`

注销当前用户账户，同时删除个人知识库、对话日志等关联数据。

**响应**：
```json
{
  "message": "账户已注销"
}
```

---

### 2.3 用户管理模块（`/users`）

> 以下接口均需**管理员权限**。

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/users/` | 获取用户列表 | 是(管理员) |
| GET | `/users/{user_id}` | 获取单个用户 | 是(管理员) |
| PUT | `/users/{user_id}` | 更新用户信息 | 是(管理员) |
| DELETE | `/users/{user_id}` | 删除用户 | 是(管理员) |
| GET | `/users/roles/` | 获取角色列表 | 是(管理员) |
| POST | `/users/roles/` | 创建角色 | 是(管理员) |

#### GET `/users/`

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| skip | int | 跳过的记录数，默认 0 |
| limit | int | 返回数量，默认 100 |
| username | string | 按用户名模糊搜索 |
| department | string | 按部门精确筛选 |

**响应**：用户对象数组

#### PUT `/users/{user_id}`

**请求体**（部分更新）：
```json
{
  "full_name": "张三（已更新）",
  "department": "技术部",
  "role_id": 1
}
```

#### POST `/users/roles/`

**请求体**：
```json
{
  "name": "auditor",
  "description": "审核员",
  "permissions": ["audit.review", "kb.read"]
}
```

---

### 2.4 知识库模块（`/knowledge-bases`）

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/knowledge-bases/modules` | 获取模块列表 | 否 |
| GET | `/knowledge-bases/` | 获取知识库列表 | 是 |
| GET | `/knowledge-bases/{kb_id}` | 获取单个知识库 | 是 |
| POST | `/knowledge-bases/` | 创建知识库 | 是 |
| PUT | `/knowledge-bases/{kb_id}` | 更新知识库 | 是 |
| DELETE | `/knowledge-bases/{kb_id}` | 删除知识库 | 是 |

#### GET `/knowledge-bases/modules`

返回四大业务模块定义。

**响应**：
```json
[
  {
    "id": "policy",
    "name": "规章制度",
    "description": "企业规章制度、流程规范、管理制度",
    "icon": "Document",
    "color": "#4f6ef7",
    "example_questions": ["报销流程是什么？", "请假制度是怎样的？"]
  },
  {
    "id": "tech",
    "name": "产品技术",
    "description": "技术文档、产品手册、API说明、开发规范",
    "icon": "Monitor",
    "color": "#22c55e",
    "example_questions": ["API接口文档在哪？", "系统架构是怎样的？"]
  },
  {
    "id": "admin",
    "name": "行政服务",
    "description": "办公场地、IT支持、福利政策、行政事务",
    "icon": "OfficeBuilding",
    "color": "#f59e0b",
    "example_questions": ["办公场地怎么申请？", "IT设备报修流程？"]
  },
  {
    "id": "general",
    "name": "自由问答",
    "description": "通用知识库，回答任何问题",
    "icon": "ChatLineRound",
    "color": "#8b5cf6",
    "example_questions": ["什么是RAG技术？", "帮我写一份周报"]
  }
]
```

#### GET `/knowledge-bases/`

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| skip | int | 跳过记录数 |
| limit | int | 返回数量 |
| name | string | 按名称模糊搜索 |
| department | string | 按部门筛选 |
| module | string | 按模块筛选（policy/tech/admin/general） |

**权限说明**：
- 管理员：看到所有知识库
- 普通用户：只能看到共享知识库 + 自己的个人知识库

#### POST `/knowledge-bases/`

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| is_personal | bool | 是否为个人知识库，默认 false |

**请求体**：
```json
{
  "name": "技术文档库",
  "description": "产品技术相关文档",
  "module": "tech",
  "embedding_model": "qwen3-embedding:0.6b"
}
```

**权限说明**：
- 管理员可创建全局知识库和个人知识库
- 普通用户只能创建个人知识库
- 管理员为 policy/tech/admin 模块创建的知识库自动设为共享

#### DELETE `/knowledge-bases/{kb_id}`

**注意**：
- 系统内置的初始知识库（is_locked=true）不可删除
- 含有文档的知识库不可删除，需先删除所有文档
- 普通用户只能删除自己的个人知识库

---

### 2.5 文档管理模块（`/documents`）

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| POST | `/documents/upload/{kb_id}` | 上传文档到知识库 | 是 |
| GET | `/documents/` | 获取文档列表 | 是 |
| GET | `/documents/{doc_id}` | 获取单个文档 | 是 |
| DELETE | `/documents/{doc_id}` | 删除文档 | 是 |
| POST | `/documents/{doc_id}/process` | 手动触发文档处理 | 是 |

#### POST `/documents/upload/{kb_id}`

上传文档到指定知识库，自动触发内容审核和解析流程。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| kb_id | int | 知识库 ID |

**请求体**：`multipart/form-data`

| 字段 | 类型 | 说明 |
|------|------|------|
| file | File | 上传的文件 |

**支持格式**：PDF、DOC、DOCX、PPT、PPTX、XLS、XLSX、MD、TXT、HTML、EPUB、MOBI、JPG、JPEG、PNG

**响应**：
```json
{
  "id": 11,
  "filename": "员工手册.pdf",
  "file_type": "pdf",
  "size": 2048576,
  "status": "pending",
  "audit_status": "pending"
}
```

#### GET `/documents/`

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| knowledge_base_id | int | 按知识库筛选 |
| status | string | 按状态筛选（pending/processing/completed/failed/rejected/pending_review） |
| audit_status | string | 按审核状态筛选 |
| skip | int | 跳过记录数 |
| limit | int | 返回数量 |

#### DELETE `/documents/{doc_id}`

删除文档，同时从向量库中移除对应的向量数据。

---

### 2.6 对话模块（`/chat`）

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| POST | `/chat/message` | 发送消息（普通响应） | 是 |
| POST | `/chat/stream` | 发送消息（SSE 流式响应） | 是 |
| POST | `/chat/upload-and-ask` | 上传文件并提问 | 是 |
| GET | `/chat/history/{conversation_id}` | 获取会话历史 | 是 |
| GET | `/chat/sessions` | 获取当前用户所有会话 | 是 |
| GET | `/chat/logs` | 获取对话日志列表 | 是 |
| DELETE | `/chat/history/{conversation_id}` | 删除会话 | 是 |
| DELETE | `/chat/logs/{log_id}` | 删除单条日志（管理员） | 是(管理员) |
| DELETE | `/chat/logs` | 批量删除日志（管理员） | 是(管理员) |
| POST | `/chat/feedback` | 提交消息反馈 | 是 |
| GET | `/chat/feedback/{conv_id}/{msg_id}` | 获取消息反馈 | 是 |
| POST | `/chat/favorite` | 收藏/取消收藏 | 是 |
| GET | `/chat/favorites` | 获取收藏列表 | 是 |
| GET | `/chat/favorites/check/{conv_id}/{msg_id}` | 检查是否已收藏 | 是 |
| DELETE | `/chat/favorites/{fav_id}` | 删除收藏 | 是 |

#### POST `/chat/message`

发送消息并获取完整回答（非流式）。

**请求体**：
```json
{
  "message": "公司年假有多少天？",
  "conversation_id": "conv-001",
  "mode": "rag",
  "provider": "api",
  "module": "policy",
  "knowledge_base_ids": [1],
  "use_web": false
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| message | string | 是 | 用户提问内容 |
| conversation_id | string | 否 | 会话 ID，不传则自动生成 |
| mode | string | 否 | 推理模式：`rag`（默认）/ `agent` / `langgraph` |
| provider | string | 否 | 模型来源：`api`（默认，DeepSeek）/ `local`（Ollama） |
| module | string | 否 | 业务模块：`policy`/`tech`/`admin`/`general` |
| knowledge_base_ids | int[] | 否 | 指定知识库 ID 列表，不传则根据 module 自动选择 |
| use_web | bool | 否 | 是否启用联网搜索，默认 false |

**响应**：
```json
{
  "answer": "根据公司《员工手册》规定：\n- 工作满1年不满10年：5天年假\n...",
  "sources": [],
  "conversation_id": "conv-001"
}
```

#### POST `/chat/stream`

SSE 流式响应，逐字返回 AI 回答。

**请求体**：同 `/chat/message`

**响应**：`text/event-stream`

**SSE 事件格式**：

首帧（meta）：
```
data: {"type": "meta", "conversation_id": "conv-001", "module": "policy"}
```

推理阶段（仅推理模型）：
```
data: {"type": "reasoning", "text": "让我分析一下这个问题..."}
```

回答阶段：
```
data: {"type": "content", "text": "根据公司规定..."}
```

附件（如有）：
```
data: {"type": "attachments", "items": [{"file_id": "xxx", "filename": "报告.docx", "download_url": "/files/download/xxx"}]}
```

结束标志：
```
data: [DONE]
```

错误：
```
data: {"type": "error", "content": "错误信息"}
```

#### POST `/chat/upload-and-ask`

上传文件并基于文件内容提问。

**请求体**：`multipart/form-data`

| 字段 | 类型 | 说明 |
|------|------|------|
| file | File | 上传的文件 |
| message | string | 提问内容，默认"请分析这个文件的内容" |
| conversation_id | string | 会话 ID（可选） |
| module | string | 模块（可选） |

**响应**：
```json
{
  "answer": "文件内容分析结果...",
  "conversation_id": "conv-002",
  "filename": "report.pdf"
}
```

#### GET `/chat/sessions`

返回当前用户所有会话列表，按时间倒序。

**响应**：
```json
[
  {
    "conversation_id": "conv-001",
    "last_message": "公司年假有多少天？",
    "last_time": "2026-07-22T10:30:00",
    "user_id": 2,
    "created_at": "2026-07-22T10:30:00",
    "module": "policy"
  }
]
```

#### GET `/chat/logs`

获取对话日志列表，支持搜索和筛选。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| search | string | 搜索关键词（匹配问题或回答） |
| user_id | string | 按用户 ID 或用户名筛选（仅管理员） |
| start_date | string | 开始日期 |
| end_date | string | 结束日期 |
| skip | int | 跳过记录数 |
| limit | int | 返回数量，默认 100 |

**权限**：管理员看全部，普通用户只看自己的。

#### POST `/chat/feedback`

提交消息反馈（点赞/点踩）。

**请求体**：
```json
{
  "conversation_id": "conv-001",
  "message_id": "msg-001",
  "rating": 1,
  "correction": "回答很准确"
}
```

**rating 说明**：`1` = 点赞，`-1` = 点踩，`0` = 取消反馈

#### POST `/chat/favorite`

收藏/取消收藏单条 AI 回复（切换模式）。

**请求体**：
```json
{
  "conversation_id": "conv-001",
  "message_id": "msg-001",
  "title": "年假天数查询",
  "query": "公司年假有多少天？",
  "answer": "根据公司《员工手册》规定...",
  "module": "policy"
}
```

**响应**：
```json
{"favorited": true, "id": 1, "message": "已收藏"}
```
再次调用同一消息则取消收藏：
```json
{"favorited": false, "message": "已取消收藏"}
```

---

### 2.7 文件下载模块（`/files`）

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/files/download/{file_id}` | 下载生成的文件 | 是 |
| GET | `/files/` | 获取文件列表 | 是 |
| DELETE | `/files/{file_id}` | 删除文件 | 是 |

#### GET `/files/download/{file_id}`

下载由文档生成功能创建的文件（Word/PDF）。

**响应**：文件流（`application/octet-stream`）

---

### 2.8 系统配置模块（`/system-config`）

> 以下接口均需**管理员权限**。

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/system-config/` | 获取所有配置项 | 是(管理员) |
| PUT | `/system-config/{key}` | 更新配置项 | 是(管理员) |

#### GET `/system-config/`

**响应**：
```json
[
  {"key": "llm_model", "value": "deepseek-chat", "description": "默认使用的LLM模型"},
  {"key": "chunk_size", "value": "500", "description": "文本切片大小"},
  {"key": "top_k", "value": "5", "description": "RAG检索返回的文档数量"}
]
```

#### PUT `/system-config/{key}`

**请求体**：
```json
{
  "value": "1000",
  "description": "文本切片大小（已更新）"
}
```

---

### 2.9 用户资料模块（`/profile`）

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/profile/` | 获取个人资料 | 是 |
| PUT | `/profile/` | 更新个人资料 | 是 |
| PUT | `/profile/password` | 修改密码 | 是 |
| PUT | `/profile/avatar` | 上传头像 | 是 |

#### PUT `/profile/`

**请求体**（部分更新）：
```json
{
  "full_name": "张三",
  "department": "技术部",
  "email": "zhangsan@company.com"
}
```

#### PUT `/profile/password`

**请求体**：
```json
{
  "old_password": "123456",
  "new_password": "newpassword123"
}
```

---

### 2.10 模型微调模块（`/finetune`）

> 以下接口均需**管理员权限**。

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| POST | `/finetune/prepare-data` | 从对话日志准备微调数据 | 是(管理员) |
| POST | `/finetune/start` | 启动微调训练 | 是(管理员) |
| GET | `/finetune/status` | 获取训练状态 | 是(管理员) |
| GET | `/finetune/logs` | 获取训练日志 | 是(管理员) |

#### POST `/finetune/prepare-data`

从历史对话日志中提取问答对，生成微调数据集。

**请求体**：
```json
{
  "min_query_length": 5,
  "min_answer_length": 10,
  "test_split_ratio": 0.1
}
```

#### POST `/finetune/start`

启动 LoRA 微调训练。

**请求体**：
```json
{
  "base_model": "Qwen/Qwen2.5-7B-Instruct",
  "lora_r": 16,
  "lora_alpha": 32,
  "num_epochs": 3,
  "batch_size": 4,
  "learning_rate": 2e-4
}
```

---

## 三、数据模型

### 3.1 用户（User）

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@company.com",
  "full_name": "系统管理员",
  "department": "技术部",
  "role_id": 1,
  "status": true,
  "avatar": null,
  "created_at": "2026-07-01T00:00:00",
  "updated_at": "2026-07-01T00:00:00"
}
```

### 3.2 知识库（KnowledgeBase）

```json
{
  "id": 1,
  "name": "规章制度",
  "description": "公司规章制度",
  "department": null,
  "owner_id": 1,
  "embedding_model": "qwen3-embedding:0.6b",
  "is_personal": false,
  "module": "policy",
  "is_shared": true,
  "is_locked": true,
  "status": true,
  "document_count": 3,
  "created_at": "2026-07-01T00:00:00"
}
```

### 3.3 文档（Document）

```json
{
  "id": 1,
  "knowledge_base_id": 1,
  "filename": "员工手册.pdf",
  "file_type": "pdf",
  "size": 2048576,
  "chunk_count": 120,
  "status": "completed",
  "audit_status": "passed",
  "uploaded_by": 1,
  "uploaded_at": "2026-07-01T00:00:00"
}
```

### 3.4 对话记录（ConversationLog）

```json
{
  "id": 1,
  "conversation_id": "conv-001",
  "user_id": 2,
  "query": "公司年假有多少天？",
  "answer": "根据公司《员工手册》规定...",
  "sources": [],
  "knowledge_base_ids": [1],
  "module": "policy",
  "created_at": "2026-07-22T10:30:00"
}
```

### 3.5 内容审核日志（ContentAuditLog）

```json
{
  "id": 1,
  "document_id": 1,
  "filename": "员工手册.pdf",
  "knowledge_base_id": 1,
  "user_id": 1,
  "verdict": "PASS",
  "confidence": 0.85,
  "categories": "[]",
  "reasons": "[]",
  "summary": "文档内容合规",
  "status": "auto_processed",
  "created_at": "2026-07-01T00:00:00"
}
```

---

## 四、错误码

| HTTP 状态码 | 说明 |
|:-----------:|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无返回体） |
| 400 | 请求参数错误 / 内容不合规 |
| 401 | 未认证 / Token 无效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁（限流） |
| 500 | 服务器内部错误 |

---

## 五、速率限制

- 每个用户每分钟最多 **20 次**对话请求
- 超限返回 `429 Too Many Requests`
- 限流基于 Redis 实现，按用户 ID 计数

---

## 六、内容审核

所有用户提问和文档上传都会经过内容审核：

| 审核对象 | 审核方式 | 说明 |
|----------|----------|------|
| 用户提问 | 关键词快速扫描 | 仅检查高危关键词，不调用 LLM，避免延迟 |
| 文档上传 | 两层审核 | 关键词扫描 + LLM 深度审核 |
| AI 回答 | 关键词快速扫描 | 检查是否包含违规内容 |

**审核结果**：
- `PASS`：内容合规，正常处理
- `REVIEW`：存疑内容，需人工审核
- `BLOCK`：违规内容，直接拒绝

---

**文档版本**：v1.0  
**生成日期**：2026年7月22日  
**API 版本**：1.0.0