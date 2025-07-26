import html
import re
from typing import List

import requests
from requests import Session


def get_grade_data(session: Session):

    grade_response = session.get(
        "https://cim.hs-mainz.de/qisserver/pages/sul/examAssessment/personExamsReadonly.xhtml?_flowId=examsOverviewForPerson-flow&_flowExecutionKey=e2s1"
    )

    if grade_response.status_code == 403:
        raise Exception("unauthenticated")

    token = re.search(
        r'name="authenticity_token" value="(\S+)"', grade_response.text
    ).group(1)

    final_resp_url = html.unescape(
        re.search(
            r'<form id="examsReadonly" name="examsReadonly" method="post" action="(\S+)"',
            grade_response.text,
        ).group(1)
    )
    form = {
        "activePageElementId": "examsReadonly:overviewAsTreeReadonly:tree:ExamOverviewForPersonTreeReadonly:0:0:0:0:t2g_0-0-0-0",
        "refreshButtonClickedId": "",
        "navigationPosition": "hisinoneMeinStudium,examAssessmentForStudent",
        "authenticity_token": html.escape(token),
        "autoScroll": "",
        "examsReadonly:overviewAsTreeReadonly:collapsiblePanelCollapsedState": "",
        "examsReadonly:degreeProgramProgressForReportAsTree:collapsiblePanelCollapsedState": "",
        "examsReadonly:degreeProgramProgressForReportAsTree:studyHistoryTree:0:0:0:0:checkTick": "true",
        "examsReadonly:degreeProgramProgressForReportAsTree:studyHistoryTree:0:0:1:0:checkTick": "true",
        "examsReadonly_SUBMIT": "1",
        "javax.faces.ViewState": final_resp_url[-4:],
        "javax.faces.behavior.event": "action",
        "javax.faces.partial.event": "click",
        "javax.faces.source": "examsReadonly:overviewAsTreeReadonly:tree:ExamOverviewForPersonTreeReadonly:0:0:0:0:t2g_0-0-0-0",
        "javax.faces.partial.ajax": "true",
        "javax.faces.partial.execute": "examsReadonly:overviewAsTreeReadonly:tree:ExamOverviewForPersonTreeReadonly",
        "javax.faces.partial.render": "examsReadonly:overviewAsTreeReadonly:tree:ExamOverviewForPersonTreeReadonly examsReadonly:messages-infobox",
        "examsReadonly": "examsReadonly",
    }

    final_resp = session.post(
        "https://cim.hs-mainz.de" + final_resp_url,
        data=form,
        headers={
            "Faces-Request": "partial/ajax",
            "Origin": "https://cim.hs-mainz.de",
            "Host": "cim.hs-mainz.de",
        },
    )

    # close menu again, to open it on next request and have data
    session.post(
        "https://cim.hs-mainz.de" + final_resp_url,
        data=form,
        headers={
            "Faces-Request": "partial/ajax",
            "Origin": "https://cim.hs-mainz.de",
            "Host": "cim.hs-mainz.de",
        },
    )

    return final_resp.text


def extract_grade_list(content: str) -> List[str]:

    return_list = []

    for match in re.finditer(
        r'<span id="examsReadonly:overviewAsTreeReadonly:tree:ExamOverviewForPersonTreeReadonly:0:0:0:0:\d:unDeftxt">(.+?)</span>',
        content,
    ):
        return_list.append(match.group(1))

    return return_list


def get_grades(session: Session) -> List[str]:
    data = get_grade_data(session)
    return extract_grade_list(data)
