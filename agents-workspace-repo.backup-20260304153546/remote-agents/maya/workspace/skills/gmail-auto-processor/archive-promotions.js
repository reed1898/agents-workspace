const { execSync } = require('child_process');

// 休眠函数
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 获取促销邮件
async function getPromotions() {
  try {
    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread category:promotions" maxResults=100', { encoding: 'utf8' });
    const data = JSON.parse(result);
    return data.messages || [];
  } catch (e) {
    console.error('获取促销邮件失败:', e.message);
    return [];
  }
}

// 归档单封邮件
function archiveMessage(msgId) {
  try {
    execSync(`mcporter call --server google-workspace --tool "gmail.modify" messageId="${msgId}" removeLabelIds='["INBOX","UNREAD"]'`, { encoding: 'utf8', timeout: 10000 });
    return true;
  } catch (e) {
    console.log(`❌ 失败: ${msgId}`);
    return false;
  }
}

// 获取未读邮件数量
function getUnreadCount() {
  try {
    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1', { encoding: 'utf8' });
    const data = JSON.parse(result);
    return data.resultSizeEstimate || 0;
  } catch (e) {
    return 0;
  }
}

// 主函数
async function main() {
  let totalArchived = 0;
  let batch = 0;
  
  console.log('🚀 开始批量归档促销邮件...\n');
  
  while (true) {
    batch++;
    const messages = await getPromotions();
    
    if (messages.length === 0) {
      console.log('\n✨ 没有更多促销邮件需要归档');
      break;
    }
    
    console.log(`\n📦 批次 ${batch}: 找到 ${messages.length} 封促销邮件`);
    
    let batchSuccess = 0;
    for (const msg of messages) {
      if (archiveMessage(msg.id)) {
        batchSuccess++;
        totalArchived++;
        process.stdout.write(`\r✅ 已归档: ${batchSuccess}/${messages.length}`);
      }
    }
    console.log(`\n批次完成: ${batchSuccess}/${messages.length}`);
    
    // 等待 2 秒避免 API 限流
    await sleep(2000);
  }
  
  // 获取剩余未读邮件
  const remainingUnread = getUnreadCount();
  
  // 输出结果
  console.log('\n📊 ===============================');
  console.log(`✅ 成功归档: ${totalArchived} 封促销邮件`);
  console.log(`📧 剩余未读: ${remainingUnread} 封`);
  console.log('===============================');
  
  // 返回结果供 Telegram 报告使用
  return { archived: totalArchived, remaining: remainingUnread };
}

main().then(result => {
  // 输出 JSON 格式供外部解析
  console.log(JSON.stringify(result));
}).catch(err => {
  console.error('脚本执行失败:', err);
  process.exit(1);
});
