from datetime import date


def format_thai_date(date_obj: date) -> str:
    """
    Convert date to Thai-English format.

    Args:
        date_obj: Date to format

    Returns:
        Thai date in format: "31 มกราคม 2568 / 31-01-2025"

    Raises:
        TypeError: If date_obj is not a date instance
    """
    if not isinstance(date_obj, date):
        raise TypeError("date_obj must be a date instance")

    thai_months = {
        1: "มกราคม",
        2: "กุมภาพันธ์",
        3: "มีนาคม",
        4: "เมษายน",
        5: "พฤษภาคม",
        6: "มิถุนายน",
        7: "กรกฎาคม",
        8: "สิงหาคม",
        9: "กันยายน",
        10: "ตุลาคม",
        11: "พฤศจิกายน",
        12: "ธันวาคม",
    }

    thai_year = date_obj.year + 543
    thai_month = thai_months[date_obj.month]
    thai_date = f"{date_obj.day} {thai_month} {thai_year}"
    eng_date = date_obj.strftime("%d-%m-%Y")

    return f"{thai_date} / {eng_date}"