from lib.smartmodules.matchstrings.MatchStrings import get_products_match
products_match = get_products_match()

oracle = products_match.setdefault('oracle', {})
oracle.setdefault('db', [])
oracle.setdefault('appserver', [])
oracle.setdefault('web-appserver', oracle['appserver'])

def _ext(dst, items):
    for i in items:
        if i not in dst:
            dst.append(i)

_ext(oracle['db'], [r'Oracle\s*Database', r'Oracle\s*11g', r'Oracle\s*12c', r'Oracle\s*19c'])
_ext(oracle['appserver'], [r'WebLogic', r'Oracle\s*HTTP\s*Server', r'Oracle\s*Application\s*Server'])
