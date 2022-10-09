import webview
window = None
def init(w:webview.Window):
    global window
    window = w

def response(http_status:int, content:str):
    return {
        "status": http_status,
        "return_value": content
    }


def update_window_title(data):
    window.set_title(data["title"])
    return response(200, "성공!")




"""            이 아래에 커스텀 API              """

import os
def calc(data):
    os.system("calc")
    print("짜란 계산기를 열었답니다?")
    return response(200, "성공!")
