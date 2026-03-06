from typing import Optional


_NOTE_PREFIXES = (
    "导入自国泰君安 - ",
    "导入自同花顺 - ",
    "导入自国信证券 - ",
    "导入自moomoo - ",
)


def extract_symbol_name(notes: Optional[str]) -> Optional[str]:
    """从导入备注中提取标的名称"""
    if not notes:
        return None

    for prefix in _NOTE_PREFIXES:
        if notes.startswith(prefix):
            name = notes[len(prefix):]
            name = name.split("(")[0].strip()
            if not name or name.lower() == "nan":
                return None
            return name

    return None
