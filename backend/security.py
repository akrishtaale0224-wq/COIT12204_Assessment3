import re


def sanitise_message(message: str) -> str:

    message = message.strip()


    # Remove potentially dangerous control characters
    message = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", message)


    # Limit excessive repeated characters
    message = re.sub(r"(.)\1{20,}", r"\1" * 20, message)


    # Limit message length
    return message[:2000]