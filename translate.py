import requests
import urllib
from urllib import parse
auth="8b5a4d6c-0196-5992-7903-9741cb5508bb"

def trans(sentence):
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
    # response=requests.post(url,headers=header,data=content)
    # print(response.status_code)
    assert response.status_code==200, print("NETWORK ERROR: ",response.status_code)
    # print(response.headers)
    # print(response.content)
    data=response.json()
    # print(data)
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

def usage():
    url="https://api.deepl.com/v1/usage"
    proxies={
    'http':'127.0.0.1:1080',
    'https':'127.0.0.1:1080'
    }
    header={"Content-Type":"application/x-www-form-urlencoded",}
    content={
        "auth_key":auth,
    }
    response=requests.post(url,headers=header,data=content,proxies=proxies)
    # response=requests.post(url,headers=header,data=content)
    print(response.status_code)
    print(response.headers)
    print(response.content)
    
if __name__=="__main__":
    usage()
    test="hello,world"
    test_zh=trans(test)
    print(test)
    print(test_zh)
    