# 远程插件协议说明

本文档提供了 VabHub 远程插件的完整接口规范和实现示例。

## 远程插件定义

远程插件运行在独立的服务进程中，通过 HTTP 与 VabHub 通信。

### plugin.json 配置

```json
{
  "id": "example.remote_processor",
  "plugin_type": "remote",
  "name": "Remote Content Processor",
  "summary": "远程内容处理服务示例",
  "version": "1.0.0",
  "channel": "community",
  "author_name": "Example Developer",
  "author_url": "https://github.com/example",
  "repo_url": "https://github.com/example/remote-processor",
  "sdk_permissions": ["media.read"],
  "remote": {
    "base_url": "https://your-remote-plugin.example.com",
    "timeout": 10,
    "events": [
      "manga.updated",
      "audiobook.tts_finished",
      "download.completed"
    ],
    "auth_token": "your_secure_token_here"
  }
}
```

## 接口协议

### 1. 事件接收接口

**端点**: `POST /events`

VabHub 向远程插件推送事件时调用此接口。

#### 请求格式

**HTTP Headers**:
```http
Content-Type: application/json
User-Agent: VabHub/2.0.0
Authorization: Bearer your_secure_token_here  // 如果配置了 auth_token
X-VabHub-Plugin-ID: example.remote_processor
X-VabHub-Timestamp: 1705319400
```

**Request Body**:
```json
{
  "plugin_id": "example.remote_processor",
  "event": "manga.updated",
  "payload": {
    "manga_id": "12345",
    "title": "Sample Manga Title",
    "chapter": 42,
    "series_id": "abc123",
    "download_url": "https://example.com/chapter42.zip",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "event_id": "evt_abc123def456"
}
```

#### 响应格式

**成功处理**:
```json
{
  "status": "ok",
  "processed": true,
  "message": "Event processed successfully"
}
```

**事件被忽略**:
```json
{
  "status": "ignored",
  "processed": false,
  "message": "Event type not supported"
}
```

**处理错误**:
```json
{
  "status": "error",
  "processed": false,
  "message": "Internal processing error",
  "error_code": "PROCESSING_FAILED"
}
```

### 2. 健康检查接口

**端点**: `GET /health`

用于 VabHub 检查远程插件的健康状态。

**响应格式**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:35:00Z",
  "uptime": "2h 15m",
  "plugin_id": "example.remote_processor"
}
```

## 支持的事件类型

### 漫画更新事件

```json
{
  "event": "manga.updated",
  "payload": {
    "manga_id": "string",
    "series_id": "string", 
    "title": "string",
    "chapter": "number",
    "download_url": "string",
    "updated_at": "string"
  }
}
```

### TTS 完成事件

```json
{
  "event": "audiobook.tts_finished",
  "payload": {
    "audiobook_id": "string",
    "title": "string",
    "file_path": "string",
    "duration": "number",
    "completed_at": "string"
  }
}
```

### 下载完成事件

```json
{
  "event": "download.completed",
  "payload": {
    "download_id": "string",
    "status": "string", // "completed", "failed", "cancelled"
    "file_path": "string",
    "file_size": "number",
    "completed_at": "string"
  }
}
```

## 实现示例

### Python + FastAPI

```python
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import datetime
import time

app = FastAPI(title="VabHub Remote Plugin")

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VabHubEvent(BaseModel):
    plugin_id: str
    event: str
    payload: Dict[str, Any]
    timestamp: str
    event_id: str

# 状态存储（实际应用中应使用数据库）
stats = {
    "processed_count": 0,
    "error_count": 0,
    "last_event": None
}

@app.post("/events")
async def handle_vabhub_event(event: VabHubEvent, request: Request):
    """处理 VabHub 事件推送"""
    
    # 验证认证
    auth_header = request.headers.get("Authorization")
    expected_token = "your_secure_token_here"
    
    if expected_token:
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authorization")
        
        token = auth_header[7:]
        if token != expected_token:
            raise HTTPException(status_code=403, detail="Invalid token")
    
    logger.info(f"Received event: {event.event} from {event.plugin_id}")
    
    try:
        # 更新统计
        stats["processed_count"] += 1
        stats["last_event"] = {
            "type": event.event,
            "timestamp": event.timestamp
        }
        
        # 根据事件类型处理
        if event.event == "manga.updated":
            await handle_manga_updated(event.payload)
            return {"status": "ok", "processed": True}
        
        elif event.event == "audiobook.tts_finished":
            await handle_tts_finished(event.payload)
            return {"status": "ok", "processed": True}
        
        elif event.event == "download.completed":
            await handle_download_completed(event.payload)
            return {"status": "ok", "processed": True}
        
        else:
            logger.info(f"Ignoring unsupported event: {event.event}")
            return {"status": "ignored", "processed": False}
    
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        stats["error_count"] += 1
        return {
            "status": "error",
            "processed": False,
            "message": str(e),
            "error_code": "PROCESSING_FAILED"
        }

async def handle_manga_updated(payload: Dict[str, Any]):
    """处理漫画更新事件"""
    manga_id = payload.get("manga_id")
    title = payload.get("title")
    chapter = payload.get("chapter")
    
    logger.info(f"Processing manga update: {title} Chapter {chapter}")
    
    # 在这里实现你的业务逻辑
    # 例如：AI 图像处理、元数据提取、自动分类等
    
    # 模拟处理时间
    await asyncio.sleep(0.1)

async def handle_tts_finished(payload: Dict[str, Any]):
    """处理 TTS 完成事件"""
    audiobook_id = payload.get("audiobook_id")
    title = payload.get("title")
    file_path = payload.get("file_path")
    
    logger.info(f"Processing TTS completion: {title} -> {file_path}")
    
    # 实现 TTS 后处理逻辑
    # 例如：音频质量检查、格式转换、元数据提取等

async def handle_download_completed(payload: Dict[str, Any]):
    """处理下载完成事件"""
    download_id = payload.get("download_id")
    status = payload.get("status")
    file_path = payload.get("file_path")
    
    logger.info(f"Processing download completion: {download_id} ({status})")
    
    # 实现下载后处理逻辑
    # 例如：文件验证、自动入库、通知发送等

@app.get("/health")
async def health_check():
    """健康检查"""
    uptime_seconds = int(time.time()) - start_time
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": f"{hours}h {minutes}m",
        "plugin_id": "example.remote_processor",
        "stats": stats
    }

# 记录启动时间
start_time = int(time.time())

if __name__ == "__main__":
    import uvicorn
    import asyncio
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Node.js + Express

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8080;
const AUTH_TOKEN = 'your_secure_token_here';

// 中间件
app.use(cors());
app.use(bodyParser.json());

// 状态存储
let stats = {
    processedCount: 0,
    errorCount: 0,
    lastEvent: null,
    startTime: Date.now()
};

// 认证中间件
function verifyAuth(req, res, next) {
    const authHeader = req.headers['authorization'];
    
    if (AUTH_TOKEN) {
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ error: 'Missing authorization' });
        }
        
        const token = authHeader.substring(7);
        if (token !== AUTH_TOKEN) {
            return res.status(403).json({ error: 'Invalid token' });
        }
    }
    
    next();
}

// 事件处理端点
app.post('/events', verifyAuth, (req, res) => {
    const { plugin_id, event, payload, timestamp } = req.body;
    
    console.log(`Received event: ${event} from ${plugin_id}`);
    
    try {
        // 更新统计
        stats.processedCount++;
        stats.lastEvent = {
            type: event,
            timestamp: timestamp
        };
        
        // 事件处理逻辑
        switch (event) {
            case 'manga.updated':
                handleMangaUpdated(payload);
                return res.json({ status: 'ok', processed: true });
                
            case 'audiobook.tts_finished':
                handleTTSFinished(payload);
                return res.json({ status: 'ok', processed: true });
                
            case 'download.completed':
                handleDownloadCompleted(payload);
                return res.json({ status: 'ok', processed: true });
                
            default:
                console.log(`Ignoring unsupported event: ${event}`);
                return res.json({ status: 'ignored', processed: false });
        }
    } catch (error) {
        console.error(`Error processing event:`, error);
        stats.errorCount++;
        return res.status(500).json({
            status: 'error',
            processed: false,
            message: error.message,
            errorCode: 'PROCESSING_FAILED'
        });
    }
});

function handleMangaUpdated(payload) {
    const mangaId = payload.manga_id;
    const title = payload.title;
    const chapter = payload.chapter;
    
    console.log(`Processing manga update: ${title} Chapter ${chapter}`);
    
    // 实现业务逻辑
    // 例如：调用外部 AI 服务处理图像
}

function handleTTSFinished(payload) {
    const audiobookId = payload.audiobook_id;
    const title = payload.title;
    const filePath = payload.file_path;
    
    console.log(`Processing TTS completion: ${title} -> ${filePath}`);
    
    // 实现 TTS 后处理
}

function handleDownloadCompleted(payload) {
    const downloadId = payload.download_id;
    const status = payload.status;
    
    console.log(`Processing download completion: ${downloadId} (${status})`);
    
    // 实现下载后处理
}

// 健康检查端点
app.get('/health', (req, res) => {
    const uptimeMs = Date.now() - stats.startTime;
    const hours = Math.floor(uptimeMs / 3600000);
    const minutes = Math.floor((uptimeMs % 3600000) / 60000);
    
    res.json({
        status: 'healthy',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        uptime: `${hours}h ${minutes}m`,
        pluginId: 'example.remote_processor',
        stats: stats
    });
});

// 启动服务
app.listen(PORT, '0.0.0.0', () => {
    console.log(`VabHub remote plugin listening on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
});
```

## 部署配置

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV AUTH_TOKEN=your_secure_token_here
ENV LOG_LEVEL=INFO

CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  vabhub-remote-plugin:
    build: .
    ports:
      - "8080:8080"
    environment:
      - AUTH_TOKEN=your_secure_token_here
      - LOG_LEVEL=INFO
      - PLUGIN_ID=example.remote_processor
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 安全最佳实践

1. **HTTPS 强制使用**：生产环境必须使用 SSL/TLS
2. **认证令牌**：使用强随机字符串作为认证令牌
3. **IP 白名单**：限制 VabHub 服务器的访问
4. **速率限制**：防止事件推送滥用
5. **日志监控**：记录所有请求和错误信息
6. **健康检查**：实现可靠的健康检查端点

## 常见问题

### Q: 事件推送失败如何处理？

A: VabHub 会自动重试失败的事件推送，建议你的服务实现幂等处理。

### Q: 如何处理大量事件？

A: 建议使用消息队列（如 Redis、RabbitMQ）缓冲事件，避免阻塞处理。

### Q: 如何与 VabHub 内部 API 交互？

A: 通过 VabHub 暴露的 HTTP API 或 GraphQL 接口，需要适当的认证。

---

这个规范为远程插件开发提供了完整的协议参考和实现示例。