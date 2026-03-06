# IBKR Flex Web Service 自动导出交易数据操作指南

## 📘 概述

Interactive Brokers (IBKR) 提供 **Flex Web
Service**，可以让你自动下载账户的交易记录、持仓、现金流等数据，**无需登录
TWS 或 Portal**。\
该服务通过两个 API 端点完成：生成报表请求 + 获取报表结果。

------------------------------------------------------------------------

## 🧩 一、前置准备

1.  登录 <https://portal.interactivebrokers.com>
2.  进入 **Reports → Flex Queries**
3.  点击 **Create New Flex Query**
    -   选择类型：`Activity` 或 `Trades`
    -   勾选所需字段（symbol, quantity, price, commission 等）
    -   在「Output Format」中选择 **XML**
4.  保存后点击 **Generate Token URL**
    -   获得两个重要参数：
        -   `t=` → Token
        -   `q=` → Query ID

------------------------------------------------------------------------

## ⚙️ 二、调用流程

### Step 1：发送请求生成报表

    https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t=TOKEN&q=QUERY_ID&v=3

返回示例：

``` xml
<FlexStatementResponse timestamp="04 November, 2025 10:28 AM EST">
  <Status>Success</Status>
  <ReferenceCode>5048148287</ReferenceCode>
</FlexStatementResponse>
```

说明： - `Status` 表示是否成功。 - `ReferenceCode`
是报表编号，用于下一步获取实际数据。

### Step 2：下载实际报表内容

    https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?t=TOKEN&q=5048148287&v=3

返回示例（部分）：

``` xml
<FlexQueryResponse>
  <FlexStatements count="1">
    <FlexStatement accountId="U1234567">
      <Trades>
        <Trade>
          <symbol>AAPL</symbol>
          <quantity>100</quantity>
          <price>175.23</price>
          <buySell>B</buySell>
        </Trade>
      </Trades>
    </FlexStatement>
  </FlexStatements>
</FlexQueryResponse>
```

------------------------------------------------------------------------

## 🔁 三、实现自动化（每日更新）

你可以用任意方式自动化执行以上两步：

  -----------------------------------------------------------------------
  环境                    方式                    说明
  ----------------------- ----------------------- -----------------------
  **Python 脚本**         使用 `requests` +       每天自动下载并保存为
                          `xml.etree`             CSV

  **n8n / Zapier**        HTTP Request 节点 +     无需代码
                          Google Drive            

  **Google Sheets**       Apps Script +           直接写入表格
                          UrlFetchApp             

  **Server / NAS**        cron + curl 命令        简单稳定
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧠 四、注意事项

-   Flex Web Service **仅支持 XML 输出**，无法直接返回 CSV。
-   Token 通常有效期为 **90\~180 天**，过期需重新生成。
-   数据更新节奏：通常在交易日结束后（美东时间深夜）刷新。
-   建议每天北京时间上午 10:00 执行自动拉取任务。

------------------------------------------------------------------------

## 🧰 五、Python 示例代码

``` python
import requests
import xml.etree.ElementTree as ET

TOKEN = "YOUR_TOKEN"
QUERY_ID = "YOUR_QUERY_ID"

# Step 1: 获取 Reference Code
url_req = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={TOKEN}&q={QUERY_ID}&v=3"
resp = requests.get(url_req)
root = ET.fromstring(resp.text)
ref_code = root.find("ReferenceCode").text

# Step 2: 下载 XML 报表
url_get = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?t={TOKEN}&q={ref_code}&v=3"
xml_data = requests.get(url_get).text

with open("ibkr_statement.xml", "w") as f:
    f.write(xml_data)

print("✅ 已下载报表：ibkr_statement.xml")
```

------------------------------------------------------------------------

## ✅ 六、总结

  目的       方法
  ---------- ---------------------------------------
  手动导出   Portal → Flex Query → Download XML
  半自动     Flex Web Service + Token URL
  自动       Python / n8n / Google Sheets 定时任务
  格式       仅支持 XML（可再转换为 CSV）

------------------------------------------------------------------------

**推荐阅读：**\
- [IBKR 官方 Flex Web Service 指南
(PDF)](https://gdcdyn.interactivebrokers.com/Universal/flexwebserviceguide.pdf) -
[Client Portal Reports 页面](https://portal.interactivebrokers.com)

------------------------------------------------------------------------
