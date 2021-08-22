import requests
import urllib
from urllib import parse
def trans(sentence):
    auth="10419bf0-8084-be2d-7d50-9053a926bbd4"
    url="https://api.deepl.com/v1/translate"
    proxies={
    'http':'127.0.0.1:1080',
    'https':'127.0.0.1:1080'
    }
    header={"Content-Type":"application/x-www-form-urlencoded",}
    content={
        "auth_key":auth,
        "text":sentence,
        "target_lang":"ZH",
    }
    response=requests.post(url,headers=header,data=content,proxies=proxies)
    data=response.json()
    data=data['translations']
    result="".join([ x['text'] for x in data])
    return result
def trans_para(para):
    if len(para)>200:
        sentences=para.split(".")
        zh_para=""
        for sent in sentences:
            if len(sent)>1500:
                parts=sent.split(";")
                pret=""
                for i,p in enumerate(parts):
                    ret=trans(p)
                    if i+1<len(parts):
                        ret+"；"
                    pret+=ret
                pret+="。"
                zh_para+=pret
            else:
                rsent=trans(sent)
                rsent+="。"
                zh_para+=rsent
    else:
        zh_para=trans(para)
    return zh_para