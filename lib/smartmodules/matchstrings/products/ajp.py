from lib.smartmodules.matchstrings.MatchStrings import get_products_match
products_match = get_products_match()

ajp = products_match.setdefault('ajp', {})
ajp.setdefault('appserver', [])
ajp.setdefault('web-appserver', ajp['appserver'])

def _ext(dst, items):
    for i in items:
        if i not in dst:
            dst.append(i)

_ext(ajp['appserver'], [
    r'Apache\s*Tomcat', r'Coyote\s*AJP', r'JBoss', r'WildFly', r'Jetty', r'WebLogic', r'GlassFish', r'Payara'
])
