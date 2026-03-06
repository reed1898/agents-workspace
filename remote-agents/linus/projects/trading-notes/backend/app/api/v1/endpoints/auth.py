from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from ....core.database import get_db
from ....core.config import settings
from ....core.security import create_access_token, create_refresh_token
from ....models.user import User as UserModel
from ....schemas.user import User, Token

router = APIRouter()


@router.post("/google", response_model=Token)
async def google_auth(id_token_str: str, db: Session = Depends(get_db)):
    """
    验证 Google ID Token 并返回 JWT tokens

    前端使用 Google Sign-In 获取 id_token 后，将其发送到这个端点
    """
    try:
        # 验证 Google ID Token
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        # 检查 token 发行者
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token issuer"
            )

        # 获取用户信息
        email = idinfo.get('email')
        google_id = idinfo.get('sub')
        name = idinfo.get('name')
        picture = idinfo.get('picture')

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )

        # 查找或创建用户
        user = db.query(UserModel).filter(UserModel.email == email).first()

        if not user:
            # 创建新用户
            user = UserModel(
                email=email,
                username=name or email.split('@')[0],
                password_hash="",  # Google OAuth 用户不需要密码
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.commit()

        # 生成 JWT tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        # Token 验证失败
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(refresh_token: str, db: Session = Depends(get_db)):
    """使用 refresh token 获取新的 access token"""
    from ....core.security import decode_token

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # 验证用户存在且活跃
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # 创建新 tokens
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
async def get_current_user_info(db: Session = Depends(get_db)):
    """获取当前用户信息 (需要实现 JWT 依赖)"""
    # TODO: 实现 JWT 认证依赖
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="需要实现 JWT 认证依赖"
    )
