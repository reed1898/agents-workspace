# AvatarKit API 部署指南

本文档详细介绍 AvatarKit API SaaS 版本的各种部署方式。

## 目录

1. [Docker Compose 部署](#docker-compose-部署)
2. [云服务器部署](#云服务器部署)
3. [支付接入指南](#支付接入指南)
4. [监控和运维](#监控和运维)

---

## Docker Compose 部署

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 服务器配置：2核4G 起步，推荐 4核8G

### 快速部署

```bash
# 1. 克隆代码
git clone <your-private-repo>
cd avatarkit-api-private

# 2. 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f api

# 5. 执行数据库迁移
docker-compose exec api alembic upgrade head
```

### 环境变量配置

```bash
# .env 文件示例

# 安全密钥（必须修改！）
JWT_SECRET=your-super-secret-jwt-key-min-32-characters-long
API_KEY_SALT=your-api-key-salt-min-16-characters

# 数据库密码
DB_PASSWORD=your-strong-db-password

# 外部 API 密钥
FAL_KEY=your_fal_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# 可选：R2 存储
R2_ACCOUNT_ID=xxx
R2_ACCESS_KEY_ID=xxx
R2_SECRET_ACCESS_KEY=xxx
```

---

## 云服务器部署

### 服务器选购建议

| 规模 | 配置 | 适用场景 |
|------|------|----------|
| 小型 | 2核4G 5M带宽 | 测试环境、小规模使用 |
| 中型 | 4核8G 10M带宽 | 生产环境初期 |
| 大型 | 8核16G 20M带宽 | 高并发生产环境 |

推荐服务商：阿里云、腾讯云、AWS、DigitalOcean

### Ubuntu 服务器部署步骤

#### 1. 系统更新

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git nginx python3-pip python3-venv postgresql redis-server
```

#### 2. 配置 PostgreSQL

```bash
# 创建数据库和用户
sudo -u postgres psql -c "CREATE USER avatarkit WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "CREATE DATABASE avatarkit OWNER avatarkit;"
sudo -u postgres psql -c "ALTER USER avatarkit WITH SUPERUSER;"
```

#### 3. 配置 Redis

```bash
# 编辑 Redis 配置
sudo nano /etc/redis/redis.conf

# 如需设置密码，取消注释并修改：
# requirepass your_redis_password

# 重启 Redis
sudo systemctl restart redis-server
```

#### 4. 部署应用

```bash
# 创建应用目录
sudo mkdir -p /opt/avatarkit
cd /opt/avatarkit

# 克隆代码
sudo git clone <your-private-repo> .

# 创建虚拟环境
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
sudo nano .env

# 执行数据库迁移
alembic upgrade head
```

#### 5. 使用 Systemd 管理服务

创建服务文件 `/etc/systemd/system/avatarkit.service`：

```ini
[Unit]
Description=AvatarKit API
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/avatarkit
Environment="PATH=/opt/avatarkit/venv/bin"
EnvironmentFile=/opt/avatarkit/.env
ExecStart=/opt/avatarkit/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable avatarkit
sudo systemctl start avatarkit
sudo systemctl status avatarkit
```

#### 6. 配置 Nginx 反向代理

创建配置 `/etc/nginx/sites-available/avatarkit`：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # 增加上传文件大小限制
    client_max_body_size 50M;
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/avatarkit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. 配置 HTTPS (Certbot)

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

---

## 支付接入指南

### 支付宝接入

#### 1. 注册支付宝商户账号

- 访问 [支付宝商家中心](https://b.alipay.com/)
- 完成企业认证
- 申请「电脑网站支付」产品

#### 2. 获取密钥

在支付宝开放平台：
1. 进入「开发设置」
2. 生成 RSA2 密钥对
3. 获取应用 ID (APPID)
4. 下载支付宝公钥

#### 3. 配置环境变量

```bash
ALIPAY_APP_ID=2024xxxxxxxxxxxx
ALIPAY_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----
ALIPAY_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhki...
-----END PUBLIC KEY-----
```

#### 4. 配置回调地址

在支付宝后台设置：
- 授权回调地址: `https://your-domain.com/v1/orders/webhook/alipay`

### 微信支付接入

#### 1. 注册微信商户号

- 访问 [微信支付商户平台](https://pay.weixin.qq.com/)
- 申请商户号并完成认证

#### 2. 获取 API 密钥

在微信商户平台：
1. 进入「账户中心」→「API 安全」
2. 设置 APIv3 密钥
3. 下载 API 证书

#### 3. 配置环境变量

```bash
WECHAT_APP_ID=wx1234567890abcdef
WECHAT_MCH_ID=1234567890
WECHAT_API_KEY=YourAPIKeyHere32CharsLong
WECHAT_NOTIFY_URL=https://your-domain.com/v1/orders/webhook/wechat
```

### 支付测试

```bash
# 创建测试订单
curl -X POST "https://your-domain.com/v1/orders/create" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 10.00,
    "payment_method": "alipay"
  }'
```

---

## 监控和运维

### 日志管理

查看应用日志：

```bash
# Docker 部署
docker-compose logs -f api

# Systemd 部署
sudo journalctl -u avatarkit -f
```

### 健康检查

```bash
# 检查服务状态
curl https://your-domain.com/health

# 预期响应
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00",
  "services": {
    "database": true,
    "redis": true
  }
}
```

### 备份策略

#### 数据库备份

```bash
# 创建备份脚本
sudo nano /opt/backup/avatarkit-backup.sh

#!/bin/bash
BACKUP_DIR="/opt/backup"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U avatarkit avatarkit > "$BACKUP_DIR/avatarkit_$DATE.sql"
# 保留最近 7 天备份
find $BACKUP_DIR -name "avatarkit_*.sql" -mtime +7 -delete
```

```bash
# 添加定时任务
crontab -e

# 每天凌晨 3 点备份
0 3 * * * /opt/backup/avatarkit-backup.sh
```

### 性能监控

推荐使用以下工具：

- **Prometheus + Grafana**: 指标收集和可视化
- **Sentry**: 错误追踪
- **Uptime Kuma**: 服务可用性监控

### 常见问题

#### 数据库连接失败

```bash
# 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 检查连接配置
psql -U avatarkit -d avatarkit -h localhost
```

#### Redis 连接失败

```bash
# 检查 Redis 状态
sudo systemctl status redis-server
redis-cli ping
```

#### 应用启动失败

```bash
# 查看详细错误
sudo journalctl -u avatarkit -n 100 --no-pager

# 检查环境变量
cat /opt/avatarkit/.env
```

---

## 安全建议

1. **修改默认密钥**: JWT_SECRET 和 API_KEY_SALT 必须修改
2. **限制端口访问**: 仅开放 80/443 端口，数据库和 Redis 不暴露公网
3. **启用防火墙**: 使用 ufw 或 cloud provider firewall
4. **定期更新**: 保持系统和依赖包更新
5. **HTTPS 强制**: 生产环境强制使用 HTTPS

```bash
# UFW 防火墙配置示例
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

---

## 升级指南

### 平滑升级步骤

```bash
# 1. 拉取新代码
cd /opt/avatarkit
git pull

# 2. 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 3. 执行数据库迁移
alembic upgrade head

# 4. 重启服务
sudo systemctl restart avatarkit

# 5. 验证服务
 curl https://your-domain.com/health
```

---

## 联系支持

部署遇到问题？请联系技术支持获取帮助。
