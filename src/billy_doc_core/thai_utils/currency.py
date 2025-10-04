from typing import Union


def thai_number_to_words(amount: Union[int, float]) -> str:
    """
    Convert numeric amount to Thai words for business documents.

    This function handles Thai Baht conversion following Thai business practices.
    Supports amounts from 0 to 999,999.99 Baht with proper Satang handling.

    Args:
        amount: Numeric amount in Baht (can include Satang)

    Returns:
        Thai text representation (e.g., "หนึ่งร้อยบาทถ้วน")

    Raises:
        TypeError: If amount is not numeric
        ValueError: If amount is negative

    Examples:
        >>> thai_number_to_words(100)
        "หนึ่งร้อยบาทถ้วน"
        >>> thai_number_to_words(123.50)
        "หนึ่งร้อยยี่สิบสามบาทห้าสิบบสตางค์"
    """
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be numeric")

    if amount < 0:
        raise ValueError("Amount cannot be negative")

    thai_numbers = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    thai_units = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

    def convert_group(n: int) -> str:
        if n == 0:
            return ""
        result = []
        unit_idx = 0
        while n > 0:
            digit = n % 10
            if digit > 0:
                if unit_idx == 1 and digit == 1:
                    result.append(thai_units[unit_idx])
                elif unit_idx == 1 and digit == 2:
                    result.append("ยี่" + thai_units[unit_idx])
                else:
                    result.append(thai_numbers[digit] + thai_units[unit_idx])
            n //= 10
            unit_idx += 1
        return "".join(reversed(result))

    if amount == 0:
        return "ศูนย์บาทถ้วน"

    number = float(amount)
    integer_part = int(number)
    decimal_part = int(round((number - integer_part) * 100))

    result = []
    if integer_part > 0:
        millions = integer_part // 1000000
        remainder = integer_part % 1000000
        if millions > 0:
            result.append(convert_group(millions) + "ล้าน")
        if remainder > 0:
            result.append(convert_group(remainder))
        text = "".join(result) + "บาท"
    else:
        text = ""

    if decimal_part > 0:
        if text:  # If we have integer part
            text += convert_group(decimal_part) + "สตางค์"
        else:  # Only decimal part
            text = convert_group(decimal_part) + "สตางค์"
    else:
        if text:  # If we have integer part
            text += "ถ้วน"

    return text