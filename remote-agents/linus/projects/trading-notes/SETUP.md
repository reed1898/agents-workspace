# Trading Notes - 开发环境设置指南

## 必要软件安装

### 1. MySQL 安装

#### macOS (使用 Homebrew)
```bash
# 安装 MySQL
brew install mysql

# 启动 MySQL 服务
brew services start mysql

# 创建数据库
mysql -u root -p -e "CREATE DATABASE trading_notes DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;"
```

#### Ubuntu/Debian
```bash
# 安装 MySQL
sudo apt-get update
sudo apt-get install mysql-server

# 启动 MySQL 服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 创建数据库
sudo mysql -e "CREATE DATABASE trading_notes DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;"
```

#### Windows
1. 下载 MySQL 安装程序: https://dev.mysql.com/downloads/installer/
2. 运行安装程序，设置 root 密码（与 `.env` 中一致）
3. 在 MySQL Shell 或 Workbench 中创建数据库 `trading_notes`

### 2. Redis 安装

#### macOS
```bash
brew install redis
brew services start redis
```

#### Ubuntu/Debian
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

#### Windows
1. 下载 Redis for Windows: https://github.com/microsoftarchive/redis/releases
2. 解压并运行 `redis-server.exe`

## 项目设置

### 后端设置

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量文件（已完成）
# cp .env.example .env

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload
```

访问 API 文档: http://localhost:8000/api/v1/docs

### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问前端: http://localhost:3000

## 验证安装

### 检查 MySQL
```bash
# 检查服务是否运行
mysqladmin ping -u root -p

# 连接到数据库
mysql -u root -p -e "SHOW DATABASES;"
```

### 检查 Redis
```bash
# 检查服务是否运行
redis-cli ping
# 应该返回: PONG
```

## 常见问题

### MySQL 连接失败
1. 确认 MySQL 服务正在运行
2. 检查 `.env` 文件中的 `DATABASE_URL` 是否正确
3. 确认数据库 `trading_notes` 已创建

### Redis 连接失败
1. 确认 Redis 服务正在运行
2. 检查 `.env` 文件中的 `REDIS_URL` 是否正确

### 端口已被占用
- 后端默认端口: 8000
- 前端默认端口: 3000
- MySQL 默认端口: 3306
- Redis 默认端口: 6379

如需修改端口，更新相应的配置文件。

## 下一步

安装完成后，可以：
1. 访问 http://localhost:8000/api/v1/docs 查看 API 文档
2. 测试用户注册功能
3. 开始前端开发
