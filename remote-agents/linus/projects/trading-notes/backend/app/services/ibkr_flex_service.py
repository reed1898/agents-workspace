"""
IBKR Flex Web Service API integration
Handles automatic data fetching from Interactive Brokers using Flex Query tokens
"""
import requests
import xml.etree.ElementTree as ET
import csv
import io
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)


class IBKRFlexService:
    """Service for interacting with IBKR Flex Web Service API"""

    BASE_URL = "https://gdcdyn.interactivebrokers.com/Universal/servlet"
    CASH_XML_KEYS = (
        "endingCash",
        "endingSettledCash",
        "cashBalance",
        "totalCashValue",
        "settledCash",
        "availableFunds"
    )
    CASH_CSV_KEYS = (
        "EndingCash",
        "EndingSettledCash",
        "Ending Settled Cash",
        "Ending Cash",
        "Cash Balance",
        "TotalCashValue",
        "Total Cash Value",
        "Total Cash",
        "Settled Cash",
        "Available Funds"
    )

    def __init__(self, token: str, query_id: str):
        """
        Initialize IBKR Flex service

        Args:
            token: Flex Query token
            query_id: Flex Query ID
        """
        self.token = token
        self.query_id = query_id

    def request_statement(self) -> str:
        """
        Step 1: Request statement generation

        Returns:
            reference_code: Reference code for retrieving the statement

        Raises:
            Exception: If request fails
        """
        url = f"{self.BASE_URL}/FlexStatementService.SendRequest"
        params = {
            "t": self.token,
            "q": self.query_id,
            "v": "3"
        }

        logger.info(f"Requesting IBKR statement for query_id: {self.query_id}")

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.text)
            status = root.find("Status")

            if status is not None and status.text == "Success":
                ref_code_elem = root.find("ReferenceCode")
                if ref_code_elem is not None:
                    ref_code = ref_code_elem.text
                    logger.info(f"Statement request successful, reference code: {ref_code}")
                    return ref_code
                else:
                    raise Exception("ReferenceCode not found in response")
            else:
                error_code = root.find("ErrorCode")
                error_msg = root.find("ErrorMessage")
                error_text = f"Code: {error_code.text if error_code is not None else 'Unknown'}, Message: {error_msg.text if error_msg is not None else 'Unknown'}"
                raise Exception(f"IBKR request failed: {error_text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to request IBKR statement: {str(e)}")
            raise Exception(f"Network error requesting statement: {str(e)}")

    def get_statement(self, reference_code: str) -> str:
        """
        Step 2: Retrieve statement data (CSV or XML format)

        Args:
            reference_code: Reference code from request_statement()

        Returns:
            Statement content as string (CSV or XML)

        Raises:
            Exception: If retrieval fails
        """
        url = f"{self.BASE_URL}/FlexStatementService.GetStatement"
        params = {
            "t": self.token,
            "q": reference_code,
            "v": "3"
        }

        logger.info(f"Retrieving IBKR statement with reference code: {reference_code}")

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            # Check if response contains XML error
            if response.text.startswith("<") and "ErrorCode" in response.text:
                root = ET.fromstring(response.text)
                error_code = root.find("ErrorCode")
                error_msg = root.find("ErrorMessage")
                error_text = f"Code: {error_code.text if error_code is not None else 'Unknown'}, Message: {error_msg.text if error_msg is not None else 'Unknown'}"
                raise Exception(f"IBKR statement retrieval failed: {error_text}")

            logger.info(f"Successfully retrieved IBKR statement (length: {len(response.text)})")
            return response.text

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve IBKR statement: {str(e)}")
            raise Exception(f"Network error retrieving statement: {str(e)}")

    def fetch_trades(self) -> List[Dict]:
        """
        Complete flow: Request and parse trades from IBKR

        Returns:
            List of trade dictionaries with normalized fields
        """
        # Step 1: Request statement
        reference_code = self.request_statement()

        # Step 2: Get statement (may need to wait a few seconds for large reports)
        import time
        time.sleep(2)  # Wait 2 seconds for report generation

        content = self.get_statement(reference_code)

        # Step 3: Parse trades (check if CSV or XML)
        if content.startswith("<"):
            trades = self._parse_trades_xml(content)
        else:
            trades = self._parse_trades_csv(content)

        logger.info(f"Successfully parsed {len(trades)} trades from IBKR")
        return trades

    def fetch_trades_and_cash(self) -> Dict[str, Any]:
        """
        Complete flow: Request and parse trades + cash balance from IBKR

        Returns:
            Dictionary with trades list and cash balance info
        """
        reference_code = self.request_statement()

        import time
        time.sleep(2)

        content = self.get_statement(reference_code)

        if content.startswith("<"):
            trades = self._parse_trades_xml(content)
            cash_entry = self._parse_cash_xml(content)
        else:
            trades = self._parse_trades_csv(content)
            cash_entry = self._parse_cash_csv(content)

        result = {
            "trades": trades,
            "cash_balance": None,
            "cash_currency": None
        }

        if cash_entry:
            result["cash_balance"] = cash_entry.get("cash_balance")
            result["cash_currency"] = cash_entry.get("currency")

        logger.info(
            "Parsed IBKR statement: trades=%s, cash=%s %s",
            len(trades),
            result["cash_balance"],
            result["cash_currency"]
        )
        return result

    def _parse_trades_xml(self, xml_content: str) -> List[Dict]:
        """
        Parse trades from IBKR Flex Query XML response

        Args:
            xml_content: XML string content

        Returns:
            List of trade dictionaries
        """
        root = ET.fromstring(xml_content)
        trades = []

        # Navigate to trades section
        # FlexQueryResponse -> FlexStatements -> FlexStatement -> Trades -> Trade
        flex_statements = root.find("FlexStatements")
        if flex_statements is None:
            logger.warning("No FlexStatements found in XML")
            return trades

        for flex_statement in flex_statements.findall("FlexStatement"):
            account_id = flex_statement.get("accountId", "")

            trades_section = flex_statement.find("Trades")
            if trades_section is None:
                continue

            for trade_elem in trades_section.findall("Trade"):
                try:
                    trade = self._parse_trade_element(trade_elem, account_id)
                    if trade:
                        trades.append(trade)
                except Exception as e:
                    logger.error(f"Error parsing trade element: {str(e)}")
                    continue

        return trades

    def _parse_trades_csv(self, csv_content: str) -> List[Dict]:
        """
        Parse trades from IBKR Flex Query CSV response

        Args:
            csv_content: CSV string content

        Returns:
            List of trade dictionaries
        """
        trades = []

        try:
            # Parse CSV
            csv_file = io.StringIO(csv_content)
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                try:
                    trade = self._parse_csv_row(row)
                    if trade:
                        trades.append(trade)
                except Exception as e:
                    logger.error(f"Error parsing CSV row: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing CSV content: {str(e)}")

        return trades

    def _parse_cash_xml(self, xml_content: str) -> Optional[Dict[str, Any]]:
        root = ET.fromstring(xml_content)
        entries = []

        # Cash fields may live on nested nodes like CashReportCurrency.
        for elem in root.iter():
            entry = self._extract_cash_entry(elem)
            if entry:
                entries.append(entry)

        return self._select_cash_entry(entries)

    def _parse_cash_csv(self, csv_content: str) -> Optional[Dict[str, Any]]:
        entries: List[Dict[str, Any]] = []

        try:
            csv_file = io.StringIO(csv_content)
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                entry = self._extract_cash_entry_from_csv(row)
                if entry:
                    entries.append(entry)
        except Exception as e:
            logger.error(f"Error parsing cash CSV content: {str(e)}")

        return self._select_cash_entry(entries)

    def _extract_cash_entry(self, elem: ET.Element) -> Optional[Dict[str, Any]]:
        currency = elem.get("currency") or elem.get("baseCurrency") or elem.get("fxCurrency")
        for key in self.CASH_XML_KEYS:
            value = self._safe_decimal(elem.get(key))
            if value is not None:
                return {
                    "cash_balance": value,
                    "currency": currency
                }
        return None

    def _extract_cash_entry_from_csv(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        currency = row.get("Currency") or row.get("currency")
        for key in self.CASH_CSV_KEYS:
            value = self._safe_decimal(row.get(key))
            if value is not None:
                return {
                    "cash_balance": value,
                    "currency": currency
                }
        return None

    def _select_cash_entry(self, entries: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not entries:
            return None

        for preferred in ("USD", "BASE_SUMMARY", "BASE"):
            for entry in entries:
                currency = (entry.get("currency") or "").upper()
                if currency == preferred:
                    return entry

        return entries[0]

    def _safe_decimal(self, value: Optional[str]) -> Optional[Decimal]:
        if value is None:
            return None
        raw = str(value).strip()
        if not raw:
            return None
        try:
            return Decimal(raw.replace(",", ""))
        except (InvalidOperation, ValueError):
            logger.warning(f"Could not parse decimal value: {value}")
            return None

    def _parse_csv_row(self, row: Dict[str, str]) -> Optional[Dict]:
        """
        Parse a single CSV row from IBKR Flex Query

        Args:
            row: Dictionary representing a CSV row

        Returns:
            Dictionary with normalized trade fields
        """
        # Extract symbol
        symbol = row.get("Symbol", "").strip()
        if not symbol:
            return None

        # Parse date/time (format: YYYYMMDD;HHMMSS)
        date_time_str = row.get("DateTime", "")
        trade_date = None
        if date_time_str:
            try:
                # Remove semicolon if present
                date_time_str = date_time_str.replace(";", "")
                trade_date = datetime.strptime(date_time_str, "%Y%m%d%H%M%S")
            except ValueError:
                logger.warning(f"Could not parse datetime: {date_time_str}")

        # Determine side (Buy/Sell)
        buy_sell = row.get("Buy/Sell", "").upper()
        side = "buy" if buy_sell == "BUY" else "sell"

        # Parse quantity (use absolute value)
        quantity_str = row.get("Quantity", "0")
        try:
            quantity = abs(float(quantity_str))
        except ValueError:
            quantity = 0.0

        # Parse price
        trade_price_str = row.get("TradePrice", "0")
        try:
            price = float(trade_price_str)
        except ValueError:
            price = 0.0

        # Parse commission (make it positive)
        commission_str = row.get("IBCommission", "0")
        try:
            commission = abs(float(commission_str))
        except ValueError:
            commission = 0.0

        # Get trade ID
        external_trade_id = row.get("TradeID", "").strip()

        # Asset class
        asset_class = row.get("AssetClass", "").strip()

        # Currency
        currency = row.get("CurrencyPrimary", "USD").strip()

        # Account ID
        account_id = row.get("ClientAccountID", "").strip()

        return {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "commission": commission,
            "trade_date": trade_date,
            "external_trade_id": external_trade_id,
            "account_id": account_id,
            "asset_class": asset_class,
            "currency": currency,
            "raw_data": str(row)  # Keep raw data for reference
        }

    def _parse_trade_element(self, elem: ET.Element, account_id: str) -> Optional[Dict]:
        """
        Parse a single Trade XML element

        Returns:
            Dictionary with normalized trade fields
        """
        # Extract common fields from IBKR Flex Query
        symbol = elem.get("symbol", "")
        if not symbol:
            return None

        # Parse datetime
        date_str = elem.get("dateTime", "")
        trade_date = None
        if date_str:
            try:
                # IBKR format: "20231025;143022" (YYYYMMDD;HHMMSS)
                trade_date = datetime.strptime(date_str.replace(";", ""), "%Y%m%d%H%M%S")
            except ValueError:
                try:
                    # Alternative format: "2023-10-25, 14:30:22"
                    trade_date = datetime.strptime(date_str, "%Y-%m-%d, %H:%M:%S")
                except ValueError:
                    logger.warning(f"Could not parse date: {date_str}")

        # Determine side (Buy/Sell)
        buy_sell = elem.get("buySell", "").upper()
        side = "buy" if buy_sell == "BUY" or buy_sell == "BOT" else "sell"

        # Parse quantity (absolute value)
        quantity_str = elem.get("quantity", "0")
        quantity = abs(float(quantity_str))

        # Parse price (IBKR XML uses tradePrice; price is optional)
        price_str = elem.get("tradePrice") or elem.get("price") or "0"
        price = float(price_str)

        # Parse commission (IBKR XML uses ibCommission; commission is optional)
        commission_str = elem.get("ibCommission") or elem.get("commission") or "0"
        commission = abs(float(commission_str))

        # Get trade ID
        external_trade_id = elem.get("tradeID", "") or elem.get("execID", "")

        # Asset class
        asset_class = elem.get("assetCategory", "")

        # Currency
        currency = elem.get("currency", "USD")

        return {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "commission": commission,
            "trade_date": trade_date,
            "external_trade_id": external_trade_id,
            "account_id": account_id,
            "asset_class": asset_class,
            "currency": currency,
            "raw_data": ET.tostring(elem, encoding="unicode")  # Keep raw XML for reference
        }
