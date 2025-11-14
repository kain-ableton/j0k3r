from lib.smartmodules.matchstrings.MatchStrings import get_products_match
products_match = get_products_match()

smtp = products_match.setdefault('smtp', {})
smtp.setdefault('server', [])
smtp.setdefault('auth', [])
smtp.setdefault('tls', [])

def _ext(dst, items):
    for i in items:
        if i not in dst:
            dst.append(i)

_ext(smtp['server'], [r'Postfix', r'Exim', r'Sendmail', r'qmail', r'Microsoft Exchange', r'MDaemon'])
_ext(smtp['auth'], [r'AUTH PLAIN', r'AUTH LOGIN', r'AUTH CRAM-MD5', r'AUTH NTLM'])
_ext(smtp['tls'], [r'STARTTLS', r'TLS', r'SSL'])
