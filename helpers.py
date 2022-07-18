import datetime
import sys

MAX_RESULTS_PER_REQUEST = 100

def sec(dt):
    if isinstance(dt, int):
        return dt
    return int(dt.timestamp())

def unsec(s):
    return datetime.datetime.fromtimestamp(s)

def quote_pattern(pattern):
    if " " in pattern:
        return '"' + pattern.replace(' ', '%20') + '"'
    return pattern

def debug(msg):
    sys.stderr.write('DEBUG: ' + str(msg) + '\n')

def format_url(pattern,
        start=None,
        end=None,
        sort='asc',
        limit=MAX_RESULTS_PER_REQUEST,
        **kwargs,
    ):
    assert limit <= MAX_RESULTS_PER_REQUEST, limit
    base = 'https://api.pushshift.io/reddit/search/comment'
    url = '{}/?q={}&limit={}&sort={}'.format(base, 
            quote_pattern(pattern), 
            limit, 
            sort,
            )
    if start is not None:
        url += '&after={}'.format(sec(start))
    if end is not None:
        url += '&before={}'.format(sec(end))
    for k, v in kwargs.items():
        url += f'&{k}={v}'
    return url

