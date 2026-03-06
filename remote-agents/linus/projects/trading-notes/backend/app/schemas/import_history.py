"""导入历史记录的Pydantic schemas"""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any


class ImportHistoryBase(BaseModel):
    """ImportHistory基础schema"""
    filename: str = Field(..., description="上传的文件名")
    broker_template: str = Field(..., description="券商模板类型")
    import_source: str = Field(default="csv_import", description="导入来源")
    total_rows: int = Field(..., ge=0, description="CSV总行数")


class ImportHistoryCreate(ImportHistoryBase):
    """创建ImportHistory时使用"""
    account_id: UUID
    user_id: UUID


class ImportHistoryUpdate(BaseModel):
    """更新ImportHistory统计信息"""
    success_count: int = Field(ge=0)
    failed_count: int = Field(ge=0)
    duplicate_count: int = Field(ge=0)
    error_details: Optional[Dict[str, Any]] = None
    completed_at: datetime


class ImportHistory(ImportHistoryBase):
    """完整的ImportHistory信息"""
    id: UUID
    account_id: UUID
    user_id: UUID
    success_count: int
    failed_count: int
    duplicate_count: int
    error_details: Optional[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ImportHistoryList(BaseModel):
    """导入历史列表响应"""
    imports: List[ImportHistory]
    total: int


class CSVImportResponse(BaseModel):
    """CSV导入结果响应"""
    import_id: UUID = Field(..., description="导入历史记录ID")
    total_rows: int = Field(..., description="CSV总行数")
    success_count: int = Field(..., description="成功导入数量")
    failed_count: int = Field(..., description="失败数量")
    duplicate_count: int = Field(..., description="重复跳过数量")
    error_details: Optional[List[Dict[str, Any]]] = Field(None, description="错误详情")
    message: str = Field(..., description="导入结果消息")


class GmailSyncFileResult(BaseModel):
    """Gmail同步单文件结果"""
    filename: str
    import_id: Optional[UUID] = None
    success_count: int
    failed_count: int
    duplicate_count: int
    message: str


class GmailSyncResponse(BaseModel):
    """Gmail同步汇总结果"""
    files_imported: int
    files_skipped: int
    files_failed: int
    total_success_count: int
    total_failed_count: int
    total_duplicate_count: int
    message: str
    details: Optional[List[GmailSyncFileResult]] = None
