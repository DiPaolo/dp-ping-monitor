import locale
import logging
import re
from typing import Optional

_MAP = {
    'en_US': ('time', '.', ' ms'),
    'ru_RU': ('время', '.', 'мс'),
}

_log = logging.getLogger('core.ping_parser')


def parse_line(line: str) -> Optional[int]:
    locale_code = locale.getlocale(locale.LC_CTYPE)[0]
    if locale_code not in _MAP:
        _log.error(f'failed to parse line from ping output: unknown locale code (code={locale_code})')
        return None

    locale_params = _MAP[locale_code]
    parsed = re.search(rf"{locale_params[0]}=(\d+)(?:{locale_params[1]}(\d+))?{locale_params[2]}", line)
    if parsed is not None:
        if len(parsed.groups()) == 1:
            return parsed.groups()[0]
        elif len(parsed.groups()) == 2:
            ping_float = float(f'{parsed.groups()[0]}.{parsed.groups()[1]}')
            return round(ping_float)

    return None
