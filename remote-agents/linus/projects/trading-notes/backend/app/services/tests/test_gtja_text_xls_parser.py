from decimal import Decimal
from pathlib import Path

from app.services.csv_parser_service import get_parser


def test_gtja_text_xls_import_parses_trades_and_cash_balance():
    repo_root = Path(__file__).resolve().parents[4]
    xls_path = repo_root / "data" / "20260103 资金流水查询.xls"

    parser = get_parser("gtja")
    trades = parser.parse_file(xls_path.name, xls_path.read_bytes())

    assert parser.errors == []
    assert len(trades) == 106
    assert parser.cash_balance == Decimal("81618.03")
    assert parser.cash_currency == "人民币"

    first = trades[0]
    assert first["symbol"] == "002167.SZ"
    assert first["side"] == "buy"
    assert first["trade_id_external"] == "105000014035113"
    assert abs(first["fee"] - 5.01) < 1e-9

