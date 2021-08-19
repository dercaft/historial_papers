import requests
import urllib
from urllib import parse
def trans(sentence):
    auth="10419bf0-8084-be2d-7d50-9053a926bbd4"
    url="https://api.deepl.com/v1/translate"
    header={"Content-Type":"application/x-www-form-urlencoded",}
    content={
        "auth_key":auth,
        "text":sentence,
        "target_lang":"ZH",
    }
    response=requests.post(url,headers=header,data=content)
    data=response.json()
    data=data['translations']
    result="".join([ x['text'] for x in data])
    return result