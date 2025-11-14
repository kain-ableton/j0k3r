from lib.smartmodules.matchstrings.MatchStrings import get_products_match
products_match = get_products_match()

mssql = products_match.setdefault('mssql', {})
mssql.setdefault('db', [])
mssql.setdefault('edition', [])

def _ext(dst, items):
    for i in items:
        if i not in dst:
            dst.append(i)

_ext(mssql['db'], [r'Microsoft\s*SQL\s*Server', r'SQL\s*Server', r'Azure\s*SQL'])
_ext(mssql['edition'], [r'Express', r'Standard', r'Enterprise', r'Developer'])
