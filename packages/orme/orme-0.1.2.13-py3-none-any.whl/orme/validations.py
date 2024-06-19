from datetime import date


def validate_date(str_date: str) -> str:
    try:
        return date.fromisoformat(str_date).isoformat()
    except ValueError as e:
        print(f"error while validating date {e}")
        exit(1)
