import re
from typing import Optional


def parse_line(line: str) -> Optional[int]:
    parsed = re.search(r'time=(\d+).(\d+) ms', line)
    if parsed is not None and len(parsed.groups()) == 2:
        ping_float = float(f'{parsed.groups()[0]}.{parsed.groups()[1]}')
        return round(ping_float)

    return None
