import random
import logging
import uuid
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse

FLEXIDUG_AUTHORIZATION_TAN = "Flexidug-Authorization-TAN"


class TanManager:

    def __init__(self, seed=None, rows=10, cols=4):
        self.tan_list = {}
        if seed:
            random.seed(seed)
        self.cols = cols
        for _ in range(cols * rows):
            number = random.randint(100000, 999999)
            self.tan_list[f"{number}"] = True

    def verify_tan(self, req: Request):

        if FLEXIDUG_AUTHORIZATION_TAN not in req.headers:
            raise HTTPException(status_code=401, detail=f"Unauthorized Access. Header '{FLEXIDUG_AUTHORIZATION_TAN}' has to be preset.")

        tan = req.headers[FLEXIDUG_AUTHORIZATION_TAN]

        if tan in self.tan_list and self.tan_list[tan] is True:
            self.tan_list[tan] = False
            return True

        raise HTTPException(
            status_code=403,
            detail="Unauthorized Access. Invalid tan."
        )

    def tans_as_html(self):

        html = "<html>"
        html += "<body>"
        html += "<table>"

        i = 0
        for key, value in self.tan_list.items():

            if i == 0:
                html += "<tr>"
            elif i % self.cols == 0:
                html += "</tr><tr>"

            i += 1

            html += '<td style="padding: 5px;">'
            if value:
                html += key
            else:
                html += "<del>"+key+"</del>"
            html += "</td>"
    
        html += "</tr>"

        html += "</table>"
        html += "</body>"
        html += "</html>"

        return HTMLResponse(content=html, status_code=200)
