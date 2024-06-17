
import argparse
import os
import re
from typing import Optional, Pattern


def regex_pattern(regex: str) -> Optional[Pattern[str]]:
    if not regex:
        return None

    try:
        return re.compile(regex)
    except re.error:
        msg = f"String '{regex}' is not valid regex pattern"
        raise argparse.ArgumentTypeError(msg)


def is_local_dev() -> bool:
    return os.getenv("LOCAL_DEV") == "1"


def is_staging() -> bool:
    if is_local_dev():
        raise Exception("You can not use both LOCAL_DEV and STAGING. Choose one environment!")
    return os.getenv("STAGING") == "1"
