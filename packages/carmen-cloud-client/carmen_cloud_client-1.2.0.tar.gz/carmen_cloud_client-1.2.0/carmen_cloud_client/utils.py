from urllib.parse import quote


def url_concat(*args):
    result = args[0]
    for part in args[1:]:
        if result.endswith('/') and part.startswith('/'):
            result += part[1:]
        elif result.endswith('/') or part.startswith('/'):
            result += part
        else:
            result += '/' + part
    return result

def url_encode(s):
    # urllib.parse.quote() doesn't encode slashes (God knows why)
    return quote(s).replace('/', '%2F')
