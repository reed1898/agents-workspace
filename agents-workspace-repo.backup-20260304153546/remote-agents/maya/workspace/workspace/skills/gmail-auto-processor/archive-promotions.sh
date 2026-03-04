#!/bin/bash

# 批量归档所有促销邮件
# 简化版本，直接操作

echo "📧 批量归档促销邮件"
echo "===================="

# 获取促销邮件列表
echo "🔍 搜索促销邮件..."
MESSAGES=$(mcporter call --server google-workspace --tool "gmail.search" query="is:unread category:promotions" maxResults=100 2>/dev/null | grep '"id":' | sed 's/.*"id": "\([^"]*\)".*/\1/')

if [ -z "$MESSAGES" ]; then
  echo "✅ 没有促销邮件需要归档"
  exit 0
fi

COUNT=$(echo "$MESSAGES" | wc -l)
echo "📨 找到 $COUNT 封促销邮件"
echo ""

# 批量归档
PROCESSED=0
for MSG_ID in $MESSAGES; do
  RESULT=$(mcporter call --server google-workspace --tool "gmail.modify" messageId="$MSG_ID" removeLabelIds='["INBOX","UNREAD"]' 2>/dev/null)
  if echo "$RESULT" | grep -q "CATEGORY_PROMOTIONS"; then
    PROCESSED=$((PROCESSED + 1))
    echo "✅ 已归档: $MSG_ID"
  else
    echo "❌ 失败: $MSG_ID"
  fi
done

echo ""
echo "===================="
echo "📊 处理完成"
echo "成功归档: $PROCESSED 封"
