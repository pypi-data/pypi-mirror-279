import functools
from datetime import datetime
import pandas as pd

def to_date_time(y: str, m: str, d: str, table: pd.DataFrame) -> datetime:
    """
    Convert year, month, and day columns to a datetime object.

    Args:
        y (str): year
        m (str): month
        d (str): day

    Returns:
        datetime: corresponding datetime set to midnight UTC
    """
    values = table[[y, m, d]].values[0].tolist()
    dtstr = "-".join([str(i).replace(",", "") for i in values])
    return pd.to_datetime(dtstr, format="%Y-%m-%d").tz_localize("UTC").to_pydatetime()


def camel_case_to_display_case(s: str) -> str:
    """
    Convert camel case to display case by introducing a space before each capital letter.

    Args:
        s (str): camel case string

    Returns:
        str: string for display
    """
    result = "".join(" " + char if char.isupper() else char for char in s).strip()
    # Capitalize the first letter of the resulting string
    return result[0].upper() + result[1:] if result else ""


def idempotent(delete_func):
    """
    A decorator to ensure idempotency by deleting an existing item before creating a new one.
    This decorator automatically extracts 'code' and 'scope' parameters from the wrapped function's
    arguments and passes them to the provided delete function.

    Args:
        delete_func (function): The function used to delete an existing item.
    """

    def decorator(create_func):
        @functools.wraps(create_func)
        def wrapper(*args, **kwargs):
            lusid_del_args = ["code", "scope", "domain","source"]
            kwargs_ = {
                k: v for k, v in kwargs.items() if k in lusid_del_args and v is not None
            }
            try:
                delete_func(**kwargs_)
                print(
                    f"Deleted existing item with code: {kwargs_['code']} and scope: {kwargs_['scope']}"
                )
            except Exception as e:
                print(f"No existing item to delete or error deleting item: {e}")

            # Execute the create function
            return create_func(*args, **kwargs)

        return wrapper

    return decorator

