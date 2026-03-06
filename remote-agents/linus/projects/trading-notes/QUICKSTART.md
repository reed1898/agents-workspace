# Trading Notes - 快速开始

## 🎯 当前状态

✅ **后端**: FastAPI + MySQL + Redis 已配置完成
✅ **前端**: Next.js 15 项目已创建
✅ **认证**: Google OAuth 已集成
✅ **数据库**: 用户表已创建并迁移完成

---

## 🚀 下一步操作

### 1. 获取 Google OAuth 凭据

按照 `docs/google-oauth-setup.md` 的指南操作：

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目 "Trading Notes"
3. 配置 OAuth 同意屏幕
4. 创建 OAuth 2.0 客户端 ID
5. 获取 `客户端 ID` 和 `客户端密钥`

### 2. 配置后端

编辑 `backend/.env` 文件，替换这两行：

```bash
GOOGLE_CLIENT_ID=你的客户端ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=你的客户端密钥
```

### 3. 启动后端服务器

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

后端将运行在: **http://localhost:8000**
API 文档: **http://localhost:8000/api/v1/docs**

### 4. 配置前端

创建 `frontend/.env.local` 文件：

```bash
NEXT_PUBLIC_GOOGLE_CLIENT_ID=你的客户端ID.apps.googleusercontent.com
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. 启动前端服务器

```bash
cd frontend
npm run dev
```

前端将运行在: **http://localhost:3000**

### 6. 实现前端登录页面

您需要创建登录页面，集成 Google Sign-In 按钮。

参考代码示例在下方 👇

---

## 📝 前端登录页面示例

### 安装依赖

```bash
cd frontend
npm install @react-oauth/google
```

### 创建登录页面

创建 `app/login/page.tsx`:

```typescript
'use client';

import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function LoginPage() {
  const router = useRouter();
  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleSuccess = async (credentialResponse: any) => {
    try {
      // 发送 ID token 到后端验证
      const response = await axios.post(
        `${apiUrl}/api/v1/auth/google`,
        null,
        {
          params: {
            id_token_str: credentialResponse.credential
          }
        }
      );

      // 保存 tokens
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);

      // 跳转到 dashboard
      router.push('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      alert('登录失败，请重试');
    }
  };

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="w-full max-w-md space-y-8 rounded-lg bg-white p-8 shadow-lg">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">Trading Notes</h1>
            <p className="mt-2 text-sm text-gray-600">
              使用 Google 账户登录
            </p>
          </div>

          <div className="flex justify-center">
            <GoogleLogin
              onSuccess={handleSuccess}
              onError={() => {
                console.error('Login Failed');
                alert('登录失败');
              }}
              useOneTap
            />
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
```

### 更新主页

编辑 `app/page.tsx`，添加登录按钮：

```typescript
import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">Trading Notes</h1>
      <Link
        href="/login"
        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        开始使用
      </Link>
    </main>
  );
}
```

---

## 🧪 测试

1. 确保后端和前端都在运行
2. 访问 http://localhost:3000
3. 点击 "开始使用"
4. 点击 Google 登录按钮
5. 选择您的 Google 账户
6. 授权应用
7. 登录成功后会跳转到 dashboard（需要创建）

---

## 📚 API 端点

### 认证相关

- **POST /api/v1/auth/google**
  参数: `id_token_str` (Google ID Token)
  返回: JWT access_token 和 refresh_token

- **POST /api/v1/auth/refresh**
  参数: `refresh_token`
  返回: 新的 access_token 和 refresh_token

- **GET /api/v1/auth/me**
  需要: Bearer Token (Authorization header)
  返回: 当前用户信息

---

## 🔍 调试

### 查看 API 文档
访问 http://localhost:8000/api/v1/docs 可以：
- 查看所有 API 端点
- 测试 API 请求
- 查看请求/响应格式

### 查看后端日志
后端服务器会输出所有请求日志，方便调试

### 查看数据库
```bash
psql -d trading_notes
\dt  # 查看所有表
SELECT * FROM users;  # 查看用户数据
```

---

## ❓ 常见问题

### 后端启动失败
- 检查 MySQL 是否运行: `brew services list`
- 检查 Redis 是否运行: `redis-cli ping`
- 检查 `.env` 文件配置是否正确

### 前端启动失败
- 删除 `node_modules` 和 `package-lock.json`
- 重新运行 `npm install`

### Google 登录失败
- 检查 Google Cloud Console 配置
- 确保测试用户列表包含您的邮箱
- 检查浏览器控制台错误信息

---

## 📖 更多文档

- `docs/requirements.md` - 完整功能需求
- `docs/architecture.md` - 技术架构设计
- `docs/development-plan.md` - 开发计划
- `docs/google-oauth-setup.md` - Google OAuth 详细配置
- `SETUP.md` - 环境安装指南

---

## 🎉 开始开发

Google OAuth 认证已经就绪！您现在可以：

1. ✅ 实现前端登录页面
2. ✅ 创建 Dashboard 页面
3. ✅ 开发其他功能（交易同步、持仓管理等）

Happy Coding! 🚀
