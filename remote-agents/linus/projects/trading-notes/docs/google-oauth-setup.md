# Google OAuth 设置指南

## 步骤 1: 创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击顶部的项目选择器
3. 点击 "新建项目"
4. 输入项目名称：`Trading Notes`
5. 点击 "创建"

## 步骤 2: 启用 Google+ API

1. 在左侧菜单中，选择 "API 和服务" > "库"
2. 搜索 "Google+ API" 或 "Google Identity"
3. 点击进入并点击 "启用"

## 步骤 3: 配置 OAuth 同意屏幕

1. 在左侧菜单中，选择 "API 和服务" > "OAuth 同意屏幕"
2. 选择 "外部"（用于测试）
3. 点击 "创建"
4. 填写必填信息：
   - **应用名称**: Trading Notes
   - **用户支持电子邮件**: 您的邮箱
   - **开发者联系信息**: 您的邮箱
5. 点击 "保存并继续"
6. **作用域**页面：点击 "保存并继续"（暂不添加）
7. **测试用户**页面：添加您的 Gmail 邮箱作为测试用户
8. 点击 "保存并继续"

## 步骤 4: 创建 OAuth 2.0 客户端 ID

1. 在左侧菜单中，选择 "API 和服务" > "凭据"
2. 点击顶部 "+ 创建凭据" > "OAuth 客户端 ID"
3. 应用类型选择 "Web 应用"
4. 名称：`Trading Notes Web Client`
5. **已获授权的 JavaScript 来源**：
   ```
   http://localhost:3000
   ```
6. **已获授权的重定向 URI**：
   ```
   http://localhost:3000
   http://localhost:3000/auth/google/callback
   ```
7. 点击 "创建"

## 步骤 5: 获取凭据

创建完成后，会弹出对话框显示：
- **客户端 ID**: 形如 `xxxxx.apps.googleusercontent.com`
- **客户端密钥**: 形如 `GOCSPX-xxxxx`

**重要**: 请妥善保管这些凭据！

## 步骤 6: 配置后端

将获取的凭据填入 `backend/.env` 文件：

```bash
# Google OAuth
GOOGLE_CLIENT_ID=你的客户端ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=你的客户端密钥
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback
```

## 步骤 7: 配置前端

在前端项目中创建 `.env.local` 文件：

```bash
NEXT_PUBLIC_GOOGLE_CLIENT_ID=你的客户端ID.apps.googleusercontent.com
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 测试步骤

1. 启动后端服务器：
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. 启动前端服务器：
   ```bash
   cd frontend
   npm run dev
   ```

3. 访问 http://localhost:3000
4. 点击 "Sign in with Google" 按钮
5. 选择您的 Google 账户
6. 授权应用访问您的基本信息
7. 登录成功！

## 常见问题

### 错误: "redirect_uri_mismatch"
- 确保 Google Cloud Console 中配置的重定向 URI 与实际使用的完全一致
- 检查是否有多余的斜杠或端口号

### 错误: "invalid_client"
- 检查 `.env` 文件中的 `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET` 是否正确
- 确保没有多余的空格或引号

### 错误: "access_denied"
- 确保在 OAuth 同意屏幕的测试用户列表中添加了您的邮箱
- 应用处于测试模式时，只有测试用户可以登录

### 如何添加更多测试用户？
1. 进入 Google Cloud Console
2. "API 和服务" > "OAuth 同意屏幕"
3. 点击 "编辑应用"
4. 滚动到 "测试用户" 部分
5. 点击 "+ ADD USERS"
6. 输入 Gmail 邮箱地址

## 生产环境部署

当应用准备发布时：
1. 完善 OAuth 同意屏幕的所有信息
2. 添加隐私政策和服务条款链接
3. 提交应用进行 Google 验证
4. 更新授权的域名和重定向 URI

## 安全提示

⚠️ **重要**:
- 永远不要将 `.env` 文件提交到 Git
- 不要在客户端代码中暴露 `GOOGLE_CLIENT_SECRET`
- 定期轮换 OAuth 凭据
- 在生产环境使用 HTTPS

---

**参考文档**:
- [Google OAuth 2.0 文档](https://developers.google.com/identity/protocols/oauth2)
- [Google Sign-In for Websites](https://developers.google.com/identity/sign-in/web)
