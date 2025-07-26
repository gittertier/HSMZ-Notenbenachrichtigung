import html
import re
from typing import Tuple

from requests import Response, Session

from util import get_csrf_token


def login_session(session: Session, username: str, password: str):
    first_res, base_url = first_request(session)
    second_res = second_request(first_res.text, base_url, username, password, session)
    third_request(second_res.text, session)




# requests
def first_request(session: Session) -> Tuple[Response, str]:
    resp = session.get(
        "https://cim.hs-mainz.de/Shibboleth.sso/Login?target=https%3A%2F%2Fcim.hs-mainz.de/qisserver/rds%3Fstate%3Duser%26type%3D1"
    )

    base_url = re.search(r"https://[^/]+", resp.url).group()
    content = resp.text
    action_url = re.search(r'<form name="form1" action="(/idp/\S+)"', content).group(1)
    csrf_token: str = get_csrf_token(content)

    form = {
        "csrf_token": csrf_token,
        "shib_idp_ls_exception.shib_idp_session_ss": "",
        "shib_idp_ls_success.shib_idp_session_ss": "false",
        "shib_idp_ls_value.shib_idp_session_ss": "",
        "shib_idp_ls_exception.shib_idp_persistent_ss": "",
        "shib_idp_ls_success.shib_idp_persistent_ss": "false",
        "shib_idp_ls_value.shib_idp_persistent_ss": "",
        "shib_idp_ls_supported": "false",
        "_eventId_proceed": "",
    }

    login_resp = session.post(base_url + action_url, data=form)
    return login_resp, base_url


def second_request(
    content: str, base_url: str, username: str, password: str, session: Session
):
    csrf_token = get_csrf_token(content)

    form = {
        "csrf_token": csrf_token,
        "j_username": username,
        "j_password": password,
        "_eventId_proceed": "",
    }

    return_url = base_url + html.unescape(
        re.search(r'<form action="(\S+)"', content).group(1)
    )

    login_complete_resp = session.post(
        return_url,
        data=form,
        headers={
            "Referer": return_url,
            "DNT": "1",
            "Host": "srv-idp-001.hs-mainz.de",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
        },
    )

    return login_complete_resp


def third_request(content: str, session: Session):
    final_url = html.unescape(re.search(r'<form action="(\S+)"', content).group(1))

    form = {
        match.group(1): html.unescape(match.group(2))
        for match in re.finditer(r'name="(\S+)" value="(\S+)"', content)
    }

    session.post(final_url, data=form)
