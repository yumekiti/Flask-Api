# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

def index(request):

    url = "持ってくるURL(?pk=まで)"
    url_login = "ログインURL"
    id = "学籍番号"
    ps = "パスワード"

    # url宣言 resultに返す
    if 'pk' in request.GET:
        url += request.GET['pk']

    # info宣言
    login_info = {
        "c": "login_2",
        "flg_auto": "1",
        "token_a": "",
        "id": id,
        "pw" : ps,
    }
    
    # セッションスタート
    session = requests.session()

    # 成功すればログイン先のページのHTMLが返却される
    res = session.post(url_login, data=login_info)

    # ほしいurlをgetする
    geturl = session.get(url)

    # htmlに変更
    soup = BeautifulSoup(geturl.content, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()

    lines = [line.strip() for line in text.splitlines()]

    text = "\n".join(line for line in lines if line)

    text = "{\"data\":\"" + text + "\"}"

    return HttpResponse(text)