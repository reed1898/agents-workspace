---
name: vercel-cli
version: 1.0.0
description: Deploy projects to Vercel using CLI

commands:
  - name: vercel-login
    description: Login to Vercel account
    usage: /vercel-login
    
  - name: vercel-deploy
    description: Deploy current project
    usage: /vercel-deploy [path]
    
  - name: vercel-deploy-prod
    description: Deploy to production
    usage: /vercel-deploy-prod [path]
    
  - name: vercel-logs
    description: View deployment logs
    usage: /vercel-logs
    
  - name: vercel-list
    description: List deployments
    usage: /vercel-list

env:
  - VERCEL_TOKEN: Optional, for non-interactive auth
---

# Vercel CLI Skill

## Quick Start

```bash
# 1. Login (one-time)
/vercel-login

# 2. Deploy
/vercel-deploy ./my-project

# 3. Deploy to production
/vercel-deploy-prod ./my-project
```

## Requirements

- Vercel CLI must be installed: `npm i -g vercel`
- Or use `npx vercel`
