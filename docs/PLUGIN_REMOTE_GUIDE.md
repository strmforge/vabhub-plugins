# VabHub 远程插件开发指南

本文档介绍如何开发 VabHub 远程插件，这种插件运行在独立的服务进程中，通过 HTTP 与 VabHub 主程序通信。

## 什么是远程插件？

### 背景与适用场景

远程插件允许开发者：

- **使用任意技术栈**：不限于 Python，可以使用 Go、Node.js、Java、Rust 等
- **独立部署**：运行在独立的服务器或容器中
- **资源隔离**：不影响 VabHub 主程序的稳定性
- **水平扩展**：可以部署多个实例实现负载均衡

### 典型使用场景

- **高性能处理**：需要大量计算资源的插件
- **跨语言集成**：集成现有的第三方服务或 SDK
- **独立维护**：插件需要独立的更新和部署节奏
- **团队协作**：不同团队负责不同插件的开发和维护

## 插件索引条目示例

### 完整配置示例

```json
{
  "id": "mycompany.ai-processor",
  "plugin_type": "remote",
  "name": "AI 内容处理器",
  "summary": "使用 AI 技术处理漫画和音频内容",
  "description": "这是一个基于深度学习的内容处理插件，支持图像识别、语音转文字等功能。使用独立的 AI 服务进行处理，避免影响主程序性能。",
  "version": "1.2.0",
  "repo_url": "https://github.com/mycompany/vabhub-ai-processor",
  "author_name": "MyCompany Team",
  "author_url": "https://github.com/mycompany",
  "channel": "community",
  "tags": ["ai", "processing", "remote"],
  "sdk_permissions": ["media.read"],
  "remote": {
    "base_url": "https://ai-processor.mycompany.com",
    "timeout": 10,
    "events": [
      "manga.updated",
      "audiobook.tts_finished",
      "download.completed"
    ],
    "auth_token": "optional_token_if_needed"
  },
  "config_schema": {
    "type": "object",
    "properties": {
      "api_endpoint": {
        "type": "string",
        "title": "AI 服务地址",
        "default": "https://api.mycompany.com"
      },
      "model_version": {
        "type": "string",
        "title": "AI 模型版本",
        "enum": ["v1.0", "v1.1", "v2.0"],
        "default": "v2.0"
      }
    }
  }
}
```

### 字段说明

- **plugin_type**: 必须设为 `"remote"`
- **remote**: 远程插件配置对象
  - **base_url**: 远程插件服务的根地址（必填）
  - **timeout**: HTTP 请求超时时间，单位秒（可选，默认 5）
  - **events**: 希望订阅的事件列表（可选）
  - **auth_token**: 认证令牌（可选）

## 事件推送协议

### 端点：POST /events

VabHub 会向 `{base_url}/events` 发送 HTTP POST 请求来推送事件。

#### 请求头

```http
Content-Type: application/json
User-Agent: VabHub/{version}
Authorization: Bearer {auth_token}  // 如果配置了 auth_token
X-VabHub-Plugin-ID: {plugin_id}
X-VabHub-Timestamp: {timestamp}
```

#### 请求体格式

```json
{
  "plugin_id": "mycompany.ai-processor",
  "event": "manga.updated",
  "payload": {
    "manga_id": "12345",
    "title": "Sample Manga",
    "chapter": 42,
    "download_url": "https://example.com/chapter42.zip"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "event_id": "evt_abc123def456"
}
```

#### 字段说明

- **plugin_id**: 插件标识符
- **event**: 事件类型名称（如 `manga.updated`）
- **payload**: 事件数据，内容因事件类型而异
- **timestamp**: 事件发生时间（ISO 8601 格式）
- **event_id**: 事件的唯一标识符，可用于去重

#### 响应格式

**成功处理**：
```json
{
  "status": "ok",
  "processed": true,
  "message": "Event processed successfully"
}
```

**事件被忽略**：
```json
{
  "status": "ignored",
  "processed": false,
  "message": "Event type not supported"
}
```

**处理错误**：
```json
{
  "status": "error",
  "processed": false,
  "message": "Internal processing error",
  "error_code": "PROCESSING_FAILED"
}
```

## 安全建议

### HTTPS 强制使用

生产环境中的远程插件必须使用 HTTPS：

```nginx
server {
    listen 443 ssl;
    server_name your-plugin.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location /events {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 认证机制

#### 1. Token 认证（推荐）

在 `remote.auth_token` 中配置令牌：

```json
{
  "remote": {
    "base_url": "https://your-plugin.example.com",
    "auth_token": "your_secure_token_here"
  }
}
```

服务端验证：

```python
import hmac
import hashlib

def verify_vabhub_request(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    
    token = auth_header[7:]  # Remove 'Bearer ' prefix
    expected_token = "your_secure_token_here"
    
    return hmac.compare_digest(token, expected_token)
```

#### 2. IP 白名单

限制只有 VabHub 服务器能访问你的插件：

```bash
# 使用 iptables
iptables -A INPUT -p tcp --dport 443 -s 192.168.1.100 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j DROP

# 或者使用防火墙规则
ufw allow from 192.168.1.100 to any port 443
```

#### 3. 签名验证（高级）

VabHub 可能会在请求头中添加签名信息，可用于验证请求的真实性：

```http
X-VabHub-Signature: sha256=abcdef1234567890...
X-VabHub-Timestamp: 1705319400
```

## 示例实现

### Python + FastAPI 示例

```python
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

app = FastAPI(title="VabHub Remote Plugin Example")

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VabHubEvent(BaseModel):
    plugin_id: str
    event: str
    payload: Dict[str, Any]
    timestamp: str
    event_id: str

@app.post("/events")
async def handle_vabhub_event(event: VabHubEvent, request: Request):
    """处理来自 VabHub 的事件"""
    
    # 验证认证（如果配置了 auth_token）
    auth_header = request.headers.get("Authorization")
    expected_token = "your_secure_token_here"
    
    if expected_token:
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authorization")
        
        token = auth_header[7:]
        if token != expected_token:
            raise HTTPException(status_code=403, detail="Invalid token")
    
    logger.info(f"Received event: {event.event} for plugin: {event.plugin_id}")
    
    # 根据事件类型处理
    if event.event == "manga.updated":
        await handle_manga_updated(event.payload)
        return {"status": "ok", "processed": True}
    
    elif event.event == "audiobook.tts_finished":
        await handle_tts_finished(event.payload)
        return {"status": "ok", "processed": True}
    
    else:
        logger.info(f"Ignoring unsupported event: {event.event}")
        return {"status": "ignored", "processed": False}

async def handle_manga_updated(payload: Dict[str, Any]):
    """处理漫画更新事件"""
    manga_id = payload.get("manga_id")
    title = payload.get("title")
    
    logger.info(f"Processing manga update: {title} (ID: {manga_id})")
    
    # 在这里实现你的业务逻辑
    # 例如：调用 AI 服务处理图片，生成摘要等

async def handle_tts_finished(payload: Dict[str, Any]):
    """处理 TTS 完成事件"""
    audiobook_id = payload.get("audiobook_id")
    file_path = payload.get("file_path")
    
    logger.info(f"Processing TTS completion: {audiobook_id} at {file_path}")
    
    # 实现你的 TTS 后处理逻辑

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Node.js + Express 示例

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 8080;

// 中间件
app.use(bodyParser.json());

// 验证中间件
function verifyAuth(req, res, next) {
    const expectedToken = 'your_secure_token_here';
    const authHeader = req.headers['authorization'];
    
    if (expectedToken) {
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ error: 'Missing authorization' });
        }
        
        const token = authHeader.substring(7);
        if (token !== expectedToken) {
            return res.status(403).json({ error: 'Invalid token' });
        }
    }
    
    next();
}

// 事件处理端点
app.post('/events', verifyAuth, (req, res) => {
    const { plugin_id, event, payload, timestamp } = req.body;
    
    console.log(`Received event: ${event} for plugin: ${plugin_id}`);
    
    // 根据事件类型处理
    switch (event) {
        case 'manga.updated':
            handleMangaUpdated(payload);
            return res.json({ status: 'ok', processed: true });
            
        case 'audiobook.tts_finished':
            handleTTSFinished(payload);
            return res.json({ status: 'ok', processed: true });
            
        default:
            console.log(`Ignoring unsupported event: ${event}`);
            return res.json({ status: 'ignored', processed: false });
    }
});

function handleMangaUpdated(payload) {
    const mangaId = payload.manga_id;
    const title = payload.title;
    
    console.log(`Processing manga update: ${title} (ID: ${mangaId})`);
    // 实现业务逻辑
}

function handleTTSFinished(payload) {
    const audiobookId = payload.audiobook_id;
    const filePath = payload.file_path;
    
    console.log(`Processing TTS completion: ${audiobookId} at ${filePath}`);
    // 实现业务逻辑
}

// 健康检查
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', version: '1.0.0' });
});

// 启动服务
app.listen(PORT, '0.0.0.0', () => {
    console.log(`VabHub remote plugin listening on port ${PORT}`);
});
```

## 部署建议

### Docker 部署

```dockerfile
# 使用 Python 示例
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  vabhub-remote-plugin:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PLUGIN_TOKEN=your_secure_token_here
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

### 云服务部署

- **AWS ECS/Fargate**: 无服务器容器部署
- **Google Cloud Run**: 托管的容器平台
- **Azure Container Instances**: 按需容器实例
- **DigitalOcean App Platform**: 简单的应用托管

## 监控和调试

### 日志记录

建议记录以下信息：
- 接收到的事件类型和 ID
- 处理结果（成功/失败/忽略）
- 处理耗时
- 错误详情（如果有）

### 性能监控

- 响应时间监控
- 错误率统计
- 并发处理能力
- 资源使用情况

### 健康检查

提供 `/health` 端点供 VabHub 检查插件状态：

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "2h 15m",
  "last_event": "2024-01-15T10:30:00Z"
}
```

## 常见问题

### Q: 远程插件如何访问 VabHub 的内部 API？

A: 远程插件通常通过 VabHub 暴露的 HTTP API 或 GraphQL 接口与宿主系统交互。不建议直接访问内部服务。

### Q: 事件推送失败怎么办？

A: VabHub 会重试失败的事件推送，建议你的服务实现幂等处理，避免重复执行相同事件。

### Q: 如何保证数据安全？

A: 使用 HTTPS、配置适当的认证机制、定期轮换令牌、限制访问 IP 范围。

### Q: 插件更新怎么办？

A: 远程插件可以独立更新，无需重启 VabHub。只需确保接口协议兼容即可。

---

**开始构建你的远程插件，扩展 VabHub 的能力边界！**