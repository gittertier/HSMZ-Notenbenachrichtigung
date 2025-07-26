import re

def get_csrf_token(content: str) -> str:
    matcher = re.search(r'name="csrf_token" value="(\S+)"', content)
    if matcher is None:
        return ""
    return matcher.group(1)

